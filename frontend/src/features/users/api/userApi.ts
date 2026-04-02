import type { APIContext } from "astro";
import { requestApi } from "../../../lib/requestApi";
import { toServiceResult } from "../../../lib/requestResult";
import { USER_ENDPOINTS } from "../endpoints/userEndpoints";

export async function getUser(context: APIContext) {
  const result = await requestApi<User | null>(context, USER_ENDPOINTS.me, {
    method: "GET",
  });

  return toServiceResult(result);
}

export async function getUserOverview(context: APIContext) {
  const result = await requestApi(context, USER_ENDPOINTS.overview, {
    method: "GET",
  });

  return toServiceResult(result);
}
