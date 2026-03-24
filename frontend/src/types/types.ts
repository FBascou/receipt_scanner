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
