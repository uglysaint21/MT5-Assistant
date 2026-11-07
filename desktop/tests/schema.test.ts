import { Ajv2020 } from "ajv/dist/2020.js";
import type { AnySchema } from "ajv";
import { describe, expect, it } from "vitest";
import requestSchema from "../../protocol/schema/request.schema.json" with { type: "json" };
import readySchema from "../../protocol/schema/ready.schema.json" with { type: "json" };
import responseSchema from "../../protocol/schema/response.schema.json" with { type: "json" };
import eventSchema from "../../protocol/schema/event.schema.json" with { type: "json" };
import requestFixture from "../../protocol/fixtures/request-account-snapshot.json" with { type: "json" };
import readyFixture from "../../protocol/fixtures/ready.json" with { type: "json" };
import successFixture from "../../protocol/fixtures/response-success.json" with { type: "json" };
import errorFixture from "../../protocol/fixtures/response-error.json" with { type: "json" };
import eventFixture from "../../protocol/fixtures/event-sync-progress.json" with { type: "json" };

const ajv = new Ajv2020({ allErrors: true });
ajv.addFormat("date-time", {
  type: "string",
  validate: (value: string) => {
    if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/.test(value)) {
      return false;
    }
    const parsed = new Date(value);
    return !Number.isNaN(parsed.getTime()) && parsed.toISOString().startsWith(value.slice(0, 19));
  },
});

describe("shared JSON Schema contracts", () => {
  it("validates the request golden fixture", () => {
    expect(ajv.compile(requestSchema as AnySchema)(requestFixture)).toBe(true);
  });

  it("validates the ready handshake golden fixture", () => {
    expect(ajv.compile(readySchema as AnySchema)(readyFixture)).toBe(true);
  });

  it("validates success and error response golden fixtures", () => {
    const validate = ajv.compile(responseSchema as AnySchema);
    expect(validate(successFixture)).toBe(true);
    expect(validate(errorFixture)).toBe(true);
  });

  it("validates the UTC event golden fixture", () => {
    expect(ajv.compile(eventSchema as AnySchema)(eventFixture)).toBe(true);
  });

  it("rejects unexpected request fields", () => {
    const validate = ajv.compile(requestSchema as AnySchema);
    expect(
      validate({
        ...requestFixture,
        injected: true,
      }),
    ).toBe(false);
  });
});

describe("UTC event timestamp schema", () => {
  it("rejects impossible calendar dates and non-UTC offsets", () => {
    const validate = ajv.compile(eventSchema as AnySchema);
    expect(
      validate({
        ...eventFixture,
        occurredAt: "2026-02-30T18:00:00Z",
      }),
    ).toBe(false);
    expect(
      validate({
        ...eventFixture,
        occurredAt: "2026-11-07T18:00:00+00:00",
      }),
    ).toBe(false);
  });
});
