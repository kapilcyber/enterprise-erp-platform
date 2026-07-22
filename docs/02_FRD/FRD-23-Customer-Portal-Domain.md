# FRD-23 — Customer Portal & Self-Service Portal

## 1. Document Control

| Field | Value |
|-------|--------|
| **Document ID** | FRD-23 |
| **Document Title** | Customer Portal & Self-Service Portal Domain |
| **Domain** | Customer Portal (`portal` / `pt_*`) |
| **Version** | 1.1 |
| **Status** | Locked — Ready for Future Reference |
| **Classification** | Internal — Confidential |
| **Aligned To** | BRD v1.0 · SDD v1.1 · DBS v1.1 · Architecture Lock v1.1 · ERD_23 (Locked) · ERP Core v1.18-beta (Sprint 23) |
| **Implementation Source of Truth** | `apps/api/src/modules/portal/` |
| **API Mount** | `/api/v1/portal` |
| **Schema / Prefix** | `portal` / `pt_` |
| **Business Tables** | Exactly **20** |
| **Predecessor Release** | ERP Core v1.17-beta |
| **Delivered In** | ERP Core v1.18-beta |

### Cross References

- Upstream: [FRD-01 Foundation Domain](./FRD-01-Foundation-Domain.md) · [FRD-02 Organization Domain](./FRD-02-Organization-Domain.md) · [FRD-03 Master Data Domain](./FRD-03-Master-Data-Domain.md) · [FRD-04 Finance & Accounting Domain](./FRD-04-Finance-Accounting-Domain.md) · [FRD-05 CRM Domain](./FRD-05-CRM-Domain.md) · [FRD-06 Sales Domain](./FRD-06-Sales-Domain.md) · [FRD-16 Service Management Domain](./FRD-16-Service-Management-Domain.md) · [FRD-17 Helpdesk & Customer Support Domain](./FRD-17-Helpdesk-Customer-Support-Domain.md) · [FRD-18 BI / Reporting / Analytics Domain](./FRD-18-BI-Reporting-Analytics-Domain.md) · [FRD-19 Document Management System Domain](./FRD-19-Document-Management-System-Domain.md) · [FRD-21 Integration Hub & Enterprise Platform Services](./FRD-21-Integration-Hub-Enterprise-Platform-Services.md) · [FRD-22 E-Commerce & External Channel Integration Domain](./FRD-22-Ecommerce-External-Channel-Integration-Domain.md)
- Design: [ERD_23 Customer Portal & Self-Service Portal (Locked)](../06_ERD/ERD_23_Customer_Portal.md)
- Sprint 23 Completion Report (Sprint 23 implementation completion)
- Sprint 23 Validation Report (Sprint 23 quality-gate validation)
- Release: [ERP Core v1.18-beta Release Notes](../07_RELEASES/ERP_Core_v1.18-beta.md)

### Related Documents

| Document | Location / Reference |
|----------|----------------------|
| Master-FRD | [Master-FRD.md](./Master-FRD.md) |
| Architecture Lock v1.1 | [ERP_Architecture_Lock_Report_v1.1.md](../05_ARCHITECTURE_LOCK/ERP_Architecture_Lock_Report_v1.1.md) |
| ERD_23 (Locked) | [ERD_23_Customer_Portal.md](../06_ERD/ERD_23_Customer_Portal.md) |
| Sprint 23 Completion Report | Sprint 23 implementation completion (Customer Portal module) |
| Sprint 23 Validation Report | Sprint 23 quality-gate validation (Alembic · FastAPI · Swagger · OpenAPI · Ruff · MyPy · Pytest) |
| ERP Core v1.18-beta Release Notes | [ERP_Core_v1.18-beta.md](../07_RELEASES/ERP_Core_v1.18-beta.md) |

---

## 2. Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-20 | Initial FRD-23 documenting implemented Customer Portal (Sprint 23 / ERD_23 / v1.18-beta). Documentation completion only — no redesign. |
| 1.1 | 2026-07-20 | Editorial lock after architect review. Status set to Locked — Ready for Future Reference. Cross References and Related Documents updated. No functional, workflow, business-rule, or architecture changes. |

---

## 3. Purpose

Provide an **enterprise external customer self-service layer** that enables authenticated customers to manage portal identity, view commercial and service information, raise support/service envelopes, access documents, communicate with internal teams, and personalize their portal experience — **without becoming the system of record** for customer, order, invoice, document, ticket, or service data.

