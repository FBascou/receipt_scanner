import type { APIContext } from "astro";
import { API_BASE_URL } from "./config";
import type { ApiErrorType } from "../types/types";

// network layer
export async function requestApi<T>(
  context: APIContext,
  endpoint: string,
  options: RequestInit = {},
): Promise<{ data?: T; error?: ApiErrorType; status: number }> {
  const token = context.cookies.get("access_token")?.value;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      signal: controller.signal,
      headers: {
        // cookie: context.request.headers.get("cookie") ?? "",
        ...(options.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
        ...(token && { Authorization: `Bearer ${token}` }),
        ...(options.headers || {}),
      },
    });

    const json = await response.json();
    // let json: any = null;
    // try {
    //   json = await response.json();
    // } catch {
    //   json = null;
    // }

    if (!response.ok) {
      return {
        error: {
          code: json?.detail?.error?.code ?? "UNKNOWN",
          message: json?.detail?.error?.message ?? "Request failed",
          field: json?.detail?.error?.field,
        },
        status: json?.detail?.error?.status,
      };
    }

    return {
      data: json as T,
      status: response.status,
    };
  } catch (err) {
    if ((err as any).name === "AbortError") {
      return {
        error: {
          code: "TIMEOUT",
          message: "Request timed out",
          details: err,
        },
        status: 0,
      };
    }

    return {
      error: {
        code: "NETWORK_ERROR",
        message: "Network error",
        details: err,
      },
      status: 0,
    };
  } finally {
    clearTimeout(timeout);
  }
}
