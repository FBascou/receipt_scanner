import type { ApiErrorType, ServiceResultType } from "../types/types";

export type Result<Error extends { reason: string }, Success> = [Error, null] | [null, Success];

export function ok<Success>(data: Success): Result<never, Success> {
  return [null, data];
}

export function err<const Reason extends string, Error extends { reason: Reason }>(
  error: Error,
): Result<Error, never> {
  return [error, null];
}

export function toServiceResult<T>(result: {
  data?: T;
  error?: ApiErrorType;
  status: number;
}): ServiceResultType<T> {
  if (result.error) {
    return { error: result.error, status: result.status };
  }

  if (result.data !== undefined) {
    return { data: result.data, status: result.status };
  }

  return {
    error: {
      code: "UNKNOWN",
      message: "Invalid API response",
    },
    status: result.status,
  };
}
