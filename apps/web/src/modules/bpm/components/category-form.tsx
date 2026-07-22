"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { StickyToolbar, UnsavedWarning } from "@/modules/bpm/components/bpm-ui";
import { bpmCategoryService } from "@/modules/bpm/services/bpm-api";

export function CategoryForm({
  mode,
  initial,
}: {
  mode: "create" | "edit";
  initial?: { id: string; category_name: string; description?: string | null; status?: string };
}) {
  const router = useRouter();
  const [name, setName] = useState(initial?.category_name ?? "");
  const [description, setDescription] = useState(initial?.description ?? "");
  const [dirty, setDirty] = useState(false);
  const [saving, setSaving] = useState(false);

  return (
    <div>
      <StickyToolbar
        title={mode === "create" ? "Create Category" : "Edit Category"}
        subtitle="Workflow category"
      >
        <button
          type="button"
          className="rounded border border-border px-3 py-1.5 text-sm"
          onClick={() => router.push("/bpm/categories")}
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
              if (mode === "create") {
                await bpmCategoryService.create({
                  category_name: name,
                  description: description || undefined,
                });
              } else if (initial) {
                await bpmCategoryService.update(initial.id, {
                  category_name: name,
                  description: description || undefined,
                });
              }
              setDirty(false);
              router.push("/bpm/categories");
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
