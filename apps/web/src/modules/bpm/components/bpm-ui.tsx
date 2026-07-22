"use client";

import type { ReactNode } from "react";

export function BpmSkeleton({ rows = 6 }: { rows?: number }) {
  return (
    <div className="space-y-3" aria-busy="true" aria-label="Loading">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="h-10 animate-pulse rounded bg-muted/60" />
      ))}
    </div>
  );
}

export function BpmEmptyState({
  title,
  description,
  action,
}: {
  title: string;
  description?: string;
  action?: ReactNode;
}) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-16 text-center">
      <h3 className="text-lg font-medium text-foreground">{title}</h3>
      {description ? (
        <p className="max-w-md text-sm text-muted-foreground">{description}</p>
      ) : null}
      {action}
    </div>
  );
}

export function BpmRetry({ onRetry, message }: { onRetry: () => void; message?: string }) {
  return (
    <div className="flex flex-col items-center gap-3 py-12">
      <p className="text-sm text-destructive">{message ?? "Something went wrong."}</p>
      <button
        type="button"
        onClick={onRetry}
        className="rounded border border-border px-3 py-1.5 text-sm hover:bg-muted"
      >
        Retry
      </button>
    </div>
  );
}

export function StickyToolbar({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle?: string;
  children?: ReactNode;
}) {
  return (
    <div className="sticky top-0 z-20 -mx-6 mb-6 border-b border-border bg-background/95 px-6 py-4 backdrop-blur">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-foreground">{title}</h1>
          {subtitle ? <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p> : null}
        </div>
        <div className="flex flex-wrap items-center gap-2">{children}</div>
      </div>
    </div>
  );
}

export function ConfirmDialog({
  open,
  title,
  description,
  confirmLabel = "Confirm",
  onConfirm,
  onCancel,
}: {
  open: boolean;
  title: string;
  description?: string;
  confirmLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
}) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div
        role="dialog"
        aria-modal="true"
        className="w-full max-w-md rounded-lg border border-border bg-background p-6 shadow-lg"
      >
        <h2 className="text-lg font-semibold">{title}</h2>
        {description ? (
          <p className="mt-2 text-sm text-muted-foreground">{description}</p>
        ) : null}
        <div className="mt-6 flex justify-end gap-2">
          <button
            type="button"
            onClick={onCancel}
            className="rounded border border-border px-3 py-1.5 text-sm"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={onConfirm}
            className="rounded bg-primary px-3 py-1.5 text-sm text-primary-foreground"
          >
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}

export function UnsavedWarning({ dirty }: { dirty: boolean }) {
  if (!dirty) return null;
  return (
    <p className="text-xs text-amber-700 dark:text-amber-400">
      You have unsaved changes.
    </p>
  );
}
