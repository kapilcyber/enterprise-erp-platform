import { apiClient } from "@/services/api-client";
import type {
  BpmListParams,
  WorkflowCategory,
  WorkflowDefinition,
  WorkflowTemplate,
  WorkflowVersion,
} from "@/modules/bpm/types/bpm";

function qs(params?: BpmListParams): string {
  if (!params) return "";
  const sp = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== "") sp.set(k, String(v));
  });
  const s = sp.toString();
  return s ? `?${s}` : "";
}

const base = "/api/v1/bpm";

export const bpmCategoryService = {
  list: (params?: BpmListParams) =>
    apiClient<WorkflowCategory[]>(`${base}/categories${qs(params)}`),
  get: (id: string) => apiClient<WorkflowCategory>(`${base}/categories/${id}`),
  create: (body: Partial<WorkflowCategory>) =>
    apiClient<WorkflowCategory>(`${base}/categories`, { method: "POST", body }),
  update: (id: string, body: Partial<WorkflowCategory>) =>
    apiClient<WorkflowCategory>(`${base}/categories/${id}`, { method: "PATCH", body }),
  remove: (id: string) =>
    apiClient<WorkflowCategory>(`${base}/categories/${id}`, { method: "DELETE" }),
};

export const bpmTemplateService = {
  list: (params?: BpmListParams) =>
    apiClient<WorkflowTemplate[]>(`${base}/templates${qs(params)}`),
  get: (id: string) => apiClient<WorkflowTemplate>(`${base}/templates/${id}`),
  create: (body: Partial<WorkflowTemplate>) =>
    apiClient<WorkflowTemplate>(`${base}/templates`, { method: "POST", body }),
  update: (id: string, body: Partial<WorkflowTemplate>) =>
    apiClient<WorkflowTemplate>(`${base}/templates/${id}`, { method: "PATCH", body }),
  copy: (id: string, template_name?: string) =>
    apiClient<WorkflowTemplate>(`${base}/templates/${id}/copy`, {
      method: "POST",
      body: { template_name },
    }),
};

export const bpmDefinitionService = {
  list: (params?: BpmListParams) =>
    apiClient<WorkflowDefinition[]>(`${base}/definitions${qs(params)}`),
  get: (id: string) => apiClient<WorkflowDefinition>(`${base}/definitions/${id}`),
  create: (body: Partial<WorkflowDefinition>) =>
    apiClient<WorkflowDefinition>(`${base}/definitions`, { method: "POST", body }),
  update: (id: string, body: Partial<WorkflowDefinition>) =>
    apiClient<WorkflowDefinition>(`${base}/definitions/${id}`, { method: "PATCH", body }),
  versions: (id: string, params?: BpmListParams) =>
    apiClient<WorkflowVersion[]>(`${base}/definitions/${id}/versions${qs(params)}`),
};

export const bpmVersionService = {
  get: (id: string) => apiClient<WorkflowVersion>(`${base}/versions/${id}`),
  createDraft: (body: {
    definition_id: string;
    version_label?: string;
    change_notes?: string;
  }) => apiClient<WorkflowVersion>(`${base}/versions`, { method: "POST", body }),
  update: (id: string, body: Partial<WorkflowVersion>) =>
    apiClient<WorkflowVersion>(`${base}/versions/${id}`, { method: "PATCH", body }),
  publish: (id: string) =>
    apiClient<WorkflowVersion>(`${base}/versions/${id}/publish`, { method: "POST" }),
  retire: (id: string) =>
    apiClient<WorkflowVersion>(`${base}/versions/${id}/retire`, { method: "POST" }),
  clone: (id: string, body?: { version_label?: string; change_notes?: string }) =>
    apiClient<WorkflowVersion>(`${base}/versions/${id}/clone`, {
      method: "POST",
      body: body ?? {},
    }),
};

export function exportRowsToCsv(filename: string, rows: Record<string, unknown>[]) {
  if (!rows.length) return;
  const keys = Object.keys(rows[0]);
  const lines = [
    keys.join(","),
    ...rows.map((r) =>
      keys.map((k) => `"${String(r[k] ?? "").replaceAll('"', '""')}"`).join(","),
    ),
  ];
  const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
