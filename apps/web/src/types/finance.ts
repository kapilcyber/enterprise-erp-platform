export type AccountType =
  "asset" | "liability" | "equity" | "revenue" | "expense";
export type JournalStatus =
  "draft" | "submitted" | "approved" | "posted" | "reversed" | "cancelled";
export type PeriodStatus = "open" | "soft_closed" | "hard_closed";

export interface AccountGroup {
  id: string;
  company_id: string;
  group_code: string;
  group_name: string;
  account_type: AccountType;
  status: string;
}
export interface ChartAccount {
  id: string;
  company_id: string;
  account_group_id: string;
  account_code: string;
  account_name: string;
  account_type: AccountType;
  normal_balance: "debit" | "credit";
  is_posting_account: boolean;
  status: string;
  version: number;
}
export interface FiscalYear {
  id: string;
  company_id: string;
  fiscal_year_code: string;
  fiscal_year_name: string;
  start_date: string;
  end_date: string;
  status: string;
}
export interface Period {
  id: string;
  company_id: string;
  fiscal_year_id: string;
  period_number: number;
  period_name: string;
  start_date: string;
  end_date: string;
  status: PeriodStatus;
  ar_closed: boolean;
  ap_closed: boolean;
  inventory_closed?: boolean;
  payroll_closed?: boolean;
  gl_closed: boolean;
}
export interface JournalLine {
  id: string;
  line_number: number;
  account_id: string;
  debit_amount: number;
  credit_amount: number;
  base_debit_amount: number;
  base_credit_amount: number;
}
export interface Journal {
  id: string;
  company_id: string;
  branch_id: string;
  journal_number: string;
  journal_date: string;
  journal_type: string;
  description: string;
  total_debit: number;
  total_credit: number;
  status: JournalStatus;
  workflow_status: string;
  workflow_instance_id: string | null;
  lines: JournalLine[];
}
export interface GlEntry {
  id: string;
  entry_number: string;
  entry_date: string;
  account_id: string;
  account_code: string;
  debit_amount: number;
  credit_amount: number;
  base_debit_amount: number;
  base_credit_amount: number;
}
export interface CustomerLedger {
  id: string;
  customer_id: string;
  document_number: string;
  document_date: string;
  due_date: string;
  balance_amount: number;
  status: string;
  aging_bucket: string | null;
}
export interface VendorLedger {
  id: string;
  vendor_id: string;
  document_number: string;
  document_date: string;
  due_date: string;
  balance_amount: number;
  status: string;
  aging_bucket: string | null;
}
export interface CurrencyRate {
  id: string;
  currency_code: string;
  base_currency_code: string;
  exchange_rate: number;
  effective_from: string;
  effective_to: string | null;
  status: string;
}
export interface AssetTransaction {
  id: string;
  transaction_number: string;
  asset_id: string;
  transaction_type: string;
  amount: number;
  status: string;
}
export interface TaxRegister {
  id: string;
  register_number: string;
  register_date: string;
  tax_type: string;
  transaction_type: string;
  taxable_amount: number;
  tax_amount: number;
  status: string;
}
export interface TrialBalanceLine {
  account_id: string;
  account_code: string;
  account_name: string;
  debit_total: number;
  credit_total: number;
  balance: number;
}
export interface AgingLine {
  aging_bucket?: string;
  bucket?: string;
  balance_amount?: number;
  amount?: number;
  customer_id?: string;
  vendor_id?: string;
  [key: string]: unknown;
}
