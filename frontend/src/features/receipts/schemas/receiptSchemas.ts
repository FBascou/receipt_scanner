import { z } from "zod";

const MIN_FILE_SIZE = 100_000;
const MAX_FILE_SIZE = 5_000_000;
const ACCEPTED_IMAGE_TYPES = ["image/jpeg", "image/jpg", "image/png"];

export const ScanSingleSchema = z.object({
  files: z
    .file()
    .min(MIN_FILE_SIZE, { error: "Min image size is 100KB" })
    .max(MAX_FILE_SIZE, { error: "Max image size is 5MB" })
    .mime(ACCEPTED_IMAGE_TYPES, {
      error: "Only .jpg, .jpeg, and .png formats are supported.",
    }),
});

export const ScanBatchSchema = z.object({
  files: z
    .file()
    .min(MIN_FILE_SIZE, { error: "Min image size is 5MB" })
    .max(MAX_FILE_SIZE, { error: "Max image size is 5MB" })
    .mime(ACCEPTED_IMAGE_TYPES, {
      error: "Only .jpg, .jpeg, and .png formats are supported.",
    })
    .array()
    .min(1, { error: "Upload at least one receipt" })
    .max(20, { error: "20 receipts are the limit" }),
});

export const ReceiptResponseSchema = z.object({
  message: z.string(),
  details: {
    error: {
      code: z.string(),
      message: z.string(),
      field: z.string(),
      status: z.number(),
    },
  },
});
