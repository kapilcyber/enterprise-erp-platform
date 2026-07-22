"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

import {
  BpmEmptyState,
  BpmRetry,
  BpmSkeleton,
  ConfirmDialog,
  StickyToolbar,
  UnsavedWarning,
} from "@/modules/bpm/components/bpm-ui";
import { PermissionGate } from "@/modules/bpm/components/permission-gate";
import {
  bpmDefinitionService,
  bpmVersionService,
} from "@/modules/bpm/services/bpm-api";
import type { WorkflowDefinition, WorkflowVersion } from "@/modules/bpm/types/bpm";
import { ApiClientError } from "@/services/api-client";

export function DefinitionDetail({ definitionId }: { definitionId: string }) {
  const [definition, setDefinition] = useState<WorkflowDefinition | null>(null);
  const [versions, setVersions] = useState<WorkflowVersion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [name, setName] = useState("");
  const [dirty, setDirty] = useState(false);
  const [publishId, setPublishId] = useState<string | null>(null);
  const [cloneId, setCloneId] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [defRes, verRes] = await Promise.all([
        bpmDefinitionService.get(definitionId),
        bpmDefinitionService.versions(definitionId, { page_size: 100 }),
      ]);
      setDefinition(defRes.data);
      setName(defRes.data?.definition_name ?? "");
      setVersions(verRes.data ?? []);
      setDirty(false);
    } catch (e) {
      setError(e instanceof ApiClientError ? e.message : "Failed to load definition");
    } finally {
      setLoading(false);
    }
  }, [definitionId]);

  useEffect(() => {
    void load();
  }, [load]);

  if (loading) return <BpmSkeleton rows={8} />;
  if (error) return <BpmRetry message={error} onRetry={() => void load()} />;
  if (!definition) return <BpmEmptyState title="Definition not found" />;

  return (
    <div>
      <StickyToolbar
        title={definition.definition_name}
        subtitle={`${definition.definition_code} · ${definition.module_code} / ${definition.entity_type}`}
      >
        <Link href="/bpm/definitions" className="rounded border border-border px-3 py-1.5 text-sm">
          Back
        </Link>
        <PermissionGate permission="bpm.definition:update">
          <button
            type="button"
            disabled={!dirty}
            className="rounded bg-primary px-3 py-1.5 text-sm text-primary-foreground disabled:opacity-50"
            onClick={async () => {
              await bpmDefinitionService.update(definitionId, { definition_name: name });
              setDirty(false);
              await load();
            }}
          >
            Save
          </button>
        </PermissionGate>
      </StickyToolbar>

      <UnsavedWarning dirty={dirty} />

      <section className="mb-8 space-y-3">
        <h2 className="text-sm font-medium uppercase tracking-wide text-muted-foreground">
          Definition
        </h2>
        <label className="block text-sm">
          Name
          <input
            className="mt-1 w-full max-w-lg rounded border border-input bg-background px-3 py-2"
            value={name}
            onChange={(e) => {
              setName(e.target.value);
              setDirty(e.target.value !== definition.definition_name);
            }}
          />
        </label>
        <p className="text-sm text-muted-foreground">Status: {definition.status}</p>
      </section>

      <section>
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-sm font-medium uppercase tracking-wide text-muted-foreground">
            Version Timeline
          </h2>
          <PermissionGate permission="bpm.version:create">
            <button
              type="button"
              className="rounded border border-border px-3 py-1.5 text-sm"
              onClick={async () => {
                await bpmVersionService.createDraft({ definition_id: definitionId });
                await load();
              }}
            >
              New Draft
            </button>
          </PermissionGate>
        </div>

        {versions.length === 0 ? (
          <BpmEmptyState title="No versions" />
        ) : (
          <ol className="relative space-y-4 border-l border-border pl-6">
            {versions.map((v) => (
              <li key={v.id} className="relative">
                <span className="absolute -left-[1.55rem] top-1 h-3 w-3 rounded-full border-2 border-primary bg-background" />
                <div className="rounded border border-border p-3">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div>
                      <p className="font-medium">
                        {v.version_label ?? `v${v.version_number}`}{" "}
                        <span className="text-xs font-normal text-muted-foreground">
                          ({v.status})
                        </span>
                      </p>
                      <p className="text-xs text-muted-foreground">{v.version_code}</p>
                      {v.change_notes ? (
                        <p className="mt-1 text-sm text-muted-foreground">{v.change_notes}</p>
                      ) : null}
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {v.status === "draft" ? (
                        <PermissionGate permission="bpm.version:publish">
                          <button
                            type="button"
                            className="rounded bg-primary px-2 py-1 text-xs text-primary-foreground"
                            onClick={() => setPublishId(v.id)}
                          >
                            Publish
                          </button>
                        </PermissionGate>
                      ) : null}
                      <PermissionGate permission="bpm.version:clone">
                        <button
                          type="button"
                          className="rounded border border-border px-2 py-1 text-xs"
                          onClick={() => setCloneId(v.id)}
                        >
                          Clone
                        </button>
                      </PermissionGate>
                      {v.status !== "retired" ? (
                        <PermissionGate permission="bpm.version:retire">
                          <button
                            type="button"
                            className="rounded border border-border px-2 py-1 text-xs"
                            onClick={async () => {
                              await bpmVersionService.retire(v.id);
                              await load();
                            }}
                          >
                            Retire
                          </button>
                        </PermissionGate>
                      ) : null}
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ol>
        )}
      </section>

      <ConfirmDialog
        open={!!publishId}
        title="Publish Version"
        description="Publishing makes this version immutable and retires any prior published version for this definition. Exactly one Published Version is allowed."
        confirmLabel="Publish"
        onCancel={() => setPublishId(null)}
        onConfirm={async () => {
          if (!publishId) return;
          await bpmVersionService.publish(publishId);
          setPublishId(null);
          await load();
        }}
      />

      <ConfirmDialog
        open={!!cloneId}
        title="Clone Version"
        description="Create a new editable draft cloned from the selected version."
        confirmLabel="Clone"
        onCancel={() => setCloneId(null)}
        onConfirm={async () => {
          if (!cloneId) return;
          await bpmVersionService.clone(cloneId);
          setCloneId(null);
          await load();
        }}
      />
    </div>
  );
}
