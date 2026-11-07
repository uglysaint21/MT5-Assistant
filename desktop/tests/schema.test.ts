import Ajv, { type AnySchema } from "ajv";
import addFormats from "ajv-formats";
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

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

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
    const validate = ajv.compile(requestSchema);
    expect(validate({
      ...requestFixture,
      injected: true
    })).toBe(false);
  });
});
