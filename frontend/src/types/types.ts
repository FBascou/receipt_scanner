export enum FileTypeEnum {
  CSV = "csv",
  PDF = "pdf",
  JSON = "json",
}

export type FiltersPageType = number;

export type FiltersPageSizeType = number;

export type FiltersSortByType = "uploaded_at" | "created_at" | "total" | "status" | "source";

export type FiltersOrderType = "ASC" | "DESC";

export type FiltersSearchType = string;

export type FiltersType = {
  page: FiltersPageType;
  page_size: FiltersPageSizeType;
  sort_by: FiltersSortByType;
  order: FiltersOrderType;
  search: FiltersSearchType;
};

export type ApiErrorType = {
  code?: string;
  message: string;
  field?: string;
  details?: any;
};

// export type ServiceResultType<T> = {
//   data?: T;
//   error?: ApiErrorType;
// };

export type PaginatedListType<T> = {
  total_pages: number;
  page: number;
  page_size: number;
  items: T[];
};

export type ServiceResultType<T> =
  | { data: T; error?: never; status: number }
  | { data?: never; error: ApiErrorType; status: number };

export type OverviewCardType = {
  id: number;
  title: string;
  value: number | string;
};

export type TableHeader = {
  id: string;
  headers: string | null;
  title: string;
};

export type TableHeadersType = TableHeader[];

export type TablePaginationType = {
  total_pages: number;
  page_size: number;
  current_page: number;
};

export type FetchStateType = "error" | "empty" | "success";
