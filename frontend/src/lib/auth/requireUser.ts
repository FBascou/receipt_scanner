import type { APIContext } from "astro";
import type { User } from "../../features/users/types/userTypes";

export function requireUser(context: APIContext): User {
  const user = context.locals.user;

  if (!user) {
    throw new Error("User not authenticated");
  }

  return user;
}
