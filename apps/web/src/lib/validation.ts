import { z } from "zod";

export const loginSchema = z.object({
  email: z.email("Enter a valid email"),
  password: z.string().min(8, "Use at least 8 characters"),
});
export const journalSchema = z.object({
  branch_id: z.string().uuid(),
  journal_date: z.string().min(1),
  description: z.string().min(3),
  journal_type: z.enum(["manual", "adjustment"]),
  currency_code: z.string().length(3),
  exchange_rate: z.number().positive(),
  period_id: z.string().uuid().optional().or(z.literal("")),
});
export const journalLineSchema = z
  .object({
    account_id: z.string().uuid(),
    description: z.string().optional(),
    debit_amount: z.number().min(0),
    credit_amount: z.number().min(0),
    cost_center_id: z.string().optional(),
    tax_id: z.string().optional(),
    customer_id: z.string().optional(),
    vendor_id: z.string().optional(),
  })
  .refine((v) => v.debit_amount > 0 !== v.credit_amount > 0, {
    message: "Enter either a debit or a credit amount",
    path: ["debit_amount"],
  });
export const paymentSchema = z.object({
  amount: z.number().positive("Payment must be greater than zero"),
});
export const isBalanced = (debit: number, credit: number) =>
  Math.abs(debit - credit) < 0.0001 && debit > 0;
