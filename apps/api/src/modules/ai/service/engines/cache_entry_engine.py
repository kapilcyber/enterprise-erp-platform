"""Cache entry lifecycle engine — expire / invalidate.

Cache entries must NOT bypass guardrails. Invalidation and expiry are metadata
operations only; they do not skip guardrail, moderation, or rate-limit evaluation
on subsequent invocations.
"""

from modules.ai.domain.enums import CacheEntryStatus
from modules.ai.domain.exceptions import InvalidCacheEntryState


class CacheEntryEngine:
    def expire(self, row) -> None:
        if row.status == CacheEntryStatus.EXPIRED.value:
            raise InvalidCacheEntryState("Cache entry already expired")
        if row.status == CacheEntryStatus.INVALIDATED.value:
            raise InvalidCacheEntryState("Invalidated cache entries cannot be expired")
        row.status = CacheEntryStatus.EXPIRED.value

    def invalidate(self, row) -> None:
        if row.status == CacheEntryStatus.INVALIDATED.value:
            raise InvalidCacheEntryState("Cache entry already invalidated")
        row.status = CacheEntryStatus.INVALIDATED.value