---

## 4. Business Overview

Customer Portal is a **consume-only / envelope** domain:

- **Identity & access:** portal accounts, customer profiles, sessions, trusted devices, login audit
- **Experience:** dashboards and widgets
- **Communications:** notifications, message threads, messages
- **Commercial views:** order views, invoice views (projections)
- **Documents:** document access grants and download history
- **Requests:** support ticket and service request envelopes
- **Personalization:** preferences, saved reports, saved searches
- **Operations:** portal reports

Authoritative ownership remains with peer domains:

| Concern | Authority |
|---------|-----------|
| Party identity | `master_customer` (C-01) |
| Customer relationship | CRM |
| Orders | Sales |
| Invoices / journals | Finance (`PostingService.post_system_journal()` only) |
| Documents | Document Management |
| Support tickets | Helpdesk |
| Service requests | Service |
| Analytics | Analytics (read-only) |
| External IdP / API transport | Integration Hub |
| Optional channel order UUID | E-Commerce (not portal SoR) |

---

## 5. Objectives

1. Enable secure customer self-service for account, profile, session, and preference management.
2. Provide projected visibility of orders and invoices without mutating Sales/Finance ledgers.
3. Allow customers to obtain document access and download history under Document authority.
4. Allow customers to raise support and service envelopes that map to Helpdesk/Service UUIDs.
5. Provide portal messaging and notifications for operational communication.
6. Preserve Architecture Lock v1.1: Clean Architecture, DDD, Modular Monolith, C-01, no peer ORM writes.
7. Enforce RBAC (`portal.*`) and Foundation workflows for controlled approvals.

---

## 6. Business Scope

Scope covers the **implemented Sprint 23 Customer Portal module** (`modules/portal`) with schema `portal`, prefix `pt_`, exactly **20** business tables, API mount `/api/v1/portal`, roles `PORTAL_ADMIN` / `PORTAL_MANAGER` / `CUSTOMER_USER` / `SUPPORT_USER`, and workflows `PT_ACCOUNT_APPROVAL`, `PT_PROFILE_APPROVAL`, `PT_DOCUMENT_ACCESS`, `PT_SUPPORT_REQUEST`, `PT_SERVICE_REQUEST`.

---

## 7. In Scope

- Portal account lifecycle (draft → submit → approve → active / lock / suspend / retire)
- Customer portal profile (non-authoritative profile surface linked to `master_customer`)
- Portal session create / expire / revoke
- Trusted device registration and revoke
- Login audit recording
- Dashboard and dashboard widget configuration
- Notifications (create / update / acknowledge)
- Message threads and messages
- Order view projection / sync (`sales_order_id` UUID)
- Invoice view projection / sync (`finance_invoice_id` UUID; optional `finance_journal_id` via PostingService)
- Document access grant submit / approve / revoke
- Download history
- Support ticket envelope submit (Helpdesk UUID)
- Service request envelope submit (Service UUID)
- Saved reports / saved searches / preferences
- Portal operational reports (read / export)
- Celery jobs: session expiry, order/invoice view sync, notification dispatch, login audit retention, ticket status poller

---

## 8. Out of Scope

- Replacing CRM / Sales / Finance / Document / Helpdesk / Service as systems of record
- Duplicate customer / employee / product / department masters (C-01 forbidden)
- Peer ORM writes to `crm_*`, `sales_*`, `fin_*`, `doc_*`, `hd_*`, `svc_*`, `bi_*`, `int_*`, `ec_*`
- Full enterprise IdP / SSO product (Phase 1 uses account + session + device shells; federation via Foundation / Hub later)
- Redesign of prior modules or addition of new portal business tables beyond the locked 20
- Native mobile app product delivery (API-capable; UI product is separate)

---

## 9. Stakeholders

| Stakeholder | Interest |
|-------------|----------|
| External customers | Self-service access to orders, invoices, documents, tickets, messages |
| Portal Admin | Account governance, locks, approvals, reports |
| Portal Manager | Day-to-day portal operations and mid-level approvals |
| Support User | Ticket / message / document-access support operations |
| Sales / Finance / Document / Helpdesk / Service owners | Preserve SoR boundaries |
| Security / Compliance | Login audit, device trust, RBAC |
| Enterprise Architect | Architecture Lock v1.1 compliance |

---

## 10. User Roles

