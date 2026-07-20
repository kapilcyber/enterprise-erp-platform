"use client";
import Link from "next/link";
import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  useMutation,
  useQueries,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  FilePlus2,
  Plus,
  RotateCcw,
  Search,
  Send,
  ShieldCheck,
} from "lucide-react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";
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
import { isBalanced, journalLineSchema, journalSchema } from "@/lib/validation";
import { financeService, lookupService } from "@/services/finance";

type JournalForm = z.infer<typeof journalSchema>;
type LineForm = z.infer<typeof journalLineSchema>;
export function JournalsView() {
  const { companyId, branchId, branches } = useFinanceContext();
  const { can } = useAuth();
  const client = useQueryClient();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [open, setOpen] = useState(false);
  const pageSize = 25;
  const journals = useQuery({
    queryKey: ["journals", companyId, page],
    queryFn: () =>
      financeService.journals({
        company_id: companyId,
        page,
        page_size: pageSize,
      }),
  });
  const periods = useQuery({
    queryKey: ["periods", companyId],
    queryFn: () => financeService.periods(undefined, companyId),
  });
  const currencies = useQuery({
    queryKey: ["lookups", "currencies"],
    queryFn: lookupService.currencies,
  });
  const form = useForm<JournalForm>({
    resolver: zodResolver(journalSchema),
    defaultValues: {
      branch_id: branchId,
      journal_date: new Date().toISOString().slice(0, 10),
      description: "",
      journal_type: "manual",
      currency_code: "INR",
      exchange_rate: 1,
      period_id: "",
    },
  });
  const create = useMutation({
    mutationFn: financeService.createJournal,
    onSuccess: async (j) => {
      toast.success("Journal created");
      setOpen(false);
      form.reset();
      await client.invalidateQueries({ queryKey: ["journals"] });
      location.href = `/finance/journals/${j.id}`;
    },
    onError: (e) => toast.error(e.message),
  });
  const rows = (journals.data ?? []).filter(
    (j) =>
      (!status || j.status === status) &&
      `${j.journal_number} ${j.description}`
        .toLowerCase()
        .includes(search.toLowerCase()),
  );
  if (journals.isLoading) return <LoadingState />;
  if (journals.error) return <ErrorState error={journals.error} />;
  return (
    <div className="space-y-6">
      <PageHeader
        eyebrow="Journal governance"
        title="Journals"
        description="Create balanced entries and move them through controlled approval and posting."
        actions={
          can("finance.journal:create") ? (
            <Button
              onClick={() => {
                form.setValue("branch_id", branchId);
                setOpen(true);
              }}
              className="bg-[#0f8b8d] hover:bg-[#0b7476]"
            >
              <FilePlus2 />
              New journal
            </Button>
          ) : undefined
        }
      />
      <section className="panel overflow-hidden">
        <div className="flex flex-col gap-3 border-b p-4 sm:flex-row">
          <label className="relative flex-1">
            <Search className="absolute left-3 top-2.5 size-4 text-muted-foreground" />
            <input
              className="control pl-9"
              placeholder="Search journal number or description"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </label>
          <select
            className="control sm:w-44"
            aria-label="Status filter"
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          >
            <option value="">All statuses</option>
            {["draft", "submitted", "approved", "posted", "reversed"].map(
              (s) => (
                <option key={s} value={s}>
                  {title(s)}
                </option>
              ),
            )}
          </select>
        </div>
        {rows.length ? (
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Journal</th>
                  <th>Date</th>
                  <th>Description</th>
                  <th>Type</th>
                  <th>Status</th>
                  <th className="text-right">Debit</th>
                  <th className="text-right">Credit</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {rows.map((j) => (
                  <tr key={j.id}>
                    <td>
                      <Link
                        className="font-mono font-semibold text-[#0f8b8d]"
                        href={`/finance/journals/${j.id}`}
                      >
                        {j.journal_number}
                      </Link>
                    </td>
                    <td>{date(j.journal_date)}</td>
                    <td className="max-w-80 truncate">{j.description}</td>
                    <td>{title(j.journal_type)}</td>
                    <td>
                      <StatusBadge value={j.status} />
                    </td>
                    <td className="amount">{money(j.total_debit)}</td>
                    <td className="amount">{money(j.total_credit)}</td>
                    <td>
                      <Link href={`/finance/journals/${j.id}`}>
                        <Button
                          variant="ghost"
                          size="icon-sm"
                          aria-label="Open journal"
                        >
                          <ArrowRight />
                        </Button>
                      </Link>
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
          count={journals.data?.length ?? 0}
          onPage={setPage}
        />
      </section>
      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title="Create journal"
        description="Start a draft entry in an open accounting period."
        wide
      >
        <form
          onSubmit={form.handleSubmit((v) =>
            create.mutate({
              ...v,
              period_id: v.period_id || null,
              company_id: companyId,
            }),
          )}
          className="grid gap-4 sm:grid-cols-2"
        >
          <FormSelect
            label="Branch"
            error={form.formState.errors.branch_id?.message}
            {...form.register("branch_id")}
            options={branches.map((x) => ({
              value: x.id,
              label: referenceLabel(x as unknown as Record<string, unknown>),
            }))}
          />
          <FormInput
            label="Journal date"
            type="date"
            error={form.formState.errors.journal_date?.message}
            {...form.register("journal_date")}
          />
          <FormSelect
            label="Journal type"
            {...form.register("journal_type")}
            options={[
              { value: "manual", label: "Manual" },
              { value: "adjustment", label: "Adjustment" },
            ]}
          />
          <FormSelect
            label="Accounting period"
            {...form.register("period_id")}
            options={[
              { value: "", label: "Resolve from journal date" },
              ...(periods.data ?? [])
                .filter((p) => p.status !== "hard_closed")
                .map((p) => ({
                  value: p.id,
                  label: `${p.period_name} · ${title(p.status)}`,
                })),
            ]}
          />
          <FormSelect
            label="Currency"
            {...form.register("currency_code")}
            options={(currencies.data ?? []).map((x) => ({
              value: x.currency_code ?? "INR",
              label: referenceLabel(x as unknown as Record<string, unknown>),
            }))}
          />
          <FormInput
            label="Exchange rate"
            type="number"
            step="0.00000001"
            error={form.formState.errors.exchange_rate?.message}
            {...form.register("exchange_rate", { valueAsNumber: true })}
          />
          <label className="field sm:col-span-2">
            <span className="field-label">Description</span>
            <textarea
              className="control-area"
              {...form.register("description")}
            />
            {form.formState.errors.description && (
              <span className="text-xs text-destructive">
                {form.formState.errors.description.message}
              </span>
            )}
          </label>
          <div className="sm:col-span-2">
            <FormActions
              onCancel={() => setOpen(false)}
              busy={create.isPending}
              label="Create draft"
            />
          </div>
        </form>
      </Modal>
    </div>
  );
}

export function JournalDetailView({ id }: { id: string }) {
  const { can } = useAuth();
  const client = useQueryClient();
  const [lineOpen, setLineOpen] = useState(false);
  const journal = useQuery({
    queryKey: ["journal", id],
    queryFn: () => financeService.journal(id),
  });
  const lookups = useQueries({
    queries: [
      {
        queryKey: ["accounts", journal.data?.company_id],
        queryFn: () => financeService.accounts(journal.data?.company_id),
        enabled: !!journal.data,
      },
      { queryKey: ["lookups", "taxes"], queryFn: lookupService.taxes },
      { queryKey: ["lookups", "customers"], queryFn: lookupService.customers },
      { queryKey: ["lookups", "vendors"], queryFn: lookupService.vendors },
      {
        queryKey: ["lookups", "cost-centers"],
        queryFn: lookupService.costCenters,
      },
    ],
  });
  const form = useForm<LineForm>({
    resolver: zodResolver(journalLineSchema),
    defaultValues: {
      account_id: "",
      description: "",
      debit_amount: 0,
      credit_amount: 0,
      cost_center_id: "",
      tax_id: "",
      customer_id: "",
      vendor_id: "",
    },
  });
  const mutation = useMutation({
    mutationFn: (v: LineForm) =>
      financeService.addJournalLine(id, {
        ...v,
        line_number: (journal.data?.lines.length ?? 0) + 1,
        cost_center_id: v.cost_center_id || null,
        tax_id: v.tax_id || null,
        customer_id: v.customer_id || null,
        vendor_id: v.vendor_id || null,
      }),
    onSuccess: async () => {
      toast.success("Journal line added");
      setLineOpen(false);
      form.reset();
      await client.invalidateQueries({ queryKey: ["journal", id] });
    },
    onError: (e) => toast.error(e.message),
  });
  const action = useMutation({
    mutationFn: (a: "submit" | "approve" | "post" | "reverse") =>
      financeService.journalAction(id, a),
    onSuccess: async (_, a) => {
      toast.success(`Journal ${a} action completed`);
      await client.invalidateQueries({ queryKey: ["journal", id] });
      await client.invalidateQueries({ queryKey: ["journals"] });
    },
    onError: (e) => toast.error(e.message),
  });
  if (journal.isLoading) return <LoadingState />;
  if (journal.error || !journal.data)
    return (
      <ErrorState error={journal.error ?? new Error("Journal not found")} />
    );
  const j = journal.data;
  const balanced = isBalanced(j.total_debit, j.total_credit);
  return (
    <div className="space-y-6">
      <Link
        href="/finance/journals"
        className="inline-flex items-center gap-2 text-sm font-semibold text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="size-4" />
        Back to journals
      </Link>
      <PageHeader
        eyebrow={j.journal_number}
        title={j.description}
        description={`${title(j.journal_type)} journal · ${date(j.journal_date)}`}
        actions={
          <>
            <StatusBadge value={j.status} />
            {j.status === "draft" && can("finance.journal:update") && (
              <Button variant="outline" onClick={() => setLineOpen(true)}>
                <Plus />
                Add line
              </Button>
            )}
            {j.status === "draft" && can("finance.journal:submit") && (
              <Button
                disabled={!balanced || action.isPending}
                onClick={() => action.mutate("submit")}
              >
                <Send />
                Submit
              </Button>
            )}
            {j.status === "submitted" && can("finance.journal:approve") && (
              <Button onClick={() => action.mutate("approve")}>
                <ShieldCheck />
                Approve
              </Button>
            )}
            {j.status === "approved" && can("finance.journal:post") && (
              <Button
                onClick={() => action.mutate("post")}
                className="bg-[#0f8b8d] hover:bg-[#0b7476]"
              >
                <CheckCircle2 />
                Post to GL
              </Button>
            )}
            {j.status === "posted" && can("finance.journal:reverse") && (
              <Button
                variant="outline"
                onClick={() => action.mutate("reverse")}
              >
                <RotateCcw />
                Reverse
              </Button>
            )}
          </>
        }
      />
      <div className="grid gap-4 sm:grid-cols-3">
        <Summary
          label="Workflow"
          value={title(j.workflow_status)}
          icon={ShieldCheck}
        />
        <Summary
          label="Total debit"
          value={money(j.total_debit)}
          icon={ArrowRight}
        />
        <Summary
          label="Total credit"
          value={money(j.total_credit)}
          icon={ArrowLeft}
        />
      </div>
      <section className="panel overflow-hidden">
        <div className="flex items-center justify-between border-b p-4">
          <div>
            <p className="font-semibold">Journal lines</p>
            <p className="text-xs text-muted-foreground">
              Double-entry detail in transaction currency
            </p>
          </div>
          <span
            className={
              balanced
                ? "text-sm font-semibold text-success"
                : "text-sm font-semibold text-warning"
            }
          >
            {balanced
              ? "Balanced"
              : "Difference: " + money(j.total_debit - j.total_credit)}
          </span>
        </div>
        {j.lines.length ? (
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Line</th>
                  <th>Account</th>
                  <th className="text-right">Debit</th>
                  <th className="text-right">Credit</th>
                  <th className="text-right">Base debit</th>
                  <th className="text-right">Base credit</th>
                </tr>
              </thead>
              <tbody>
                {j.lines.map((l) => (
                  <tr key={l.id}>
                    <td>{l.line_number}</td>
                    <td>
                      <p className="font-mono font-semibold">
                        {lookups[0].data?.find((a) => a.id === l.account_id)
                          ?.account_code ?? l.account_id.slice(0, 8)}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {
                          lookups[0].data?.find((a) => a.id === l.account_id)
                            ?.account_name
                        }
                      </p>
                    </td>
                    <td className="amount">
                      {l.debit_amount ? money(l.debit_amount) : "—"}
                    </td>
                    <td className="amount">
                      {l.credit_amount ? money(l.credit_amount) : "—"}
                    </td>
                    <td className="amount">
                      {l.base_debit_amount ? money(l.base_debit_amount) : "—"}
                    </td>
                    <td className="amount">
                      {l.base_credit_amount ? money(l.base_credit_amount) : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
              <tfoot>
                <tr className="bg-muted/50 font-semibold">
                  <td colSpan={2} className="px-3 py-3 text-right">
                    Totals
                  </td>
                  <td className="amount px-3">{money(j.total_debit)}</td>
                  <td className="amount px-3">{money(j.total_credit)}</td>
                  <td colSpan={2} />
                </tr>
              </tfoot>
            </table>
          </div>
        ) : (
          <EmptyState
            title="No journal lines"
            description="Add at least two lines with equal debit and credit totals."
          />
        )}
      </section>
      <section className="panel p-5">
        <p className="font-semibold">Workflow trail</p>
        <div className="mt-5 flex items-center gap-0 overflow-x-auto">
          {["Draft", "Submitted", "Approved", "Posted"].map((s, i) => {
            const order = ["draft", "submitted", "approved", "posted"];
            const reached =
              order.indexOf(j.status) >= i || j.status === "reversed";
            return (
              <div key={s} className="flex min-w-32 flex-1 items-center">
                <span
                  className={`grid size-7 shrink-0 place-items-center rounded-full border text-xs font-bold ${reached ? "border-[#0f8b8d] bg-[#0f8b8d] text-white" : "bg-card text-muted-foreground"}`}
                >
                  {i + 1}
                </span>
                <span className="ml-2 text-xs font-semibold">{s}</span>
                {i < 3 && (
                  <i
                    className={`mx-3 h-px min-w-8 flex-1 ${reached ? "bg-[#0f8b8d]" : "bg-border"}`}
                  />
                )}
              </div>
            );
          })}
        </div>
      </section>
      <Modal
        open={lineOpen}
        onClose={() => setLineOpen(false)}
        title="Add journal line"
        description="Enter either a debit or a credit amount."
        wide
      >
        <form
          onSubmit={form.handleSubmit((v) => mutation.mutate(v))}
          className="grid gap-4 sm:grid-cols-2"
        >
          <FormSelect
            label="Account"
            error={form.formState.errors.account_id?.message}
            {...form.register("account_id")}
            options={[
              { value: "", label: "Select posting account" },
              ...(lookups[0].data ?? [])
                .filter((a) => a.is_posting_account)
                .map((a) => ({
                  value: a.id,
                  label: `${a.account_code} · ${a.account_name}`,
                })),
            ]}
          />
          <FormInput label="Description" {...form.register("description")} />
          <FormInput
            label="Debit amount"
            type="number"
            step="0.01"
            error={form.formState.errors.debit_amount?.message}
            {...form.register("debit_amount", { valueAsNumber: true })}
          />
          <FormInput
            label="Credit amount"
            type="number"
            step="0.01"
            {...form.register("credit_amount", { valueAsNumber: true })}
          />
          <FormSelect
            label="Cost center (optional)"
            {...form.register("cost_center_id")}
            options={toOptions(lookups[4].data)}
          />
          <FormSelect
            label="Tax (optional)"
            {...form.register("tax_id")}
            options={toOptions(lookups[1].data)}
          />
          <FormSelect
            label="Customer (optional)"
            {...form.register("customer_id")}
            options={toOptions(lookups[2].data)}
          />
          <FormSelect
            label="Vendor (optional)"
            {...form.register("vendor_id")}
            options={toOptions(lookups[3].data)}
          />
          <div className="sm:col-span-2">
            <FormActions
              onCancel={() => setLineOpen(false)}
              busy={mutation.isPending}
              label="Add line"
            />
          </div>
        </form>
      </Modal>
    </div>
  );
}
function toOptions(items?: { id: string }[]) {
  return [
    { value: "", label: "None" },
    ...(items ?? []).map((x) => ({
      value: String(x.id),
      label: referenceLabel(x as unknown as Record<string, unknown>),
    })),
  ];
}
function Summary({
  label,
  value,
  icon: Icon,
}: {
  label: string;
  value: string;
  icon: typeof ShieldCheck;
}) {
  return (
    <div className="panel flex items-center gap-4 p-4">
      <span className="grid size-10 place-items-center rounded-xl bg-[#0f8b8d]/10 text-[#0f8b8d]">
        <Icon className="size-5" />
      </span>
      <div>
        <p className="text-xs font-semibold text-muted-foreground">{label}</p>
        <p className="mt-1 font-semibold">{value}</p>
      </div>
    </div>
  );
}
function FormInput({
  label,
  error,
  ...props
}: {
  label: string;
  error?: string;
} & React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      <input className="control" {...props} />
      {error && <span className="text-xs text-destructive">{error}</span>}
    </label>
  );
}
function FormSelect({
  label,
  error,
  options,
  ...props
}: {
  label: string;
  error?: string;
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
      {error && <span className="text-xs text-destructive">{error}</span>}
    </label>
  );
}
