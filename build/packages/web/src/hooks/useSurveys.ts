"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type {
  PaginatedResponse,
  Survey,
  SurveyQuestion,
  SurveyResponseItem,
  SurveyCreate,
  SurveyQuestionCreate,
  SurveyFilters,
} from "@/types/api";

const QUERY_KEY = "surveys";

// Build query string from filters
function buildQueryString(filters?: SurveyFilters): string {
  if (!filters) return "";
  const params = new URLSearchParams();
  if (filters.mode) params.set("mode", filters.mode);
  if (filters.status) params.set("status", filters.status);
  if (filters.search) params.set("search", filters.search);
  if (filters.page) params.set("page", String(filters.page));
  if (filters.per_page) params.set("per_page", String(filters.per_page));
  const qs = params.toString();
  return qs ? `?${qs}` : "";
}

export function useSurveys(filters?: SurveyFilters) {
  return useQuery({
    queryKey: [QUERY_KEY, filters],
    queryFn: () =>
      api.get<PaginatedResponse<Survey>>(
        `/api/v1/surveys/${buildQueryString(filters)}`
      ),
  });
}

export function useSurvey(id: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => api.get<Survey>(`/api/v1/surveys/${id}`),
    enabled: !!id,
  });
}

export function useSurveyWithQuestions(id: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, id, "questions"],
    queryFn: async () => {
      const [survey, questionsRes] = await Promise.all([
        api.get<Survey>(`/api/v1/surveys/${id}`),
        api.get<PaginatedResponse<SurveyQuestion>>(
          `/api/v1/surveys/${id}/questions`
        ),
      ]);
      return { ...survey, questions: questionsRes.items };
    },
    enabled: !!id,
  });
}

export function useCreateSurvey() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: SurveyCreate) =>
      api.post<Survey>("/api/v1/surveys/", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}

export function useUpdateSurvey() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<SurveyCreate> }) =>
      api.patch<Survey>(`/api/v1/surveys/${id}`, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY, id] });
    },
  });
}

export function useDeleteSurvey() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/surveys/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}

// Questions
export function useSurveyQuestions(surveyId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, surveyId, "questions"],
    queryFn: () =>
      api.get<PaginatedResponse<SurveyQuestion>>(
        `/api/v1/surveys/${surveyId}/questions`
      ),
    enabled: !!surveyId,
  });
}

export function useCreateSurveyQuestion() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      surveyId,
      data,
    }: {
      surveyId: string;
      data: SurveyQuestionCreate;
    }) =>
      api.post<SurveyQuestion>(`/api/v1/surveys/${surveyId}/questions`, data),
    onSuccess: (_, { surveyId }) => {
      queryClient.invalidateQueries({
        queryKey: [QUERY_KEY, surveyId, "questions"],
      });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY, surveyId] });
    },
  });
}

export function useUpdateSurveyQuestion() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      surveyId,
      questionId,
      data,
    }: {
      surveyId: string;
      questionId: string;
      data: Partial<SurveyQuestionCreate>;
    }) =>
      api.patch<SurveyQuestion>(
        `/api/v1/surveys/${surveyId}/questions/${questionId}`,
        data
      ),
    onSuccess: (_, { surveyId }) => {
      queryClient.invalidateQueries({
        queryKey: [QUERY_KEY, surveyId, "questions"],
      });
    },
  });
}

export function useDeleteSurveyQuestion() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      surveyId,
      questionId,
    }: {
      surveyId: string;
      questionId: string;
    }) => api.delete(`/api/v1/surveys/${surveyId}/questions/${questionId}`),
    onSuccess: (_, { surveyId }) => {
      queryClient.invalidateQueries({
        queryKey: [QUERY_KEY, surveyId, "questions"],
      });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY, surveyId] });
    },
  });
}

// Responses
export function useSurveyResponses(surveyId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, surveyId, "responses"],
    queryFn: () =>
      api.get<PaginatedResponse<SurveyResponseItem>>(
        `/api/v1/surveys/${surveyId}/responses`
      ),
    enabled: !!surveyId,
  });
}
