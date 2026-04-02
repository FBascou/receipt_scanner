import z from "zod";
import type { DeviceAddSchema } from "../schemas/deviceSchemas";

export type DeviceStatus = "ONLINE" | "OFFLINE";

export type CardDeviceType = {
  id: string;
  name: string;
  mac: string;
  ip: string;
  status: DeviceStatus;
  created_at: string;
};

export type CardDeviceListType = CardDeviceType[];

export type DeviceAddSchemaType = z.infer<typeof DeviceAddSchema>;

export type DevicePostType = {
  user_id: string;
  name: string;
  mac: string;
  ip: string;
};

export type DevicePostResponseType = {};

export type DeviceGetType = string;

export type DeviceGetResponseType = {
  total: number;
  page: number;
  page_size: number;
  items: [];
};
