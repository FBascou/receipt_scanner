import type { APIContext } from "astro";
import { err } from "./requestResult";

export function createService<Input, Parsed, Output, ErrorType>(
  schema: {
    safeParse: (data: Input) => {
      success: boolean;
      data?: Parsed;
      error?: unknown;
    };
  },
  handler: (context: APIContext, data: Parsed) => Promise<[ErrorType, null] | [null, Output]>,
) {
  return async function service(context: APIContext, data: Input) {
    const parsed = schema.safeParse(data);
    console.log("createService parse", { data, parsed, parsedData: parsed.data?.files });

    if (!parsed.success) {
      return err({
        reason: "InvalidData",
        details: parsed.error,
      });
    }

    try {
      return await handler(context, parsed.data as Parsed);
    } catch {
      return err({ reason: "Unexpected" });
    }
  };
}
