import { getUser } from "../api/userApi";
import z from "zod";
import { createService } from "../../../lib/createService";

const UserSchema = z.string().optional();

export const getUserService = createService(UserSchema, async (context) => {
  return getUser(context);
});

// export async function getUserService(context: APIContext) {
//   const token = context.cookies.has("access_token");
//   if (!token) {
//     return err({ reason: "Unauthenticated" });
//   }

//   const result = UserSchema.safeParse(token);

//   if (!result.success) {
//     return err({ reason: "InvalidData", details: result.error });
//   }

//   try {
//     return ok(await getUser(context));
//   } catch (error) {
//     return err({ reason: "Unexpected" });
//   }
// }
