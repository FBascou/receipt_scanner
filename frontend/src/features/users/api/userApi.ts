import type { APIContext } from "astro";
import { requestApi } from "../../../lib/requestApi";
import { toServiceResult } from "../../../lib/requestResult";
import { USER_ENDPOINTS } from "../endpoints/userEndpoints";
import type { UserOverviewType } from "../types/userTypes";

export async function getUser(context: APIContext) {
  const result = await requestApi<UserType | null>(context, USER_ENDPOINTS.me, {
    method: "GET",
  });

  return toServiceResult(result);
}

export async function getUserOverview(context: APIContext) {
  const result = await requestApi<UserOverviewType | null>(context, USER_ENDPOINTS.overview, {
    method: "GET",
  });

  return toServiceResult(result);
}

export async function patchUser(context: APIContext) {
  const result = await requestApi<UserType | null>(context, USER_ENDPOINTS.users, {
    method: "PATCH",
  });

  return toServiceResult(result);
}
