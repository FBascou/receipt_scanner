import z from "zod";
import type { ScanBatchSchema } from "../schemas/receiptSchemas";

// export type JobSchemaType = z.infer<typeof any>;

export type JobGetType = {
  total: 0;
  page: 0;
  page_size: 0;
  items: [
    {
      id: "3fa85f64-5717-4562-b3fc-2c963f66afa6";
      uploaded_at: "2026-03-16T20:57:11.432Z";
      source: "manual_upload";
      image_count: 0;
      status: "PENDING";
    },
  ];
};

// export type JobResponseSchemaType = z.infer<typeof ScanBatchSchema>;

export type JobFiltersType = {
  page: number;
  page_size: number;
  sort_by: "uploaded_at";
  order: "asc" | "desc";
};

export type ScanBatchPostType = { files: File[] };

export type ScanBatchSchemaType = z.infer<typeof ScanBatchSchema>;
