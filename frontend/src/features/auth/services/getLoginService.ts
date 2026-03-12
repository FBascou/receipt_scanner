import { createService } from "../../../lib/createService";
import { postLogin } from "../api/authApi";
import { LoginSchema } from "../schemas/authSchemas";

export const getLoginService = createService(LoginSchema, async (context, data) => {
  return postLogin(context, data);
});

// export async function getLoginService(data: LoginPostType) {
//   // if (!data) {
//   //   return err({ reason: "InvalidData" });
//   // }

//   const result = LoginSchema.safeParse(data);

//   if (!result.success) {
//     return err({ reason: "InvalidData", details: result.error });
//   }

//   // return postLogin(result.data);
//   try {
//     return await postLogin(result.data);
//   } catch {
//     return err({ reason: "Unexpected" });
//   }

//   // try {
//   // Here its wrong, it affects the redirect
//   // const response = await postLogin(result.data);
//   // if (response.ok) {
//   //   return ok(response.json());
//   // } else {
//   //   return err({ reason: "Unauthorized" });
//   // }
//   //   return ok(await postLogin(result.data));
//   // } catch (error) {
//   //   return err({ reason: "Unexpected" });
//   // }
// }
