import z from "zod";

// TODO:
// Password should be at least 8 different characters

export const LoginSchema = z.object({
  email: z.email().min(1),
  password: z.string().min(1),
});

export const RegisterSchema = z
  .object({
    email: z.email({ error: "Invalid email address" }).min(1, { error: "Email cannot be empty" }),
    password: z.string().min(1, { error: "Password cannot be empty" }),
    confirm: z.string().min(1, { error: "Password cannot be empty" }),
  })
  .refine((data) => data.password === data.confirm, {
    message: "Passwords don't match",
    path: ["confirm"],
    // when(payload) {
    //   return RegisterSchema.pick({ password: true, confirmPassword: true }).safeParse(
    //     payload.value,
    //   ).success;
    // },
  });
