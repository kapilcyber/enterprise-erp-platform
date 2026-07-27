"""Citation engine stub — build citation refs from chunk/source/document UUIDs."""

from uuid import UUID


class CitationEngine:
    def build_citations(
        self,
        *,
        chunk_id: UUID | None = None,
        source_id: UUID | None = None,
        document_id: UUID | None = None,
        chunk_code: str | None = None,
        source_code: str | None = None,
    ) -> dict:
        """Return structured citation metadata — no document ORM load."""
        return {
            "citations": [
                {
                    "chunk_id": str(chunk_id) if chunk_id else None,
                    "source_id": str(source_id) if source_id else None,
                    "document_id": str(document_id) if document_id else None,
                    "chunk_code": chunk_code,
                    "source_code": source_code,
                    "citation_type": "metadata_ref",
                }
            ]
        }

    def build_citations_from_chunks(self, chunks: list, sources: list | None = None) -> dict:
        source_map = {str(s.id): s for s in (sources or [])}
        citations = []
        for chunk in chunks:
            source = source_map.get(str(getattr(chunk, "knowledge_source_id", "")))
            citations.append(
                {
                    "chunk_id": str(getattr(chunk, "id", "")),
                    "source_id": str(getattr(chunk, "knowledge_source_id", "")),
                    "document_id": str(getattr(source, "document_id", ""))
                    if source and getattr(source, "document_id", None)
                    else None,
                    "chunk_code": getattr(chunk, "chunk_code", None),
                    "source_code": getattr(source, "source_code", None) if source else None,
                    "citation_type": "metadata_ref",
                }
            )
        return {"citations": citations}
