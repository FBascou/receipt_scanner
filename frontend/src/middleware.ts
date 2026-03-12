import { defineMiddleware } from "astro:middleware";
import { getUser } from "./features/users/api/userApi";
import type { MiddlewareHandler } from "astro";
import type { User } from "./features/users/types/userTypes";

const PUBLIC_ROUTES = ["/login", "/register", "/forgot-password"];
// const PROTECTED_ROUTES = [
//   "/",
//   "/receipts",
//   "/account",
//   "/devices",
//   "/settings",
//   "/subscription",
//   "/logout",
// ];

export const onRequest: MiddlewareHandler = defineMiddleware(async (context, next) => {
  const token = context.cookies.get("access_token")?.value;

  let user: User | null = null;

  if (token) {
    try {
      const [error, res] = await getUser(context);
      if (!error) user = res;
    } catch {
      user = null;
    }
  }

  context.locals.user = user;

  const path = context.url.pathname;

  const isPublic = PUBLIC_ROUTES.includes(path);

  // 🚫 Not logged in trying to access protected page
  if (!isPublic && !user) {
    return context.redirect("/login");
  }

  // 🔁 Logged in user going to login/register
  if (user && isPublic) {
    return context.redirect("/");
  }

  // When adding admin
  // if (path.startsWith("/admin") && user?.role !== "admin") {
  //   return context.redirect("/");
  // }

  return next();
});
