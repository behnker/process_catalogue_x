"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type {
  RAGAssessmentRequest,
  RAGAssessmentResponse,
  RAGHistory,
  RAGSummary,
} from "@/types/issue.types";

const QUERY_KEY = "rag-assessment";

// Set explicit RAG assessment for a process dimension
export function useSetRAGAssessment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      processId,
      data,
    }: {
      processId: string;
      data: RAGAssessmentRequest;
    }) => api.post<RAGAssessmentResponse>(`/api/v1/processes/${processId}/rag-assessment`, data),
    onSuccess: (_, { processId }) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY, "history", processId] });
      queryClient.invalidateQueries({ queryKey: ["processes"] });
      queryClient.invalidateQueries({ queryKey: ["issues", "heatmap"] });
    },
  });
}

// Get RAG history for a process
export function useRAGHistory(processId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, "history", processId],
    queryFn: () => api.get<RAGHistory>(`/api/v1/processes/${processId}/rag-history`),
    enabled: !!processId,
  });
}

// Get org-wide RAG summary
export function useRAGSummary() {
  return useQuery({
    queryKey: [QUERY_KEY, "summary"],
    queryFn: () => api.get<RAGSummary>("/api/v1/processes/rag-summary"),
  });
}

// Admin: recalculate RAG statuses
export function useRecalculateRAG() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (processIds?: string[]) =>
      api.post<{ processes_updated: number; errors: string[] }>(
        "/api/v1/processes/rag-recalculate",
        { process_ids: processIds }
      ),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      queryClient.invalidateQueries({ queryKey: ["processes"] });
      queryClient.invalidateQueries({ queryKey: ["issues", "heatmap"] });
    },
  });
}
