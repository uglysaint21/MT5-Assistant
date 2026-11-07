"""Strict transport primitives for the versioned stdin/stdout JSON Lines protocol."""

from __future__ import annotations

import json
import threading
from datetime import datetime
from typing import Any

PROTOCOL_VERSION = 1
MAX_FRAME_BYTES = 1_048_576
MAX_ACTIVE_REQUESTS = 1_024


class ProtocolError(ValueError):
    """Raised when a process-protocol frame is invalid."""


class ActiveRequestIds:
    """Bounded registry that rejects duplicate IDs while requests are in flight."""

    def __init__(self, max_active: int = MAX_ACTIVE_REQUESTS) -> None:
        if max_active < 1:
            raise ValueError("max_active must be positive.")
        self._active: set[str] = set()
        self._max_active = max_active
        self._lock = threading.Lock()

    def register(self, request_id: str) -> None:
        if not isinstance(request_id, str) or not request_id.strip() or len(request_id) > 128:
            raise ProtocolError("Request ID must be a non-empty string.")
        with self._lock:
            if request_id in self._active:
                raise ProtocolError("Duplicate active request ID.")
            if len(self._active) >= self._max_active:
                raise ProtocolError("Maximum number of active requests reached.")
            self._active.add(request_id)

    def release(self, request_id: str) -> None:
        with self._lock:
            self._active.discard(request_id)


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ProtocolError(f"Protocol frame contains duplicate key: {key}")
        result[key] = value
    return result


def _reject_non_json_constant(value: str) -> None:
    raise ProtocolError(f"Invalid JSON numeric constant: {value}")


def decode_frame(line: str) -> dict[str, Any]:
    try:
        encoded = line.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ProtocolError("Protocol frame is not valid UTF-8.") from exc
    if len(encoded) > MAX_FRAME_BYTES:
        raise ProtocolError("Protocol frame exceeds the maximum size.")
    try:
        value = json.loads(
            line, object_pairs_hook=_reject_duplicate_keys, parse_constant=_reject_non_json_constant
        )
    except ProtocolError:
        raise
    except (json.JSONDecodeError, UnicodeEncodeError) as exc:
        raise ProtocolError("Protocol frame is not valid UTF-8 JSON.") from exc
    if not isinstance(value, dict):
        raise ProtocolError("Protocol frame must be a JSON object.")
    if (
        type(value.get("protocolVersion")) is not int
        or value.get("protocolVersion") != PROTOCOL_VERSION
    ):
        raise ProtocolError("Unsupported protocol version.")
    return value


def _require_exact_keys(
    value: dict[str, Any], required: set[str], optional: set[str] | None = None
) -> None:
    optional = optional or set()
    missing = required - value.keys()
    unknown = value.keys() - required - optional
    if missing:
        raise ProtocolError(f"Protocol envelope is missing fields: {', '.join(sorted(missing))}")
    if unknown:
        raise ProtocolError(
            f"Protocol envelope contains unknown fields: {', '.join(sorted(unknown))}"
        )


def _require_nonempty_string(value: Any, field: str, max_length: int = 256) -> None:
    if not isinstance(value, str) or not value.strip() or len(value) > max_length:
        raise ProtocolError(f"Protocol field '{field}' must be a non-empty string.")


def validate_envelope(message: dict[str, Any]) -> dict[str, Any]:
    """Validate one complete protocol-v1 envelope and return it unchanged."""
    if not isinstance(message, dict):
        raise ProtocolError("Protocol envelope must be an object.")
    if (
        type(message.get("protocolVersion")) is not int
        or message.get("protocolVersion") != PROTOCOL_VERSION
    ):
        raise ProtocolError("Unsupported protocol version.")

    kind = message.get("kind")
    if kind == "request":
        _require_exact_keys(
            message, {"kind", "protocolVersion", "requestId", "operation", "payload"}
        )
        _require_nonempty_string(message["requestId"], "requestId", 128)
        _require_nonempty_string(message["operation"], "operation", 128)
        if not isinstance(message["payload"], dict):
            raise ProtocolError("Protocol request payload must be an object.")

    elif kind == "response":
        _require_exact_keys(
            message, {"kind", "protocolVersion", "requestId", "ok"}, {"result", "error"}
        )
        _require_nonempty_string(message["requestId"], "requestId", 128)
        if not isinstance(message["ok"], bool):
            raise ProtocolError("Protocol response 'ok' must be boolean.")
        if message["ok"]:
            if "result" not in message or "error" in message:
                raise ProtocolError("Successful response requires result and forbids error.")
            if not isinstance(message["result"], dict):
                raise ProtocolError("Protocol response result must be an object.")
        else:
            if "error" not in message or "result" in message:
                raise ProtocolError("Error response requires error and forbids result.")
            error = message["error"]
            if not isinstance(error, dict):
                raise ProtocolError("Protocol response error must be an object.")
            _require_exact_keys(error, {"code", "message", "retryable"}, {"details"})
            _require_nonempty_string(error["code"], "error.code", 128)
            _require_nonempty_string(error["message"], "error.message", 1024)
            if not isinstance(error["retryable"], bool):
                raise ProtocolError("Protocol error retryable must be boolean.")
            if "details" in error and not isinstance(error["details"], dict):
                raise ProtocolError("Protocol error details must be an object.")

    elif kind == "ready":
        _require_exact_keys(message, {"kind", "protocolVersion", "serviceVersion", "capabilities"})
        _require_nonempty_string(message["serviceVersion"], "serviceVersion", 64)
        capabilities = message["capabilities"]
        if not isinstance(capabilities, list) or any(
            not isinstance(item, str) or not item.strip() for item in capabilities
        ):
            raise ProtocolError(
                "Protocol ready capabilities must be an array of non-empty strings."
            )
        if len(capabilities) != len(set(capabilities)):
            raise ProtocolError("Protocol ready capabilities must not contain duplicates.")

    elif kind == "event":
        _require_exact_keys(
            message, {"kind", "protocolVersion", "eventId", "event", "occurredAt", "payload"}
        )
        _require_nonempty_string(message["eventId"], "eventId", 128)
        _require_nonempty_string(message["event"], "event", 128)
        if not isinstance(message["payload"], dict):
            raise ProtocolError("Protocol event payload must be an object.")
        timestamp = message["occurredAt"]
        if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
            raise ProtocolError("Protocol event occurredAt must be a UTC ISO-8601 timestamp.")
        try:
            parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ProtocolError(
                "Protocol event occurredAt must be a UTC ISO-8601 timestamp."
            ) from exc
        if parsed.tzinfo is None or parsed.utcoffset().total_seconds() != 0:
            raise ProtocolError("Protocol event occurredAt must use UTC.")
    else:
        raise ProtocolError("Unknown protocol envelope kind.")

    return message


def encode_frame(message: dict[str, Any]) -> str:
    validate_envelope(message)
    try:
        encoded = (
            json.dumps(message, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n"
        )
    except (TypeError, ValueError) as exc:
        raise ProtocolError("Protocol message is not JSON serializable.") from exc
    if len(encoded.encode("utf-8")) > MAX_FRAME_BYTES:
        raise ProtocolError("Protocol frame exceeds the maximum size.")
    return encoded
