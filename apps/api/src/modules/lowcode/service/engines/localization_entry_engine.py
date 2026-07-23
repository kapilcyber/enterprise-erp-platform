"""LocalizationEntry lifecycle engine — Phase 3A metadata only."""

from datetime import datetime, timezone
from uuid import UUID

from modules.lowcode.domain.enums import (
    LOCALIZATION_OWNER_TYPE_VALUES,
    LocalizationOwnerType,
    VersionStatus,
)
from modules.lowcode.domain.exceptions import (
    InvalidLocalizationEntryState,
    PublishedLocalizationImmutable,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class LocalizationEntryEngine:
    def assert_valid_owner_type(self, owner_type: str | None) -> None:
        if not owner_type or owner_type not in LOCALIZATION_OWNER_TYPE_VALUES:
            raise InvalidLocalizationEntryState(f"Unsupported owner_type: {owner_type}")

    def assert_locale(self, locale: str | None) -> None:
        if not locale or not str(locale).strip():
            raise InvalidLocalizationEntryState("locale is required")
        if len(str(locale).strip()) > 20:
            raise InvalidLocalizationEntryState("locale must be <= 20 characters")

    def assert_translation_key(self, translation_key: str | None) -> None:
        if not translation_key or not str(translation_key).strip():
            raise InvalidLocalizationEntryState("translation_key is required")

    def assert_translated_value(self, translated_value: str | None) -> None:
        if translated_value is None or not str(translated_value).strip():
            raise InvalidLocalizationEntryState("translated_value is required")

    def assert_editable(self, row) -> None:
        if row.status == VersionStatus.PUBLISHED.value:
            raise PublishedLocalizationImmutable()
        if row.status == VersionStatus.RETIRED.value:
            raise InvalidLocalizationEntryState(
                "Retired localization entries are read-only"
            )
        if row.status != VersionStatus.DRAFT.value:
            raise InvalidLocalizationEntryState(
                "Only draft localization entries are editable"
            )

    def publish(self, row, *, user_id) -> None:
        if row.status != VersionStatus.DRAFT.value:
            raise InvalidLocalizationEntryState(
                "Only draft localization entries can be published"
            )
        row.status = VersionStatus.PUBLISHED.value
        row.published_at = _utcnow()
        row.published_by = user_id

    def retire(self, row, *, user_id) -> None:
        if row.status not in {
            VersionStatus.PUBLISHED.value,
            VersionStatus.DRAFT.value,
        }:
            raise InvalidLocalizationEntryState(
                "Only draft or published localization entries can be retired"
            )
        row.status = VersionStatus.RETIRED.value
        row.retired_at = _utcnow()
        row.retired_by = user_id

    def resolve_owner_refs(
        self,
        *,
        owner_type: str,
        form_version_id: UUID | None,
        section_id: UUID | None,
        field_id: UUID | None,
        component_id: UUID | None,
        page_version_id: UUID | None,
    ) -> tuple[UUID, dict]:
        """Return (owner_ref_id, column payload) for the selected owner_type."""
        self.assert_valid_owner_type(owner_type)
        if owner_type == LocalizationOwnerType.FORM.value:
            if form_version_id is None:
                raise InvalidLocalizationEntryState(
                    "form_version_id is required for form localization"
                )
            if section_id or field_id or component_id or page_version_id:
                raise InvalidLocalizationEntryState(
                    "form localization must not set section/field/component/page"
                )
            return form_version_id, {
                "form_version_id": form_version_id,
                "section_id": None,
                "field_id": None,
                "component_id": None,
                "page_version_id": None,
            }
        if owner_type == LocalizationOwnerType.SECTION.value:
            if section_id is None or form_version_id is None:
                raise InvalidLocalizationEntryState(
                    "section_id and form_version_id are required for section localization"
                )
            if field_id or component_id or page_version_id:
                raise InvalidLocalizationEntryState(
                    "section localization must not set field/component/page"
                )
            return section_id, {
                "form_version_id": form_version_id,
                "section_id": section_id,
                "field_id": None,
                "component_id": None,
                "page_version_id": None,
            }
        if owner_type == LocalizationOwnerType.FIELD.value:
            if field_id is None or form_version_id is None:
                raise InvalidLocalizationEntryState(
                    "field_id and form_version_id are required for field localization"
                )
            if component_id or page_version_id:
                raise InvalidLocalizationEntryState(
                    "field localization must not set component/page"
                )
            return field_id, {
                "form_version_id": form_version_id,
                "section_id": section_id,
                "field_id": field_id,
                "component_id": None,
                "page_version_id": None,
            }
        if owner_type == LocalizationOwnerType.COMPONENT.value:
            if component_id is None:
                raise InvalidLocalizationEntryState(
                    "component_id is required for component localization"
                )
            if form_version_id or section_id or field_id or page_version_id:
                raise InvalidLocalizationEntryState(
                    "component localization must not set form/section/field/page"
                )
            return component_id, {
                "form_version_id": None,
                "section_id": None,
                "field_id": None,
                "component_id": component_id,
                "page_version_id": None,
            }
        # page — future UUID only
        if page_version_id is None:
            raise InvalidLocalizationEntryState(
                "page_version_id is required for page localization"
            )
        if form_version_id or section_id or field_id or component_id:
            raise InvalidLocalizationEntryState(
                "page localization must not set form/section/field/component"
            )
        return page_version_id, {
            "form_version_id": None,
            "section_id": None,
            "field_id": None,
            "component_id": None,
            "page_version_id": page_version_id,
        }
