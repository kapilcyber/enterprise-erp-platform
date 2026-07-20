import { expect, test } from "@playwright/test";

test("shows the secure finance login at desktop and tablet sizes", async ({ page }) => {
  await page.route("**/api/session/me", route => route.fulfill({status:401,contentType:"application/json",body:JSON.stringify({success:false,message:"Authentication required",errors:[]})}));
  await page.goto("/login");
  await expect(page.getByRole("heading", {name:"Welcome back"})).toBeVisible();
  await expect(page.getByLabel("Email address")).toBeVisible();
  await expect(page.getByRole("button", {name:/sign in/i})).toBeVisible();
});
