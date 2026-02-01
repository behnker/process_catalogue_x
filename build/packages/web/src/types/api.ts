// Common API types

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  has_more: boolean;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: unknown[];
  };
}

// Pagination params
export interface PaginationParams {
  page?: number;
  per_page?: number;
}

// Process types
export type ProcessLevel = "L0" | "L1" | "L2" | "L3" | "L4" | "L5";
export type ProcessType = "primary" | "secondary";
export type LifecycleStatus = "draft" | "active" | "under_review" | "deprecated" | "archived";
export type AutomationLevel = "manual" | "semi_automated" | "fully_automated" | "ai_assisted";

export interface Process {
  id: string;
  organization_id: string;
  code: string;
  name: string;
  description?: string;
  level: ProcessLevel;
  parent_id?: string;
  sort_order: number;
  process_type: ProcessType;
  status: LifecycleStatus;
  current_automation: AutomationLevel;
  target_automation?: AutomationLevel;
  automation_notes?: string;
  owner_id?: string;
  sponsor_id?: string;
  function_id?: string;
  tags?: string[];
  metadata_extra?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
  children?: Process[];
}

export interface ProcessCreate {
  code: string;
  name: string;
  description?: string;
  level: ProcessLevel;
  parent_id?: string;
  process_type?: ProcessType;
  status?: LifecycleStatus;
  current_automation?: AutomationLevel;
  target_automation?: AutomationLevel;
  owner_id?: string;
  sponsor_id?: string;
  tags?: string[];
}

export interface ProcessUpdate extends Partial<ProcessCreate> {}

export interface ProcessFilters extends PaginationParams {
  level?: ProcessLevel;
  process_type?: ProcessType;
  status?: LifecycleStatus;
  parent_id?: string;
  search?: string;
}

// RIADA types
export type RiadaType = "risk" | "issue" | "action" | "dependency" | "assumption";
export type RiadaCategory = "people" | "process" | "system" | "data";
export type RiadaSeverity = "critical" | "high" | "medium" | "low";
export type RiadaStatus = "open" | "in_progress" | "mitigated" | "resolved" | "closed" | "accepted";
export type RagStatus = "red" | "amber" | "green";

export interface RiadaItem {
  id: string;
  organization_id: string;
  code: string;
  title: string;
  description?: string;
  riada_type: RiadaType;
  category: RiadaCategory;
  severity: RiadaSeverity;
  status: RiadaStatus;
  probability?: number;
  impact?: number;
  risk_score?: number;
  mitigation_plan?: string;
  due_date?: string;
  assigned_to_id?: string;
  raised_by_id?: string;
  process_id?: string;
  portfolio_item_id?: string;
  business_model_entry_id?: string;
  rag_status?: RagStatus;
  resolution_notes?: string;
  resolved_at?: string;
  resolved_by_id?: string;
  tags?: string[];
  created_at: string;
  updated_at: string;
}

export interface RiadaItemCreate {
  code: string;
  title: string;
  description?: string;
  riada_type: RiadaType;
  category: RiadaCategory;
  severity?: RiadaSeverity;
  probability?: number;
  impact?: number;
  mitigation_plan?: string;
  due_date?: string;
  assigned_to_id?: string;
  process_id?: string;
  portfolio_item_id?: string;
  business_model_entry_id?: string;
}

export interface RiadaItemUpdate extends Partial<RiadaItemCreate> {
  status?: RiadaStatus;
  resolution_notes?: string;
}

export interface RiadaFilters extends PaginationParams {
  riada_type?: RiadaType;
  category?: RiadaCategory;
  severity?: RiadaSeverity;
  status?: RiadaStatus;
  process_id?: string;
  search?: string;
}

// Business Model types
export type BMCComponent =
  | "key_partners"
  | "key_activities"
  | "key_resources"
  | "value_propositions"
  | "customer_relationships"
  | "channels"
  | "customer_segments"
  | "cost_structure"
  | "revenue_streams";

export interface BusinessModel {
  id: string;
  organization_id: string;
  name: string;
  description?: string;
  status: string;
  canvas_layout?: Record<string, unknown>;
  entries?: BusinessModelEntry[];
  created_at: string;
  updated_at: string;
}

export interface BusinessModelEntry {
  id: string;
  organization_id: string;
  business_model_id: string;
  component: BMCComponent;
  title: string;
  description?: string;
  sort_order: number;
  agentic_opportunity?: string;
  agentic_readiness?: "low" | "medium" | "high";
  agentic_impact?: "low" | "medium" | "high";
  agentic_notes?: string;
  metadata_extra?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface BusinessModelCreate {
  name: string;
  description?: string;
}

export interface BusinessModelEntryCreate {
  business_model_id: string;
  component: BMCComponent;
  title: string;
  description?: string;
  agentic_opportunity?: string;
  agentic_readiness?: "low" | "medium" | "high";
  agentic_impact?: "low" | "medium" | "high";
}

// Portfolio types
export type PortfolioLevel =
  | "strategy"
  | "portfolio"
  | "programme"
  | "project"
  | "workstream"
  | "epic"
  | "task";

export type PortfolioStatus =
  | "proposed"
  | "approved"
  | "in_progress"
  | "on_hold"
  | "completed"
  | "cancelled";

export interface PortfolioItem {
  id: string;
  organization_id: string;
  code: string;
  name: string;
  description?: string;
  level: PortfolioLevel;
  parent_id?: string;
  sort_order: number;
  status: PortfolioStatus;
  rag_status?: RagStatus;
  rag_notes?: string;
  business_value?: number;
  time_criticality?: number;
  risk_reduction?: number;
  job_size?: number;
  wsvf_score?: number;
  planned_start?: string;
  planned_end?: string;
  actual_start?: string;
  actual_end?: string;
  budget_approved?: number;
  budget_spent?: number;
  budget_forecast?: number;
  budget_currency: string;
  owner_id?: string;
  sponsor_id?: string;
  linked_process_ids?: string[];
  tags?: string[];
  metadata_extra?: Record<string, unknown>;
  children?: PortfolioItem[];
  milestones?: PortfolioMilestone[];
  created_at: string;
  updated_at: string;
}

export interface PortfolioMilestone {
  id: string;
  organization_id: string;
  portfolio_item_id: string;
  name: string;
  description?: string;
  due_date?: string;
  completed_date?: string;
  status: string;
  sort_order: number;
  created_at: string;
  updated_at: string;
}

export interface PortfolioItemCreate {
  code: string;
  name: string;
  description?: string;
  level: PortfolioLevel;
  parent_id?: string;
  status?: PortfolioStatus;
  business_value?: number;
  time_criticality?: number;
  risk_reduction?: number;
  job_size?: number;
  planned_start?: string;
  planned_end?: string;
  budget_approved?: number;
  budget_currency?: string;
  owner_id?: string;
  sponsor_id?: string;
  linked_process_ids?: string[];
}

export interface PortfolioItemUpdate extends Partial<PortfolioItemCreate> {
  rag_status?: RagStatus;
  rag_notes?: string;
  actual_start?: string;
  actual_end?: string;
  budget_spent?: number;
  budget_forecast?: number;
}

export interface PortfolioFilters extends PaginationParams {
  level?: PortfolioLevel;
  status?: PortfolioStatus;
  parent_id?: string;
  search?: string;
}
