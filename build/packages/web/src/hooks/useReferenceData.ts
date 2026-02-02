"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";

const QUERY_KEY = "reference";

export type CatalogueType =
  | "departments"
  | "functions"
  | "roles"
  | "systems"
  | "clients"
  | "markets"
  | "categories"
  | "partners"
  | "suppliers"
  | "tags";

export interface ReferenceItem {
  id: string;
  catalogue_type: CatalogueType;
  code: string;
  name: string;
  description?: string;
  status: string;
  sort_order: number;
  parent_id?: string;
  created_at: string;
  updated_at: string;
}

export interface ReferenceItemCreate {
  catalogue_type: CatalogueType;
  code: string;
  name: string;
  description?: string;
  parent_id?: string;
  sort_order?: number;
}

export interface ReferenceItemUpdate {
  code?: string;
  name?: string;
  description?: string;
  status?: string;
  parent_id?: string;
  sort_order?: number;
}

export interface ReferenceListResponse {
  items: ReferenceItem[];
  total: number;
}

export interface ReferenceFilters {
  catalogue_type?: CatalogueType;
  status?: string;
  search?: string;
}

function buildQueryString(filters: ReferenceFilters): string {
  const params = new URLSearchParams();
  if (filters.catalogue_type) params.set("catalogue_type", filters.catalogue_type);
  if (filters.status) params.set("status", filters.status);
  if (filters.search) params.set("search", filters.search);
  return params.toString();
}

export function useReferenceData(filters: ReferenceFilters = {}) {
  return useQuery({
    queryKey: [QUERY_KEY, filters],
    queryFn: () => {
      const queryString = buildQueryString(filters);
      const url = queryString ? `/api/v1/reference?${queryString}` : "/api/v1/reference";
      return api.get<ReferenceListResponse>(url);
    },
  });
}

export function useReferenceItem(id: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => api.get<ReferenceItem>(`/api/v1/reference/${id}`),
    enabled: !!id,
  });
}

export function useCreateReferenceItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ReferenceItemCreate) =>
      api.post<ReferenceItem>("/api/v1/reference", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}

export function useUpdateReferenceItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: ReferenceItemUpdate }) =>
      api.patch<ReferenceItem>(`/api/v1/reference/${id}`, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY, id] });
    },
  });
}

export function useDeleteReferenceItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.delete(`/api/v1/reference/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEY] });
    },
  });
}
