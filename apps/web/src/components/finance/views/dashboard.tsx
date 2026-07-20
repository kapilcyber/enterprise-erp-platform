"use client";
import Link from "next/link";
import { useQueries, useQuery } from "@tanstack/react-query";
import {
  AlertTriangle,
  ArrowRight,
  BookOpenCheck,
  CalendarClock,
  CreditCard,
  FileCheck2,
  FileClock,
  UsersRound,
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { financeService } from "@/services/finance";
import { useFinanceContext } from "@/components/finance/finance-context";
import {
  ErrorState,
  LoadingState,
  PageHeader,
  StatusBadge,
} from "@/components/ui/finance-ui";
import { money } from "@/lib/format";
export function DashboardView() {
  const { companyId } = useFinanceContext();
  const results = useQueries({
    queries: [
      {
        queryKey: ["journals", "dashboard", companyId],
        queryFn: () => financeService.allJournals(companyId),
      },
      {
        queryKey: ["periods", companyId],
        queryFn: () => financeService.periods(undefined, companyId),
      },
      {
        queryKey: ["ar", companyId],
        queryFn: () => financeService.allAr(companyId),
      },
      {
        queryKey: ["ap", companyId],
        queryFn: () => financeService.allAp(companyId),
      },
      {
        queryKey: ["ar-aging", companyId],
        queryFn: () => financeService.arAging(companyId),
      },
      {
        queryKey: ["ap-aging", companyId],
        queryFn: () => financeService.apAging(companyId),
      },
    ],
  });
  const periodId =
    results[1].data?.find((period) => period.status === "open")?.id ??
    results[1].data?.[0]?.id ??
    "";
  const trial = useQuery({
    queryKey: ["trial-balance", "dashboard", companyId, periodId],
    queryFn: () => financeService.trialBalance(periodId, companyId),
    enabled: !!periodId,
  });
  if (results.some((r) => r.isLoading) || trial.isLoading)
    return <LoadingState />;
  const failed = results.find((r) => r.error);
  if (failed) return <ErrorState error={failed.error} />;
  const journals = results[0].data ?? [],
    periods = results[1].data ?? [],
    ar = results[2].data ?? [],
    ap = results[3].data ?? [];
  const action = journals.filter((j) =>
    ["draft", "submitted", "approved"].includes(j.status),
  );
  const arTotal = ar.reduce((s, x) => s + Number(x.balance_amount), 0),
    apTotal = ap.reduce((s, x) => s + Number(x.balance_amount), 0);
  const trialDifference = (trial.data ?? []).reduce(
    (sum, row) => sum + row.debit_total - row.credit_total,
    0,
  );
  const current = periods.find((p) => p.status === "open") ?? periods[0];
  const chart = [
    {
      name: "Current",
      AR: ar
        .filter((x) => !x.aging_bucket || x.aging_bucket.includes("0"))
        .reduce((s, x) => s + x.balance_amount, 0),
      AP: ap
        .filter((x) => !x.aging_bucket || x.aging_bucket.includes("0"))
        .reduce((s, x) => s + x.balance_amount, 0),
    },
    { name: "1–30", AR: bucket(ar, "30"), AP: bucket(ap, "30") },
    { name: "31–60", AR: bucket(ar, "60"), AP: bucket(ap, "60") },
    { name: "61–90", AR: bucket(ar, "90"), AP: bucket(ap, "90") },
    { name: "90+", AR: bucket(ar, "90+"), AP: bucket(ap, "90+") },
  ];
  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Operational control"
        title="Finance control center"
        description="Monitor close readiness, approvals, receivables and payables from one trusted workspace."
        actions={
          <Link
            className="inline-flex h-9 items-center gap-2 rounded-lg bg-[#0f8b8d] px-3 text-sm font-semibold text-white hover:bg-[#0b7476]"
            href="/finance/journals"
          >
            Review journals <ArrowRight className="size-4" />
          </Link>
        }
      />
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
        <Kpi
          icon={CalendarClock}
          label="Current period"
          value={current?.period_name ?? "Not configured"}
          detail={
            current ? (
              <StatusBadge value={current.status} />
            ) : (
              "Create a fiscal calendar"
            )
          }
        />
        <Kpi
          icon={FileClock}
          label="Action queue"
          value={String(action.length)}
          detail="Draft, submitted or approved journals"
        />
        <Kpi
          icon={UsersRound}
          label="Receivables"
          value={money(arTotal)}
          detail={`${ar.filter((x) => x.balance_amount > 0).length} open customer items`}
        />
        <Kpi
          icon={CreditCard}
          label="Payables"
          value={money(apTotal)}
          detail={`${ap.filter((x) => x.balance_amount > 0).length} open vendor items`}
        />
        <Kpi
          icon={BookOpenCheck}
          label="Trial balance control"
          value={money(trialDifference)}
          detail={
            Math.abs(trialDifference) < 0.0001
              ? "Debits and credits are balanced"
              : "Control difference requires review"
          }
        />
      </div>
      <div className="grid gap-5 xl:grid-cols-[1.35fr_.65fr]">
        <section className="panel p-5">
          <div className="mb-5 flex items-start justify-between">
            <div>
              <p className="font-semibold">Working capital aging</p>
              <p className="text-sm text-muted-foreground">
                Open exposure by aging bucket
              </p>
            </div>
            <div className="flex gap-3 text-xs">
              <span className="flex items-center gap-1">
                <i className="size-2 rounded-full bg-[#0f8b8d]" />
                AR
              </span>
              <span className="flex items-center gap-1">
                <i className="size-2 rounded-full bg-[#2f6f9f]" />
                AP
              </span>
            </div>
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chart} margin={{ left: 0, right: 8 }}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                  opacity={0.3}
                />
                <XAxis
                  dataKey="name"
                  tickLine={false}
                  axisLine={false}
                  fontSize={12}
                />
                <YAxis
                  tickLine={false}
                  axisLine={false}
                  fontSize={11}
                  tickFormatter={(v) => `${Math.round(v / 1000)}k`}
                />
                <Tooltip formatter={(v) => money(Number(v))} />
                <Bar dataKey="AR" fill="#0f8b8d" radius={[4, 4, 0, 0]} />
                <Bar dataKey="AP" fill="#2f6f9f" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>
        <section className="panel overflow-hidden">
          <div className="border-b p-5">
            <p className="font-semibold">Action required</p>
            <p className="text-sm text-muted-foreground">
              Journal workflow queue
            </p>
          </div>
          <div className="divide-y">
            {action.slice(0, 6).map((j) => (
              <Link
                href={`/finance/journals/${j.id}`}
                key={j.id}
                className="flex items-center gap-3 p-4 hover:bg-accent/35"
              >
                <span className="grid size-9 place-items-center rounded-lg bg-warning/10 text-warning">
                  {j.status === "approved" ? (
                    <FileCheck2 className="size-4" />
                  ) : (
                    <BookOpenCheck className="size-4" />
                  )}
                </span>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-semibold">
                    {j.journal_number}
                  </p>
                  <p className="truncate text-xs text-muted-foreground">
                    {j.description}
                  </p>
                </div>
                <StatusBadge value={j.status} />
              </Link>
            ))}
            {!action.length && (
              <div className="p-8 text-center">
                <AlertTriangle className="mx-auto mb-2 size-5 text-success" />
                <p className="text-sm font-medium">No pending actions</p>
              </div>
            )}
          </div>
        </section>
      </div>
      <section className="panel overflow-hidden">
        <div className="flex items-center justify-between border-b p-5">
          <div>
            <p className="font-semibold">Recent journals</p>
            <p className="text-sm text-muted-foreground">
              Latest activity across the selected company
            </p>
          </div>
          <Link
            href="/finance/journals"
            className="text-sm font-semibold text-[#0f8b8d]"
          >
            View all
          </Link>
        </div>
        <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                <th>Journal</th>
                <th>Date</th>
                <th>Description</th>
                <th>Status</th>
                <th className="text-right">Debit</th>
                <th className="text-right">Credit</th>
              </tr>
            </thead>
            <tbody>
              {journals.slice(0, 8).map((j) => (
                <tr key={j.id}>
                  <td>
                    <Link
                      href={`/finance/journals/${j.id}`}
                      className="font-semibold text-[#0f8b8d]"
                    >
                      {j.journal_number}
                    </Link>
                  </td>
                  <td>{j.journal_date}</td>
                  <td>{j.description}</td>
                  <td>
                    <StatusBadge value={j.status} />
                  </td>
                  <td className="amount">{money(j.total_debit)}</td>
                  <td className="amount">{money(j.total_credit)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
function bucket(
  items: { aging_bucket: string | null; balance_amount: number }[],
  key: string,
) {
  return items
    .filter((x) => x.aging_bucket?.includes(key))
    .reduce((s, x) => s + x.balance_amount, 0);
}
function Kpi({
  icon: Icon,
  label,
  value,
  detail,
}: {
  icon: typeof FileClock;
  label: string;
  value: string;
  detail: React.ReactNode;
}) {
  return (
    <div className="panel p-5">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-semibold text-muted-foreground">{label}</p>
          <p className="mt-2 text-2xl font-semibold tracking-tight">{value}</p>
        </div>
        <span className="grid size-10 place-items-center rounded-xl bg-[#0f8b8d]/10 text-[#0f8b8d]">
          <Icon className="size-5" />
        </span>
      </div>
      <div className="mt-3 text-xs text-muted-foreground">{detail}</div>
    </div>
  );
}
