"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

import {
  BpmEmptyState,
  BpmRetry,
  BpmSkeleton,
  StickyToolbar,
} from "@/modules/bpm/components/bpm-ui";
import { PermissionGate } from "@/modules/bpm/components/permission-gate";
import {
  bpmDefinitionService,
  exportRowsToCsv,
} from "@/modules/bpm/services/bpm-api";
import type { WorkflowDefinition } from "@/modules/bpm/types/bpm";
import { ApiClientError } from "@/services/api-client";

export function DefinitionList() {
  const [rows, setRows] = useState<WorkflowDefinition[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [moduleCode, setModuleCode] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await bpmDefinitionService.list({
        search: search || undefined,
        status: status || undefined,
        module_code: moduleCode || undefined,
        page_size: 100,
      });
      setRows(res.data ?? []);
    } catch (e) {
      setError(e instanceof ApiClientError ? e.message : "Failed to load definitions");
    } finally {
      setLoading(false);
    }
  }, [search, status, moduleCode]);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <div>
      <StickyToolbar
        title="Workflow Definitions"
        subtitle="Stable process identity across versions"
      >
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search…"
          className="rounded border border-input bg-background px-3 py-1.5 text-sm"
        />
        <input
          value={moduleCode}
          onChange={(e) => setModuleCode(e.target.value)}
          placeholder="Module filter"
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
              "bpm-definitions.csv",
              rows.map((r) => ({
                definition_code: r.definition_code,
                definition_name: r.definition_name,
                module_code: r.module_code,
                entity_type: r.entity_type,
                status: r.status,
              })),
            )
          }
        >
          Export
        </button>
        <PermissionGate permission="bpm.definition:create">
          <Link
            href="/bpm/definitions/new"
            className="rounded bg-primary px-3 py-1.5 text-sm text-primary-foreground"
          >
            Create
          </Link>
        </PermissionGate>
      </StickyToolbar>

      {loading ? <BpmSkeleton /> : null}
      {error ? <BpmRetry message={error} onRetry={() => void load()} /> : null}
      {!loading && !error && rows.length === 0 ? (
        <BpmEmptyState title="No definitions" />
      ) : null}
      {!loading && !error && rows.length > 0 ? (
        <div className="overflow-x-auto rounded border border-border">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-border bg-muted/40">
              <tr>
                <th className="px-3 py-2">Code</th>
                <th className="px-3 py-2">Name</th>
                <th className="px-3 py-2">Module</th>
                <th className="px-3 py-2">Entity</th>
                <th className="px-3 py-2">Status</th>
                <th className="px-3 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.id} className="border-b border-border/60">
                  <td className="px-3 py-2">{row.definition_code}</td>
                  <td className="px-3 py-2">{row.definition_name}</td>
                  <td className="px-3 py-2">{row.module_code}</td>
                  <td className="px-3 py-2">{row.entity_type}</td>
                  <td className="px-3 py-2">{row.status}</td>
                  <td className="px-3 py-2">
                    <Link
                      href={`/bpm/definitions/${row.id}`}
                      className="text-primary hover:underline"
                    >
                      Detail
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
