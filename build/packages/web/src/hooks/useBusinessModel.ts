"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type {
  PaginatedResponse,
  BusinessModel,
  BusinessModelEntry,
  BusinessModelCreate,
  BusinessModelEntryCreate,
} from "@/types/api";

const QUERY_KEY = "business-models";

export function useBusinessModels() {
  return useQuery({
    queryKey: [QUERY_KEY],
    queryFn: () => api.get<PaginatedResponse<BusinessModel>>("/api/v1/business-models"),
  });
}

export function useBusinessModel(id: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => api.get<BusinessModel>(`/api/v1/business-models/${id}`),
    enabled: !!id,
  });
}

export function useBusinessModelWithEntries(id: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, id, "entries"],
    queryFn: () => api.get<BusinessModel>(`/api/v1/business-models/${id}?include_entries=true`),
    enabled: !!id,
  });
}

export function useCreateBusinessModel() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: BusinessModelCreate) =>
      api.post<BusinessModel>("/api/v1/business-models", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}

export function useUpdateBusinessModel() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<BusinessModelCreate> }) =>
      api.patch<BusinessModel>(`/api/v1/business-models/${id}`, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY, id] });
    },
  });
}

export function useDeleteBusinessModel() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/business-models/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}

// Entries
export function useCreateBusinessModelEntry() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: BusinessModelEntryCreate) =>
      api.post<BusinessModelEntry>("/api/v1/business-model-entries", data),
    onSuccess: (_, { business_model_id }) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY, business_model_id] });
    },
  });
}

export function useUpdateBusinessModelEntry() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: string;
      data: Partial<BusinessModelEntryCreate>;
    }) => api.patch<BusinessModelEntry>(`/api/v1/business-model-entries/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}

export function useDeleteBusinessModelEntry() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/business-model-entries/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}
