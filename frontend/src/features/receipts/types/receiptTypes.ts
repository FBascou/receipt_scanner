import z from "zod";
import type { ScanBatchSchema } from "../schemas/receiptSchemas";

export type JobUploadSourceType = "MANUAL" | "AUTOMATIC";

export type JobStatusType = "PENDING" | "PROCESSED" | "FAILED";

export type JobGetResponseType = {
  id: string;
  device_id: string | null;
  total_amount: number;
  uploaded_at: string;
  image_count: number;
  source: JobUploadSourceType;
  status: JobStatusType;
};

export type JobGetType = {
  total_pages: number;
  page: number;
  page_size: number;
  items: JobGetResponseType[];
};
// export type JobResponseSchemaType = z.infer<typeof ScanBatchSchema>;

export type ScanBatchPostType = { files: File[] };

export type ScanBatchSchemaType = z.infer<typeof ScanBatchSchema>;

export type TableReceiptsRowsType = {
  id: string;
  device_id: string | null;
  total_amount: number;
  uploaded_at: string;
  image_count: number;
  source: JobUploadSourceType;
  status: JobStatusType;
};
