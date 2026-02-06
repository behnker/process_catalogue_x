"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type {
  OperatingModelComponent,
  OperatingModelSummary,
} from "@/types/api";

const QUERY_KEY = "operating-model";

export function useOperatingModel(processId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, processId],
    queryFn: () =>
      api.get<OperatingModelComponent[]>(
        `/api/v1/processes/${processId}/operating-model`
      ),
    enabled: !!processId,
  });
}

export function useOperatingModelSummary(processId: string | undefined) {
  return useQuery({
    queryKey: [QUERY_KEY, "summary", processId],
    queryFn: () =>
      api.get<OperatingModelSummary>(
        `/api/v1/processes/${processId}/operating-model/summary`
      ),
    enabled: !!processId,
  });
}
