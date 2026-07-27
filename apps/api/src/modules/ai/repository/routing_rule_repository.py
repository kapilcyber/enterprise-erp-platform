"""AiRoutingRule repository — Phase 1."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from modules.ai.domain.value_objects import PageResult
from modules.ai.models.routing_rule import AiRoutingRule
from modules.ai.repository.base import AiScopedRepository, utcnow
from modules.foundation.domain.value_objects import TenantContext

_SORT = {"rule_code", "priority", "status", "created_at", "updated_at"}


class RoutingRuleRepository(AiScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> AiRoutingRule | None:
        stmt = select(AiRoutingRule).where(
            AiRoutingRule.id == row_id,
            AiRoutingRule.is_deleted.is_(False),
        )
        stmt = self.apply_ai_filter(stmt, AiRoutingRule, ctx)
        return self.db.scalar(stmt)

    def get_including_archived(self, ctx: TenantContext, row_id: UUID) -> AiRoutingRule | None:
        stmt = select(AiRoutingRule).where(AiRoutingRule.id == row_id)
        stmt = self.apply_ai_filter(stmt, AiRoutingRule, ctx)
        return self.db.scalar(stmt)


    def list_by_gateway_policy(self, ctx: TenantContext, gateway_policy_id: UUID) -> list[AiRoutingRule]:
        stmt = (
            select(AiRoutingRule)
            .where(
                AiRoutingRule.gateway_policy_id == gateway_policy_id,
                AiRoutingRule.is_deleted.is_(False),
            )
            .order_by(AiRoutingRule.priority.asc(), AiRoutingRule.rule_code.asc())
        )
        stmt = self.apply_ai_filter(stmt, AiRoutingRule, ctx)
        return list(self.db.scalars(stmt).all())

    def list_rows(
        self,
        ctx: TenantContext,
        company_id: UUID,
        *,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "priority",
        sort_dir: str = "asc",
        include_archived: bool = False,
        gateway_policy_id: UUID | None = None,
        provider_id: UUID | None = None
    ) -> PageResult:
        stmt = select(AiRoutingRule).where(AiRoutingRule.company_id == company_id)
        if not include_archived:
            stmt = stmt.where(AiRoutingRule.is_deleted.is_(False))
        if status:
            stmt = stmt.where(AiRoutingRule.status == status)
        if gateway_policy_id:
            stmt = stmt.where(AiRoutingRule.gateway_policy_id == gateway_policy_id)
        if provider_id:
            stmt = stmt.where(AiRoutingRule.provider_id == provider_id)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(AiRoutingRule.rule_code.ilike(like) | AiRoutingRule.description.ilike(like))
        stmt = self.apply_ai_filter(stmt, AiRoutingRule, ctx)
        return self.paginate_sorted(
            stmt,
            AiRoutingRule,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            allowed_sort=_SORT,
        )

    def create(self, ctx: TenantContext, **fields) -> AiRoutingRule:
        row = AiRoutingRule(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> AiRoutingRule | None:
        row = self.get(ctx, row_id)
        if row is None:
            return None
        for k, v in fields.items():
            if v is not None:
                setattr(row, k, v)
        row.updated_at = utcnow()
        row.updated_by = ctx.user_id
        row.version = int(row.version or 1) + 1
        self.db.flush()
        return row

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> AiRoutingRule | None:
        row = self.get(ctx, row_id)
        if row is None:
            return None
        row.is_deleted = True
        row.deleted_at = utcnow()
        row.deleted_by = ctx.user_id
        row.updated_at = utcnow()
        row.updated_by = ctx.user_id
        row.version = int(row.version or 1) + 1
        self.db.flush()
        return row

    def restore(self, ctx: TenantContext, row_id: UUID) -> AiRoutingRule | None:
        row = self.get_including_archived(ctx, row_id)
        if row is None or not row.is_deleted:
            return None
        row.is_deleted = False
        row.deleted_at = None
        row.deleted_by = None
        row.updated_at = utcnow()
        row.updated_by = ctx.user_id
        row.version = int(row.version or 1) + 1
        self.db.flush()
        return row
