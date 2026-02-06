"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type { ProcessSystemsResponse } from "@/types/api";

export function useProcessSystems(processId: string | undefined) {
  return useQuery({
    queryKey: ["process-systems", processId],
    queryFn: () =>
      api.get<ProcessSystemsResponse>(
        `/api/v1/processes/${processId}/systems`
      ),
    enabled: !!processId,
  });
}
