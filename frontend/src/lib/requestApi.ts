import type { APIContext } from "astro";
import { API_BASE_URL } from "./config";

export async function requestApi(
  context: APIContext,
  url: string,
  options: RequestInit = {},
): Promise<Response> {
  const token = context.cookies.get("access_token")?.value;

  const headers = {
    // "Content-Type": "application/json",
    cookie: context.request.headers.get("cookie") ?? "",
    ...(token && { Authorization: `Bearer ${token}` }),
    ...(options.headers || {}),
  };

  return await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers,
  });
}
