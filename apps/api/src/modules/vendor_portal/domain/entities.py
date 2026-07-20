"""Vendor Portal domain entity markers."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class PortalAccountIdentity:
    account_id: UUID
    vendor_id: UUID
