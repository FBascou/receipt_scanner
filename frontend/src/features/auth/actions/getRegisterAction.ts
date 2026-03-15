import type { AstroGlobal } from "astro";
import { getRegisterService } from "../services/getRegisterService";
import type { RegisterPostType } from "../types/authTypes";

export async function getRegisterAction(data: RegisterPostType, Astro: AstroGlobal) {
  const [error, _] = await getRegisterService(Astro, data);

  if (!error) {
    return Astro.redirect("/login");
  }

  const reason = error.reason;
  switch (reason) {
    case "InvalidData":
      return { message: "Registration failed", details: error?.details?.detail };
    case "Unauthorized":
      return { message: "Invalid credentials", details: error?.details?.detail };
    case "Unexpected":
      return { message: "Unexpected error" };
    default:
      throw new Error(`Unhandled error: ${reason satisfies never}`);
  }
}
