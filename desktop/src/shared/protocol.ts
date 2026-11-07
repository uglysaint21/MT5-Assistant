export const PROTOCOL_VERSION = 1 as const;

export type RequestEnvelope<TPayload = Record<string, unknown>> = {
  kind: "request";
  protocolVersion: typeof PROTOCOL_VERSION;
  requestId: string;
  operation: string;
  payload: TPayload;
};

export type SuccessResponse<TResult = Record<string, unknown>> = {
  kind: "response";
  protocolVersion: typeof PROTOCOL_VERSION;
  requestId: string;
  ok: true;
  result: TResult;
};

export type ErrorResponse = {
  kind: "response";
  protocolVersion: typeof PROTOCOL_VERSION;
  requestId: string;
  ok: false;
  error: {
    code: string;
    message: string;
    retryable: boolean;
    details?: Record<string, unknown>;
  };
};

export type ProtocolResponse<TResult = Record<string, unknown>> =
  | SuccessResponse<TResult>
  | ErrorResponse;

export type ReadyMessage = {
  kind: "ready";
  protocolVersion: typeof PROTOCOL_VERSION;
  serviceVersion: string;
  capabilities: string[];
};

export type EventMessage = {
  kind: "event";
  protocolVersion: typeof PROTOCOL_VERSION;
  eventId: string;
  event: string;
  occurredAt: string;
  payload: Record<string, unknown>;
};

export type ProtocolEnvelope =
  | RequestEnvelope
  | ProtocolResponse
  | ReadyMessage
  | EventMessage;

type UnknownRecord = Record<string, unknown>;

function isRecord(value: unknown): value is UnknownRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function hasExactKeys(
  value: UnknownRecord,
  required: string[],
  optional: string[] = []
): boolean {
  const keys = Object.keys(value);
  return required.every((key) => Object.hasOwn(value, key)) &&
    keys.every((key) => required.includes(key) || optional.includes(key));
}

function isNonEmptyString(value: unknown, maxLength = 256): value is string {
  return typeof value === "string" && value.trim().length > 0 && value.length <= maxLength;
}

function isUtcTimestamp(value: unknown): value is string {
  if (typeof value !== "string") return false;
  const match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,6})?Z$/.exec(value);
  if (!match) return false;

  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  const hour = Number(match[4]);
  const minute = Number(match[5]);
  const second = Number(match[6]);
  const date = new Date(Date.UTC(year, month - 1, day, hour, minute, second));

  return Number.isFinite(date.getTime()) &&
    date.getUTCFullYear() === year &&
    date.getUTCMonth() === month - 1 &&
    date.getUTCDate() === day &&
    date.getUTCHours() === hour &&
    date.getUTCMinutes() === minute &&
    date.getUTCSeconds() === second;
}

function isErrorPayload(value: unknown): value is ErrorResponse["error"] {
  if (!isRecord(value) ||
      !hasExactKeys(value, ["code", "message", "retryable"], ["details"])) return false;
  return isNonEmptyString(value.code, 128) &&
    isNonEmptyString(value.message, 1024) &&
    typeof value.retryable === "boolean" &&
    (!Object.hasOwn(value, "details") || isRecord(value.details));
}

export function isProtocolResponse(value: unknown): value is ProtocolResponse {
  if (!isRecord(value) ||
      value.kind !== "response" ||
      value.protocolVersion !== PROTOCOL_VERSION ||
      !isNonEmptyString(value.requestId, 128) ||
      typeof value.ok !== "boolean") return false;

  if (value.ok) {
    return hasExactKeys(value, ["kind", "protocolVersion", "requestId", "ok", "result"]) &&
      isRecord(value.result);
  }
  return hasExactKeys(value, ["kind", "protocolVersion", "requestId", "ok", "error"]) &&
    isErrorPayload(value.error);
}

export function isProtocolEnvelope(value: unknown): value is ProtocolEnvelope {
  if (!isRecord(value) || value.protocolVersion !== PROTOCOL_VERSION) return false;

  if (value.kind === "response") return isProtocolResponse(value);

  if (value.kind === "request") {
    return hasExactKeys(value, [
      "kind", "protocolVersion", "requestId", "operation", "payload"
    ]) &&
      isNonEmptyString(value.requestId, 128) &&
      isNonEmptyString(value.operation, 128) &&
      isRecord(value.payload);
  }

  if (value.kind === "ready") {
    if (!hasExactKeys(value, [
      "kind", "protocolVersion", "serviceVersion", "capabilities"
    ]) || !isNonEmptyString(value.serviceVersion, 64) || !Array.isArray(value.capabilities)) {
      return false;
    }
    return value.capabilities.every((item) => isNonEmptyString(item)) &&
      new Set(value.capabilities).size === value.capabilities.length;
  }

  if (value.kind === "event") {
    return hasExactKeys(value, [
      "kind", "protocolVersion", "eventId", "event", "occurredAt", "payload"
    ]) &&
      isNonEmptyString(value.eventId, 128) &&
      isNonEmptyString(value.event, 128) &&
      isRecord(value.payload) &&
      isUtcTimestamp(value.occurredAt);
  }

  return false;
}
