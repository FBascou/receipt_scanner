import type { APIContext } from "astro";
import type { ServiceResultType } from "../types/types";

// validation + safety
export function createService<Input, Parsed, Output>(
  schema: {
    safeParse: (data: Input) => { success: boolean; data?: Parsed; error?: any };
  },
  handler: (context: APIContext, data: Parsed) => Promise<ServiceResultType<Output>>,
) {
  return async function service(
    context: APIContext,
    data: Input,
  ): Promise<ServiceResultType<Output>> {
    const parsed = schema.safeParse(data);

    if (!parsed.success || !parsed.data) {
      return {
        error: {
          code: "INVALID_DATA",
          message: "Invalid input",
          details: parsed.error,
        },
      };
    }

    try {
      return await handler(context, parsed.data);
    } catch (error) {
      return {
        error: {
          code: "UNEXPECTED",
          message: "Something went wrong, please try again",
          details: error,
        },
      };
    }
  };
}
