export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T | null;
}
export interface ErrorResponse {
  success: false;
  message: string;
  errors: string[];
}
export interface TokenResponse {
  access_token: string | null;
  refresh_token: string | null;
  token_type: string;
  session_id: string | null;
  mfa_required: boolean;
  mfa_challenge_token: string | null;
}
export interface User {
  id: string;
  tenant_id: string;
  email: string;
  display_name: string;
  user_type: string;
  status: string;
  mfa_enabled: boolean;
}
export interface SessionData {
  user: User;
  permissions: string[];
}
export interface ReferenceItem {
  id: string;
  company_id?: string;
  code?: string;
  name?: string;
  status?: string;
  company_code?: string;
  company_name?: string;
  branch_code?: string;
  branch_name?: string;
  customer_code?: string;
  customer_name?: string;
  vendor_code?: string;
  vendor_name?: string;
  currency_code?: string;
  currency_name?: string;
  tax_code?: string;
  tax_name?: string;
  asset_code?: string;
  asset_name?: string;
  cost_center_code?: string;
  cost_center_name?: string;
}
export interface OrgContext {
  company_id?: string | null;
  branch_id?: string | null;
  [key: string]: unknown;
}
export interface HealthData {
  status: string;
  environment: string;
  version: string;
  database: string;
}
