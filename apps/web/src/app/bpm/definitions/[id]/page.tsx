"use client";

import { useParams } from "next/navigation";

import { DefinitionDetail } from "@/modules/bpm/components/definition-detail";

export default function DefinitionDetailPage() {
  const params = useParams<{ id: string }>();
  return <DefinitionDetail definitionId={params.id} />;
}
