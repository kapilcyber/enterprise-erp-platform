import type { ApiResponse, ErrorResponse } from "@/types/api";

export class ApiClientError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly errors: string[] = [],
  ) {
    super(message);
    this.name = "ApiClientError";
  }
}

type RequestOptions = Omit<RequestInit, "body"> & { body?: unknown };

export async function apiClient<T>(
  path: string,
  options: RequestOptions = {},
): Promise<ApiResponse<T>> {
  const { body, headers, ...rest } = options;
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  const response = await fetch(`/api/erp${normalizedPath}`, {
    ...rest,
    credentials: "same-origin",
    headers: {
      Accept: "application/json",
      ...(body !== undefined ? { "Content-Type": "application/json" } : {}),
      ...headers,
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
    cache: "no-store",
  });

  const payload = (await response.json().catch(() => ({
    success: false,
    message: "The server returned an unreadable response.",
    errors: [],
  }))) as ApiResponse<T> | ErrorResponse;

  if (!response.ok || payload.success === false) {
    const errorPayload = payload as ErrorResponse;
    if (response.status === 401 && typeof window !== "undefined") {
      window.dispatchEvent(new Event("erp:unauthorized"));
    }
    throw new ApiClientError(
      errorPayload.message ?? "API request failed",
      response.status,
      errorPayload.errors ?? [],
    );
  }
  return payload as ApiResponse<T>;
}

export async function sessionRequest<T>(
  path: string,
  body?: unknown,
): Promise<T> {
  const response = await fetch(`/api/session/${path}`, {
    method: body === undefined ? "GET" : "POST",
    credentials: "same-origin",
    headers:
      body === undefined
        ? { Accept: "application/json" }
        : {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
    body: body === undefined ? undefined : JSON.stringify(body),
    cache: "no-store",
  });
  const payload = await response
    .json()
    .catch(() => ({ message: "Unable to contact server" }));
  if (!response.ok) {
    throw new ApiClientError(
      payload.message ?? "Request failed",
      response.status,
      payload.errors ?? [],
    );
  }
  return payload as T;
}

export const healthService = {
  check: () => apiClient<Record<string, string>>("/health"),
};
