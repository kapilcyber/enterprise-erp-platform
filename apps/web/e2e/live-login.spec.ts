import { expect, test } from "@playwright/test";

test("seeded Finance administrator can sign in through the UI", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email address").fill("finance.admin@example.com");
  await page.getByLabel("Password").fill("Finance@2026!Secure");
  await page.getByRole("button", { name: /^sign in$/i }).click();
  await expect(page).toHaveURL(/\/finance$/, { timeout: 15_000 });
  await expect(page.getByRole("heading", { name: "Finance control center" })).toBeVisible();
});
