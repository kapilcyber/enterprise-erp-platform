"use client";
import { useState } from "react";
import {
  useMutation,
  useQueries,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import { Banknote, Plus, Search } from "lucide-react";
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
  Pager,
  StatusBadge,
} from "@/components/ui/finance-ui";
import { date, money, referenceLabel, title } from "@/lib/format";
import { financeService, lookupService } from "@/services/finance";
import type { CustomerLedger, GlEntry, VendorLedger } from "@/types/finance";

export function LedgerView() {
  const { companyId } = useFinanceContext();
  const [page, setPage] = useState(1);
  const [account, setAccount] = useState("");
  const [period, setPeriod] = useState("");
  const pageSize = 25;
  const lookups = useQueries({
    queries: [
      {
        queryKey: ["accounts", companyId],
        queryFn: () => financeService.accounts(companyId),
      },
      {
        queryKey: ["periods", companyId],
        queryFn: () => financeService.periods(undefined, companyId),
      },
    ],
  });
  const entries = useQuery<GlEntry[]>({
    queryKey: ["gl", companyId, account, period, page],
    queryFn: () =>
      financeService.gl({
        company_id: companyId,
        account_id: account,
        period_id: period,
        page,
        page_size: pageSize,
      }),
  });
  if (entries.isLoading) return <LoadingState />;
  if (entries.error) return <ErrorState error={entries.error} />;
  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Posted books"
        title="General ledger"
        description="Immutable entries created only from approved and balanced journals."
      />
      <section className="panel overflow-hidden">
        <div className="grid gap-3 border-b p-4 sm:grid-cols-2">
          <Select
            value={account}
            onChange={setAccount}
            label="Account"
            options={(lookups[0].data ?? []).map((a) => ({
              value: a.id,
              label: `${a.account_code} · ${a.account_name}`,
            }))}
          />
          <Select
            value={period}
            onChange={setPeriod}
            label="Period"
            options={(lookups[1].data ?? []).map((p) => ({
              value: p.id,
              label: p.period_name,
            }))}
          />
        </div>
        {entries.data?.length ? (
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Entry</th>
                  <th>Date</th>
                  <th>Account</th>
                  <th className="text-right">Debit</th>
                  <th className="text-right">Credit</th>
                  <th className="text-right">Base debit</th>
                  <th className="text-right">Base credit</th>
                </tr>
              </thead>
              <tbody>
                {entries.data.map((e) => (
                  <tr key={e.id}>
                    <td className="font-mono font-semibold">
                      {e.entry_number}
                    </td>
                    <td>{date(e.entry_date)}</td>
                    <td>
                      <p className="font-mono">{e.account_code}</p>
                      <p className="text-xs text-muted-foreground">
                        {
                          lookups[0].data?.find((a) => a.id === e.account_id)
                            ?.account_name
                        }
                      </p>
                    </td>
                    <td className="amount">
                      {e.debit_amount ? money(e.debit_amount) : "—"}
                    </td>
                    <td className="amount">
                      {e.credit_amount ? money(e.credit_amount) : "—"}
                    </td>
                    <td className="amount">
                      {e.base_debit_amount ? money(e.base_debit_amount) : "—"}
                    </td>
                    <td className="amount">
                      {e.base_credit_amount ? money(e.base_credit_amount) : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <EmptyState
            title="No ledger entries"
            description="Adjust filters or post an approved journal."
          />
        )}
        <Pager
          page={page}
          pageSize={pageSize}
          count={entries.data?.length ?? 0}
          onPage={setPage}
        />
      </section>
    </div>
  );
}

export function SubledgerView({ kind }: { kind: "ar" | "ap" }) {
  const isAr = kind === "ar";
  const { companyId, branchId, branches } = useFinanceContext();
  const { can } = useAuth();
  const client = useQueryClient();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [createOpen, setCreateOpen] = useState(false);
  const [payment, setPayment] = useState<CustomerLedger | VendorLedger | null>(
    null,
  );
  const pageSize = 25;
  const parties = useQuery({
    queryKey: ["lookups", isAr ? "customers" : "vendors"],
    queryFn: isAr ? lookupService.customers : lookupService.vendors,
  });
  const entries = useQuery<(CustomerLedger | VendorLedger)[]>({
    queryKey: [kind, companyId, page],
    queryFn: () =>
      isAr
        ? financeService.ar({
            company_id: companyId,
            page,
            page_size: pageSize,
          })
        : financeService.ap({
            company_id: companyId,
            page,
            page_size: pageSize,
          }),
  });
  const create = useMutation<CustomerLedger | VendorLedger, Error, unknown>({
    mutationFn: (body: unknown) =>
      isAr ? financeService.createAr(body) : financeService.createAp(body),
    onSuccess: async () => {
      toast.success(`${isAr ? "Receivable" : "Payable"} created`);
      setCreateOpen(false);
      await client.invalidateQueries({ queryKey: [kind] });
    },
    onError: (e) => toast.error(e.message),
  });
  const pay = useMutation<
    CustomerLedger | VendorLedger,
    Error,
    { id: string; amount: number }
  >({
    mutationFn: ({ id, amount }: { id: string; amount: number }) =>
      isAr
        ? financeService.payAr(id, amount)
        : financeService.payAp(id, amount),
    onSuccess: async () => {
      toast.success("Payment recorded");
      setPayment(null);
      await client.invalidateQueries({ queryKey: [kind] });
    },
    onError: (e) => toast.error(e.message),
  });
  if (entries.isLoading) return <LoadingState />;
  if (entries.error) return <ErrorState error={entries.error} />;
  const partyName = (id: string) => {
    const p = parties.data?.find((x) => x.id === id);
    return p
      ? referenceLabel(p as unknown as Record<string, unknown>)
      : id.slice(0, 8);
  };
  const rows = (entries.data ?? []).filter((e) =>
    `${e.document_number} ${partyName(isAr ? (e as CustomerLedger).customer_id : (e as VendorLedger).vendor_id)}`
      .toLowerCase()
      .includes(search.toLowerCase()),
  );
  const permission = `finance.${kind}`;
  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow={isAr ? "Customer subledger" : "Vendor subledger"}
        title={isAr ? "Accounts receivable" : "Accounts payable"}
        description={
          isAr
            ? "Track customer dues, aging and collections."
            : "Track vendor obligations, due dates and payments."
        }
        actions={
          can(`${permission}:create`) ? (
            <Button
              className="bg-[#0f8b8d] hover:bg-[#0b7476]"
              onClick={() => setCreateOpen(true)}
            >
              <Plus />
              New {isAr ? "receivable" : "payable"}
            </Button>
          ) : undefined
        }
      />
      <section className="panel overflow-hidden">
        <div className="border-b p-4">
          <label className="relative block max-w-md">
            <Search className="absolute left-3 top-2.5 size-4 text-muted-foreground" />
            <input
              className="control pl-9"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder={`Search ${isAr ? "customer" : "vendor"} or document`}
            />
          </label>
        </div>
        {rows.length ? (
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Document</th>
                  <th>{isAr ? "Customer" : "Vendor"}</th>
                  <th>Date</th>
                  <th>Due date</th>
                  <th>Aging</th>
                  <th>Status</th>
                  <th className="text-right">Balance</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {rows.map((e) => (
                  <tr key={e.id}>
                    <td className="font-mono font-semibold">
                      {e.document_number}
                    </td>
                    <td>
                      {partyName(
                        isAr
                          ? (e as CustomerLedger).customer_id
                          : (e as VendorLedger).vendor_id,
                      )}
                    </td>
                    <td>{date(e.document_date)}</td>
                    <td>{date(e.due_date)}</td>
                    <td>{e.aging_bucket ?? "Current"}</td>
                    <td>
                      <StatusBadge value={e.status} />
                    </td>
                    <td className="amount font-semibold">
                      {money(e.balance_amount)}
                    </td>
                    <td>
                      {e.balance_amount > 0 && can(`${permission}:payment`) && (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => setPayment(e)}
                        >
                          <Banknote />
                          Record payment
                        </Button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <EmptyState />
        )}
        <Pager
          page={page}
          pageSize={pageSize}
          count={entries.data?.length ?? 0}
          onPage={setPage}
        />
      </section>
      <Modal
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        title={`Create ${isAr ? "receivable" : "payable"}`}
        description="Record an opening or standalone subledger document."
      >
        <form
          onSubmit={(e) => {
            e.preventDefault();
            const f = new FormData(e.currentTarget);
            const amount = Number(f.get("amount"));
            create.mutate({
              branch_id: f.get("branch_id"),
              [isAr ? "customer_id" : "vendor_id"]: f.get("party_id"),
              document_date: f.get("document_date"),
              due_date: f.get("due_date"),
              document_type: f.get("document_type"),
              debit_amount: isAr ? amount : 0,
              credit_amount: isAr ? 0 : amount,
              currency_code: "INR",
              company_id: companyId,
            });
          }}
          className="grid gap-4"
        >
          <FieldSelect
            name="branch_id"
            label="Branch"
            defaultValue={branchId}
            options={branches.map((x) => ({
              value: x.id,
              label: referenceLabel(x as unknown as Record<string, unknown>),
            }))}
          />
          <FieldSelect
            name="party_id"
            label={isAr ? "Customer" : "Vendor"}
            options={(parties.data ?? []).map((x) => ({
              value: x.id,
              label: referenceLabel(x as unknown as Record<string, unknown>),
            }))}
          />
          <div className="grid grid-cols-2 gap-3">
            <Field
              name="document_date"
              label="Document date"
              type="date"
              required
            />
            <Field name="due_date" label="Due date" type="date" required />
          </div>
          <FieldSelect
            name="document_type"
            label="Document type"
            options={["invoice", "debit_note", "credit_note", "adjustment"].map(
              (x) => ({ value: x, label: title(x) }),
            )}
          />
          <Field
            name="amount"
            label="Amount"
            type="number"
            step="0.01"
            min="0.01"
            required
          />
          <FormActions
            onCancel={() => setCreateOpen(false)}
            busy={create.isPending}
            label="Create entry"
          />
        </form>
      </Modal>
      <Modal
        open={!!payment}
        onClose={() => setPayment(null)}
        title="Record payment"
        description={
          payment
            ? `${payment.document_number} · Outstanding ${money(payment.balance_amount)}`
            : ""
        }
      >
        <form
          onSubmit={(e) => {
            e.preventDefault();
            if (payment)
              pay.mutate({
                id: payment.id,
                amount: Number(new FormData(e.currentTarget).get("amount")),
              });
          }}
        >
          <Field
            name="amount"
            label="Payment amount"
            type="number"
            min="0.01"
            max={payment?.balance_amount}
            step="0.01"
            required
          />
          <FormActions
            onCancel={() => setPayment(null)}
            busy={pay.isPending}
            label="Record payment"
          />
        </form>
      </Modal>
    </div>
  );
}

export function TaxView() {
  const { companyId } = useFinanceContext();
  const [period, setPeriod] = useState("");
  const periods = useQuery({
    queryKey: ["periods", companyId],
    queryFn: () => financeService.periods(undefined, companyId),
  });
  const rows = useQuery({
    queryKey: ["tax", companyId, period],
    queryFn: () => financeService.tax(companyId, period),
  });
  if (rows.isLoading) return <LoadingState />;
  if (rows.error) return <ErrorState error={rows.error} />;
  const total = rows.data?.reduce((s, x) => s + x.tax_amount, 0) ?? 0;
  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Tax accounting"
        title="Tax register"
        description="Input, output and withholding tax derived from posted journal lines."
      />
      <div className="grid gap-4 sm:grid-cols-[1fr_260px]">
        <div className="panel p-5">
          <p className="text-xs font-semibold text-muted-foreground">
            Registered tax
          </p>
          <p className="mt-2 text-2xl font-semibold">{money(total)}</p>
        </div>
        <label className="field panel p-4">
          <span className="field-label">Accounting period</span>
          <select
            className="control"
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
          >
            <option value="">All periods</option>
            {periods.data?.map((p) => (
              <option key={p.id} value={p.id}>
                {p.period_name}
              </option>
            ))}
          </select>
        </label>
      </div>
      <section className="panel overflow-hidden">
        {rows.data?.length ? (
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Register</th>
                  <th>Date</th>
                  <th>Tax type</th>
                  <th>Transaction</th>
                  <th className="text-right">Taxable value</th>
                  <th className="text-right">Tax</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {rows.data.map((r) => (
                  <tr key={r.id}>
                    <td className="font-mono font-semibold">
                      {r.register_number}
                    </td>
                    <td>{date(r.register_date)}</td>
                    <td>{title(r.tax_type)}</td>
                    <td>{title(r.transaction_type)}</td>
                    <td className="amount">{money(r.taxable_amount)}</td>
                    <td className="amount font-semibold">
                      {money(r.tax_amount)}
                    </td>
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
    </div>
  );
}

export function AssetTransactionsView() {
  const { companyId, branchId, branches } = useFinanceContext();
  const { can } = useAuth();
  const client = useQueryClient();
  const [open, setOpen] = useState(false);
  const rows = useQuery({
    queryKey: ["asset-transactions", companyId],
    queryFn: () => financeService.assetTransactions(companyId),
  });
  const lookups = useQueries({
    queries: [
      { queryKey: ["lookups", "assets"], queryFn: lookupService.assets },
      {
        queryKey: ["periods", companyId],
        queryFn: () => financeService.periods(undefined, companyId),
      },
    ],
  });
  const create = useMutation({
    mutationFn: financeService.createAssetTransaction,
    onSuccess: async () => {
      toast.success("Asset transaction created");
      setOpen(false);
      await client.invalidateQueries({ queryKey: ["asset-transactions"] });
    },
    onError: (e) => toast.error(e.message),
  });
  if (rows.isLoading) return <LoadingState />;
  if (rows.error) return <ErrorState error={rows.error} />;
  const assetName = (id: string) => {
    const a = lookups[0].data?.find((x) => x.id === id);
    return a
      ? referenceLabel(a as unknown as Record<string, unknown>)
      : id.slice(0, 8);
  };
  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Asset accounting"
        title="Asset transactions"
        description="Record acquisition, capitalization, depreciation and disposal accounting events."
        actions={
          can("finance.asset_transaction:create") ? (
            <Button
              className="bg-[#0f8b8d] hover:bg-[#0b7476]"
              onClick={() => setOpen(true)}
            >
              <Plus />
              New transaction
            </Button>
          ) : undefined
        }
      />
      <section className="panel overflow-hidden">
        {rows.data?.length ? (
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Transaction</th>
                  <th>Asset</th>
                  <th>Type</th>
                  <th className="text-right">Amount</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {rows.data.map((r) => (
                  <tr key={r.id}>
                    <td className="font-mono font-semibold">
                      {r.transaction_number}
                    </td>
                    <td>{assetName(r.asset_id)}</td>
                    <td>{title(r.transaction_type)}</td>
                    <td className="amount">{money(r.amount)}</td>
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
        title="Create asset transaction"
      >
        <form
          onSubmit={(e) => {
            e.preventDefault();
            const f = new FormData(e.currentTarget);
            create.mutate({
              branch_id: f.get("branch_id"),
              asset_id: f.get("asset_id"),
              transaction_date: f.get("transaction_date"),
              transaction_type: f.get("transaction_type"),
              amount: Number(f.get("amount")),
              period_id: f.get("period_id"),
              currency_code: "INR",
              description: f.get("description") || null,
              company_id: companyId,
            });
          }}
          className="grid gap-4"
        >
          <FieldSelect
            name="branch_id"
            label="Branch"
            defaultValue={branchId}
            options={branches.map((x) => ({
              value: x.id,
              label: referenceLabel(x as unknown as Record<string, unknown>),
            }))}
          />
          <FieldSelect
            name="asset_id"
            label="Asset"
            options={(lookups[0].data ?? []).map((x) => ({
              value: x.id,
              label: referenceLabel(x as unknown as Record<string, unknown>),
            }))}
          />
          <FieldSelect
            name="period_id"
            label="Accounting period"
            options={(lookups[1].data ?? [])
              .filter((p) => p.status !== "hard_closed")
              .map((p) => ({ value: p.id, label: p.period_name }))}
          />
          <FieldSelect
            name="transaction_type"
            label="Transaction type"
            options={[
              "acquisition",
              "capitalization",
              "depreciation",
              "revaluation",
              "disposal",
            ].map((x) => ({ value: x, label: title(x) }))}
          />
          <div className="grid grid-cols-2 gap-3">
            <Field
              name="transaction_date"
              label="Transaction date"
              type="date"
              required
            />
            <Field
              name="amount"
              label="Amount"
              type="number"
              min="0.01"
              step="0.01"
              required
            />
          </div>
          <Field name="description" label="Description" />
          <FormActions
            onCancel={() => setOpen(false)}
            busy={create.isPending}
            label="Create transaction"
          />
        </form>
      </Modal>
    </div>
  );
}
function Select({
  label,
  value,
  onChange,
  options,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  options: { value: string; label: string }[];
}) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      <select
        className="control"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="">All {label.toLowerCase()}s</option>
        {options.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>
    </label>
  );
}
function Field({
  label,
  ...props
}: { label: string } & React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      <input className="control" {...props} />
    </label>
  );
}
function FieldSelect({
  label,
  options,
  ...props
}: {
  label: string;
  options: { value: string; label: string }[];
} & React.SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      <select className="control" {...props}>
        {options.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>
    </label>
  );
}
