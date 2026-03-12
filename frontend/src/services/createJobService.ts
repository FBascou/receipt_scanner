// import { err, ok } from "../lib/requestResult";

// export async function createJobService(data) {
// const user = await getCurrentUser();
// if (user == null) {
//   return err({ reason: "Unauthenticated" });
// }
// const result = jobSchema.safeParse(data);
// if (!result.success) {
//   return err({ reason: "InvalidData", details: result.error });
// }
// try {
//   return ok(await createJob({ ...result.data }));
// } catch (error) {
//   return err({ reason: "Unexpected" });
// }
// }
