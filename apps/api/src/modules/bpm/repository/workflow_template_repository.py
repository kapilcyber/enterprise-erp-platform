"""BPM BpmWorkflowTemplate repository — Phase 1.5."""

from uuid import UUID, uuid4

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from modules.bpm.domain.value_objects import PageResult
from modules.bpm.models import BpmWorkflowDefinition, BpmWorkflowTemplate
from modules.bpm.repository.base import BpmScopedRepository, utcnow
from modules.foundation.domain.value_objects import TenantContext

_SORT = {
    "template_code",
    "template_name",
    "status",
    "module_code",
    "created_at",
    "updated_at",
}


class WorkflowTemplateRepository(BpmScopedRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowTemplate | None:
        stmt = select(BpmWorkflowTemplate).where(
            BpmWorkflowTemplate.id == row_id,
            BpmWorkflowTemplate.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowTemplate, ctx)
        return self.db.scalar(stmt)

    def get_including_archived(
        self, ctx: TenantContext, row_id: UUID
    ) -> BpmWorkflowTemplate | None:
        stmt = select(BpmWorkflowTemplate).where(BpmWorkflowTemplate.id == row_id)
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowTemplate, ctx)
        return self.db.scalar(stmt)

    def list_rows(
        self,
        ctx: TenantContext,
        company_id: UUID,
        *,
        status: str | None = None,
        category_id: UUID | None = None,
        search: str | None = None,
        page: int = 1,
        page_size: int = 25,
        sort_by: str | None = "template_name",
        sort_dir: str = "asc",
        include_archived: bool = False,
    ) -> PageResult:
        stmt = select(BpmWorkflowTemplate).where(BpmWorkflowTemplate.company_id == company_id)
        if not include_archived:
            stmt = stmt.where(BpmWorkflowTemplate.is_deleted.is_(False))
        if status:
            stmt = stmt.where(BpmWorkflowTemplate.status == status)
        if category_id:
            stmt = stmt.where(BpmWorkflowTemplate.category_id == category_id)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(
                BpmWorkflowTemplate.template_name.ilike(like)
                | BpmWorkflowTemplate.template_code.ilike(like)
            )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowTemplate, ctx)
        return self.paginate_sorted(
            stmt,
            BpmWorkflowTemplate,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            allowed_sort=_SORT,
        )

    def autocomplete(
        self, ctx: TenantContext, company_id: UUID, q: str, *, limit: int = 10
    ) -> list[BpmWorkflowTemplate]:
        like = f"%{q}%"
        stmt = (
            select(BpmWorkflowTemplate)
            .where(
                BpmWorkflowTemplate.company_id == company_id,
                BpmWorkflowTemplate.is_deleted.is_(False),
                BpmWorkflowTemplate.template_name.ilike(like)
                | BpmWorkflowTemplate.template_code.ilike(like),
            )
            .order_by(BpmWorkflowTemplate.template_name)
            .limit(limit)
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowTemplate, ctx)
        return list(self.db.scalars(stmt).all())

    def recent(self, ctx: TenantContext, company_id: UUID, *, limit: int = 10) -> list:
        stmt = (
            select(BpmWorkflowTemplate)
            .where(
                BpmWorkflowTemplate.company_id == company_id,
                BpmWorkflowTemplate.is_deleted.is_(False),
            )
            .order_by(desc(BpmWorkflowTemplate.updated_at))
            .limit(limit)
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowTemplate, ctx)
        return list(self.db.scalars(stmt).all())

    def popular(self, ctx: TenantContext, company_id: UUID, *, limit: int = 10) -> list[dict]:
        """Popular = templates with most linked definitions."""
        stmt = (
            select(
                BpmWorkflowTemplate,
                func.count(BpmWorkflowDefinition.id).label("usage_count"),
            )
            .outerjoin(
                BpmWorkflowDefinition,
                (BpmWorkflowDefinition.template_id == BpmWorkflowTemplate.id)
                & (BpmWorkflowDefinition.is_deleted.is_(False)),
            )
            .where(
                BpmWorkflowTemplate.company_id == company_id,
                BpmWorkflowTemplate.is_deleted.is_(False),
            )
            .group_by(BpmWorkflowTemplate.id)
            .order_by(desc("usage_count"), BpmWorkflowTemplate.template_name)
            .limit(limit)
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowTemplate, ctx)
        rows = self.db.execute(stmt).all()
        return [{"template": t, "usage_count": int(c or 0)} for t, c in rows]

    def count_active(self, ctx: TenantContext, company_id: UUID) -> int:
        stmt = select(func.count()).select_from(BpmWorkflowTemplate).where(
            BpmWorkflowTemplate.company_id == company_id,
            BpmWorkflowTemplate.is_deleted.is_(False),
        )
        stmt = self.apply_bpm_filter(stmt, BpmWorkflowTemplate, ctx)
        return int(self.db.scalar(stmt) or 0)

    def create(self, ctx: TenantContext, **fields) -> BpmWorkflowTemplate:
        row = BpmWorkflowTemplate(
            id=uuid4(),
            tenant_id=ctx.tenant_id,
            created_by=ctx.user_id,
            updated_by=ctx.user_id,
            **fields,
        )
        self.db.add(row)
        self.db.flush()
        return row

    def update(self, ctx: TenantContext, row_id: UUID, **fields) -> BpmWorkflowTemplate | None:
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

    def soft_delete(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowTemplate | None:
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

    def restore(self, ctx: TenantContext, row_id: UUID) -> BpmWorkflowTemplate | None:
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
