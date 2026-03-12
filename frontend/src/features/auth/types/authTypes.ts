import type z from "zod";
import type { LoginSchema, RegisterSchema } from "../schemas/authSchemas";

export type LoginSchemaType = z.infer<typeof LoginSchema>;

export type LoginPostType = {
  email: string;
  password: string;
};

export type RegisterSchemaType = z.infer<typeof RegisterSchema>;

export type RegisterPostType = {
  email: string;
  password: string;
  confirm: string;
};

export type RegisterSchemaFlattenedErrorsType =
  | z.core.$ZodFlattenedError<RegisterSchemaType, { message: string; errorCode: string }>
  | { fieldErrors?: Record<string, string[]> };
