import { describe, expect, it } from "vitest";
import { isProtocolEnvelope, isProtocolResponse } from "../src/shared/protocol.js";

describe("protocol envelope validation", () => {
  it("accepts a successful response", () => {
    expect(isProtocolResponse({
      kind: "response", protocolVersion: 1, requestId: "req-1",
      ok: true, result: { connected: false }
    })).toBe(true);
  });

  it("accepts a structured error response", () => {
    expect(isProtocolResponse({
      kind: "response", protocolVersion: 1, requestId: "req-2",
      ok: false, error: { code: "TERMINAL_DISCONNECTED", message: "Disconnected", retryable: true }
    })).toBe(true);
  });

  it("rejects unsupported versions, malformed errors and unknown response fields", () => {
    expect(isProtocolResponse({
      kind: "response", protocolVersion: 2, requestId: "req-3", ok: true, result: {}
    })).toBe(false);
    expect(isProtocolResponse({
      kind: "response", protocolVersion: 1, requestId: "req-4", ok: false, error: {}
    })).toBe(false);
    expect(isProtocolResponse({
      kind: "response", protocolVersion: 1, requestId: "req-5",
      ok: true, result: {}, debug: true
    })).toBe(false);
  });

  it("accepts a valid request and ready handshake", () => {
    expect(isProtocolEnvelope({
      kind: "request", protocolVersion: 1, requestId: "req-6",
      operation: "account.getSnapshot", payload: {}
    })).toBe(true);
    expect(isProtocolEnvelope({
      kind: "ready", protocolVersion: 1, serviceVersion: "0.1.0",
      capabilities: ["account.read"]
    })).toBe(true);
  });

  it("rejects request payloads that are not objects and duplicate capabilities", () => {
    expect(isProtocolEnvelope({
      kind: "request", protocolVersion: 1, requestId: "req-7",
      operation: "account.getSnapshot", payload: []
    })).toBe(false);
    expect(isProtocolEnvelope({
      kind: "ready", protocolVersion: 1, serviceVersion: "0.1.0",
      capabilities: ["account.read", "account.read"]
    })).toBe(false);
  });

  it("accepts UTC events and rejects invalid timestamps", () => {
    expect(isProtocolEnvelope({
      kind: "event", protocolVersion: 1, eventId: "evt-1",
      event: "sync.progress", occurredAt: "2026-11-07T18:00:00Z", payload: {}
    })).toBe(true);
    expect(isProtocolEnvelope({
      kind: "event", protocolVersion: 1, eventId: "evt-2",
      event: "sync.progress", occurredAt: "2026-11-07T18:00:00+03:00", payload: {}
    })).toBe(false);
  });
});
