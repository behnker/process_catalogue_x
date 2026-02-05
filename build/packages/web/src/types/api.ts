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

  // RAG status (Issue Log alignment)
  rag_process?: RagStatusExtended;
  rag_system?: RagStatusExtended;
  rag_people?: RagStatusExtended;
  rag_data?: RagStatusExtended;
  rag_overall?: RagStatusExtended;
  rag_last_reviewed?: string;
}

export interface ProcessCreate {
  name: string;
  description?: string;
  level: ProcessLevel;
  parent_id?: string;
  sort_order?: number;
  process_type?: ProcessType;
  status?: LifecycleStatus;
  current_automation?: AutomationLevel;
  target_automation?: AutomationLevel;
  owner_id?: string;
  sponsor_id?: string;
  function_id?: string;
  tags?: string[];
}

export interface ProcessReorder {
  process_id: string;
  new_sort_order: number;
  new_parent_id?: string;
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
export type RagStatusExtended = "red" | "amber" | "green" | "neutral";

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

// Survey types
export type SurveyMode = "adoption" | "sentiment" | "readiness" | "feedback" | "custom";
export type SurveyStatus = "draft" | "active" | "paused" | "closed" | "archived";
export type QuestionType = "single_choice" | "multi_choice" | "rating" | "text" | "scale";

export interface Survey {
  id: string;
  organization_id: string;
  title: string;
  description?: string;
  mode: SurveyMode;
  status: SurveyStatus;
  start_date?: string;
  end_date?: string;
  is_anonymous: boolean;
  target_role?: string;
  target_department?: string;
  linked_process_id?: string;
  linked_portfolio_id?: string;
  question_count: number;
  response_count: number;
  created_at: string;
  updated_at: string;
  questions?: SurveyQuestion[];
}

export interface SurveyQuestion {
  id: string;
  survey_id: string;
  question_text: string;
  question_type: QuestionType;
  options?: string[];
  is_required: boolean;
  sort_order: number;
  help_text?: string;
  created_at: string;
  updated_at: string;
}

export interface SurveyResponseItem {
  id: string;
  survey_id: string;
  respondent_id?: string;
  submitted_at: string;
  answers: Record<string, unknown>;
}

export interface SurveyCreate {
  title: string;
  description?: string;
  mode: SurveyMode;
  start_date?: string;
  end_date?: string;
  is_anonymous?: boolean;
  target_role?: string;
  target_department?: string;
  linked_process_id?: string;
  linked_portfolio_id?: string;
}

export interface SurveyQuestionCreate {
  question_text: string;
  question_type: QuestionType;
  options?: string[];
  is_required?: boolean;
  sort_order?: number;
  help_text?: string;
}

export interface SurveyFilters extends PaginationParams {
  mode?: SurveyMode;
  status?: SurveyStatus;
  search?: string;
}

// Prompt types
export type PromptCategory = "analysis" | "documentation" | "optimization" | "reporting" | "custom";
export type ContextType = "process" | "portfolio" | "riada" | "business_model";

export interface PromptTemplate {
  id: string;
  organization_id: string;
  name: string;
  description?: string;
  category: PromptCategory;
  system_prompt?: string;
  user_prompt_template: string;
  context_type: ContextType;
  include_riada: boolean;
  include_kpis: boolean;
  include_raci: boolean;
  is_active: boolean;
  usage_count: number;
  created_at: string;
  updated_at: string;
}

export interface PromptTemplateCreate {
  name: string;
  description?: string;
  category: PromptCategory;
  system_prompt?: string;
  user_prompt_template: string;
  context_type?: ContextType;
  include_riada?: boolean;
  include_kpis?: boolean;
  include_raci?: boolean;
}

export interface PromptExecution {
  id: string;
  organization_id: string;
  template_id?: string;
  user_id: string;
  target_entity_type: string;
  target_entity_id: string;
  prompt_sent: string;
  response_received?: string;
  model_used: string;
  prompt_tokens?: number;
  completion_tokens?: number;
  total_cost?: number;
  execution_time_ms?: number;
  status: "pending" | "completed" | "failed";
  error_message?: string;
  created_at: string;
}

export interface PromptExecutionRequest {
  template_id?: string;
  custom_prompt?: string;
  target_entity_type: ContextType;
  target_entity_id: string;
  temperature?: number;
  max_tokens?: number;
}

export interface LLMConfig {
  id: string;
  organization_id: string;
  provider: string;
  model: string;
  endpoint_url?: string;
  default_temperature: number;
  default_max_tokens: number;
  rate_limit_rpm: number;
  monthly_token_limit?: number;
  is_enabled: boolean;
  created_at: string;
  updated_at: string;
}

export interface PromptFilters extends PaginationParams {
  category?: PromptCategory;
  context_type?: ContextType;
  search?: string;
}
