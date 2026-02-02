/**
 * API client with automatic auth header injection.
 * Wraps fetch with token refresh and error handling.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
  private getToken(): string | null {
    if (typeof window === "undefined") return null;
    try {
      const stored = localStorage.getItem("pc-auth");
      if (stored) {
        const parsed = JSON.parse(stored);
        return parsed.state?.accessToken || null;
      }
    } catch {
      return null;
    }
    return null;
  }

  // Normalize path to include trailing slash for FastAPI compatibility
  // This prevents 307 redirects which don't work with POST/PATCH/DELETE
  private normalizePath(path: string): string {
    // Don't add slash if path has query params or already ends with slash
    if (path.includes("?") || path.endsWith("/")) {
      return path;
    }
    return `${path}/`;
  }

  private async request<T>(
    path: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getToken();
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    };

    // Normalize path for mutating methods to avoid 307 redirects
    const method = options.method || "GET";
    const normalizedPath = ["POST", "PATCH", "PUT", "DELETE"].includes(method)
      ? this.normalizePath(path)
      : path;

    const res = await fetch(`${API_URL}${normalizedPath}`, {
      ...options,
      headers,
    });

    if (res.status === 401) {
      // Token expired — redirect to login
      if (typeof window !== "undefined") {
        window.location.href = "/auth/login";
      }
      throw new Error("Unauthorized");
    }

    if (res.status === 204) {
      return undefined as T;
    }

    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: "Request failed" }));
      // Handle FastAPI validation errors (detail is an array of error objects)
      let message: string;
      if (Array.isArray(error.detail)) {
        message = error.detail
          .map((e: { loc?: string[]; msg?: string }) => {
            const field = e.loc?.slice(1).join(".") || "unknown";
            return `${field}: ${e.msg || "validation error"}`;
          })
          .join(", ");
      } else if (typeof error.detail === "string") {
        message = error.detail;
      } else {
        message = `HTTP ${res.status}`;
      }
      throw new Error(message);
    }

    return res.json();
  }

  get<T>(path: string) {
    return this.request<T>(path);
  }

  post<T>(path: string, body?: unknown) {
    return this.request<T>(path, {
      method: "POST",
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  patch<T>(path: string, body: unknown) {
    return this.request<T>(path, {
      method: "PATCH",
      body: JSON.stringify(body),
    });
  }

  delete(path: string) {
    return this.request(path, { method: "DELETE" });
  }
}

export const api = new ApiClient();