| Role | Status | Intent |
|------|--------|--------|
| `PORTAL_ADMIN` | `active` | Full `portal.*` including approve / lock / revoke |
| `PORTAL_MANAGER` | `active` | Operational management excluding approve / lock |
| `CUSTOMER_USER` | `active` | Customer-facing self-service subset (no approve / lock / revoke) |
| `SUPPORT_USER` | `active` | Support operations subset (tickets, messages, document access support) |

Namespace: **`portal.*`**

---

## 11. Business Processes

### 11.1 Account onboarding
Draft account → submit (`PT_ACCOUNT_APPROVAL`) → approve → activate → optional lock/suspend → retire.

### 11.2 Profile maintenance
Customer maintains portal profile → submit (`PT_PROFILE_APPROVAL`) → approve → active/inactive. Master customer remains SoR.

### 11.3 Session & device security
Login creates session; trusted devices may be registered; sessions expire/revoke; events written to login audit.

### 11.4 Commercial visibility
Order/invoice views refreshed from Sales/Finance; customers browse projected status; no ledger mutation.

### 11.5 Document self-service
Document access requested/granted (`PT_DOCUMENT_ACCESS`) → download history recorded; Document module remains SoR.

### 11.6 Support & service intake
Customer raises support ticket / service request envelope → workflow routing → Helpdesk/Service UUID stored; peers remain SoR.

### 11.7 Messaging & notifications
Portal notifications delivered; message threads/messages support conversation around tickets, orders, invoices, documents.

### 11.8 Personalization & reporting
Preferences, saved searches/reports; portal operational reports finalized for admins.

---

## 12. Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-CP-001 | System shall manage portal accounts linked to `master_customer` with submit/approve/lock capabilities. |
| FR-CP-002 | System shall manage customer portal profiles without replacing CRM or master customer. |
| FR-CP-003 | System shall manage portal sessions with active/expired/revoked lifecycle. |
| FR-CP-004 | System shall register and revoke trusted devices. |
| FR-CP-005 | System shall record login success/failure/logout/lockout/password-reset audit events. |
| FR-CP-006 | System shall provide dashboards and configurable widgets. |
| FR-CP-007 | System shall create, update, and acknowledge portal notifications. |
| FR-CP-008 | System shall support message threads and messages between customer accounts and internal employees. |
| FR-CP-009 | System shall maintain order views as projections referencing Sales order UUIDs only. |
| FR-CP-010 | System shall maintain invoice views as projections referencing Finance invoice UUIDs only. |
| FR-CP-011 | System shall manage document access grants with submit/approve/revoke. |
| FR-CP-012 | System shall record document download history. |
| FR-CP-013 | System shall create support ticket envelopes mapped to Helpdesk ticket UUIDs. |
| FR-CP-014 | System shall create service request envelopes mapped to Service request UUIDs. |
| FR-CP-015 | System shall manage preferences, saved reports, and saved searches. |
| FR-CP-016 | System shall produce portal operational reports with read/export permissions. |
| FR-CP-017 | System shall enforce `portal.*` RBAC and Foundation workflow seeds listed in §15. |
| FR-CP-018 | System shall never ORM-write peer business schemas; Finance journals only via `PostingService.post_system_journal()`. |

---

## 13. Module Features

### Implemented aggregates (20 tables)

| # | Table | Feature |
|---|-------|---------|
| 1 | `pt_portal_account` | Portal login identity |
| 2 | `pt_customer_profile` | Self-service profile surface |
| 3 | `pt_portal_session` | Authenticated sessions |
| 4 | `pt_dashboard` | Personal / managed dashboards |
| 5 | `pt_dashboard_widget` | Dashboard widgets |
| 6 | `pt_notification` | Portal notifications |
| 7 | `pt_message_thread` | Conversation threads |
| 8 | `pt_message` | Message bodies |
| 9 | `pt_order_view` | Sales order projections |
| 10 | `pt_invoice_view` | Finance invoice projections |
| 11 | `pt_document_access` | Document entitlement envelopes |
| 12 | `pt_support_ticket` | Helpdesk ticket envelopes |
| 13 | `pt_service_request` | Service request envelopes |
| 14 | `pt_download_history` | Download audit trail |
| 15 | `pt_saved_report` | Saved report bookmarks |
| 16 | `pt_saved_search` | Saved search criteria |
| 17 | `pt_preference` | UX / locale preferences |
| 18 | `pt_device` | Trusted devices |
| 19 | `pt_login_audit` | Login security audit |
| 20 | `pt_report` | Portal operational reports |

---

## 14. Business Rules

