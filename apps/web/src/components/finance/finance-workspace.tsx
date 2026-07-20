"use client";
import { DashboardView } from "@/components/finance/views/dashboard";
import {
  ChartOfAccountsView,
  FiscalCalendarView,
  CurrencyRatesView,
} from "@/components/finance/views/setup";
import {
  JournalsView,
  JournalDetailView,
} from "@/components/finance/views/journals";
import {
  LedgerView,
  SubledgerView,
  TaxView,
  AssetTransactionsView,
} from "@/components/finance/views/ledgers";
import { ReportView } from "@/components/finance/views/reports";
export function FinanceWorkspace({ section }: { section: string[] }) {
  const [first, second] = section;
  if (!first) return <DashboardView />;
  if (first === "chart-of-accounts") return <ChartOfAccountsView />;
  if (first === "fiscal-calendar") return <FiscalCalendarView />;
  if (first === "currency-rates") return <CurrencyRatesView />;
  if (first === "journals" && second) return <JournalDetailView id={second} />;
  if (first === "journals") return <JournalsView />;
  if (first === "general-ledger") return <LedgerView />;
  if (first === "accounts-receivable") return <SubledgerView kind="ar" />;
  if (first === "accounts-payable") return <SubledgerView kind="ap" />;
  if (first === "tax-register") return <TaxView />;
  if (first === "asset-transactions") return <AssetTransactionsView />;
  if (first === "reports" && second)
    return (
      <ReportView kind={second as "trial-balance" | "ar-aging" | "ap-aging"} />
    );
  return <DashboardView />;
}
