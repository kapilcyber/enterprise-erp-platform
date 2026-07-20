import "server-only";

import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import type { ApiResponse, TokenResponse } from "@/types/api";

export const ACCESS_COOKIE = "erp_access";
export const REFRESH_COOKIE = "erp_refresh";

export function backendUrl(path: string): string {
  const base =
    process.env.ERP_API_URL ??
    process.env.NEXT_PUBLIC_API_URL ??
    "http://localhost:8000/api/v1";
  return `${base.replace(/\/$/, "")}/${path.replace(/^\//, "")}`;
}

const cookieOptions = {
  httpOnly: true,
  sameSite: "lax" as const,
  secure: process.env.NODE_ENV === "production",
  path: "/",
  priority: "high" as const,
};

export function setSessionCookies(
  response: NextResponse,
  tokens: TokenResponse,
): void {
  if (tokens.access_token) {
    response.cookies.set(ACCESS_COOKIE, tokens.access_token, {
      ...cookieOptions,
      maxAge: 15 * 60,
    });
  }
  if (tokens.refresh_token) {
    response.cookies.set(REFRESH_COOKIE, tokens.refresh_token, {
      ...cookieOptions,
      maxAge: 7 * 24 * 60 * 60,
    });
  }
}

export function clearSessionCookies(response: NextResponse): void {
  response.cookies.set(ACCESS_COOKIE, "", { ...cookieOptions, maxAge: 0 });
  response.cookies.set(REFRESH_COOKIE, "", { ...cookieOptions, maxAge: 0 });
}

export async function refreshSession(): Promise<TokenResponse | null> {
  const store = await cookies();
  const refreshToken = store.get(REFRESH_COOKIE)?.value;
  if (!refreshToken) return null;
  const response = await fetch(backendUrl("auth/refresh"), {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ refresh_token: refreshToken }),
    cache: "no-store",
  });
  if (!response.ok) return null;
  const payload = (await response.json()) as ApiResponse<TokenResponse>;
  return payload.data ?? null;
}

export function jsonError(message: string, status = 500): NextResponse {
  return NextResponse.json({ success: false, message, errors: [] }, { status });
}
