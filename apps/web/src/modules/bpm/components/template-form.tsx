"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { StickyToolbar, UnsavedWarning } from "@/modules/bpm/components/bpm-ui";
import { bpmTemplateService } from "@/modules/bpm/services/bpm-api";

export function TemplateForm({
  mode,
  initial,
}: {
  mode: "create" | "edit";
  initial?: {
    id: string;
    template_name: string;
    description?: string | null;
    module_code?: string | null;
    entity_type?: string | null;
  };
}) {
  const router = useRouter();
  const [name, setName] = useState(initial?.template_name ?? "");
  const [description, setDescription] = useState(initial?.description ?? "");
  const [moduleCode, setModuleCode] = useState(initial?.module_code ?? "");
  const [entityType, setEntityType] = useState(initial?.entity_type ?? "");
  const [dirty, setDirty] = useState(false);
  const [saving, setSaving] = useState(false);

  return (
    <div>
      <StickyToolbar
        title={mode === "create" ? "Create Template" : "Edit Template"}
        subtitle="Template Library"
      >
        <button
          type="button"
          className="rounded border border-border px-3 py-1.5 text-sm"
          onClick={() => router.push("/bpm/templates")}
        >
          Cancel
        </button>
        <button
          type="button"
          disabled={saving || !name.trim()}
          className="rounded bg-primary px-3 py-1.5 text-sm text-primary-foreground disabled:opacity-50"
          onClick={async () => {
            setSaving(true);
            try {
              const payload = {
                template_name: name,
                description: description || undefined,
                module_code: moduleCode || undefined,
                entity_type: entityType || undefined,
              };
              if (mode === "create") {
                await bpmTemplateService.create(payload);
              } else if (initial) {
                await bpmTemplateService.update(initial.id, payload);
              }
              setDirty(false);
              router.push("/bpm/templates");
            } finally {
              setSaving(false);
            }
          }}
        >
          Save
        </button>
      </StickyToolbar>
      <UnsavedWarning dirty={dirty} />
      <div className="max-w-lg space-y-4">
        <label className="block text-sm">
          Name
          <input
            className="mt-1 w-full rounded border border-input bg-background px-3 py-2"
            value={name}
            onChange={(e) => {
              setName(e.target.value);
              setDirty(true);
            }}
          />
        </label>
        <label className="block text-sm">
          Module code
          <input
            className="mt-1 w-full rounded border border-input bg-background px-3 py-2"
            value={moduleCode}
            onChange={(e) => {
              setModuleCode(e.target.value);
              setDirty(true);
            }}
          />
        </label>
        <label className="block text-sm">
          Entity type
          <input
            className="mt-1 w-full rounded border border-input bg-background px-3 py-2"
            value={entityType}
            onChange={(e) => {
              setEntityType(e.target.value);
              setDirty(true);
            }}
          />
        </label>
        <label className="block text-sm">
          Description
          <textarea
            className="mt-1 w-full rounded border border-input bg-background px-3 py-2"
            rows={4}
            value={description}
            onChange={(e) => {
              setDescription(e.target.value);
              setDirty(true);
            }}
          />
        </label>
      </div>
    </div>
  );
}
