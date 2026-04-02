import { createService } from "../../../lib/createService";
import { postDevices } from "../api/deviceApi";
import { DeviceAddSchema } from "../schemas/deviceSchemas";

export const getDeviceService = createService(DeviceAddSchema, async (context, data) => {
  return postDevices(context, data);
});
