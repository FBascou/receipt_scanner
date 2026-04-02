import type { AstroGlobal } from "astro";
import { getRegisterService } from "../services/getRegisterService";
import type { RegisterPostType } from "../types/authTypes";

export async function getRegisterAction(data: RegisterPostType, Astro: AstroGlobal) {
  const result = await getRegisterService(Astro, data);

  if ("data" in result) {
    return Astro.redirect("/");
  }

  return {
    message: result.error?.message ?? "Login failed",
    code: result.error?.code,
    field: result.error?.field,
  };
}
