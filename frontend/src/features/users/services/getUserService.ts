import { getUser } from "../api/userApi";
import { createService } from "../../../lib/createService";
import { UserSchema } from "../types/userTypes";

export const getUserService = createService(UserSchema, async (context) => {
  return getUser(context);
});
