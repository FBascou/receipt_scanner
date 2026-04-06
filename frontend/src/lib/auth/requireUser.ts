import type { APIContext } from "astro";

export function requireUser(context: APIContext): UserType {
  const user = context.locals.user;

  if (!user) {
    throw new Error("User not authenticated");
  }

  return user;
}