1. Portal is **not** system of record for orders, invoices, documents, tickets, service requests, or customer master.
2. **C-01:** only `master_customer`, `master_employee`, `master_product`, `org_department` are authoritative masters.
3. CRM remains relationship authority — optional CRM UUID only; no `crm_*` ORM writes.
4. Sales remains order authority — `sales_order_id` UUID only.
5. Finance remains invoice authority — invoice UUID; journals only via `PostingService.post_system_journal()`.
6. Document remains document authority — `document_id` UUID only.
7. Helpdesk / Service remain ticket / request authority — UUID + service APIs.
8. Soft delete + optimistic versioning on mutable `pt_*` tables.
9. Credentials stored as vault/hash refs only — never plaintext.
10. Analytics read-only; Integration Hub transport only; E-Commerce optional channel UUID only.
11. No peer ORM writes.

---

## 15. Workflow

| Workflow Code | Document | Path |
|---------------|----------|------|
| `PT_ACCOUNT_APPROVAL` | Portal Account | Support User → Portal Manager → Portal Admin |
| `PT_PROFILE_APPROVAL` | Customer Profile | Customer User → Portal Manager → Portal Admin |
| `PT_DOCUMENT_ACCESS` | Document Access | Support User → Portal Manager → Portal Admin |
| `PT_SUPPORT_REQUEST` | Support Ticket | Customer User → Support User → Portal Manager |
| `PT_SERVICE_REQUEST` | Service Request | Customer User → Support User → Portal Manager |

Instances use Foundation `wf_instance`. Seed-only definitions; `is_parallel` only on `wf_step`.

---

## 16. Notifications

Portal notifications (`pt_notification`) support operational types including order update, invoice ready, document shared, ticket update, service update, message, and system events.

Delivery statuses include pending / sent / failed / read; acknowledge action supported under `portal.notification:acknowledge`.

Platform Notification (Foundation) and Integration Hub may transport delivery; portal stores portal-scoped notification rows.

Celery: `portal.notification_dispatcher`.

---

## 17. Reports

Portal operational reports (`pt_report`) cover metrics such as active users, login failures, ticket volume, service volume, document downloads, and session metrics.

Saved reports (`pt_saved_report`) may reference Analytics report UUIDs read-only.

Permissions: `portal.report:read`, `portal.report:export`.

---

## 18. Audit Requirements

- Soft-delete and version columns on mutable portal tables.
- `pt_login_audit` for authentication events.
- `pt_download_history` for document download events.
- Foundation Audit Service used by portal services for significant mutations.
- Workflow instance linkage on approval-bearing entities.

---

## 19. Security Requirements

- RBAC namespace `portal.*` with four seeded roles.
- Tenant and company isolation on portal tables.
- Session expiry / revoke; device trust revoke.
- Credential vault/hash refs only.
- No peer schema ORM writes; UUID/service boundaries enforced.
- Finance posting restricted to `PostingService.post_system_journal()`.

---

## 20. Integration Requirements

| Module | Pattern |
|--------|---------|
| Master Data | `master_customer` · `master_employee` · `master_product` (C-01) |
| Organization | `org_department` FK (optional on account) |
| CRM | Relationship UUID optional — no CRM ORM writes |
| Sales | Order authority via `sales_order_id` UUID / sync jobs |
| Finance | Invoice UUID + PostingService only |
| Document | `document_id` UUID for access/download |
| Helpdesk | Ticket UUID via service |
| Service | Service request UUID via service |
| Analytics | Read-only report refs |
| Integration Hub | IdP / API transport UUID only |
| E-Commerce | Optional `ec_order_id` UUID |
| Foundation | Workflow, RBAC, Audit, Notification, Celery |

---

## 21. Non Functional Requirements

| Area | Requirement |
|------|-------------|
| Architecture | Clean Architecture · DDD · Modular Monolith · Architecture Lock v1.1 |
| Scalability | Stateless API; Celery for sync/dispatch/retention |
| Reliability | Soft delete; optimistic locking (`version`) |
| Observability | Login audit + Foundation audit |
| Performance | Projection sync jobs for order/invoice views |
| Extensibility | Adapter ports for peers (UUID/services) |
| Compliance | Tenant isolation; least-privilege RBAC |

---

## 22. Acceptance Criteria

