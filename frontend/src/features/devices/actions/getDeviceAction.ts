import type { AstroGlobal } from "astro";
import type { DeviceAddSchemaType } from "../types/deviceTypes";
import { getDeviceService } from "../services/getDeviceService";

export async function getDeviceAction(data: DeviceAddSchemaType, Astro: AstroGlobal) {
  const result = await getDeviceService(Astro, data);

  if ("data" in result) {
    return {
      message: "Device successfully added",
      code: "SUCCESS",
    };
  }

  return {
    message: result.error?.message ?? "Device call failed",
    code: result.error?.code ?? "ERROR",
    field: result.error?.field,
  };
}
