"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type {
  PaginatedResponse,
  PromptTemplate,
  PromptTemplateCreate,
  PromptExecution,
  PromptExecutionRequest,
  LLMConfig,
  PromptFilters,
} from "@/types/api";

const TEMPLATES_KEY = "prompt-templates";
const EXECUTIONS_KEY = "prompt-executions";
const LLM_CONFIG_KEY = "llm-config";

// Build query string from filters
function buildQueryString(filters?: PromptFilters): string {
  if (!filters) return "";
  const params = new URLSearchParams();
  if (filters.category) params.set("category", filters.category);
  if (filters.context_type) params.set("context_type", filters.context_type);
  if (filters.search) params.set("search", filters.search);
  if (filters.page) params.set("page", String(filters.page));
  if (filters.per_page) params.set("per_page", String(filters.per_page));
  const qs = params.toString();
  return qs ? `?${qs}` : "";
}

// Templates
export function usePromptTemplates(filters?: PromptFilters) {
  return useQuery({
    queryKey: [TEMPLATES_KEY, filters],
    queryFn: () =>
      api.get<PaginatedResponse<PromptTemplate>>(
        `/api/v1/prompts/templates${buildQueryString(filters)}`
      ),
  });
}

export function usePromptTemplate(id: string | undefined) {
  return useQuery({
    queryKey: [TEMPLATES_KEY, id],
    queryFn: () => api.get<PromptTemplate>(`/api/v1/prompts/templates/${id}`),
    enabled: !!id,
  });
}

export function useCreatePromptTemplate() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: PromptTemplateCreate) =>
      api.post<PromptTemplate>("/api/v1/prompts/templates", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [TEMPLATES_KEY] });
    },
  });
}

export function useUpdatePromptTemplate() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: string;
      data: Partial<PromptTemplateCreate>;
    }) => api.patch<PromptTemplate>(`/api/v1/prompts/templates/${id}`, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: [TEMPLATES_KEY] });
      queryClient.invalidateQueries({ queryKey: [TEMPLATES_KEY, id] });
    },
  });
}

export function useDeletePromptTemplate() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/prompts/templates/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [TEMPLATES_KEY] });
    },
  });
}

// Executions
export function usePromptExecutions(limit: number = 20) {
  return useQuery({
    queryKey: [EXECUTIONS_KEY, limit],
    queryFn: () =>
      api.get<PaginatedResponse<PromptExecution>>(
        `/api/v1/prompts/executions?per_page=${limit}`
      ),
  });
}

export function useExecutePrompt() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: PromptExecutionRequest) =>
      api.post<PromptExecution>("/api/v1/prompts/execute", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [EXECUTIONS_KEY] });
      queryClient.invalidateQueries({ queryKey: [TEMPLATES_KEY] }); // Update usage counts
    },
  });
}

// LLM Configuration
export function useLLMConfigs() {
  return useQuery({
    queryKey: [LLM_CONFIG_KEY],
    queryFn: () =>
      api.get<PaginatedResponse<LLMConfig>>("/api/v1/prompts/llm-config"),
  });
}

export function useUpdateLLMConfig() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: string;
      data: Partial<LLMConfig>;
    }) => api.patch<LLMConfig>(`/api/v1/prompts/llm-config/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [LLM_CONFIG_KEY] });
    },
  });
}
