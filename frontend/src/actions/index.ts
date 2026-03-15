// import { ActionError, defineAction } from "astro:actions";
// import { RegisterSchema } from "../features/auth/schemas/authSchemas";
// import { getRegisterAction } from "../features/auth/actions/getRegisterAction";

// export const server = {
//   register: defineAction({
//     accept: "form",
//     input: RegisterSchema,

//     async handler(data, context) {
//       const result = await getRegisterAction(data, context);
//       console.log("server result", result);

//       if (!result) {
//         throw new ActionError({
//           code: result.details.error.code,
//           message: result.details.error.message,
//         });
//       }

//       return {
//         success: true,
//         values: data,
//       };
//     },
//   }),
// };
