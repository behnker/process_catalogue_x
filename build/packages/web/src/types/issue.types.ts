/**
 * Issue Log Types
 *
 * AMD-01: OPS- prefix for display_id (not ISS-)
 * AMD-02: JSONB arrays for beneficiary_roles
 */

// Enums
export type IssueClassification = "people" | "process" | "system" | "data";
export type IssueCriticality = "high" | "medium" | "low";
export type IssueComplexity = "high" | "medium" | "low";
export type IssueStatus = "open" | "in_progress" | "resolved" | "closed" | "deferred";
export type OpportunityStatus =
  | "identified"
  | "evaluating"
  | "approved"
  | "in_delivery"
  | "delivered"
  | "rejected";

// Extended RAG status (includes neutral per addendum)
export type RAGStatusExtended = "red" | "amber" | "green" | "neutral";

// Issue response
export interface Issue {
  id: string;
  display_id: string; // OPS-001 format (AMD-01)
  issue_number: number;
  title: string;
  description?: string;
  issue_classification: IssueClassification;
  issue_criticality: IssueCriticality;
  issue_complexity: IssueComplexity;
  issue_status: IssueStatus;

  // Process linkage (denormalized)
  process_id: string;
  process_level: number; // 0-5
  process_ref: string;
  process_name: string;

  // Ownership
  raised_by_id: string;
  assigned_to_id?: string;

  // Dates
  date_raised: string;
  target_resolution_date?: string;
  actual_resolution_date?: string;

  // Resolution
  resolution_summary?: string;

  // Opportunity tracking
  opportunity_flag: boolean;
  opportunity_status?: OpportunityStatus;
  opportunity_description?: string;
  opportunity_expected_benefit?: string;
  opportunity_beneficiary_roles: string[]; // AMD-02: JSONB array

  // Audit
  created_by: string;
  updated_by?: string;
  created_at: string;
  updated_at: string;
}

// Create request
export interface IssueCreate {
  title: string;
  description?: string;
  issue_classification: IssueClassification;
  issue_criticality?: IssueCriticality;
  issue_complexity?: IssueComplexity;
  process_id: string;
  assigned_to_id?: string;
  target_resolution_date?: string;
  opportunity_flag?: boolean;
  opportunity_description?: string;
  opportunity_expected_benefit?: string;
  opportunity_beneficiary_roles?: string[];
}

// Update request
export interface IssueUpdate {
  title?: string;
  description?: string;
  issue_criticality?: IssueCriticality;
  issue_complexity?: IssueComplexity;
  issue_status?: IssueStatus;
  assigned_to_id?: string;
  target_resolution_date?: string;
  actual_resolution_date?: string;
  resolution_summary?: string;
  opportunity_flag?: boolean;
  opportunity_status?: OpportunityStatus;
  opportunity_description?: string;
  opportunity_expected_benefit?: string;
  opportunity_beneficiary_roles?: string[];
}

// Filters
export interface IssueFilters {
  page?: number;
  per_page?: number;
  status_filter?: string; // Comma-separated
  classification?: IssueClassification;
  criticality?: IssueCriticality;
  process_id?: string;
  assigned_to?: string;
}

// History
export interface IssueHistoryEntry {
  id: string;
  field_name: string;
  old_value?: string;
  new_value?: string;
  change_note?: string;
  changed_by: string;
  changed_at: string;
}

export interface IssueHistory {
  issue_id: string;
  display_id: string;
  entries: IssueHistoryEntry[];
}

// Summary
export interface IssueSummary {
  total_open: number;
  total_in_progress: number;
  total_resolved: number;
  total_closed: number;
  total_deferred: number;
  by_classification: Record<IssueClassification, number>;
  by_criticality: Record<IssueCriticality, number>;
  opportunities_identified: number;
  opportunities_delivered: number;
  overdue_count: number;
  due_this_week: number;
}

// Heatmap
export interface HeatmapCell {
  process_id: string;
  process_ref: string;
  process_name: string;
  level: string;
  parent_id?: string;
  people_count: number;
  process_count: number;
  system_count: number;
  data_count: number;
  total_issues: number;
  people_colour: RAGStatusExtended;
  process_colour: RAGStatusExtended;
  system_colour: RAGStatusExtended;
  data_colour: RAGStatusExtended;
  overall_colour: RAGStatusExtended;
}

export interface HeatmapResponse {
  cells: HeatmapCell[];
  rollup: boolean;
}

// Export request
export interface IssueExportRequest {
  format: "csv" | "xlsx";
  status_filter?: IssueStatus[];
  classification_filter?: IssueClassification[];
  criticality_filter?: IssueCriticality[];
  process_ids?: string[];
  date_from?: string;
  date_to?: string;
}

// RAG Assessment types
export interface RAGAssessmentRequest {
  dimension: IssueClassification;
  status: RAGStatusExtended;
  notes?: string;
}

export interface RAGAssessmentResponse {
  process_id: string;
  process_code: string;
  dimension: IssueClassification;
  old_status: RAGStatusExtended;
  new_status: RAGStatusExtended;
  rag_overall: RAGStatusExtended;
  assessed_by: string;
  assessed_at: string;
}

export interface RAGConflictError {
  error: string;
  dimension: IssueClassification;
  open_issue_count: number;
  open_issue_ids: string[];
}

export interface RAGHistoryEntry {
  timestamp: string;
  dimension: string;
  old_status?: RAGStatusExtended;
  new_status: RAGStatusExtended;
  source: "issue_sync" | "explicit_assessment";
  notes?: string;
  changed_by?: string;
}

export interface RAGHistory {
  process_id: string;
  process_code: string;
  entries: RAGHistoryEntry[];
}

export interface RAGSummaryItem {
  status: RAGStatusExtended;
  count: number;
}

export interface RAGSummary {
  overall_distribution: RAGSummaryItem[];
  by_dimension: Record<IssueClassification, RAGSummaryItem[]>;
  total_processes: number;
  processes_with_issues: number;
}
