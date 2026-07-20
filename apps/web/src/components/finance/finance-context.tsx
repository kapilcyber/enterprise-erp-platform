"use client";
import { createContext, useCallback, useContext, useMemo, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { contextService } from "@/services/finance";
import type { ReferenceItem } from "@/types/api";

type Value = {
  companyId: string;
  branchId: string;
  companies: ReferenceItem[];
  branches: ReferenceItem[];
  setCompany: (id: string) => Promise<void>;
  setBranch: (id: string) => Promise<void>;
  ready: boolean;
};
const Context = createContext<Value | null>(null);
export function FinanceContextProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const client = useQueryClient();
  const [companyId, setCompanyId] = useState("");
  const [branchId, setBranchId] = useState("");
  const companies = useQuery({
    queryKey: ["context", "companies"],
    queryFn: contextService.companies,
  });
  const current = useQuery({
    queryKey: ["context"],
    queryFn: contextService.get,
  });
  const effectiveCompany = companyId || current.data?.company_id || companies.data?.[0]?.id || "";
  const branches = useQuery({
    queryKey: ["context", "branches", effectiveCompany],
    queryFn: () => contextService.branches(effectiveCompany),
    enabled: !!effectiveCompany,
  });
  const effectiveBranch = branchId || current.data?.branch_id || branches.data?.[0]?.id || "";
  const switchContext = useCallback(async (cid: string, bid?: string) => {
    await contextService.switch(cid, bid);
    setCompanyId(cid);
    setBranchId(bid ?? "");
    await client.invalidateQueries();
  }, [client]);
  const value = useMemo<Value>(
    () => ({
      companyId: effectiveCompany,
      branchId: effectiveBranch,
      companies: companies.data ?? [],
      branches: branches.data ?? [],
      setCompany: async (id) => switchContext(id),
      setBranch: async (id) => switchContext(effectiveCompany, id),
      ready: !companies.isLoading && !!effectiveCompany,
    }),
    [effectiveCompany, effectiveBranch, companies.data, companies.isLoading, branches.data, switchContext],
  );
  return <Context.Provider value={value}>{children}</Context.Provider>;
}
export function useFinanceContext() {
  const v = useContext(Context);
  if (!v) throw new Error("Finance context unavailable");
  return v;
}
