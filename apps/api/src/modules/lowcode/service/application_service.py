"""Low-Code application facade — Phase 1–4 (18/18)."""

from sqlalchemy.orm import Session

from modules.lowcode.service.component_service import ComponentService
from modules.lowcode.service.component_version_service import ComponentVersionService
from modules.lowcode.service.data_source_service import DataSourceService
from modules.lowcode.service.event_handler_service import EventHandlerService
from modules.lowcode.service.expression_binding_service import ExpressionBindingService
from modules.lowcode.service.expression_service import ExpressionService
from modules.lowcode.service.form_category_service import FormCategoryService
from modules.lowcode.service.form_definition_service import FormDefinitionService
from modules.lowcode.service.form_field_service import FormFieldService
from modules.lowcode.service.form_section_service import FormSectionService
from modules.lowcode.service.form_structure_validation_service import (
    FormStructureValidationService,
)
from modules.lowcode.service.form_version_service import FormVersionService
from modules.lowcode.service.localization_entry_service import LocalizationEntryService
from modules.lowcode.service.page_definition_service import PageDefinitionService
from modules.lowcode.service.page_region_service import PageRegionService
from modules.lowcode.service.page_version_service import PageVersionService
from modules.lowcode.service.preview_session_service import PreviewSessionService
from modules.lowcode.service.publish_history_service import PublishHistoryService
from modules.lowcode.service.publish_validation_service import PublishValidationService
from modules.lowcode.service.runtime_submission_service import RuntimeSubmissionService


class LowcodeApplicationService:
    def __init__(self, db: Session) -> None:
        self.categories = FormCategoryService(db)
        self.definitions = FormDefinitionService(db)
        self.versions = FormVersionService(db)
        self.publish_validation = PublishValidationService(db)
        self.sections = FormSectionService(db)
        self.fields = FormFieldService(db)
        self.structure_validation = FormStructureValidationService(db)
        self.components = ComponentService(db)
        self.component_versions = ComponentVersionService(db)
        self.data_sources = DataSourceService(db)
        self.expressions = ExpressionService(db)
        self.expression_bindings = ExpressionBindingService(db)
        self.event_handlers = EventHandlerService(db)
        self.localization_entries = LocalizationEntryService(db)
        self.page_definitions = PageDefinitionService(db)
        self.page_versions = PageVersionService(db)
        self.page_regions = PageRegionService(db)
        self.publish_history = PublishHistoryService(db)
        self.runtime_submissions = RuntimeSubmissionService(db)
        self.preview_sessions = PreviewSessionService(db)
