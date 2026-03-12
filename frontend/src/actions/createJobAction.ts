// import type { AstroGlobal } from "astro";
// import { createJobService } from "../../../services/createJobService";

// export async function createJobAction(data, Astro: AstroGlobal) {
//   const [error, job] = createJobService(data);

//   if (error === null) {
//     return Astro.redirect(`/receipts/${job.id}`);
//   }

//   const reason = error.reason;
//   switch (reason) {
//     case "InvalidData":
//       return { message: "Invalid data", details: error.details };
//     case "Unauthenticated":
//       return Astro.redirect("/login");
//     case "Unexpected":
//       return { message: "Unexpected error" };
//     default:
//       throw new Error(`Unhandled error: ${reason satisfies never}`);
//   }
// }
