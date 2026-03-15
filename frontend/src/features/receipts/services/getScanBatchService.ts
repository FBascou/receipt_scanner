import { createService } from "../../../lib/createService";
import { postScanBatch } from "../api/receiptApi";
import { ScanBatchSchema } from "../schemas/receiptSchemas";

export const getScanBatchService = createService(ScanBatchSchema, async (context, data) => {
  return postScanBatch(context, data);
});
