/** BPM Phase 1 domain types. */

export type CategoryStatus = "active" | "inactive";
export type TemplateStatus = "draft" | "active" | "retired";
export type DefinitionStatus = "draft" | "active" | "retired";
export type VersionStatus = "draft" | "published" | "retired";

export interface WorkflowCategory {
  id: string;
  company_id: string;
  category_code: string;
  category_name: string;
  description?: string | null;
  status: CategoryStatus | string;
  sort_order: number;
  owner_employee_id?: string | null;
  version: number;
}

export interface WorkflowTemplate {
  id: string;
  company_id: string;
  template_code: string;
  template_name: string;
  description?: string | null;
  status: TemplateStatus | string;
  category_id?: string | null;
  module_code?: string | null;
  entity_type?: string | null;
  owner_employee_id?: string | null;
  version: number;
}

export interface WorkflowDefinition {
  id: string;
  company_id: string;
  definition_code: string;
  definition_name: string;
  description?: string | null;
  status: DefinitionStatus | string;
  template_id?: string | null;
  module_code: string;
  entity_type: string;
  owner_employee_id?: string | null;
  department_id?: string | null;
  version: number;
}

export interface WorkflowVersion {
  id: string;
  company_id: string;
  definition_id: string;
  version_code: string;
  version_number: number;
  version_label?: string | null;
  change_notes?: string | null;
  status: VersionStatus | string;
  published_at?: string | null;
  published_by?: string | null;
  retired_at?: string | null;
  retired_by?: string | null;
  cloned_from_version_id?: string | null;
  version: number;
}

export interface BpmListParams {
  page?: number;
  page_size?: number;
  search?: string;
  status?: string;
  category_id?: string;
  module_code?: string;
  entity_type?: string;
  company_id?: string;
}

export type BpmPermission =
  | "bpm.category:read"
  | "bpm.category:create"
  | "bpm.category:update"
  | "bpm.category:delete"
  | "bpm.template:read"
  | "bpm.template:create"
  | "bpm.template:update"
  | "bpm.template:copy"
  | "bpm.definition:read"
  | "bpm.definition:create"
  | "bpm.definition:update"
  | "bpm.version:read"
  | "bpm.version:create"
  | "bpm.version:update"
  | "bpm.version:publish"
  | "bpm.version:retire"
  | "bpm.version:clone";
