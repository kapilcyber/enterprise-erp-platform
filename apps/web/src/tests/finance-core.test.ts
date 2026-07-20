import { describe, expect, it } from "vitest";
import { isBalanced, journalLineSchema, journalSchema, paymentSchema } from "@/lib/validation";
import { date, money, title } from "@/lib/format";

describe("finance validation", () => {
  it("accepts a valid manual journal", () => {
    expect(journalSchema.safeParse({branch_id:"00000000-0000-4000-8000-000000000001",journal_date:"2026-07-20",description:"Month-end accrual",journal_type:"manual",currency_code:"INR",exchange_rate:1,period_id:""}).success).toBe(true);
  });
  it("requires exactly one side of a journal line", () => {
    const base={account_id:"00000000-0000-4000-8000-000000000001",description:"",cost_center_id:"",tax_id:"",customer_id:"",vendor_id:""};
    expect(journalLineSchema.safeParse({...base,debit_amount:100,credit_amount:0}).success).toBe(true);
    expect(journalLineSchema.safeParse({...base,debit_amount:100,credit_amount:100}).success).toBe(false);
    expect(journalLineSchema.safeParse({...base,debit_amount:0,credit_amount:0}).success).toBe(false);
  });
  it("requires positive payments and exact balance", () => {
    expect(paymentSchema.safeParse({amount:1}).success).toBe(true);
    expect(paymentSchema.safeParse({amount:0}).success).toBe(false);
    expect(isBalanced(100.01,100.01)).toBe(true);
    expect(isBalanced(100,99)).toBe(false);
  });
});

describe("finance formatters", () => {
  it("formats Indian currency, dates and enum labels", () => {
    expect(money(125000)).toContain("1,25,000");
    expect(date("2026-07-20")).toContain("2026");
    expect(title("soft_closed")).toBe("Soft Closed");
  });
});
