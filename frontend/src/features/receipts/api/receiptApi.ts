import { toServiceResult } from "../../../lib/requestResult";
import { requestApi } from "../../../lib/requestApi";
import { RECEIPT_ENDPOINTS } from "../endpoints/receiptEndpoints";
import type { APIContext } from "astro";
import type { JobGetResponseType, ScanBatchSchemaType } from "../types/receiptTypes";
import type { FileTypeEnum, PaginatedListType } from "../../../types/types";
import { API_BASE_URL } from "../../../lib/config";

export async function getJobs(
  context: APIContext,
  filterParams: string = "?page=1&page_size=20&sort_by=uploaded_at&order=desc",
) {
  const result = await requestApi<PaginatedListType<JobGetResponseType>>(
    context,
    `${RECEIPT_ENDPOINTS.jobs}/${filterParams}`,
    {
      method: "GET",
    },
  );

  return toServiceResult(result);
}

export async function postScanBatch(context: APIContext, data: ScanBatchSchemaType) {
  const formData = new FormData();

  data.files?.forEach((file) => {
    formData.append("files", file);
  });

  const result = await requestApi(context, RECEIPT_ENDPOINTS.receiptsBatch, {
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

export function downloadJobFile(jobId: string, fileType: FileTypeEnum) {
  return `${API_BASE_URL}${RECEIPT_ENDPOINTS.jobs}/${jobId}/${fileType}`;
}
