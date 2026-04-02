import { AUTH_ENDPOINTS } from "../endpoints/authEndpoints";
import type {
  LoginPostResponseType,
  LoginPostType,
  RegisterPostResponseType,
  RegisterPostType,
} from "../types/authTypes";
import { toServiceResult } from "../../../lib/requestResult";
import { requestApi } from "../../../lib/requestApi";
import type { APIContext } from "astro";
import type { ServiceResultType } from "../../../types/types";

export async function postLogin(
  context: APIContext,
  data: LoginPostType,
): Promise<ServiceResultType<LoginPostResponseType>> {
  const result = await requestApi<LoginPostResponseType>(context, AUTH_ENDPOINTS.login, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return toServiceResult(result);
}

export async function postRegister(
  context: APIContext,
  data: RegisterPostType,
): Promise<ServiceResultType<RegisterPostResponseType>> {
  const result = await requestApi<RegisterPostResponseType>(context, AUTH_ENDPOINTS.register, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return toServiceResult(result);
}
