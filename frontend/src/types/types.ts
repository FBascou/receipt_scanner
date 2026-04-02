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

export type ServiceResultType<T> =
  | { data: T; error?: never; status: number }
  | { data?: never; error: ApiErrorType; status: number };
