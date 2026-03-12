import { createService } from "../../../lib/createService";
import { postRegister } from "../api/authApi";
import { RegisterSchema } from "../schemas/authSchemas";

export const getRegisterService = createService(RegisterSchema, async (context, data) => {
  return postRegister(context, data);
});
