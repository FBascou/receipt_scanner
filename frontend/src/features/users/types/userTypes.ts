export type User = {
  id: string;
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
