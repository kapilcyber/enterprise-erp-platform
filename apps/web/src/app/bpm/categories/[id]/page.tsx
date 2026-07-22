"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { BpmRetry, BpmSkeleton } from "@/modules/bpm/components/bpm-ui";
import { CategoryForm } from "@/modules/bpm/components/category-form";
import { bpmCategoryService } from "@/modules/bpm/services/bpm-api";
import type { WorkflowCategory } from "@/modules/bpm/types/bpm";
import { ApiClientError } from "@/services/api-client";

export default function EditCategoryPage() {
  const params = useParams<{ id: string }>();
  const [row, setRow] = useState<WorkflowCategory | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    void (async () => {
      try {
        const res = await bpmCategoryService.get(params.id);
        setRow(res.data);
      } catch (e) {
        setError(e instanceof ApiClientError ? e.message : "Failed to load");
      } finally {
        setLoading(false);
      }
    })();
  }, [params.id]);

  if (loading) return <BpmSkeleton />;
  if (error || !row) return <BpmRetry message={error ?? "Not found"} onRetry={() => location.reload()} />;
  return (
    <CategoryForm
      mode="edit"
      initial={{
        id: row.id,
        category_name: row.category_name,
        description: row.description,
        status: row.status,
      }}
    />
  );
}
