import type { AstroGlobal } from "astro";
import { getScanBatchService } from "../services/getScanBatchService";
import type { ScanBatchPostType } from "../types/receiptTypes";

export async function getScanBatchAction(data: ScanBatchPostType, Astro: AstroGlobal) {
  const result = await getScanBatchService(Astro, data);

  if ("data" in result) {
    return {
      message: "Receipts successfully uploaded",
      code: "SUCCESS",
    };
  }

  return {
    message: result.error?.message ?? "Device call failed",
    code: result.error?.code ?? "ERROR",
    field: result.error?.field,
  };
}
