import type { AstroGlobal } from "astro";
import { getRegisterService } from "../services/getRegisterService";
import type { RegisterPostType } from "../types/authTypes";

export async function getRegisterAction(data: RegisterPostType, Astro: AstroGlobal) {
  const [error, response] = await getRegisterService(Astro, data);

  if (!error) {
    // Astro.cookies.set("access_token", response.access_token, {
    //   httpOnly: true,
    //   secure: true,
    //   sameSite: "lax",
    //   path: "/",
    // });

    return Astro.redirect("/login");
  }

  const reason = error.reason;
  switch (reason) {
    case "InvalidData":
      return { message: "Register failed", details: error.details };
    case "Unauthorized":
      return { message: "Invalid credentials" };
    // case "Unauthenticated":
    //   return Astro.redirect("/register");
    case "Unexpected":
      return { message: "Unexpected error" };
    default:
      throw new Error(`Unhandled error: ${reason satisfies never}`);
  }
}
