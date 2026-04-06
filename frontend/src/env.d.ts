type UserType = {
  // id: string;
  email: string;
  role: "user" | "admin";
  created_at: string;
};

declare namespace App {
  interface Locals {
    user: UserType | null;
  }
}
