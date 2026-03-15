import { AUTH_ENDPOINTS } from "../endpoints/authEndpoints";
import type { LoginPostType, RegisterPostType } from "../types/authTypes";
import { err, ok } from "../../../lib/requestResult";
import { requestApi } from "../../../lib/requestApi";
import type { APIContext } from "astro";

export async function postLogin(context: APIContext, data: LoginPostType) {
  const response = await requestApi(context, AUTH_ENDPOINTS.login, {
    method: "POST",
    body: JSON.stringify(data),
  });

  const json = await response.json();

  if (!response.ok) {
    return err({ reason: "Unauthorized", details: json });
  }

  return ok(json);
}

export async function postRegister(context: APIContext, data: RegisterPostType) {
  const response = await requestApi(context, AUTH_ENDPOINTS.register, {
    method: "POST",
    body: JSON.stringify(data),
  });

  const json = await response.json();

  if (!response.ok) {
    // return err({ reason: "Unauthorized", details: json });
    // maybe return err({reason: json.error.code, details: json}) or simply err(json)
    return err({ reason: "Unauthorized", details: json });
  }

  return ok(json);
}
