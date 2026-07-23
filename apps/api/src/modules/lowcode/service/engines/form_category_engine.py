"""FormCategory lifecycle engine."""

from modules.lowcode.domain.enums import CategoryStatus
from modules.lowcode.domain.exceptions import InvalidCategoryState


class FormCategoryEngine:
    def activate(self, row) -> None:
        if row.status == CategoryStatus.ACTIVE.value:
            raise InvalidCategoryState("Category already active")
        row.status = CategoryStatus.ACTIVE.value

    def deactivate(self, row) -> None:
        if row.status != CategoryStatus.ACTIVE.value:
            raise InvalidCategoryState("Only active categories can be deactivated")
        row.status = CategoryStatus.INACTIVE.value
