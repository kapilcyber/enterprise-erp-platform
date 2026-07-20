import { cookies } from "next/headers";
import { type NextRequest, NextResponse } from "next/server";

import {
  ACCESS_COOKIE,
  backendUrl,
  clearSessionCookies,
  jsonError,
  refreshSession,
  setSessionCookies,
} from "@/lib/server/backend";

const allowed = [
  "finance/",
  "auth/context",
  "customers",
  "vendors",
  "currencies",
  "taxes",
  "assets",
  "companies",
  "branches",
  "cost-centers",
  "profit-centers",
];

function allowedPath(path: string) {
  return allowed.some(
    (prefix) => path === prefix.replace(/\/$/, "") || path.startsWith(prefix),
  );
}

async function proxy(
  request: NextRequest,
  context: { params: Promise<{ path: string[] }> },
) {
  const { path: parts } = await context.params;
  const path = parts.join("/");
  if (!allowedPath(path))
    return jsonError(
      "Route is not available through the Finance gateway.",
      404,
    );
  if (!["GET", "HEAD"].includes(request.method)) {
    const origin = request.headers.get("origin");
    if (origin && origin !== request.nextUrl.origin)
      return jsonError("Cross-site request blocked.", 403);
  }

  const store = await cookies();
  let token = store.get(ACCESS_COOKIE)?.value;
  if (!token) return jsonError("Authentication required.", 401);
  const body = ["GET", "HEAD"].includes(request.method)
    ? undefined
    : await request.arrayBuffer();
  const target = `${backendUrl(path)}${request.nextUrl.search}`;
  const call = (access: string) =>
    fetch(target, {
      method: request.method,
      headers: {
        Authorization: `Bearer ${access}`,
        Accept: request.headers.get("accept") ?? "application/json",
        ...(request.headers.get("content-type")
          ? { "Content-Type": request.headers.get("content-type")! }
          : {}),
      },
      body,
      cache: "no-store",
    });

  let upstream = await call(token).catch(() => null);
  let refreshed = null;
  if (upstream?.status === 401) {
    refreshed = await refreshSession();
    token = refreshed?.access_token ?? undefined;
    if (token) upstream = await call(token).catch(() => null);
  }
  if (!upstream) return jsonError("Finance API is unavailable.", 502);
  const response = new NextResponse(await upstream.arrayBuffer(), {
    status: upstream.status,
    headers: {
      "Content-Type":
        upstream.headers.get("content-type") ?? "application/json",
    },
  });
  if (refreshed) setSessionCookies(response, refreshed);
  if (upstream.status === 401) clearSessionCookies(response);
  return response;
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const PATCH = proxy;
export const DELETE = proxy;
