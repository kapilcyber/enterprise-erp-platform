"use client";
import { useState } from "react";
import {
  ArrowRight,
  Building2,
  CheckCircle2,
  KeyRound,
  Landmark,
  Loader2,
  ShieldCheck,
} from "lucide-react";
import { useAuth } from "@/components/auth/auth-provider";
import { Button } from "@/components/ui/button";
import { loginSchema } from "@/lib/validation";

export default function LoginPage() {
  const { login, verifyMfa, loading, session } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [mfa, setMfa] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  if (loading || session)
    return (
      <div className="grid min-h-screen place-items-center">
        <Loader2 className="animate-spin text-primary" />
      </div>
    );
  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      if (mfa) {
        await verifyMfa(email, otp);
      } else {
        const parsed = loginSchema.safeParse({ email, password });
        if (!parsed.success) throw new Error(parsed.error.issues[0]?.message);
        const result = await login(email, password);
        setMfa(result.mfa_required);
      }
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Sign in failed");
    } finally {
      setBusy(false);
    }
  }
  return (
    <main className="grid min-h-screen bg-[#0d263b] lg:grid-cols-[1.05fr_.95fr]">
      <section className="relative hidden overflow-hidden p-12 text-white lg:flex lg:flex-col lg:justify-between">
        <div className="absolute inset-0 opacity-20 [background-image:radial-gradient(circle_at_20%_20%,#31b6b7_0,transparent_38%),radial-gradient(circle_at_80%_70%,#2f6f9f_0,transparent_35%)]" />
        <div className="relative flex items-center gap-3">
          <span className="grid size-11 place-items-center rounded-xl bg-[#0f8b8d]">
            <Landmark />
          </span>
          <div>
            <p className="font-semibold">Enterprise ERP</p>
            <p className="text-sm text-slate-300">Finance Control Center</p>
          </div>
        </div>
        <div className="relative max-w-xl">
          <p className="mb-5 text-sm font-semibold uppercase tracking-[.2em] text-[#7dd6d4]">
            Financial operations, under control
          </p>
          <h1 className="text-5xl font-semibold leading-tight tracking-tight">
            One trusted workspace for every accounting decision.
          </h1>
          <p className="mt-6 max-w-lg text-lg leading-8 text-slate-300">
            Close periods confidently, govern journals, and keep every ledger
            movement traceable.
          </p>
          <div className="mt-10 grid gap-4 sm:grid-cols-3">
            {[
              [ShieldCheck, "Role-secured"],
              [CheckCircle2, "Audit-ready"],
              [Building2, "Company-scoped"],
            ].map(([Icon, label]) => (
              <div
                key={String(label)}
                className="flex items-center gap-2 text-sm text-slate-200"
              >
                <Icon className="size-4 text-[#7dd6d4]" />
                {label as string}
              </div>
            ))}
          </div>
        </div>
        <p className="relative text-xs text-slate-400">
          Finance Phase 1 · Double-entry accounting · Secure workflow
        </p>
      </section>
      <section className="flex items-center justify-center bg-background px-6 py-12">
        <div className="w-full max-w-md">
          <div className="mb-8 lg:hidden">
            <div className="mb-3 flex items-center gap-2 text-primary">
              <Landmark />
              <span className="font-semibold">Finance Control Center</span>
            </div>
          </div>
          <div className="panel p-7 sm:p-9">
            <div className="mb-7">
              <p className="eyebrow text-[#0f8b8d]">Secure access</p>
              <h2 className="mt-2 text-2xl font-semibold">
                {mfa ? "Verify your identity" : "Welcome back"}
              </h2>
              <p className="mt-2 text-sm text-muted-foreground">
                {mfa
                  ? "Enter the six-digit code from your authenticator."
                  : "Sign in with your enterprise Finance account."}
              </p>
            </div>
            <form onSubmit={submit} className="space-y-5">
              {!mfa ? (
                <>
                  <label className="field">
                    <span className="field-label">Email address</span>
                    <input
                      className="control"
                      type="email"
                      autoComplete="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="finance@company.com"
                    />
                  </label>
                  <label className="field">
                    <span className="field-label">Password</span>
                    <input
                      className="control"
                      type="password"
                      autoComplete="current-password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••"
                    />
                  </label>
                </>
              ) : (
                <label className="field">
                  <span className="field-label">Verification code</span>
                  <div className="relative">
                    <KeyRound className="absolute left-3 top-2.5 size-4 text-muted-foreground" />
                    <input
                      className="control pl-9 font-mono tracking-[.35em]"
                      inputMode="numeric"
                      maxLength={6}
                      value={otp}
                      onChange={(e) =>
                        setOtp(e.target.value.replace(/\D/g, ""))
                      }
                      placeholder="000000"
                    />
                  </div>
                </label>
              )}
              {error && (
                <div
                  role="alert"
                  className="rounded-lg border border-destructive/25 bg-destructive/10 px-3 py-2 text-sm text-destructive"
                >
                  {error}
                </div>
              )}
              <Button
                className="h-10 w-full bg-[#0f8b8d] hover:bg-[#0b7476]"
                disabled={busy}
              >
                {busy ? (
                  <Loader2 className="animate-spin" />
                ) : (
                  <>
                    {mfa ? "Verify and continue" : "Sign in"}
                    <ArrowRight />
                  </>
                )}
              </Button>
            </form>
          </div>
          <p className="mt-5 text-center text-xs text-muted-foreground">
            Protected by encrypted, HttpOnly session cookies.
          </p>
        </div>
      </section>
    </main>
  );
}
