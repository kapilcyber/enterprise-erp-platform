import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import {
  ACCESS_COOKIE,
  backendUrl,
  clearSessionCookies,
} from "@/lib/server/backend";

export async function POST() {
  const token = (await cookies()).get(ACCESS_COOKIE)?.value;
  if (token) {
    await fetch(backendUrl("auth/logout"), {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, Accept: "application/json" },
      cache: "no-store",
    }).catch(() => null);
  }
  const response = NextResponse.json({
    success: true,
    message: "Logged out",
    data: null,
  });
  clearSessionCookies(response);
  return response;
}
