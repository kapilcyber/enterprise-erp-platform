"use client";

import { createContext, useCallback, useContext, useEffect, useMemo } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { usePathname, useRouter } from "next/navigation";
import { sessionRequest } from "@/services/api-client";
import type { ApiResponse, SessionData, TokenResponse } from "@/types/api";

type AuthValue = {
  session: SessionData | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<TokenResponse>;
  verifyMfa: (email: string, otp: string) => Promise<void>;
  logout: () => Promise<void>;
  refresh: () => Promise<void>;
  can: (permission: string) => boolean;
};

const AuthContext = createContext<AuthValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const client = useQueryClient();
  const router = useRouter();
  const pathname = usePathname();
  const sessionQuery = useQuery({
    queryKey: ["session"],
    queryFn: async () => (await sessionRequest<ApiResponse<SessionData>>("me")).data,
    retry: false,
    staleTime: 30_000,
  });
  const session = sessionQuery.data ?? null;
  const loading = sessionQuery.isPending;

  const refresh = useCallback(async () => {
    await sessionQuery.refetch();
  }, [sessionQuery]);

  useEffect(() => {
    const handler = () => {
      client.setQueryData(["session"], null);
      router.replace("/login");
    };
    window.addEventListener("erp:unauthorized", handler);
    return () => window.removeEventListener("erp:unauthorized", handler);
  }, [client, router]);

  useEffect(() => {
    if (!loading && !session && pathname !== "/login") router.replace("/login");
    if (!loading && session && pathname === "/login") router.replace("/finance");
  }, [loading, session, pathname, router]);

  const login = useCallback(async (email: string, password: string) => {
    const payload = await sessionRequest<ApiResponse<TokenResponse>>("login", { email, password });
    if (!payload.data) throw new Error(payload.message);
    if (!payload.data.mfa_required) await client.invalidateQueries({ queryKey: ["session"] });
    return payload.data;
  }, [client]);

  const verifyMfa = useCallback(async (email: string, otp: string) => {
    await sessionRequest("mfa", { email, otp });
    await client.invalidateQueries({ queryKey: ["session"] });
  }, [client]);

  const logout = useCallback(async () => {
    await sessionRequest("logout", {}).catch(() => null);
    client.setQueryData(["session"], null);
    router.replace("/login");
  }, [client, router]);

  const value = useMemo<AuthValue>(() => ({
    session, loading, login, verifyMfa, logout, refresh,
    can: (permission) => session?.permissions.includes(permission) ?? false,
  }), [session, loading, login, verifyMfa, logout, refresh]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error("useAuth must be used within AuthProvider");
  return value;
}
