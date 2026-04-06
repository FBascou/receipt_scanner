// export type UserType = {
//   // id: string;
//   email: string;
//   role: "user" | "admin";
//   created_at: string;
// };

import z from "zod";

export const UserSchema = z.string().optional();

export type UserOverviewType = {
  device_count: number;
  job_count: number;
  receipt_count: number;
  receipt_amount: number;
};
