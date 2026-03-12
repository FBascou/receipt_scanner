import type { APIContext } from "astro";
import { requestApi } from "../../../lib/requestApi";
import { err, ok } from "../../../lib/requestResult";
import { USER_ENDPOINTS } from "../endpoints/endpointUsers";

export async function getUser(context: APIContext) {
  const response = await requestApi(context, USER_ENDPOINTS.me, {
    method: "GET",
  });

  const json = await response.json();

  if (!response.ok) {
    return err({ reason: "Unauthorized", details: json });
  }

  return ok(json);
}
