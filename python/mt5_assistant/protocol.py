"""Transport primitives for the versioned stdin/stdout JSON Lines protocol."""
from __future__ import annotations

import json
from typing import Any

PROTOCOL_VERSION = 1
MAX_FRAME_BYTES = 1_048_576


class ProtocolError(ValueError):
    """Raised when a process-protocol frame is invalid."""


def decode_frame(line: str) -> dict[str, Any]:
    encoded = line.encode("utf-8")
    if len(encoded) > MAX_FRAME_BYTES:
        raise ProtocolError("Protocol frame exceeds the maximum size.")
    try:
        value = json.loads(line)
    except json.JSONDecodeError as exc:
        raise ProtocolError("Protocol frame is not valid JSON.") from exc
    if not isinstance(value, dict):
        raise ProtocolError("Protocol frame must be a JSON object.")
    if value.get("protocolVersion") != PROTOCOL_VERSION:
        raise ProtocolError("Unsupported protocol version.")
    return value


def encode_frame(message: dict[str, Any]) -> str:
    if message.get("protocolVersion") != PROTOCOL_VERSION:
        raise ProtocolError("Unsupported protocol version.")
    try:
        return json.dumps(message, separators=(",", ":"), ensure_ascii=False) + "\n"
    except (TypeError, ValueError) as exc:
        raise ProtocolError("Protocol message is not JSON serializable.") from exc
