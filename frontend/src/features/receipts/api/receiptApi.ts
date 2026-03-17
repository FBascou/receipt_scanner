import { err, ok } from "../../../lib/requestResult";
import { requestApi } from "../../../lib/requestApi";
import { RECEIPT_ENDPOINTS } from "../endpoints/receiptEndpoints";
import type { APIContext } from "astro";
import type { ScanBatchSchemaType } from "../types/receiptTypes";

export async function getJobs(
  context: APIContext,
  filterParams: string = "?page=1&page_size=20&sort_by=uploaded_at&order=desc",
) {
  const response = await requestApi(context, `${RECEIPT_ENDPOINTS.jobs}/${filterParams}`, {
    method: "GET",
  });

  const json = await response.json();

  if (!response.ok) {
    return err({ reason: "Unauthorized", details: json });
  }

  return ok(json);
}

export async function postScanBatch(context: APIContext, data: ScanBatchSchemaType) {
  const formData = new FormData();

  data.files?.forEach((file) => {
    formData.append("files", file);
  });

  const response = await requestApi(context, RECEIPT_ENDPOINTS.scanBatch, {
    method: "POST",
    body: formData,
    headers: {
      // backend uses cookies????
      // cookie: context.request.headers.get("cookie") ?? "",
      // "Content-Type": "multipart/form-data",
    },
    // credentials: "include", // CHECK HOW TO IMPLEMENT THIS
  });

  console.log("postScanBatch response", response);

  const json = await response.json();

  if (!response.ok) {
    return err({ reason: "Unauthorized", details: json });
  }

  return ok(json);
}
