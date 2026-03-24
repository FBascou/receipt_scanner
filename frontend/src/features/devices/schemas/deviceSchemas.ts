import { z } from "zod";

export const DeviceAddSchema = z.object({
  user_id: z.uuidv4(),
  name: z.string(),
  mac: z.string(),
  ip: z.string(),
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
