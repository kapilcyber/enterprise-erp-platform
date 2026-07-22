"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { StickyToolbar, UnsavedWarning } from "@/modules/bpm/components/bpm-ui";
import { bpmDefinitionService } from "@/modules/bpm/services/bpm-api";

export function DefinitionForm() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [moduleCode, setModuleCode] = useState("");
  const [entityType, setEntityType] = useState("");
  const [description, setDescription] = useState("");
  const [dirty, setDirty] = useState(false);
  const [saving, setSaving] = useState(false);

  return (
    <div>
      <StickyToolbar title="Create Definition" subtitle="Stable workflow identity">
        <button
          type="button"
          className="rounded border border-border px-3 py-1.5 text-sm"
          onClick={() => router.push("/bpm/definitions")}
        >
          Cancel
        </button>
        <button
          type="button"
          disabled={saving || !name.trim() || !moduleCode.trim() || !entityType.trim()}
          className="rounded bg-primary px-3 py-1.5 text-sm text-primary-foreground disabled:opacity-50"
          onClick={async () => {
            setSaving(true);
            try {
              const res = await bpmDefinitionService.create({
                definition_name: name,
                module_code: moduleCode,
                entity_type: entityType,
                description: description || undefined,
              });
              setDirty(false);
              router.push(`/bpm/definitions/${res.data?.id}`);
            } finally {
              setSaving(false);
            }
          }}
        >
          Create
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
