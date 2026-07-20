export const money = (value: number, currency = "INR") =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency,
    maximumFractionDigits: 2,
  }).format(value || 0);
export const number = (value: number) =>
  new Intl.NumberFormat("en-IN", { maximumFractionDigits: 2 }).format(
    value || 0,
  );
export const date = (value?: string | null) =>
  value
    ? new Intl.DateTimeFormat("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
      }).format(new Date(`${value}T00:00:00`))
    : "—";
export const title = (value: string) =>
  value.replaceAll("_", " ").replace(/\b\w/g, (c) => c.toUpperCase());
export const referenceLabel = (item: Record<string, unknown>) => {
  const name =
    item.company_name ??
    item.branch_name ??
    item.customer_name ??
    item.vendor_name ??
    item.currency_name ??
    item.tax_name ??
    item.asset_name ??
    item.name;
  const code =
    item.company_code ??
    item.branch_code ??
    item.customer_code ??
    item.vendor_code ??
    item.currency_code ??
    item.tax_code ??
    item.asset_code ??
    item.code;
  return (
    [code, name].filter(Boolean).join(" · ") || String(item.id ?? "Unknown")
  );
};
