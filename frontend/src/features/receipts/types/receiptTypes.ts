import z from "zod";
import type { ScanBatchSchema } from "../schemas/receiptSchemas";

// export type JobSchemaType = z.infer<typeof any>;

export type JobGetType = {
  files: string[];
};

// export type JobResponseSchemaType = z.infer<typeof ScanBatchSchema>;

export type JobFiltersType = {
  page: number;
  page_size: number;
  sort_by: "uploaded_at";
  order: "asc" | "desc";
};

export type ScanBatchPostType = { files: string[] };

export type ScanBatchSchemaType = z.infer<typeof ScanBatchSchema>;
