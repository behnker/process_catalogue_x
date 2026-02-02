"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type {
  BusinessModel,
  BusinessModelEntry,
  BusinessModelCreate,
  BusinessModelEntryCreate,
  BMCComponent,
} from "@/types/api";

const QUERY_KEY = "business-models";

// API Response type - the backend returns entries grouped by component
interface BusinessModelWithEntries extends Omit<BusinessModel, 'entries'> {
  entries_by_component: Record<BMCComponent, BusinessModelEntry[]>;
}

// Fetch the organization's business model canvas (single object, not paginated)
export function useBusinessModelCanvas() {
  return useQuery({
    queryKey: [QUERY_KEY, "canvas"],
    queryFn: () => api.get<BusinessModelWithEntries>("/api/v1/business-model/canvas"),
  });
}

// Legacy alias for backward compatibility
export function useBusinessModels() {
  return useBusinessModelCanvas();
}

export function useBusinessModel(id: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => api.get<BusinessModelWithEntries>(`/api/v1/business-model/canvas/${id}`),
    enabled: !!id,
  });
}

export function useBusinessModelWithEntries(id: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, id, "entries"],
    queryFn: () => api.get<BusinessModelWithEntries>(`/api/v1/business-model/canvas/${id}?include_entries=true`),
    enabled: !!id,
  });
}

export function useCreateBusinessModel() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: BusinessModelCreate) =>
      api.post<BusinessModel>("/api/v1/business-model/canvas", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}

export function useUpdateBusinessModel() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<BusinessModelCreate> }) =>
      api.patch<BusinessModel>(`/api/v1/business-model/canvas/${id}`, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY, id] });
    },
  });
}

export function useDeleteBusinessModel() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/business-model/canvas/${id}`),
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
      api.post<BusinessModelEntry>("/api/v1/business-model/entries", data),
    onSuccess: () => {
      // Invalidate all business model queries to refresh the canvas
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
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
    }) => api.patch<BusinessModelEntry>(`/api/v1/business-model/entries/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}

export function useDeleteBusinessModelEntry() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/business-model/entries/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}
