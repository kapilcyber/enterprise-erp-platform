"use client";
import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Printer } from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useFinanceContext } from "@/components/finance/finance-context";
import { Button } from "@/components/ui/button";
import {
  CsvButton,
  EmptyState,
  ErrorState,
  LoadingState,
  PageHeader,
} from "@/components/ui/finance-ui";
import { date, money, title } from "@/lib/format";
import { financeService } from "@/services/finance";
export function ReportView({
  kind,
}: {
  kind: "trial-balance" | "ar-aging" | "ap-aging";
}) {
  return kind === "trial-balance" ? (
    <TrialBalance />
  ) : (
    <Aging kind={kind === "ar-aging" ? "ar" : "ap"} />
  );
}
function TrialBalance() {
  const { companyId } = useFinanceContext();
  const periods = useQuery({
    queryKey: ["periods", companyId],
    queryFn: () => financeService.periods(undefined, companyId),
  });
  const [selected, setSelected] = useState("");
  const period =
    selected ||
    periods.data?.find((p) => p.status === "open")?.id ||
    periods.data?.[0]?.id ||
    "";
  const report = useQuery({
    queryKey: ["trial-balance", companyId, period],
    queryFn: () => financeService.trialBalance(period, companyId),
    enabled: !!period,
  });
  if (periods.isLoading) return <LoadingState />;
  const debit = report.data?.reduce((s, x) => s + x.debit_total, 0) ?? 0,
    credit = report.data?.reduce((s, x) => s + x.credit_total, 0) ?? 0,
    balanced = Math.abs(debit - credit) < 0.0001;
  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Financial reporting"
        title="Trial balance"
        description="Posted debit and credit movement summarized by account for the selected period."
        actions={
          <>
            <CsvButton
              rows={(report.data ?? []) as unknown as Record<string, unknown>[]}
              filename="trial-balance.csv"
            />
            <Button variant="outline" onClick={() => window.print()}>
              <Printer />
              Print
            </Button>
          </>
        }
      />
      <div className="no-print panel p-4">
        <label className="field max-w-sm">
          <span className="field-label">Accounting period</span>
          <select
            className="control"
            value={period}
            onChange={(e) => setSelected(e.target.value)}
          >
            {periods.data?.map((p) => (
              <option key={p.id} value={p.id}>
                {p.period_name} · {title(p.status)}
              </option>
            ))}
          </select>
        </label>
      </div>
      {report.isLoading ? (
        <LoadingState />
      ) : report.error ? (
        <ErrorState error={report.error} />
      ) : (
        <section className="panel print-panel overflow-hidden">
          <div className="grid border-b sm:grid-cols-3">
            <Metric label="Total debits" value={money(debit)} />
            <Metric label="Total credits" value={money(credit)} />
            <div className="p-5">
              <p className="text-xs font-semibold text-muted-foreground">
                Control status
              </p>
              <p
                className={`mt-2 text-xl font-semibold ${balanced ? "text-success" : "text-destructive"}`}
              >
                {balanced ? "Balanced" : "Out of balance"}
              </p>
            </div>
          </div>
          {report.data?.length ? (
            <div className="overflow-x-auto">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Account code</th>
                    <th>Account name</th>
                    <th className="text-right">Debit</th>
                    <th className="text-right">Credit</th>
                    <th className="text-right">Balance</th>
                  </tr>
                </thead>
                <tbody>
                  {report.data.map((r) => (
                    <tr key={r.account_id}>
                      <td className="font-mono font-semibold">
                        {r.account_code}
                      </td>
                      <td>{r.account_name}</td>
                      <td className="amount">{money(r.debit_total)}</td>
                      <td className="amount">{money(r.credit_total)}</td>
                      <td className="amount font-semibold">
                        {money(r.balance)}
                      </td>
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  <tr className="bg-muted/60 font-semibold">
                    <td colSpan={2} className="px-3 py-3">
                      Control totals
                    </td>
                    <td className="amount px-3">{money(debit)}</td>
                    <td className="amount px-3">{money(credit)}</td>
                    <td className="amount px-3">{money(debit - credit)}</td>
                  </tr>
                </tfoot>
              </table>
            </div>
          ) : (
            <EmptyState
              title="No posted balances"
              description="Post journals in this period to populate the trial balance."
            />
          )}
        </section>
      )}
    </div>
  );
}
function Aging({ kind }: { kind: "ar" | "ap" }) {
  const { companyId } = useFinanceContext();
  const report = useQuery({
    queryKey: [`${kind}-aging`, companyId],
    queryFn: () =>
      kind === "ar"
        ? financeService.arAging(companyId)
        : financeService.apAging(companyId),
  });
  const groups = useMemo(() => {
    const map = new Map<string, number>();
    for (const row of report.data ?? []) {
      const bucket = String(row.aging_bucket ?? "Current");
      map.set(bucket, (map.get(bucket) ?? 0) + Number(row.balance_amount ?? 0));
    }
    return [...map].map(([bucket, amount]) => ({ bucket, amount }));
  }, [report.data]);
  const total = groups.reduce((s, x) => s + x.amount, 0);
  if (report.isLoading) return <LoadingState />;
  if (report.error) return <ErrorState error={report.error} />;
  const label = kind === "ar" ? "Customer aging" : "Vendor aging";
  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Working capital"
        title={label}
        description={`Outstanding ${kind === "ar" ? "receivables" : "payables"} grouped by overdue age.`}
        actions={
          <>
            <CsvButton
              rows={(report.data ?? []) as Record<string, unknown>[]}
              filename={`${kind}-aging.csv`}
            />
            <Button variant="outline" onClick={() => window.print()}>
              <Printer />
              Print
            </Button>
          </>
        }
      />
      <div className="grid gap-5 lg:grid-cols-[280px_1fr]">
        <div className="panel p-5">
          <p className="text-xs font-semibold text-muted-foreground">
            Total outstanding
          </p>
          <p className="mt-2 text-2xl font-semibold">{money(total)}</p>
          <div className="mt-5 space-y-3">
            {groups.map((g) => (
              <div key={g.bucket} className="flex justify-between text-sm">
                <span>{g.bucket}</span>
                <span className="font-mono font-semibold">
                  {money(g.amount)}
                </span>
              </div>
            ))}
          </div>
        </div>
        <div className="panel p-5">
          <p className="mb-4 font-semibold">Exposure by bucket</p>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={groups}>
                <CartesianGrid
                  vertical={false}
                  strokeDasharray="3 3"
                  opacity={0.3}
                />
                <XAxis dataKey="bucket" axisLine={false} tickLine={false} />
                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tickFormatter={(v) => `${Math.round(v / 1000)}k`}
                />
                <Tooltip formatter={(v) => money(Number(v))} />
                <Bar
                  dataKey="amount"
                  fill={kind === "ar" ? "#0f8b8d" : "#2f6f9f"}
                  radius={[5, 5, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
      <section className="panel print-panel overflow-hidden">
        {report.data?.length ? (
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Document</th>
                  <th>{kind === "ar" ? "Customer ID" : "Vendor ID"}</th>
                  <th>Due date</th>
                  <th>Aging bucket</th>
                  <th className="text-right">Outstanding</th>
                </tr>
              </thead>
              <tbody>
                {report.data.map((r, i) => (
                  <tr key={String(r.id ?? i)}>
                    <td className="font-mono font-semibold">
                      {String(r.document_number ?? "—")}
                    </td>
                    <td className="font-mono text-xs">
                      {String(
                        r[kind === "ar" ? "customer_id" : "vendor_id"] ?? "—",
                      )}
                    </td>
                    <td>{date(String(r.due_date ?? ""))}</td>
                    <td>{String(r.aging_bucket ?? "Current")}</td>
                    <td className="amount font-semibold">
                      {money(Number(r.balance_amount ?? 0))}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <EmptyState />
        )}
      </section>
    </div>
  );
}
function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="border-b p-5 sm:border-b-0 sm:border-r">
      <p className="text-xs font-semibold text-muted-foreground">{label}</p>
      <p className="mt-2 text-xl font-semibold">{value}</p>
    </div>
  );
}
