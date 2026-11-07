import pytest

from mt5_assistant.protocol import ProtocolError, decode_frame, encode_frame, validate_envelope


def test_rejects_duplicate_json_object_keys():
    with pytest.raises(ProtocolError, match="duplicate"):
        decode_frame('{"protocolVersion":1,"kind":"request","kind":"event"}')


def test_rejects_oversized_frame():
    with pytest.raises(ProtocolError, match="maximum size"):
        decode_frame('{"protocolVersion":1,"payload":"' + ("x" * 1_048_576) + '"}')


def test_validates_request_envelope_and_rejects_unknown_fields():
    request = {
        "kind": "request", "protocolVersion": 1, "requestId": "req-1",
        "operation": "account.getSnapshot", "payload": {}
    }
    assert validate_envelope(request) == request
    with pytest.raises(ProtocolError, match="unknown"):
        validate_envelope({**request, "debug": True})


def test_validates_success_and_error_responses():
    success = {
        "kind": "response", "protocolVersion": 1, "requestId": "req-1",
        "ok": True, "result": {}
    }
    error = {
        "kind": "response", "protocolVersion": 1, "requestId": "req-1",
        "ok": False, "error": {
            "code": "TERMINAL_DISCONNECTED", "message": "Disconnected",
            "retryable": True
        }
    }
    assert validate_envelope(success) == success
    assert validate_envelope(error) == error


def test_rejects_response_with_both_result_and_error():
    invalid = {
        "kind": "response", "protocolVersion": 1, "requestId": "req-1",
        "ok": True, "result": {}, "error": {}
    }
    with pytest.raises(ProtocolError):
        validate_envelope(invalid)


def test_validates_ready_and_event_envelopes():
    ready = {
        "kind": "ready", "protocolVersion": 1, "serviceVersion": "0.1.0",
        "capabilities": ["account.read"]
    }
    event = {
        "kind": "event", "protocolVersion": 1, "eventId": "evt-1",
        "event": "sync.progress", "occurredAt": "2026-11-07T18:00:00Z",
        "payload": {}
    }
    assert validate_envelope(ready) == ready
    assert validate_envelope(event) == event


def test_rejects_invalid_timestamp_and_unknown_envelope_kind():
    event = {
        "kind": "event", "protocolVersion": 1, "eventId": "evt-1",
        "event": "sync.progress", "occurredAt": "not-a-time", "payload": {}
    }
    with pytest.raises(ProtocolError):
        validate_envelope(event)
    with pytest.raises(ProtocolError):
        validate_envelope({"kind": "mystery", "protocolVersion": 1})


def test_rejects_boolean_protocol_version():
    with pytest.raises(ProtocolError):
        decode_frame('{"protocolVersion":true,"kind":"request"}')


def test_rejects_duplicate_active_request_ids_until_released():
    from mt5_assistant.protocol import ActiveRequestIds

    active = ActiveRequestIds()
    active.register("request-1")
    with pytest.raises(ProtocolError, match="duplicate"):
        active.register("request-1")
    active.release("request-1")
    active.register("request-1")


def test_active_request_registry_rejects_empty_ids():
    from mt5_assistant.protocol import ActiveRequestIds

    with pytest.raises(ProtocolError):
        ActiveRequestIds().register("")


def test_active_request_registry_enforces_capacity():
    from mt5_assistant.protocol import ActiveRequestIds

    active = ActiveRequestIds(max_active=1)
    active.register("request-1")
    with pytest.raises(ProtocolError, match="Maximum"):
        active.register("request-2")


def test_rejects_non_json_numeric_constants():
    with pytest.raises(ProtocolError, match="JSON"):
        decode_frame('{"protocolVersion":1,"value":NaN}')


def test_rejects_non_zulu_event_timestamps_to_match_schema():
    event = {
        "kind": "event", "protocolVersion": 1, "eventId": "evt-offset",
        "event": "sync.progress", "occurredAt": "2026-11-07T18:00:00+00:00",
        "payload": {}
    }
    with pytest.raises(ProtocolError):
        validate_envelope(event)


def test_active_request_registry_rejects_overlong_ids():
    from mt5_assistant.protocol import ActiveRequestIds

    with pytest.raises(ProtocolError):
        ActiveRequestIds().register("x" * 129)


def test_encoder_rejects_non_json_numeric_values():
    with pytest.raises(ProtocolError, match="serializable"):
        encode_frame({
            "kind": "response", "protocolVersion": 1, "requestId": "req-nan",
            "ok": True, "result": {"value": float("nan")}
        })
