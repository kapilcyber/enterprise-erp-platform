"use client";

import { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { CalendarPlus, LockKeyhole, Plus, Search } from "lucide-react";
import { toast } from "sonner";
import { useAuth } from "@/components/auth/auth-provider";
import { useFinanceContext } from "@/components/finance/finance-context";
import { Button } from "@/components/ui/button";
import {
  EmptyState,
  ErrorState,
  FormActions,
  LoadingState,
  Modal,
  PageHeader,
  StatusBadge,
} from "@/components/ui/finance-ui";
import { date, number, referenceLabel, title } from "@/lib/format";
import { financeService, lookupService } from "@/services/finance";
import type { Period } from "@/types/finance";

function useSave<T>(
  fn: (body: unknown) => Promise<T>,
  keys: string[],
  message: string,
) {
  const client = useQueryClient();
  return useMutation({
    mutationFn: fn,
    onSuccess: async () => {
      toast.success(message);
      await Promise.all(
        keys.map((key) => client.invalidateQueries({ queryKey: [key] })),
      );
    },
    onError: (error) => toast.error(error.message),
  });
}

export function ChartOfAccountsView() {
  const { companyId } = useFinanceContext();
  const { can } = useAuth();
  const [search, setSearch] = useState("");
  const [groupOpen, setGroupOpen] = useState(false);
  const [accountOpen, setAccountOpen] = useState(false);
  const groups = useQuery({
    queryKey: ["account-groups", companyId],
    queryFn: () => financeService.accountGroups(companyId),
  });
  const accounts = useQuery({
    queryKey: ["accounts", companyId],
    queryFn: () => financeService.accounts(companyId),
  });
  const createGroup = useSave(
    financeService.createAccountGroup,
    ["account-groups"],
    "Account group created",
  );
  const createAccount = useSave(
    financeService.createAccount,
    ["accounts"],
    "Account created",
  );
  const rows = useMemo(
    () =>
      accounts.data?.filter((a) =>
        `${a.account_code} ${a.account_name}`
          .toLowerCase()
          .includes(search.toLowerCase()),
      ) ?? [],
    [accounts.data, search],
  );
  if (groups.isLoading || accounts.isLoading) return <LoadingState />;
  if (groups.error || accounts.error)
    return <ErrorState error={groups.error ?? accounts.error} />;
  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Accounting setup"
        title="Chart of accounts"
        description="Maintain the controlled account hierarchy used by every financial posting."
        actions={
          can("finance.coa:create") ? (
            <>
              <Button variant="outline" onClick={() => setGroupOpen(true)}>
                <Plus />
                Account group
              </Button>
              <Button
                onClick={() => setAccountOpen(true)}
                className="bg-[#0f8b8d]"
              >
                <Plus />
                New account
              </Button>
            </>
          ) : undefined
        }
      />
      <div className="grid gap-5 xl:grid-cols-[300px_1fr]">
        <aside className="panel overflow-hidden">
          <div className="border-b p-4">
            <p className="font-semibold">Account groups</p>
            <p className="text-xs text-muted-foreground">
              Financial statement hierarchy
            </p>
          </div>
          <div className="divide-y">
            {groups.data?.map((g) => (
              <div key={g.id} className="flex items-center justify-between p-4">
                <div>
                  <p className="font-mono text-xs text-muted-foreground">
                    {g.group_code}
                  </p>
                  <p className="text-sm font-semibold">{g.group_name}</p>
                </div>
                <StatusBadge value={g.status} />
              </div>
            ))}
          </div>
        </aside>
        <section className="panel overflow-hidden">
          <div className="flex items-center justify-between gap-3 border-b p-4">
            <div>
              <p className="font-semibold">Posting accounts</p>
              <p className="text-xs text-muted-foreground">
                {rows.length} accounts
              </p>
            </div>
            <label className="relative">
              <Search className="absolute left-3 top-2.5 size-4 text-muted-foreground" />
              <input
                className="control w-64 pl-9"
                placeholder="Search accounts"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </label>
          </div>
          {rows.length ? (
            <div className="overflow-x-auto">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Code</th>
                    <th>Account</th>
                    <th>Type</th>
                    <th>Normal balance</th>
                    <th>Posting</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((a) => (
                    <tr key={a.id}>
                      <td className="font-mono font-semibold">
                        {a.account_code}
                      </td>
                      <td>{a.account_name}</td>
                      <td>{title(a.account_type)}</td>
                      <td>{title(a.normal_balance)}</td>
                      <td>{a.is_posting_account ? "Yes" : "Header"}</td>
                      <td>
                        <StatusBadge value={a.status} />
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
      <Modal
        open={groupOpen}
        onClose={() => setGroupOpen(false)}
        title="Create account group"
      >
        <form
          className="grid gap-4"
          onSubmit={(e) => {
            e.preventDefault();
            createGroup.mutate(
              Object.fromEntries(new FormData(e.currentTarget)),
              { onSuccess: () => setGroupOpen(false) },
            );
          }}
        >
          <Field name="group_code" label="Group code" required />
          <Field name="group_name" label="Group name" required />
          <Select
            name="account_type"
            label="Account type"
            options={["asset", "liability", "equity", "revenue", "expense"]}
          />
          <Field
            name="display_order"
            label="Display order"
            type="number"
            defaultValue="1"
          />
          <input type="hidden" name="status" value="active" />
          <FormActions
            onCancel={() => setGroupOpen(false)}
            busy={createGroup.isPending}
            label="Create group"
          />
        </form>
      </Modal>
      <Modal
        open={accountOpen}
        onClose={() => setAccountOpen(false)}
        title="Create account"
        wide
      >
        <form
          className="grid gap-4 sm:grid-cols-2"
          onSubmit={(e) => {
            e.preventDefault();
            const f = new FormData(e.currentTarget);
            createAccount.mutate(
              {
                account_group_id: f.get("account_group_id"),
                account_code: f.get("account_code"),
                account_name: f.get("account_name"),
                account_type: f.get("account_type"),
                normal_balance: f.get("normal_balance"),
                is_posting_account: f.get("is_posting_account") === "on",
                is_cost_center_enabled:
                  f.get("is_cost_center_enabled") === "on",
                is_profit_center_enabled:
                  f.get("is_profit_center_enabled") === "on",
                status: "draft",
              },
              { onSuccess: () => setAccountOpen(false) },
            );
          }}
        >
          <Select
            name="account_group_id"
            label="Account group"
            options={(groups.data ?? []).map((g) => ({
              value: g.id,
              label: `${g.group_code} · ${g.group_name}`,
            }))}
          />
          <Field name="account_code" label="Account code" required />
          <Field name="account_name" label="Account name" required />
          <Select
            name="account_type"
            label="Account type"
            options={["asset", "liability", "equity", "revenue", "expense"]}
          />
          <Select
            name="normal_balance"
            label="Normal balance"
            options={["debit", "credit"]}
          />
          <div className="flex flex-col gap-3 pt-6">
            <Check
              name="is_posting_account"
              label="Allow direct posting"
              defaultChecked
            />
            <Check name="is_cost_center_enabled" label="Require cost center" />
            <Check
              name="is_profit_center_enabled"
              label="Enable profit center"
            />
          </div>
          <div className="sm:col-span-2">
            <FormActions
              onCancel={() => setAccountOpen(false)}
              busy={createAccount.isPending}
              label="Create account"
            />
          </div>
        </form>
      </Modal>
    </div>
  );
}

export function FiscalCalendarView() {
  const { companyId } = useFinanceContext();
  const { can } = useAuth();
  const client = useQueryClient();
  const [open, setOpen] = useState(false);
  const [yearId, setYearId] = useState("");
  const [flagPeriod, setFlagPeriod] = useState<Period | null>(null);
  const years = useQuery({
    queryKey: ["fiscal-years", companyId],
    queryFn: () => financeService.fiscalYears(companyId),
  });
  const activeYear = yearId || years.data?.[0]?.id || "";
  const periods = useQuery({
    queryKey: ["periods", companyId, activeYear],
    queryFn: () => financeService.periods(activeYear, companyId),
    enabled: !!activeYear,
  });
  const create = useSave(
    financeService.createFiscalYear,
    ["fiscal-years", "periods"],
    "Fiscal year created",
  );
  const action = useMutation({
    mutationFn: ({
      id,
      a,
    }: {
      id: string;
      a: "soft-close" | "hard-close" | "reopen";
    }) => financeService.periodAction(id, a),
    onSuccess: async () => {
      toast.success("Period status updated");
      await client.invalidateQueries({ queryKey: ["periods"] });
    },
    onError: (e) => toast.error(e.message),
  });
  const closeYear = useMutation({
    mutationFn: financeService.closeFiscalYear,
    onSuccess: async () => {
      toast.success("Fiscal year closed");
      await client.invalidateQueries({ queryKey: ["fiscal-years"] });
    },
    onError: (error) => toast.error(error.message),
  });
  const saveFlags = useMutation({
    mutationFn: ({ id, body }: { id: string; body: unknown }) =>
      financeService.periodFlags(id, body),
    onSuccess: async () => {
      toast.success("Period close checklist updated");
      setFlagPeriod(null);
      await client.invalidateQueries({ queryKey: ["periods"] });
    },
    onError: (error) => toast.error(error.message),
  });
  if (years.isLoading) return <LoadingState />;
  if (years.error) return <ErrorState error={years.error} />;
  const selected = years.data?.find((y) => y.id === activeYear);
  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Close management"
        title="Fiscal calendar"
        description="Control fiscal years, monthly posting periods and subledger close readiness."
        actions={
          can("finance.fiscal_year:create") ? (
            <Button className="bg-[#0f8b8d]" onClick={() => setOpen(true)}>
              <CalendarPlus />
              New fiscal year
            </Button>
          ) : undefined
        }
      />
      <div className="panel flex flex-wrap items-end gap-4 p-4">
        <label className="field min-w-64">
          <span className="field-label">Fiscal year</span>
          <select
            className="control"
            value={activeYear}
            onChange={(e) => setYearId(e.target.value)}
          >
            {years.data?.map((y) => (
              <option key={y.id} value={y.id}>
                {y.fiscal_year_code} · {y.fiscal_year_name}
              </option>
            ))}
          </select>
        </label>
        {selected && (
          <div className="mb-1 flex items-center gap-2 text-sm">
            <span>
              {date(selected.start_date)} – {date(selected.end_date)}
            </span>
            <StatusBadge value={selected.status} />
          </div>
        )}
        {selected?.status === "open" && can("finance.fiscal_year:close") && (
          <Button className="ml-auto" variant="outline" onClick={() => closeYear.mutate(selected.id)} disabled={closeYear.isPending}>
            <LockKeyhole /> Close fiscal year
          </Button>
        )}
      </div>
      <section className="panel overflow-hidden">
        {periods.isLoading ? (
          <LoadingState />
        ) : periods.error ? (
          <ErrorState error={periods.error} />
        ) : periods.data?.length ? (
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Period</th>
                  <th>Date range</th>
                  <th>AR</th>
                  <th>AP</th>
                  <th>GL</th>
                  <th>Status</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {periods.data.map((p) => (
                  <tr key={p.id}>
                    <td>
                      <p className="font-semibold">{p.period_name}</p>
                      <p className="text-xs text-muted-foreground">
                        Period {p.period_number}
                      </p>
                    </td>
                    <td>
                      {date(p.start_date)} – {date(p.end_date)}
                    </td>
                    <td>{p.ar_closed ? "Closed" : "Open"}</td>
                    <td>{p.ap_closed ? "Closed" : "Open"}</td>
                    <td>{p.gl_closed ? "Closed" : "Open"}</td>
                    <td>
                      <StatusBadge value={p.status} />
                    </td>
                    <td>
                        <div className="flex justify-end gap-1">
                          {can("finance.period:close") && (
                            <Button size="sm" variant="ghost" onClick={() => setFlagPeriod(p)}>Checklist</Button>
                          )}
                        {p.status === "open" && can("finance.period:close") && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() =>
                              action.mutate({ id: p.id, a: "soft-close" })
                            }
                          >
                            Soft close
                          </Button>
                        )}
                        {p.status === "soft_closed" &&
                          can("finance.period:close") && (
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() =>
                                action.mutate({ id: p.id, a: "hard-close" })
                              }
                            >
                              <LockKeyhole />
                              Hard close
                            </Button>
                          )}
                        {p.status !== "open" &&
                          can("finance.period:reopen") && (
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() =>
                                action.mutate({ id: p.id, a: "reopen" })
                              }
                            >
                              Reopen
                            </Button>
                          )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <EmptyState
            title="No accounting periods"
            description="Creating a fiscal year generates its accounting periods."
          />
        )}
      </section>
      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title="Create fiscal year"
        description="Accounting periods are generated automatically."
      >
        <form
          className="grid gap-4"
          onSubmit={(e) => {
            e.preventDefault();
            create.mutate(Object.fromEntries(new FormData(e.currentTarget)), {
              onSuccess: () => setOpen(false),
            });
          }}
        >
          <Field
            name="fiscal_year_code"
            label="Year code"
            placeholder="FY2026"
            required
          />
          <Field name="fiscal_year_name" label="Year name" required />
          <div className="grid grid-cols-2 gap-3">
            <Field name="start_date" label="Start date" type="date" required />
            <Field name="end_date" label="End date" type="date" required />
          </div>
          <FormActions
            onCancel={() => setOpen(false)}
            busy={create.isPending}
            label="Create fiscal year"
          />
        </form>
      </Modal>
      <Modal open={!!flagPeriod} onClose={() => setFlagPeriod(null)} title="Period close checklist" description={flagPeriod?.period_name}>
        <form className="space-y-3" onSubmit={(e) => {e.preventDefault();if (!flagPeriod) return;const f=new FormData(e.currentTarget);saveFlags.mutate({id:flagPeriod.id,body:{ar_closed:f.get("ar_closed")==="on",ap_closed:f.get("ap_closed")==="on",inventory_closed:f.get("inventory_closed")==="on",payroll_closed:f.get("payroll_closed")==="on",gl_closed:f.get("gl_closed")==="on"}})}}>
          <Check name="ar_closed" label="Accounts receivable closed" defaultChecked={flagPeriod?.ar_closed}/>
          <Check name="ap_closed" label="Accounts payable closed" defaultChecked={flagPeriod?.ap_closed}/>
          <Check name="inventory_closed" label="Inventory closed" defaultChecked={flagPeriod?.inventory_closed}/>
          <Check name="payroll_closed" label="Payroll closed" defaultChecked={flagPeriod?.payroll_closed}/>
          <Check name="gl_closed" label="General ledger closed" defaultChecked={flagPeriod?.gl_closed}/>
          <FormActions onCancel={() => setFlagPeriod(null)} busy={saveFlags.isPending} label="Save checklist"/>
        </form>
      </Modal>
    </div>
  );
}

export function CurrencyRatesView() {
  const { companyId } = useFinanceContext();
  const { can } = useAuth();
  const [open, setOpen] = useState(false);
  const rates = useQuery({
    queryKey: ["currency-rates", companyId],
    queryFn: () => financeService.rates(companyId),
  });
  const currencies = useQuery({
    queryKey: ["lookups", "currencies"],
    queryFn: lookupService.currencies,
  });
  const create = useSave(
    financeService.createRate,
    ["currency-rates"],
    "Exchange rate created",
  );
  if (rates.isLoading) return <LoadingState />;
  if (rates.error) return <ErrorState error={rates.error} />;
  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Multi-currency"
        title="Currency rates"
        description="Maintain effective-dated conversion rates used for base-currency journal values."
        actions={
          can("finance.currency_rate:create") ? (
            <Button className="bg-[#0f8b8d]" onClick={() => setOpen(true)}>
              <Plus />
              New rate
            </Button>
          ) : undefined
        }
      />
      <section className="panel overflow-hidden">
        {rates.data?.length ? (
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Currency</th>
                  <th>Base currency</th>
                  <th className="text-right">Rate</th>
                  <th>Effective from</th>
                  <th>Effective to</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {rates.data.map((r) => (
                  <tr key={r.id}>
                    <td className="font-semibold">{r.currency_code}</td>
                    <td>{r.base_currency_code}</td>
                    <td className="amount">{number(r.exchange_rate)}</td>
                    <td>{date(r.effective_from)}</td>
                    <td>{date(r.effective_to)}</td>
                    <td>
                      <StatusBadge value={r.status} />
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
      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title="Create currency rate"
      >
        <form
          className="grid gap-4"
          onSubmit={(e) => {
            e.preventDefault();
            const f = new FormData(e.currentTarget);
            const currency = currencies.data?.find(
              (c) => c.id === f.get("currency_id"),
            );
            create.mutate(
              {
                currency_id: f.get("currency_id"),
                currency_code: currency?.currency_code,
                base_currency_code: f.get("base_currency_code"),
                exchange_rate: Number(f.get("exchange_rate")),
                rate_type: "manual",
                effective_from: f.get("effective_from"),
                effective_to: f.get("effective_to") || null,
                status: "active",
                company_id: companyId,
              },
              { onSuccess: () => setOpen(false) },
            );
          }}
        >
          <Select
            name="currency_id"
            label="Currency"
            options={(currencies.data ?? []).map((c) => ({
              value: c.id,
              label: referenceLabel(c as unknown as Record<string, unknown>),
            }))}
          />
          <Field
            name="base_currency_code"
            label="Base currency"
            defaultValue="INR"
            maxLength={3}
          />
          <Field
            name="exchange_rate"
            label="Exchange rate"
            type="number"
            step="0.00000001"
            required
          />
          <Field
            name="effective_from"
            label="Effective from"
            type="date"
            required
          />
          <Field name="effective_to" label="Effective to" type="date" />
          <FormActions
            onCancel={() => setOpen(false)}
            busy={create.isPending}
            label="Create rate"
          />
        </form>
      </Modal>
    </div>
  );
}

function Field({
  label,
  ...props
}: React.InputHTMLAttributes<HTMLInputElement> & { label: string }) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      <input className="control" {...props} />
    </label>
  );
}
function Select({
  label,
  options,
  ...props
}: {
  label: string;
  options: (string | { value: string; label: string })[];
} & React.SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      <select className="control" {...props}>
        {options.map((o) =>
          typeof o === "string" ? (
            <option key={o} value={o}>
              {title(o)}
            </option>
          ) : (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ),
        )}
      </select>
    </label>
  );
}
function Check({
  label,
  ...props
}: { label: string } & React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <label className="flex items-center gap-2 text-sm">
      <input type="checkbox" className="size-4 accent-[#0f8b8d]" {...props} />
      {label}
    </label>
  );
}
