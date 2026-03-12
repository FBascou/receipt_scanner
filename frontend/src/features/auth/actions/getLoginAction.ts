import type { AstroGlobal } from "astro";
import { getLoginService } from "../services/getLoginService";
import type { LoginPostType } from "../types/authTypes";

export async function getLoginAction(data: LoginPostType, Astro: AstroGlobal) {
  const [error, response] = await getLoginService(Astro, data);

  if (!error) {
    Astro.cookies.set("access_token", response.access_token, {
      httpOnly: true,
      secure: true,
      sameSite: "lax",
      path: "/",
    });

    return Astro.redirect("/");
  }

  const reason = error.reason;
  switch (reason) {
    case "InvalidData":
      return { message: "Login failed", details: error.details };
    case "Unauthorized":
      return { message: "Invalid credentials, wrong email and/or password" };
    // case "Unauthenticated":
    //   return Astro.redirect("/login");
    case "Unexpected":
      return { message: "Unexpected error" };
    default:
      throw new Error(`Unhandled error: ${reason satisfies never}`);
  }
}
