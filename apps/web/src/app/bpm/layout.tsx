import Link from "next/link";
import type { ReactNode } from "react";

import { AppShell } from "@/components/layout/app-shell";

const NAV = [
  { href: "/bpm", label: "Overview" },
  { href: "/bpm/categories", label: "Categories" },
  { href: "/bpm/templates", label: "Templates" },
  { href: "/bpm/definitions", label: "Definitions" },
];

export default function BpmLayout({ children }: { children: ReactNode }) {
  return (
    <AppShell subtitle="Workflow & BPM Designer — Phase 1">
      <nav className="mb-6 flex flex-wrap gap-4 border-b border-border pb-3 text-sm">
        {NAV.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="text-muted-foreground transition-colors hover:text-foreground"
          >
            {item.label}
          </Link>
        ))}
      </nav>
      {children}
    </AppShell>
  );
}
