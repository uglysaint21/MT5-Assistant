import pytest

from mt5_assistant.protocol import ProtocolError, decode_frame, encode_frame


def test_decodes_valid_versioned_object():
    assert decode_frame('{"protocolVersion":1,"kind":"request"}') == {
        "protocolVersion": 1, "kind": "request"
    }


def test_rejects_invalid_json_and_non_object_frames():
    with pytest.raises(ProtocolError):
        decode_frame("{")
    with pytest.raises(ProtocolError):
        decode_frame('[{"protocolVersion":1}]')


def test_rejects_unsupported_protocol_version():
    with pytest.raises(ProtocolError):
        decode_frame('{"protocolVersion":2}')


def test_encodes_one_json_line():
    assert encode_frame({"protocolVersion": 1, "kind": "ready"}).endswith("\n")
