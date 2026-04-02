import z from "zod";
import type { LoginSchema, RegisterResponseSchema, RegisterSchema } from "../schemas/authSchemas";

export type LoginSchemaType = z.infer<typeof LoginSchema>;

export type LoginPostType = {
  email: string;
  password: string;
};

export type LoginPostResponseType = {
  access_token: string;
  token_type: string;
};

export type RegisterSchemaType = z.infer<typeof RegisterSchema>;

export type RegisterPostType = {
  email: string;
  password: string;
  confirm: string;
};

export type RegisterPostResponseType = {};

export type RegisterSchemaFlattenedErrorsType =
  | z.core.$ZodFlattenedError<RegisterSchemaType, { message: string; errorCode: string }>
  | { fieldErrors?: Record<string, string[]> };

export type RegisterResponseSchemaType = z.infer<typeof RegisterResponseSchema>;

export type SchemaFlattenedErrorsType<T> =
  | z.core.$ZodFlattenedError<T, { message: string; errorCode: string }>
  | { fieldErrors?: Record<string, string[]> };
