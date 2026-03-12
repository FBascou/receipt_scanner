import type { User } from "../../features/users/types/userTypes";

type RouteGuard = {
  path: string;
  requireAuth?: boolean;
  roles?: User["role"][];
};

export const routeGuards: RouteGuard[] = [
  { path: "/login" },
  { path: "/register" },
  { path: "/reset-password" },

  { path: "/", requireAuth: true },
  { path: "/receipts", requireAuth: true },
  { path: "/account", requireAuth: true },
  { path: "/devices", requireAuth: true },
  { path: "/settings", requireAuth: true },
  { path: "/subscription", requireAuth: true },
  { path: "/logout", requireAuth: true },

  { path: "/admin", requireAuth: true, roles: ["admin"] },
  { path: "/users", requireAuth: true, roles: ["admin"] },
];
