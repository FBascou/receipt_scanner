import { z } from "zod";

const PasswordSchema = z
  .string()
  .min(8, { message: "Password should have a minimum of 8 characters" })
  // .max(20, { message: maxLengthErrorMessage })
  .refine((password: string) => /[A-Z]/.test(password), {
    message: "Password should have at least one uppercase character",
  })
  .refine((password: string) => /[a-z]/.test(password), {
    message: "Password should have at least one lowercase character",
  })
  .refine((password: string) => /[0-9]/.test(password), {
    message: "Password should have at least one number",
  })
  .refine((password: string) => /[#?!@$%^&*-]/.test(password), {
    message: "Password should have at least one special character: #?!@$%^&*-",
  });

export const LoginSchema = z.object({
  email: z.email().min(1, { error: "Email cannot be empty" }),
  password: z.string().min(1, { error: "Password cannot be empty" }),
});

export const RegisterSchema = z
  .object({
    email: z.email({ error: "Invalid email address" }).min(1, { error: "Email cannot be empty" }),
    password: PasswordSchema,
    confirm: z.string().min(1, { error: "Password cannot be empty" }),
  })
  .refine((data: any) => data.password === data.confirm, {
    message: "Passwords don't match",
    path: ["confirm"],
    // when(payload) {
    //   return RegisterSchema.pick({ password: true, confirmPassword: true }).safeParse(
    //     payload.value,
    //   ).success;
    // },
  });

export const RegisterResponseSchema = z.object({
  message: z.string(),
  details: {
    error: {
      code: z.string(),
      message: z.string(),
      field: z.string(),
      status: z.number(),
    },
  },
});
