"""Finance port — PostingService.post_system_journal only; no fin_* ORM writes."""

from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from modules.finance.domain.enums import JournalType
from modules.finance.service.journal_service import JournalService
from modules.finance.service.posting_service import PostingService
from modules.foundation.domain.value_objects import TenantContext
from modules.vendor_portal.models import VpPaymentStatus


class VendorPortalFinanceAdapter:
    def __init__(self, db: Session) -> None:
        self._journals = JournalService(db)
        self._posting = PostingService(db)

    def resolve_payment_ref(self, ctx: TenantContext, finance_payment_id: UUID | None) -> UUID | None:  # noqa: E501
        _ = ctx
        return finance_payment_id

    def post_portal_fee(
        self,
        ctx: TenantContext,
        row: VpPaymentStatus,
        *,
        amount: Decimal,
        debit_account_id: UUID,
        credit_account_id: UUID,
        fiscal_year_id: UUID | None = None,
    ) -> UUID:
        amount = amount.quantize(Decimal("0.0001"))
        resolved_branch_id = getattr(row, "branch_id", None) or ctx.branch_id
        if resolved_branch_id is None:
            raise ValueError("branch_id is required for vendor portal finance posting")
        journal = self._journals.create_journal(
            ctx,
            company_id=row.company_id,
            branch_id=resolved_branch_id,
            journal_date=date.today(),
            description=f"Vendor portal fee {row.status_number}",
            journal_type=JournalType.SYSTEM.value,
            fiscal_year_id=fiscal_year_id,
        )
        self._journals.add_line(ctx, journal.id, line_number=1, account_id=debit_account_id, debit_amount=float(amount), credit_amount=0, description="Vendor portal fee debit")  # noqa: E501
        self._journals.add_line(ctx, journal.id, line_number=2, account_id=credit_account_id, debit_amount=0, credit_amount=float(amount), description="Vendor portal fee credit")  # noqa: E501
        self._posting.post_system_journal(ctx, journal.id)
        return journal.id
