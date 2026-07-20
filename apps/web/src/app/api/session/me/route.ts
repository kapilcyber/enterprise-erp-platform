import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import {
  ACCESS_COOKIE,
  backendUrl,
  clearSessionCookies,
  jsonError,
  refreshSession,
  setSessionCookies,
} from "@/lib/server/backend";

export async function GET() {
  const store = await cookies();
  let token = store.get(ACCESS_COOKIE)?.value;
  let upstream = token
    ? await fetch(backendUrl("auth/me"), {
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "application/json",
        },
        cache: "no-store",
      }).catch(() => null)
    : null;
  let refreshed = null;
  if (!upstream || upstream.status === 401) {
    refreshed = await refreshSession();
    token = refreshed?.access_token ?? undefined;
    if (token)
      upstream = await fetch(backendUrl("auth/me"), {
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "application/json",
        },
        cache: "no-store",
      }).catch(() => null);
  }
  if (!upstream) return jsonError("Finance API is unavailable.", 502);
  const response = new NextResponse(await upstream.text(), {
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
