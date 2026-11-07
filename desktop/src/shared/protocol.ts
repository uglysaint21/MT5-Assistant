export const PROTOCOL_VERSION = 1 as const;

export type RequestEnvelope<TPayload = unknown> = {
  kind: "request";
  protocolVersion: typeof PROTOCOL_VERSION;
  requestId: string;
  operation: string;
  payload: TPayload;
};

export type SuccessResponse<TResult = unknown> = {
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

export type ProtocolResponse<TResult = unknown> =
  | SuccessResponse<TResult>
  | ErrorResponse;

export type ReadyMessage = {
  kind: "ready";
  protocolVersion: typeof PROTOCOL_VERSION;
  serviceVersion: string;
  capabilities: string[];
};

export function isProtocolResponse(value: unknown): value is ProtocolResponse {
  if (typeof value !== "object" || value === null) return false;
  const candidate = value as Record<string, unknown>;
  if (
    candidate.kind !== "response" ||
    candidate.protocolVersion !== PROTOCOL_VERSION ||
    typeof candidate.requestId !== "string" ||
    typeof candidate.ok !== "boolean"
  ) return false;

  if (candidate.ok) return "result" in candidate;
  const error = candidate.error;
  return typeof error === "object" && error !== null &&
    typeof (error as Record<string, unknown>).code === "string" &&
    typeof (error as Record<string, unknown>).message === "string" &&
    typeof (error as Record<string, unknown>).retryable === "boolean";
}
