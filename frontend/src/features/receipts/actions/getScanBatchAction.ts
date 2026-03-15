import type { AstroGlobal } from "astro";
import { getScanBatchService } from "../services/getScanBatchService";
import type { ScanBatchPostType } from "../types/receiptTypes";

export async function getScanBatchAction(data: ScanBatchPostType, Astro: AstroGlobal) {
  const [error, response] = await getScanBatchService(Astro, data);
  console.log("getScanBatchAction", { error, response });

  if (!error) {
    console.log("Success");
  }

  // FIX ERROR MESSAGES
  const reason = error?.reason || "InvalidData";
  switch (reason) {
    case "InvalidData":
      return { message: "Scan batch failed", details: error?.details };
    case "Unauthorized":
      return { message: "Invalid credentials, wrong email and/or password" };
    case "Unexpected":
      return { message: "Unexpected error" };
    default:
      throw new Error(`Unhandled error: ${reason satisfies never}`);
  }
}
