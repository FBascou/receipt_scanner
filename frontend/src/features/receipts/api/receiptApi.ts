import { toServiceResult } from "../../../lib/requestResult";
import { requestApi } from "../../../lib/requestApi";
import { RECEIPT_ENDPOINTS } from "../endpoints/receiptEndpoints";
import type { APIContext } from "astro";
import type { ScanBatchSchemaType } from "../types/receiptTypes";

export async function getJobs(
  context: APIContext,
  filterParams: string = "?page=1&page_size=20&sort_by=uploaded_at&order=desc",
) {
  const result = await requestApi(context, `${RECEIPT_ENDPOINTS.jobs}/${filterParams}`, {
    method: "GET",
  });

  return toServiceResult(result);
}

export async function postScanBatch(context: APIContext, data: ScanBatchSchemaType) {
  const formData = new FormData();

  data.files?.forEach((file) => {
    formData.append("files", file);
  });

  const result = await requestApi(context, RECEIPT_ENDPOINTS.scanBatch, {
    method: "POST",
    body: formData,
    headers: {
      // backend uses cookies????
      // cookie: context.request.headers.get("cookie") ?? "",
      // "Content-Type": "multipart/form-data",
    },
    // credentials: "include", // CHECK HOW TO IMPLEMENT THIS
  });

  return toServiceResult(result);
}
