export type Result<Error extends { reason: string }, Success> = [Error, null] | [null, Success];

export function ok<Success>(data: Success): Result<never, Success> {
  return [null, data];
}

export function err<const Reason extends string, Error extends { reason: Reason }>(
  error: Error,
): Result<Error, never> {
  return [error, null];
}
