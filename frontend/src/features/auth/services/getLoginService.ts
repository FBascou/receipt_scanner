import { createService } from "../../../lib/createService";
import { postLogin } from "../api/authApi";
import { LoginSchema } from "../schemas/authSchemas";

export const getLoginService = createService(LoginSchema, async (context, data) => {
  return postLogin(context, data);
});
