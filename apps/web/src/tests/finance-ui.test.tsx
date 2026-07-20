import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { EmptyState, StatusBadge } from "@/components/ui/finance-ui";

describe("finance UI states", () => {
  it("renders status text without relying on color", () => {
    render(<StatusBadge value="soft_closed"/>);
    expect(screen.getByText("soft closed")).toBeVisible();
  });
  it("renders an actionable empty state", () => {
    render(<EmptyState title="No journals" description="Create the first journal."/>);
    expect(screen.getByText("No journals")).toBeVisible();
    expect(screen.getByText("Create the first journal.")).toBeVisible();
  });
});
