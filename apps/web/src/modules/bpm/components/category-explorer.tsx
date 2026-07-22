"use client";

import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";

import {
  BpmEmptyState,
  BpmRetry,
  BpmSkeleton,
  StickyToolbar,
} from "@/modules/bpm/components/bpm-ui";
import { PermissionGate } from "@/modules/bpm/components/permission-gate";
import {
  bpmCategoryService,
  exportRowsToCsv,
} from "@/modules/bpm/services/bpm-api";
import type { WorkflowCategory } from "@/modules/bpm/types/bpm";
import { ApiClientError } from "@/services/api-client";

const COLUMNS = [
  { key: "category_code", label: "Code" },
  { key: "category_name", label: "Name" },
  { key: "status", label: "Status" },
  { key: "sort_order", label: "Order" },
] as const;

export function CategoryExplorer() {
  const [rows, setRows] = useState<WorkflowCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [visibleCols, setVisibleCols] = useState<Record<string, boolean>>({
    category_code: true,
    category_name: true,
    status: true,
    sort_order: true,
  });

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await bpmCategoryService.list({
        search: search || undefined,
        status: status || undefined,
        page_size: 100,
      });
      setRows(res.data ?? []);
    } catch (e) {
      setError(e instanceof ApiClientError ? e.message : "Failed to load categories");
    } finally {
      setLoading(false);
    }
  }, [search, status]);

  useEffect(() => {
    void load();
  }, [load]);

  const filteredCols = useMemo(
    () => COLUMNS.filter((c) => visibleCols[c.key]),
    [visibleCols],
  );

  return (
    <div>
      <StickyToolbar
        title="Category Explorer"
        subtitle="Organize reusable workflow templates"
      >
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search…"
          className="rounded border border-input bg-background px-3 py-1.5 text-sm"
        />
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="rounded border border-input bg-background px-2 py-1.5 text-sm"
        >
          <option value="">All statuses</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
        <button
          type="button"
          className="rounded border border-border px-3 py-1.5 text-sm"
          onClick={() =>
            exportRowsToCsv(
              "bpm-categories.csv",
              rows.map((r) => ({
                category_code: r.category_code,
                category_name: r.category_name,
                status: r.status,
                sort_order: r.sort_order,
              })),
            )
          }
        >
          CSV Export
        </button>
        <PermissionGate permission="bpm.category:create">
          <Link
            href="/bpm/categories/new"
            className="rounded bg-primary px-3 py-1.5 text-sm text-primary-foreground"
          >
            Create
          </Link>
        </PermissionGate>
      </StickyToolbar>

      <div className="mb-3 flex flex-wrap gap-3 text-xs text-muted-foreground">
        {COLUMNS.map((c) => (
          <label key={c.key} className="inline-flex items-center gap-1">
            <input
              type="checkbox"
              checked={visibleCols[c.key]}
              onChange={() =>
                setVisibleCols((v) => ({ ...v, [c.key]: !v[c.key] }))
              }
            />
            {c.label}
          </label>
        ))}
      </div>

      {loading ? <BpmSkeleton /> : null}
      {error ? <BpmRetry message={error} onRetry={() => void load()} /> : null}
      {!loading && !error && rows.length === 0 ? (
        <BpmEmptyState
          title="No categories"
          description="Create a category to organize the Template Library."
        />
      ) : null}
      {!loading && !error && rows.length > 0 ? (
        <div className="overflow-x-auto rounded border border-border">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-border bg-muted/40">
              <tr>
                {filteredCols.map((c) => (
                  <th key={c.key} className="px-3 py-2 font-medium">
                    {c.label}
                  </th>
                ))}
                <th className="px-3 py-2 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.id} className="border-b border-border/60">
                  {filteredCols.map((c) => (
                    <td key={c.key} className="px-3 py-2">
                      {String(row[c.key as keyof WorkflowCategory] ?? "")}
                    </td>
                  ))}
                  <td className="px-3 py-2">
                    <Link
                      href={`/bpm/categories/${row.id}`}
                      className="text-primary underline-offset-2 hover:underline"
                    >
                      Edit
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </div>
  );
}
