import type { APIContext, AstroGlobal } from "astro";
import { getUserService } from "../services/getUserService";

export async function getUserAction(data: string | APIContext | undefined, Astro: AstroGlobal) {
  const [error, _] = await getUserService(Astro, data);

  if (!error) {
    return Astro.redirect(`/`);
  }

  const reason = error.reason;
  switch (reason) {
    case "InvalidData":
      return { message: "Invalid data", details: error.details };
    case "Unauthorized":
      return Astro.redirect("/login");
    case "Unexpected":
      return { message: "Unexpected error" };
    default:
      throw new Error(`Unhandled error: ${reason satisfies never}`);
  }
}
