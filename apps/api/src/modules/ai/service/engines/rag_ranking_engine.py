"""RAG ranking engine stub — metadata-only ranking by sequence_no, no vector DB calls."""


class RagRankingEngine:
    def rank_chunks(self, chunks: list) -> dict:
        """Rank chunk metadata by sequence_no ascending; returns citation-style refs."""
        sorted_chunks = sorted(chunks, key=lambda c: getattr(c, "sequence_no", 0))
        ranked = []
        for rank, chunk in enumerate(sorted_chunks, start=1):
            ranked.append(
                {
                    "rank": rank,
                    "chunk_id": str(getattr(chunk, "id", "")),
                    "chunk_code": getattr(chunk, "chunk_code", None),
                    "sequence_no": getattr(chunk, "sequence_no", None),
                    "knowledge_source_id": str(getattr(chunk, "knowledge_source_id", "")),
                    "content_preview": getattr(chunk, "content_preview", None),
                }
            )
        return {"ranked_chunks": ranked, "retrieval_mode": "metadata_stub"}
