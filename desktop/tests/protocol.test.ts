import { describe, expect, it } from "vitest";
import { isProtocolResponse } from "../src/shared/protocol.js";

describe("isProtocolResponse", () => {
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

  it("rejects unsupported versions and malformed errors", () => {
    expect(isProtocolResponse({
      kind: "response", protocolVersion: 2, requestId: "req-3", ok: true, result: {}
    })).toBe(false);
    expect(isProtocolResponse({
      kind: "response", protocolVersion: 1, requestId: "req-4", ok: false, error: {}
    })).toBe(false);
  });
});
