import type { AstroGlobal } from "astro";
import { getLoginService } from "../services/getLoginService";
import type { LoginPostType } from "../types/authTypes";

// side effects (cookies, redirect)
export async function getLoginAction(data: LoginPostType, Astro: AstroGlobal) {
  const result = await getLoginService(Astro, data);

  if ("data" in result) {
    Astro.cookies.set("access_token", result.data.access_token, {
      httpOnly: true,
      secure: true,
      sameSite: "lax",
      path: "/",
    });

    return Astro.redirect("/");
  }

  return {
    message: result.error?.message ?? "Login failed",
    code: result.error?.code,
    field: result.error?.field,
  };
}
