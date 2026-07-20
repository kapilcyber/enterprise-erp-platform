"use client";
import { AlertCircle, Inbox, Loader2, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function PageHeader({
  eyebrow = "Finance",
  title,
  description,
  actions,
}: {
  eyebrow?: string;
  title: string;
  description: string;
  actions?: React.ReactNode;
}) {
  return (
    <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
      <div>
        <p className="eyebrow text-[#0f8b8d]">{eyebrow}</p>
        <h1 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
          {title}
        </h1>
        <p className="mt-1 max-w-2xl text-sm text-muted-foreground">
          {description}
        </p>
      </div>
      {actions && (
        <div className="flex shrink-0 flex-wrap gap-2">{actions}</div>
      )}
    </div>
  );
}
export function StatusBadge({ value }: { value: string }) {
  const v = value.toLowerCase();
  const tone =
    v.includes("open") ||
    v === "active" ||
    v === "posted" ||
    v === "approved" ||
    v === "paid"
      ? "bg-success/10 text-success border-success/20"
      : v.includes("close") || v === "reversed" || v === "cancelled"
        ? "bg-muted text-muted-foreground border-border"
        : v === "submitted" || v.includes("progress")
          ? "bg-[#2f6f9f]/10 text-[#2f6f9f] border-[#2f6f9f]/20"
          : "bg-warning/10 text-warning border-warning/20";
  return (
    <span
      className={cn(
        "inline-flex rounded-full border px-2 py-0.5 text-xs font-semibold capitalize",
        tone,
      )}
    >
      {value.replaceAll("_", " ")}
    </span>
  );
}
export function LoadingState({
  label = "Loading finance data",
}: {
  label?: string;
}) {
  return (
    <div className="grid min-h-56 place-items-center">
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Loader2 className="size-4 animate-spin text-[#0f8b8d]" />
        {label}
      </div>
    </div>
  );
}
export function EmptyState({
  title = "No records found",
  description = "Create the first record or adjust your filters.",
}: {
  title?: string;
  description?: string;
}) {
  return (
    <div className="grid min-h-52 place-items-center px-6 text-center">
      <div>
        <span className="mx-auto mb-3 grid size-10 place-items-center rounded-full bg-muted">
          <Inbox className="size-5 text-muted-foreground" />
        </span>
        <p className="font-medium">{title}</p>
        <p className="mt-1 text-sm text-muted-foreground">{description}</p>
      </div>
    </div>
  );
}
export function ErrorState({ error }: { error: unknown }) {
  return (
    <div className="m-4 flex items-start gap-3 rounded-lg border border-destructive/25 bg-destructive/10 p-4 text-sm text-destructive">
      <AlertCircle className="mt-0.5 size-4 shrink-0" />
      <div>
        <p className="font-semibold">Unable to load data</p>
        <p>
          {error instanceof Error
            ? error.message
            : "An unexpected error occurred."}
        </p>
      </div>
    </div>
  );
}
export function Modal({
  open,
  onClose,
  title,
  description,
  children,
  wide = false,
}: {
  open: boolean;
  onClose: () => void;
  title: string;
  description?: string;
  children: React.ReactNode;
  wide?: boolean;
}) {
  if (!open) return null;
  return (
    <div
      className="fixed inset-0 z-50 grid place-items-center bg-[#07131d]/65 p-4 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
      aria-label={title}
      onMouseDown={(e) => {
        if (e.currentTarget === e.target) onClose();
      }}
    >
      <div
        className={cn(
          "max-h-[90vh] w-full overflow-auto rounded-xl border bg-card shadow-2xl",
          wide ? "max-w-3xl" : "max-w-lg",
        )}
      >
        <div className="sticky top-0 z-10 flex items-start justify-between border-b bg-card px-5 py-4">
          <div>
            <h2 className="text-lg font-semibold">{title}</h2>
            {description && (
              <p className="mt-1 text-sm text-muted-foreground">
                {description}
              </p>
            )}
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            aria-label="Close"
          >
            <X />
          </Button>
        </div>
        <div className="p-5">{children}</div>
      </div>
    </div>
  );
}
export function FormActions({
  onCancel,
  busy,
  label = "Save",
}: {
  onCancel: () => void;
  busy?: boolean;
  label?: string;
}) {
  return (
    <div className="mt-6 flex justify-end gap-2 border-t pt-4">
      <Button type="button" variant="outline" onClick={onCancel}>
        Cancel
      </Button>
      <Button
        type="submit"
        disabled={busy}
        className="bg-[#0f8b8d] hover:bg-[#0b7476]"
      >
        {busy && <Loader2 className="animate-spin" />}
        {label}
      </Button>
    </div>
  );
}
export function Pager({
  page,
  pageSize,
  count,
  onPage,
}: {
  page: number;
  pageSize: number;
  count: number;
  onPage: (page: number) => void;
}) {
  return (
    <div className="flex items-center justify-between border-t px-4 py-3 text-sm">
      <p className="text-muted-foreground">
        Page {page} · {count} records
      </p>
      <div className="flex gap-2">
        <Button
          variant="outline"
          size="sm"
          disabled={page === 1}
          onClick={() => onPage(page - 1)}
        >
          Previous
        </Button>
        <Button
          variant="outline"
          size="sm"
          disabled={count < pageSize}
          onClick={() => onPage(page + 1)}
        >
          Next
        </Button>
      </div>
    </div>
  );
}
export function CsvButton({
  rows,
  filename,
}: {
  rows: Record<string, unknown>[];
  filename: string;
}) {
  function download() {
    if (!rows.length) return;
    const keys = Object.keys(rows[0]);
    const esc = (v: unknown) => `"${String(v ?? "").replaceAll('"', '""')}"`;
    const csv = [
      keys.map(esc).join(","),
      ...rows.map((row) => keys.map((k) => esc(row[k])).join(",")),
    ].join("\n");
    const url = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }
  return (
    <Button variant="outline" onClick={download} disabled={!rows.length}>
      Export CSV
    </Button>
  );
}
