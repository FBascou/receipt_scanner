import type { APIContext } from "astro";
import { toServiceResult } from "../../../lib/requestResult";
import type { PaginatedListType, ServiceResultType } from "../../../types/types";
import { requestApi } from "../../../lib/requestApi";
import { DEVICE_ENDPOINTS } from "../endpoints/deviceEndpoints";
import type {
  DeviceAddSchemaType,
  DevicePostResponseType,
  DeviceGetType,
  DeviceGetResponseType,
} from "../types/deviceTypes";

export async function getDevices(
  context: APIContext,
  data: DeviceGetType,
): Promise<ServiceResultType<PaginatedListType<DeviceGetResponseType>>> {
  // Add  return data type
  const result = await requestApi<PaginatedListType<DeviceGetResponseType>>(
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
  data: DeviceAddSchemaType,
): Promise<ServiceResultType<DevicePostResponseType>> {
  // Add  return data type
  const result = await requestApi<DevicePostResponseType>(context, DEVICE_ENDPOINTS.devices, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  return toServiceResult(result);
}