1. Exactly 20 `pt_*` tables in schema `portal` as implemented.
2. API available under `/api/v1/portal` for all aggregates listed in ERD_23.
3. Roles and permissions seeded as `portal.*` with four roles.
4. Five `PT_*` workflows seeded and usable via Foundation.
5. Order/invoice views never mutate Sales/Finance ORM tables.
6. Support/service envelopes store peer UUIDs only.
7. Document access stores Document UUID only.
8. Finance journal writes only through PostingService when portal fee configured.
9. Celery tasks registered: session_expiry_sweeper, order_view_sync, invoice_view_sync, notification_dispatcher, login_audit_retention, ticket_status_poller.
10. Architecture Lock v1.1 preserved; no redesign of prior modules.

---

## 23. Assumptions

1. One `master_customer` may have one primary portal profile and one or more portal accounts (delegates).
2. Order/invoice views are projections refreshed from authoritative modules.
3. Portal support ticket / service request creation invokes peer services and stores returned UUIDs.
4. Message thread is parent of messages.
5. Sprint 23 implementation and ERP Core v1.18-beta release already completed; this FRD is documentation completion.

---

## 24. Constraints

1. Architecture Lock v1.1 immutable.
2. No new business capabilities beyond implemented Sprint 23 scope.
3. No new tables beyond locked ERD_23 set.
4. No peer ORM writes.
5. C-01 masters only.
6. Finance PostingService-only for journals.

---

## 25. Traceability

| Artifact | Reference |
|----------|-----------|
| BRD | Enterprise BRD v1.0 — Self-Service / Portal capabilities |
| ERD | ERD_23 Customer Portal & Self-Service Portal (Locked) |
| SDD / DBS | SDD v1.1 · DBS v1.1 |
| Implementation | `apps/api/src/modules/portal/` |
| Migrations | `0421`–`0442` · head `0442_seed_portal_workflows` |
| Release | ERP Core v1.18-beta |
| Sprint 23 Completion Report | Sprint 23 implementation completion |
| Sprint 23 Validation Report | Sprint 23 quality-gate validation |
| Architecture Lock | v1.1 |

---

## 26. Future Enhancements

- Full IdP / SSO federation via Foundation / Integration Hub
- Richer real-time push notification channels
- Expanded Analytics-driven customer dashboards (still read-only)
- Deeper E-Commerce channel UX (UUID only; no portal SoR)
- Mobile-first UX product layer over existing APIs

*(Enhancements must not violate Architecture Lock or C-01.)*

---

## 27. Phase Gate

| # | Gate Criterion | Status |
|---|----------------|--------|
| 1 | Business tables = 20; schema = `portal`; prefix = `pt_` | ✅ |
| 2 | Documents implemented Customer Portal only (no redesign) | ✅ |
| 3 | C-01 masters consumed; no duplicates | ✅ |
| 4 | CRM/Sales/Finance/Document/Helpdesk/Service authorities preserved | ✅ |
| 5 | Finance PostingService-only; Analytics read-only; Hub transport-only | ✅ |
| 6 | Workflows `PT_*` and RBAC `portal.*` documented | ✅ |
| 7 | Architecture Lock v1.1 preserved | ✅ |
| 8 | Traceable to ERD_23 + Sprint 23 implementation / v1.18-beta | ✅ |
| 9 | Architect review completed; FRD editorially locked | ✅ |

**Phase Gate: PASS — Locked — Ready for Future Reference**

---

## 28. Document Status

| Field | Value |
|-------|--------|
| **FRD Status** | Locked — Ready for Future Reference |
| **Design** | ERD_23 Locked |
| **Implementation** | Completed (Sprint 23) |
| **Release** | ERP Core v1.18-beta |
| **Editorial Lock** | v1.1 — Editorial lock after architect review |
| **Architecture Lock** | v1.1 — Unchanged |

---

## Validation

| Check | Result |
|-------|--------|
| Document structure preserved | PASS |
| Functional Requirements unchanged | PASS |
| Business Rules unchanged | PASS |
| Workflow definitions unchanged | PASS |
| Integration requirements unchanged | PASS |
| Acceptance Criteria unchanged | PASS |
| Traceability preserved | PASS |
| Related Documents added | PASS |
| Cross References updated | PASS |
| Architecture Lock v1.1 preserved | PASS |
| Status = Locked | PASS |

---

**FRD-23 Customer Portal & Self-Service Portal is locked and ready for future reference.**

This document reflects the implemented Sprint 23 module and ERP Core v1.18-beta release without introducing any redesign. Architecture Lock v1.1 is unchanged.
