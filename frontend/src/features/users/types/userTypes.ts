export type User = {
  id: number;
  email: string;
  role: "user" | "admin";
  created_at: string;
};

export type UserOverview = {
  devices: number;
  job_count: number;
  receipt_count: number;
  receipt_amount: number;
};
