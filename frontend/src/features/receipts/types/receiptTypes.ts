import z from "zod";
import type { ScanBatchSchema } from "../schemas/receiptSchemas";

export type JobUploadSource = "MANUAL" | "AUTOMATIC";

export type JobStatus = "PENDING" | "PROCESSED" | "FAILED";

export type JobReceiptType = {
  id: string;
  uploaded_at: string;
  source: JobUploadSource;
  image_count: number;
  status: JobStatus;
};

export type JobGetType = {
  total: number;
  page: number;
  page_size: number;
  items: JobReceiptType[];
};
// export type JobResponseSchemaType = z.infer<typeof ScanBatchSchema>;

export type ScanBatchPostType = { files: File[] };

export type ScanBatchSchemaType = z.infer<typeof ScanBatchSchema>;
