import type { APIContext } from "astro";
import { API_BASE_URL } from "./config";

export async function requestApi(
  context: APIContext,
  endpoint: string,
  options: RequestInit = {},
): Promise<Response> {
  const token = context.cookies.get("access_token")?.value;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);

  const headers = {
    // cookie: context.request.headers.get("cookie") ?? "",
    ...(token && { Authorization: `Bearer ${token}` }),
    ...(options.headers || {}),
  };

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      signal: controller.signal,
      headers,
    });
    return response;
  } catch (err) {
    if ((err as any).name === "AbortError") {
      console.error(`Request to ${endpoint} timed out`);
    }
    throw err;
  } finally {
    clearTimeout(timeout);
  }
}
