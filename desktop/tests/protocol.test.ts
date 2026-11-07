import { describe, expect, it } from "vitest";
import requestFixture from "../../protocol/fixtures/request-account-snapshot.json" with { type: "json" };
import readyFixture from "../../protocol/fixtures/ready.json" with { type: "json" };
import successFixture from "../../protocol/fixtures/response-success.json" with { type: "json" };
import errorFixture from "../../protocol/fixtures/response-error.json" with { type: "json" };
import eventFixture from "../../protocol/fixtures/event-sync-progress.json" with { type: "json" };
import { isProtocolEnvelope, isProtocolResponse } from "../src/shared/protocol.js";

describe("protocol envelope validation", () => {
  it("accepts shared request and handshake golden fixtures", () => {
    expect(isProtocolEnvelope(requestFixture)).toBe(true);
    expect(isProtocolEnvelope(readyFixture)).toBe(true);
  });

  it("accepts shared success and error response golden fixtures", () => {
    expect(isProtocolResponse(successFixture)).toBe(true);
    expect(isProtocolResponse(errorFixture)).toBe(true);
  });

  it("accepts the shared UTC event golden fixture", () => {
    expect(isProtocolEnvelope(eventFixture)).toBe(true);
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

  it("accepts UTC events and rejects invalid or non-UTC timestamps", () => {
    expect(isProtocolEnvelope(eventFixture)).toBe(true);
    expect(isProtocolEnvelope({
      kind: "event", protocolVersion: 1, eventId: "evt-2",
      event: "sync.progress", occurredAt: "not-a-time", payload: {}
    })).toBe(false);
    expect(isProtocolEnvelope({
      kind: "event", protocolVersion: 1, eventId: "evt-3",
      event: "sync.progress", occurredAt: "2026-11-07T18:00:00+03:00", payload: {}
    })).toBe(false);
    expect(isProtocolEnvelope({
      kind: "event", protocolVersion: 1, eventId: "evt-4",
      event: "sync.progress", occurredAt: "2026-02-30T18:00:00Z", payload: {}
    })).toBe(false);
  });
});
