import type { APIContext, AstroGlobal } from "astro";
import { getUserService } from "../services/getUserService";

export async function getUserAction(data: string | APIContext | undefined, Astro: AstroGlobal) {
  const result = await getUserService(Astro, data);

  if ("data" in result) {
    return Astro.redirect("/");
  }

  return {
    message: result.error?.message ?? "User not found",
    code: result.error?.code,
    field: result.error?.field,
  };
}
