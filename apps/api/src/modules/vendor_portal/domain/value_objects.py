"""Vendor Portal value objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class VendorPortalCodes:
    account: str
