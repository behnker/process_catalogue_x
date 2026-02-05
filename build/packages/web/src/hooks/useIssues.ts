"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type { PaginatedResponse } from "@/types/api";
import type {
  Issue,
  IssueFilters,
  IssueSummary,
  IssueHistory,
  HeatmapResponse,
} from "@/types/issue.types";

export { useCreateIssue, useUpdateIssue, useDeleteIssue, useExportIssues } from "./useIssueMutations";

const QUERY_KEY = "issues";

function buildQueryString(filters: IssueFilters): string {
  const params = new URLSearchParams();
  if (filters.page) params.set("page", filters.page.toString());
  if (filters.per_page) params.set("per_page", filters.per_page.toString());
  if (filters.status_filter) params.set("status_filter", filters.status_filter);
  if (filters.classification) params.set("classification", filters.classification);
  if (filters.criticality) params.set("criticality", filters.criticality);
  if (filters.process_id) params.set("process_id", filters.process_id);
  if (filters.assigned_to) params.set("assigned_to", filters.assigned_to);
  return params.toString();
}

export function useIssues(filters: IssueFilters = {}) {
  return useQuery({
    queryKey: [QUERY_KEY, filters],
    queryFn: () => {
      const queryString = buildQueryString(filters);
      const url = queryString ? `/api/v1/issues?${queryString}` : "/api/v1/issues";
      return api.get<PaginatedResponse<Issue>>(url);
    },
  });
}

export function useIssue(id: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => api.get<Issue>(`/api/v1/issues/${id}`),
    enabled: !!id,
  });
}

export function useProcessIssues(
  processId: string | undefined,
  options: {
    includeDescendants?: boolean;
    statusFilter?: string;
    page?: number;
    perPage?: number;
  } = {}
) {
  const { includeDescendants = false, statusFilter, page = 1, perPage = 50 } = options;

  return useQuery({
    queryKey: [QUERY_KEY, "process", processId, options],
    queryFn: () => {
      const params = new URLSearchParams();
      params.set("page", page.toString());
      params.set("per_page", perPage.toString());
      if (includeDescendants) params.set("include_descendants", "true");
      if (statusFilter) params.set("status_filter", statusFilter);
      return api.get<PaginatedResponse<Issue>>(
        `/api/v1/processes/${processId}/issues?${params.toString()}`
      );
    },
    enabled: !!processId,
  });
}

export function useIssueHistory(issueId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, "history", issueId],
    queryFn: () => api.get<IssueHistory>(`/api/v1/issues/${issueId}/history`),
    enabled: !!issueId,
  });
}

export function useIssueSummary() {
  return useQuery({
    queryKey: [QUERY_KEY, "summary"],
    queryFn: () => api.get<IssueSummary>("/api/v1/issues/summary"),
  });
}

export function useIssueHeatmap(rollup: boolean = false) {
  return useQuery({
    queryKey: [QUERY_KEY, "heatmap", { rollup }],
    queryFn: () => api.get<HeatmapResponse>(`/api/v1/issues/heatmap?rollup=${rollup}`),
  });
}
