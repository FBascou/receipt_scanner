import type { APIContext } from "astro";
import { toServiceResult } from "../../../lib/requestResult";
import type { ServiceResultType } from "../../../types/types";
import { requestApi } from "../../../lib/requestApi";
import { DEVICE_ENDPOINTS } from "../endpoints/deviceEndpoints";
import type {
  DevicePostType,
  DevicePostResponseType,
  DeviceGetType,
  DeviceGetResponseType,
} from "../types/deviceTypes";

export async function getDevices(
  context: APIContext,
  data: DeviceGetType,
): Promise<ServiceResultType<DeviceGetResponseType>> {
  // Add  return data type
  const result = await requestApi<DeviceGetResponseType>(
    context,
    `${DEVICE_ENDPOINTS.devices}/${data}`,
    {
      method: "GET",
    },
  );

  return toServiceResult(result);
}

export async function postDevices(
  context: APIContext,
  data: DevicePostType,
): Promise<ServiceResultType<DevicePostResponseType>> {
  // Add  return data type
  const result = await requestApi<DevicePostResponseType>(context, DEVICE_ENDPOINTS.devices, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  return toServiceResult(result);
}
