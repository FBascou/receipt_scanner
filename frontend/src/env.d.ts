// import type { User } from "./types/user";

type User = {
  id: number;
  email: string;
  role: "user" | "admin";
  created_at: string;
};

declare namespace App {
  interface Locals {
    user: User | null;
  }
}
