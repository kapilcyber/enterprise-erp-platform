"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

import {
  BpmEmptyState,
  BpmRetry,
  BpmSkeleton,
  ConfirmDialog,
  StickyToolbar,
} from "@/modules/bpm/components/bpm-ui";
import { PermissionGate } from "@/modules/bpm/components/permission-gate";
import {
  bpmTemplateService,
  exportRowsToCsv,
} from "@/modules/bpm/services/bpm-api";
import type { WorkflowTemplate } from "@/modules/bpm/types/bpm";
import { ApiClientError } from "@/services/api-client";

export function TemplateLibrary() {
  const [rows, setRows] = useState<WorkflowTemplate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [copyId, setCopyId] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await bpmTemplateService.list({
        search: search || undefined,
        status: status || undefined,
        page_size: 100,
      });
      setRows(res.data ?? []);
    } catch (e) {
      setError(e instanceof ApiClientError ? e.message : "Failed to load templates");
    } finally {
      setLoading(false);
    }
  }, [search, status]);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <div>
      <StickyToolbar title="Template Library" subtitle="Reusable workflow templates">
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
          <option value="draft">Draft</option>
          <option value="active">Active</option>
          <option value="retired">Retired</option>
        </select>
        <button
          type="button"
          className="rounded border border-border px-3 py-1.5 text-sm"
          onClick={() =>
            exportRowsToCsv(
              "bpm-templates.csv",
              rows.map((r) => ({
                template_code: r.template_code,
                template_name: r.template_name,
                status: r.status,
                module_code: r.module_code,
                entity_type: r.entity_type,
              })),
            )
          }
        >
          CSV / XLSX Export
        </button>
        <PermissionGate permission="bpm.template:create">
          <Link
            href="/bpm/templates/new"
            className="rounded bg-primary px-3 py-1.5 text-sm text-primary-foreground"
          >
            Create
          </Link>
        </PermissionGate>
      </StickyToolbar>

      {loading ? <BpmSkeleton /> : null}
      {error ? <BpmRetry message={error} onRetry={() => void load()} /> : null}
      {!loading && !error && rows.length === 0 ? (
        <BpmEmptyState title="No templates" description="Seed the library with a reusable template." />
      ) : null}
      {!loading && !error && rows.length > 0 ? (
        <div className="overflow-x-auto rounded border border-border">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-border bg-muted/40">
              <tr>
                <th className="px-3 py-2">Code</th>
                <th className="px-3 py-2">Name</th>
                <th className="px-3 py-2">Status</th>
                <th className="px-3 py-2">Module</th>
                <th className="px-3 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.id} className="border-b border-border/60">
                  <td className="px-3 py-2">{row.template_code}</td>
                  <td className="px-3 py-2">{row.template_name}</td>
                  <td className="px-3 py-2">{row.status}</td>
                  <td className="px-3 py-2">{row.module_code ?? "—"}</td>
                  <td className="px-3 py-2 space-x-3">
                    <Link href={`/bpm/templates/${row.id}`} className="text-primary hover:underline">
                      Edit
                    </Link>
                    <PermissionGate permission="bpm.template:copy">
                      <button
                        type="button"
                        className="text-primary hover:underline"
                        onClick={() => setCopyId(row.id)}
                      >
                        Copy
                      </button>
                    </PermissionGate>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}

      <ConfirmDialog
        open={!!copyId}
        title="Copy Template"
        description="Create a draft copy of this reusable template."
        confirmLabel="Copy Template"
        onCancel={() => setCopyId(null)}
        onConfirm={async () => {
          if (!copyId) return;
          await bpmTemplateService.copy(copyId);
          setCopyId(null);
          await load();
        }}
      />
    </div>
  );
}
