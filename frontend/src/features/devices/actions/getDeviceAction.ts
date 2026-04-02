import type { AstroGlobal } from "astro";
import type { DevicePostType } from "../types/deviceTypes";
import { getDeviceService } from "../services/getDeviceService";

export async function getDeviceAction(data: DevicePostType, Astro: AstroGlobal) {
  const result = await getDeviceService(Astro, data);

  if ("data" in result) {
    console.log("result", result);
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
