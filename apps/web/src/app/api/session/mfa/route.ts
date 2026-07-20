import { NextResponse } from "next/server";
import { z } from "zod";

import { backendUrl, jsonError, setSessionCookies } from "@/lib/server/backend";
import type { ApiResponse, TokenResponse } from "@/types/api";

const schema = z.object({ email: z.email(), otp: z.string().regex(/^\d{6}$/) });

export async function POST(request: Request) {
  const tenantId = process.env.ERP_TENANT_ID;
  if (!tenantId) return jsonError("ERP_TENANT_ID is not configured.", 503);
  const parsed = schema.safeParse(await request.json().catch(() => null));
  if (!parsed.success)
    return jsonError("Enter the six-digit verification code.", 422);
  try {
    const upstream = await fetch(backendUrl("auth/mfa/verify"), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ tenant_id: tenantId, ...parsed.data }),
      cache: "no-store",
    });
    const payload = (await upstream.json()) as ApiResponse<TokenResponse>;
    const response = NextResponse.json(payload, { status: upstream.status });
    if (upstream.ok && payload.data) setSessionCookies(response, payload.data);
    return response;
  } catch {
    return jsonError("Finance API is unavailable.", 502);
  }
}
