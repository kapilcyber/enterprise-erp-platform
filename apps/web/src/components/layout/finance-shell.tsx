"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import {
  BookOpenCheck,
  Building2,
  CalendarRange,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  CircleDollarSign,
  CreditCard,
  FileBarChart,
  FileText,
  Landmark,
  LayoutDashboard,
  LogOut,
  Menu,
  Moon,
  ReceiptText,
  Scale,
  Sun,
  UsersRound,
  WalletCards,
  X,
} from "lucide-react";
import { useAuth } from "@/components/auth/auth-provider";
import {
  FinanceContextProvider,
  useFinanceContext,
} from "@/components/finance/finance-context";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { referenceLabel } from "@/lib/format";
const nav = [
  {
    label: "Overview",
    items: [
      {
        href: "/finance",
        label: "Control center",
        icon: LayoutDashboard,
        permission: "finance.journal:read",
      },
    ],
  },
  {
    label: "Accounting",
    items: [
      {
        href: "/finance/journals",
        label: "Journals",
        icon: FileText,
        permission: "finance.journal:read",
      },
      {
        href: "/finance/general-ledger",
        label: "General ledger",
        icon: BookOpenCheck,
        permission: "finance.gl:read",
      },
      {
        href: "/finance/accounts-receivable",
        label: "Accounts receivable",
        icon: UsersRound,
        permission: "finance.ar:read",
      },
      {
        href: "/finance/accounts-payable",
        label: "Accounts payable",
        icon: CreditCard,
        permission: "finance.ap:read",
      },
      {
        href: "/finance/tax-register",
        label: "Tax register",
        icon: ReceiptText,
        permission: "finance.tax:read",
      },
      {
        href: "/finance/asset-transactions",
        label: "Asset transactions",
        icon: Building2,
        permission: "finance.asset_transaction:read",
      },
    ],
  },
  {
    label: "Configuration",
    items: [
      {
        href: "/finance/chart-of-accounts",
        label: "Chart of accounts",
        icon: Scale,
        permission: "finance.coa:read",
      },
      {
        href: "/finance/fiscal-calendar",
        label: "Fiscal calendar",
        icon: CalendarRange,
        permission: "finance.fiscal_year:read",
      },
      {
        href: "/finance/currency-rates",
        label: "Currency rates",
        icon: CircleDollarSign,
        permission: "finance.currency_rate:read",
      },
    ],
  },
  {
    label: "Reporting",
    items: [
      {
        href: "/finance/reports/trial-balance",
        label: "Trial balance",
        icon: FileBarChart,
        permission: "finance.report:read",
      },
      {
        href: "/finance/reports/ar-aging",
        label: "AR aging",
        icon: WalletCards,
        permission: "finance.report:read",
      },
      {
        href: "/finance/reports/ap-aging",
        label: "AP aging",
        icon: WalletCards,
        permission: "finance.report:read",
      },
    ],
  },
];
function ContextSelectors() {
  const c = useFinanceContext();
  return (
    <div className="hidden items-center gap-2 md:flex">
      <label className="relative">
        <Building2 className="pointer-events-none absolute left-2.5 top-2.5 size-4 text-muted-foreground" />
        <select
          aria-label="Company"
          className="control w-48 pl-8"
          value={c.companyId}
          onChange={(e) => void c.setCompany(e.target.value)}
        >
          {c.companies.map((x) => (
            <option key={x.id} value={x.id}>
              {referenceLabel(x as unknown as Record<string, unknown>)}
            </option>
          ))}
        </select>
        <ChevronDown className="pointer-events-none absolute right-2 top-3 size-3 text-muted-foreground" />
      </label>
      <select
        aria-label="Branch"
        className="control w-44"
        value={c.branchId}
        onChange={(e) => void c.setBranch(e.target.value)}
      >
        <option value="">All permitted branches</option>
        {c.branches.map((x) => (
          <option key={x.id} value={x.id}>
            {referenceLabel(x as unknown as Record<string, unknown>)}
          </option>
        ))}
      </select>
    </div>
  );
}
function InnerShell({ children }: { children: React.ReactNode }) {
  const { session, loading, logout, can } = useAuth();
  const path = usePathname();
  const [collapsed, setCollapsed] = useState(false);
  const [mobile, setMobile] = useState(false);
  const [dark, setDark] = useState(false);
  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);
  if (loading || !session)
    return (
      <div className="grid min-h-screen place-items-center text-sm text-muted-foreground">
        Securing your workspace…
      </div>
    );
  const sidebar = (
    <aside
      className={cn(
        "flex h-full flex-col bg-sidebar text-sidebar-foreground transition-all",
        collapsed ? "w-[76px]" : "w-[260px]",
      )}
    >
      <div className="flex h-16 items-center gap-3 border-b border-white/10 px-4">
        <span className="grid size-9 shrink-0 place-items-center rounded-lg bg-[#0f8b8d]">
          <Landmark className="size-5" />
        </span>
        {!collapsed && (
          <div>
            <p className="font-semibold leading-tight">Finance</p>
            <p className="text-xs text-slate-400">Control Center</p>
          </div>
        )}
        <Button
          variant="ghost"
          size="icon-sm"
          className="ml-auto text-slate-300 hover:bg-white/10 hover:text-white"
          onClick={() => setCollapsed(!collapsed)}
        >
          {collapsed ? <ChevronRight /> : <ChevronLeft />}
        </Button>
      </div>
      <nav className="flex-1 space-y-5 overflow-y-auto px-3 py-5">
        {nav.map((group) => {
          const items = group.items.filter((i) => can(i.permission));
          if (!items.length) return null;
          return (
            <div key={group.label}>
              {!collapsed && (
                <p className="mb-2 px-2 text-[10px] font-bold uppercase tracking-[.18em] text-slate-500">
                  {group.label}
                </p>
              )}
              <div className="space-y-1">
                {items.map((item) => {
                  const active =
                    item.href === "/finance"
                      ? path === item.href
                      : path.startsWith(item.href);
                  return (
                    <Link
                      title={collapsed ? item.label : undefined}
                      key={item.href}
                      href={item.href}
                      onClick={() => setMobile(false)}
                      className={cn(
                        "flex h-9 items-center gap-3 rounded-lg px-2.5 text-sm transition",
                        active
                          ? "bg-[#0f8b8d] text-white shadow-sm"
                          : "text-slate-300 hover:bg-sidebar-accent hover:text-white",
                      )}
                    >
                      <item.icon className="size-4 shrink-0" />
                      {!collapsed && <span>{item.label}</span>}
                    </Link>
                  );
                })}
              </div>
            </div>
          );
        })}
      </nav>
      <div className="border-t border-white/10 p-3">
        {!collapsed && (
          <div className="mb-3 px-2">
            <p className="truncate text-sm font-medium">
              {session.user.display_name}
            </p>
            <p className="truncate text-xs text-slate-400">
              {session.user.email}
            </p>
          </div>
        )}
        <Button
          variant="ghost"
          className={cn(
            "w-full text-slate-300 hover:bg-white/10 hover:text-white",
            collapsed ? "px-0" : "justify-start",
          )}
          onClick={() => void logout()}
        >
          <LogOut />
          {!collapsed && "Sign out"}
        </Button>
      </div>
    </aside>
  );
  return (
    <div className="flex min-h-screen">
      <div className="fixed inset-y-0 left-0 z-40 hidden lg:block">
        {sidebar}
      </div>
      {mobile && (
        <div
          className="fixed inset-0 z-50 bg-black/50 lg:hidden"
          onClick={() => setMobile(false)}
        >
          <div
            className="h-full w-[280px]"
            onClick={(e) => e.stopPropagation()}
          >
            {sidebar}
          </div>
          <button
            className="absolute right-4 top-4 text-white"
            onClick={() => setMobile(false)}
          >
            <X />
          </button>
        </div>
      )}
      <div
        className={cn(
          "min-w-0 flex-1 transition-all",
          collapsed ? "lg:ml-[76px]" : "lg:ml-[260px]",
        )}
      >
        <header className="no-print sticky top-0 z-30 flex h-16 items-center justify-between border-b bg-card/95 px-4 backdrop-blur sm:px-6">
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setMobile(true)}
            >
              <Menu />
            </Button>
            <div className="hidden sm:block">
              <p className="text-sm font-semibold">Finance operations</p>
              <p className="text-xs text-muted-foreground">
                Accurate books. Controlled close.
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <ContextSelectors />
            <Button
              variant="ghost"
              size="icon"
              aria-label="Toggle theme"
              onClick={() => setDark(!dark)}
            >
              {dark ? <Sun /> : <Moon />}
            </Button>
          </div>
        </header>
        <main className="mx-auto max-w-[1600px] p-4 sm:p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
export function FinanceShell({ children }: { children: React.ReactNode }) {
  return (
    <FinanceContextProvider>
      <InnerShell>{children}</InnerShell>
    </FinanceContextProvider>
  );
}
