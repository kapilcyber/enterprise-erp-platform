import Link from "next/link";

export default function BpmOverviewPage() {
  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-semibold tracking-tight">Workflow & BPM</h1>
        <p className="mt-2 max-w-2xl text-muted-foreground">
          Phase 1 design spine: Category → Template → Definition → Version. Publish
          enforces exactly one published version per definition.
        </p>
      </header>
      <div className="grid gap-4 sm:grid-cols-3">
        {[
          {
            href: "/bpm/categories",
            title: "Category Explorer",
            body: "Organize the Template Library.",
          },
          {
            href: "/bpm/templates",
            title: "Template Library",
            body: "Reusable cross-module templates.",
          },
          {
            href: "/bpm/definitions",
            title: "Definitions",
            body: "Stable identity and version timeline.",
          },
        ].map((card) => (
          <Link
            key={card.href}
            href={card.href}
            className="rounded-lg border border-border p-5 transition-colors hover:bg-muted/40"
          >
            <h2 className="font-medium">{card.title}</h2>
            <p className="mt-1 text-sm text-muted-foreground">{card.body}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
