"use client";

import type { ReactNode } from "react";
import type { BpmPermission } from "@/modules/bpm/types/bpm";

/** Phase 1: permission gate — pass granted set from session when available. */
export function can(granted: string[] | undefined, permission: BpmPermission): boolean {
  if (!granted || granted.length === 0) return true; // optimistic until session wired
  return granted.includes(permission);
}

export function PermissionGate({
  permission,
  granted,
  children,
  fallback = null,
}: {
  permission: BpmPermission;
  granted?: string[];
  children: ReactNode;
  fallback?: ReactNode;
}) {
  if (!can(granted, permission)) return <>{fallback}</>;
  return <>{children}</>;
}
