import { apiClient } from "@/services/api-client";
import type { ReferenceItem, OrgContext } from "@/types/api";
import type {
  AccountGroup,
  AgingLine,
  AssetTransaction,
  ChartAccount,
  CurrencyRate,
  CustomerLedger,
  FiscalYear,
  GlEntry,
  Journal,
  JournalLine,
  Period,
  TaxRegister,
  TrialBalanceLine,
  VendorLedger,
} from "@/types/finance";

function query(
  path: string,
  params: Record<string, string | number | undefined | null> = {},
) {
  const q = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "")
      q.set(key, String(value));
  });
  return `${path}${q.size ? `?${q}` : ""}`;
}
const data = async <T>(promise: ReturnType<typeof apiClient<T>>) =>
  (await promise).data as T;
const getList = <T>(
  path: string,
  params: Record<string, string | number | undefined | null> = {},
) => data<T[]>(apiClient<T[]>(query(path, params)));
const post = <T>(path: string, body?: unknown) =>
  data<T>(apiClient<T>(path, { method: "POST", body: body ?? {} }));

async function collectPages<T>(fetchPage: (page: number) => Promise<T[]>) {
  const all: T[] = [];
  for (let page = 1; page <= 100; page += 1) {
    const rows = await fetchPage(page);
    all.push(...rows);
    if (rows.length < 200) break;
  }
  return all;
}

export const contextService = {
  get: () => data<OrgContext>(apiClient("/auth/context")),
  companies: () => getList<ReferenceItem>("/auth/context/companies"),
  branches: (companyId: string) =>
    getList<ReferenceItem>("/auth/context/branches", { company_id: companyId }),
  switch: (company_id: string, branch_id?: string) =>
    post<OrgContext>("/auth/context/switch", {
      company_id,
      branch_id: branch_id || null,
    }),
};
export const lookupService = {
  customers: () => getList<ReferenceItem>("/customers", { page_size: 200 }),
  vendors: () => getList<ReferenceItem>("/vendors", { page_size: 200 }),
  currencies: () => getList<ReferenceItem>("/currencies", { page_size: 200 }),
  taxes: () => getList<ReferenceItem>("/taxes", { page_size: 200 }),
  assets: () => getList<ReferenceItem>("/assets", { page_size: 200 }),
  costCenters: () =>
    getList<ReferenceItem>("/cost-centers", { page_size: 200 }),
};
export const financeService = {
  accountGroups: (company_id?: string) =>
    getList<AccountGroup>("/finance/account-groups", {
      company_id,
      page_size: 200,
    }),
  createAccountGroup: (body: unknown) =>
    post<AccountGroup>("/finance/account-groups", body),
  accounts: (company_id?: string) =>
    getList<ChartAccount>("/finance/chart-of-accounts", {
      company_id,
      page_size: 200,
    }),
  createAccount: (body: unknown) =>
    post<ChartAccount>("/finance/chart-of-accounts", body),
  fiscalYears: (company_id?: string) =>
    getList<FiscalYear>("/finance/fiscal-years", {
      company_id,
      page_size: 200,
    }),
  createFiscalYear: (body: unknown) =>
    post<FiscalYear>("/finance/fiscal-years", body),
  closeFiscalYear: (id: string) =>
    post<FiscalYear>(`/finance/fiscal-years/${id}/close`),
  periods: (fiscal_year_id?: string, company_id?: string) =>
    getList<Period>("/finance/periods", {
      fiscal_year_id,
      company_id,
      page_size: 200,
    }),
  periodAction: (id: string, action: "soft-close" | "hard-close" | "reopen") =>
    post<Period>(`/finance/periods/${id}/${action}`),
  periodFlags: (id: string, body: unknown) =>
    data<Period>(
      apiClient(`/finance/periods/${id}/flags`, { method: "PATCH", body }),
    ),
  journals: (params: Record<string, string | number | undefined>) =>
    getList<Journal>("/finance/journals", params),
  allJournals: (company_id: string) =>
    collectPages((page) =>
      getList<Journal>("/finance/journals", { company_id, page, page_size: 200 }),
    ),
  journal: (id: string) => data<Journal>(apiClient(`/finance/journals/${id}`)),
  createJournal: (body: unknown) => post<Journal>("/finance/journals", body),
  addJournalLine: (id: string, body: unknown) =>
    post<JournalLine>(`/finance/journals/${id}/lines`, body),
  journalAction: (
    id: string,
    action: "submit" | "approve" | "post" | "reverse",
  ) =>
    post<unknown>(
      `/finance/journals/${id}/${action}`,
      action === "submit" || action === "approve"
        ? { comments: null }
        : undefined,
    ),
  gl: (params: Record<string, string | number | undefined>) =>
    getList<GlEntry>("/finance/gl", params),
  ar: (params: Record<string, string | number | undefined>) =>
    getList<CustomerLedger>("/finance/ar", params),
  allAr: (company_id: string) =>
    collectPages((page) =>
      getList<CustomerLedger>("/finance/ar", { company_id, page, page_size: 200 }),
    ),
  createAr: (body: unknown) => post<CustomerLedger>("/finance/ar", body),
  payAr: (id: string, amount: number) =>
    post<CustomerLedger>(`/finance/ar/${id}/payment`, { amount }),
  ap: (params: Record<string, string | number | undefined>) =>
    getList<VendorLedger>("/finance/ap", params),
  allAp: (company_id: string) =>
    collectPages((page) =>
      getList<VendorLedger>("/finance/ap", { company_id, page, page_size: 200 }),
    ),
  createAp: (body: unknown) => post<VendorLedger>("/finance/ap", body),
  payAp: (id: string, amount: number) =>
    post<VendorLedger>(`/finance/ap/${id}/payment`, { amount }),
  tax: (company_id?: string, period_id?: string) =>
    getList<TaxRegister>("/finance/tax-register", {
      company_id,
      period_id,
      page_size: 200,
    }),
  rates: (company_id?: string) =>
    getList<CurrencyRate>("/finance/currency-rates", {
      company_id,
      page_size: 200,
    }),
  createRate: (body: unknown) =>
    post<CurrencyRate>("/finance/currency-rates", body),
  assetTransactions: (company_id?: string) =>
    getList<AssetTransaction>("/finance/asset-transactions", {
      company_id,
      page_size: 200,
    }),
  createAssetTransaction: (body: unknown) =>
    post<AssetTransaction>("/finance/asset-transactions", body),
  trialBalance: (period_id: string, company_id?: string) =>
    getList<TrialBalanceLine>("/finance/reports/trial-balance", {
      period_id,
      company_id,
    }),
  arAging: (company_id?: string, as_of?: string) =>
    getList<AgingLine>("/finance/reports/ar-aging", { company_id, as_of }),
  apAging: (company_id?: string, as_of?: string) =>
    getList<AgingLine>("/finance/reports/ap-aging", { company_id, as_of }),
};
