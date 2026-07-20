"""Organization port — department FK only."""

from uuid import UUID

from sqlalchemy.orm import Session

from core.exceptions import NotFoundException
from modules.foundation.domain.value_objects import TenantContext
from modules.organization.repository.hierarchy_repository import DepartmentRepository


class VendorPortalOrganizationAdapter:
    def __init__(self, db: Session) -> None:
        self._depts = DepartmentRepository(db)

    def get_department(self, ctx: TenantContext, department_id: UUID):
        row = self._depts.get_by_id(ctx, department_id)
        if row is None:
            raise NotFoundException("Department not found")
        return row
