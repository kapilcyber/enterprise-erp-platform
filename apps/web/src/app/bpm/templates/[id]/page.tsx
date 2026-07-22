"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { BpmRetry, BpmSkeleton } from "@/modules/bpm/components/bpm-ui";
import { TemplateForm } from "@/modules/bpm/components/template-form";
import { bpmTemplateService } from "@/modules/bpm/services/bpm-api";
import type { WorkflowTemplate } from "@/modules/bpm/types/bpm";
import { ApiClientError } from "@/services/api-client";

export default function EditTemplatePage() {
  const params = useParams<{ id: string }>();
  const [row, setRow] = useState<WorkflowTemplate | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    void (async () => {
      try {
        const res = await bpmTemplateService.get(params.id);
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
    <TemplateForm
      mode="edit"
      initial={{
        id: row.id,
        template_name: row.template_name,
        description: row.description,
        module_code: row.module_code,
        entity_type: row.entity_type,
      }}
    />
  );
}
