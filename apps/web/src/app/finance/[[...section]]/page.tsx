import { FinanceShell } from "@/components/layout/finance-shell";
import { FinanceWorkspace } from "@/components/finance/finance-workspace";
export default async function FinancePage({
  params,
}: {
  params: Promise<{ section?: string[] }>;
}) {
  const { section = [] } = await params;
  return (
    <FinanceShell>
      <FinanceWorkspace section={section} />
    </FinanceShell>
  );
}
