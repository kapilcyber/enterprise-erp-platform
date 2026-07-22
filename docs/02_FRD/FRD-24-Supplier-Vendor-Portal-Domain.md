# FRD-24 — Supplier / Vendor Portal

## 1. Document Control

| Field | Value |
|-------|--------|
| **Document ID** | FRD-24 |
| **Document Title** | Supplier / Vendor Portal Domain |
| **Domain** | Supplier / Vendor Portal (`vendor_portal` / `vp_*`) |
| **Version** | 1.1 |
| **Status** | Locked — Ready for Future Reference |
| **Classification** | Internal — Confidential |
| **Aligned To** | BRD v1.0 · SDD v1.1 · DBS v1.1 · Architecture Lock v1.1 · ERD_24 (Locked) · ERP Core v1.19-beta (Sprint 24) |
| **Implementation Source of Truth** | `apps/api/src/modules/vendor_portal/` |
| **API Mount** | `/api/v1/vendor-portal` |
| **Schema / Prefix** | `vendor_portal` / `vp_` |
| **Business Tables** | Exactly **20** |
| **Predecessor Release** | ERP Core v1.18-beta |
| **Delivered In** | ERP Core v1.19-beta |

### Cross References

- Upstream: [FRD-01 Foundation Domain](./FRD-01-Foundation-Domain.md) · [FRD-02 Organization Domain](./FRD-02-Organization-Domain.md) · [FRD-03 Master Data Domain](./FRD-03-Master-Data-Domain.md) · [FRD-04 Finance & Accounting Domain](./FRD-04-Finance-Accounting-Domain.md) · [FRD-07 Procurement Domain](./FRD-07-Procurement-Domain.md) · [FRD-08 Inventory & Warehouse Domain](./FRD-08-Inventory-Warehouse-Domain.md) · [FRD-14 Quality Management Domain](./FRD-14-Quality-Management-Domain.md) · [FRD-18 BI / Reporting / Analytics Domain](./FRD-18-BI-Reporting-Analytics-Domain.md) · [FRD-19 Document Management System Domain](./FRD-19-Document-Management-System-Domain.md) · [FRD-21 Integration Hub & Enterprise Platform Services](./FRD-21-Integration-Hub-Enterprise-Platform-Services.md) · [FRD-23 Customer Portal & Self-Service Portal Domain](./FRD-23-Customer-Portal-Domain.md)
- Design: [ERD_24 Supplier / Vendor Portal (Locked)](../06_ERD/ERD_24_Supplier_Vendor_Portal.md)
- Sprint 24 Completion Report (Sprint 24 implementation completion)
- Sprint 24 Validation Report (Sprint 24 quality-gate validation)
- Release: [ERP Core v1.19-beta Release Notes](../07_RELEASES/ERP_Core_v1.19-beta.md)

---

## 2. Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-20 | Initial FRD-24 documenting implemented Supplier / Vendor Portal (Sprint 24 / ERD_24 / v1.19-beta). Documentation completion only — no redesign. |
| 1.1 | 2026-07-20 | Editorial lock after architect review. Cross references synchronized with Sprint 24 Completion Report, Sprint 24 Validation Report and ERP Core v1.19-beta. No functional changes. |

---

## 3. Purpose

Provide an **enterprise external supplier / vendor self-service layer** that enables authenticated suppliers to manage portal identity, view RFQs and purchase orders, submit quotations / acknowledgements / ASNs / invoices, track payment status, access documents, communicate with procurement and quality teams, and personalize portal experience — **without becoming the system of record** for vendor master, RFQ, purchase order, receipt, invoice, payment, quality, or document data.

---

## 4. Business Overview

Supplier / Vendor Portal is a **consume-only / envelope** domain:

- **Identity & access:** portal accounts, supplier profiles, sessions, login audit
- **Experience:** dashboards and widgets
- **Sourcing:** RFQ views, quote submission envelopes
- **Fulfilment:** purchase-order views, PO acknowledgements, delivery schedules, ASN envelopes
- **Commercial:** invoice submission envelopes, payment-status projections
- **Documents & communications:** document access, notifications, message threads, messages
- **Personalization & operations:** preferences, portal reports

Authoritative ownership remains with peer domains:

| Concern | Authority |
|---------|-----------|
| Party identity | `master_vendor` (C-01) |
| RFQ / quote / PO / purchase-invoice | Procurement |
| ASN → receipt / GRN | Inventory |
| Payment / journals | Finance (`PostingService.post_system_journal()` only) |
| Quality NCR / inspection | Quality |
| Documents | Document Management |
| Analytics | Analytics (read-only) |
| External IdP / API transport | Integration Hub |

---

## 5. Objectives

1. Enable secure supplier self-service for account, profile, session, and preference management.
2. Provide projected visibility of RFQs, purchase orders, and payment status without mutating Procurement / Finance ledgers.
3. Allow suppliers to submit quotation, PO acknowledgement, ASN, and invoice envelopes mapped to peer UUIDs.
4. Allow suppliers to obtain document access under Document authority.
5. Provide portal messaging and notifications, including quality-issue response threads.
6. Preserve Architecture Lock v1.1: Clean Architecture, DDD, Modular Monolith, C-01, no peer ORM writes.
7. Enforce RBAC (`vendor_portal.*`) and Foundation workflows for controlled approvals.

---

## 6. Business Scope

Scope covers the **implemented Sprint 24 Supplier / Vendor Portal module** (`modules/vendor_portal`) with schema `vendor_portal`, prefix `vp_`, exactly **20** business tables, API mount `/api/v1/vendor-portal`, roles `VENDOR_PORTAL_ADMIN` / `PROCUREMENT_MANAGER` / `SUPPLIER_USER` / `QUALITY_COORDINATOR`, and workflows `VP_ACCOUNT_APPROVAL`, `VP_QUOTE_SUBMISSION`, `VP_PO_ACKNOWLEDGEMENT`, `VP_INVOICE_SUBMISSION`, `VP_ASN_APPROVAL`.

---

## 7. In Scope

- Vendor portal account lifecycle (draft → submit → approve → active / lock / suspend / retire)
- Supplier portal profile (non-authoritative profile surface linked to `master_vendor`)
- Portal session create / expire / revoke
- Login audit recording
- Dashboard and dashboard widget configuration
- RFQ view projection / sync (`proc_rfq_header_id` UUID)
- Quote submission envelope submit / approve (Procurement quotation UUID)
- Purchase-order view projection / sync
- PO acknowledgement envelope submit / approve
- Delivery schedule maintenance
- ASN envelope submit / approve (Inventory receipt / GRN UUID)
- Invoice submission envelope submit / approve (Procurement / Finance AP UUID)
- Payment status projection / sync
- Document access grant submit / approve / revoke
- Notifications (create / update / acknowledge)
- Message threads and messages (including quality-issue response threads)
- Preferences
- Portal operational reports (read / export)
- Celery jobs: session expiry, RFQ/PO/payment sync, notification dispatch, login audit retention, ASN status poller, quality issue poller

---

## 8. Out of Scope

- Replacing Procurement as RFQ / quote / PO / purchase-invoice system of record
- Replacing Inventory as receipt / GRN system of record
- Replacing Finance as payment / journal system of record
- Replacing Quality as NCR / inspection / CAPA system of record
- Replacing Document Management as document system of record
- Duplicate vendor / employee / product / department masters (C-01 forbidden)
- Peer ORM writes to `proc_*`, `inv_*`, `fin_*`, `qm_*`, `doc_*`, `bi_*`, `int_*`
- Full enterprise IdP / SSO product (Phase 1 uses account + session shells; federation via Foundation / Hub later)
- Redesign of prior modules or addition of new vendor-portal business tables beyond the locked 20
- Native mobile app product delivery (API-capable; UI product is separate)

---

## 9. Stakeholders

| Stakeholder | Interest |
|-------------|----------|
| External suppliers / vendors | Self-service RFQ, PO, ASN, invoice, payment, document, message access |
| Vendor Portal Admin | Account governance, locks, approvals, reports |
| Procurement Manager | Quote / PO ack / ASN / invoice operational approvals |
| Supplier User | Day-to-day supplier self-service |
| Quality Coordinator | ASN review and quality-issue response threads |
| Procurement / Inventory / Finance / Quality / Document owners | Preserve SoR boundaries |
| Security / Compliance | Login audit, RBAC |
| Enterprise Architect | Architecture Lock v1.1 compliance |

---

## 10. User Roles

| Role | Status | Intent |
|------|--------|--------|
| `VENDOR_PORTAL_ADMIN` | `active` | Full `vendor_portal.*` including approve / lock / revoke |
| `PROCUREMENT_MANAGER` | `active` | Operational management excluding lock |
| `SUPPLIER_USER` | `active` | Supplier-facing self-service subset (no approve / lock) |
| `QUALITY_COORDINATOR` | `active` | Quality response, ASN, document access, messaging / notification subset |

Namespace: **`vendor_portal.*`**

---

## 11. Business Processes

### 11.1 Account onboarding
Draft account → submit (`VP_ACCOUNT_APPROVAL`) → approve → activate → optional lock/suspend → retire.

### 11.2 Profile maintenance
Supplier maintains portal profile → submit / approve → active/inactive. Master vendor remains SoR.

### 11.3 Session security
Login creates session; sessions expire/revoke; events written to login audit.

### 11.4 Sourcing participation
RFQ views refreshed from Procurement; supplier submits quote envelopes; Procurement remains quote SoR.

### 11.5 Order fulfilment
PO views refreshed from Procurement; supplier acknowledges PO; maintains delivery schedules; submits ASN envelopes mapped to Inventory receipt UUID.

### 11.6 Commercial settlement
Supplier submits invoice envelopes; payment status projected from Finance; no ledger mutation from portal.

### 11.7 Document self-service
Document access requested/granted → Document module remains SoR.

### 11.8 Messaging, quality response & notifications
Portal notifications delivered; message threads support procurement / quality conversations; quality UUID hooks via services only.

### 11.9 Personalization & reporting
Preferences; portal operational reports for admins / managers.

---

## 12. Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-VP-001 | System shall manage vendor portal accounts linked to `master_vendor` with submit/approve/lock capabilities. |
| FR-VP-002 | System shall manage supplier portal profiles without replacing master vendor. |
| FR-VP-003 | System shall manage portal sessions with active/expired/revoked lifecycle. |
| FR-VP-004 | System shall record login success/failure/logout/lockout/password-reset audit events. |
| FR-VP-005 | System shall provide dashboards and configurable widgets. |
| FR-VP-006 | System shall maintain RFQ views as projections referencing Procurement RFQ UUIDs only. |
| FR-VP-007 | System shall create quote submission envelopes mapped to Procurement quotation UUIDs. |
| FR-VP-008 | System shall maintain purchase-order views as projections referencing Procurement PO UUIDs only. |
| FR-VP-009 | System shall create PO acknowledgement envelopes with submit/approve. |
| FR-VP-010 | System shall manage delivery schedules linked to PO views / acknowledgements. |
| FR-VP-011 | System shall create ASN envelopes mapped to Inventory receipt / GRN UUIDs. |
| FR-VP-012 | System shall create invoice submission envelopes mapped to Procurement / Finance AP UUIDs. |
| FR-VP-013 | System shall maintain payment-status projections referencing Finance payment UUIDs only. |
| FR-VP-014 | System shall manage document access grants with submit/approve/revoke. |
| FR-VP-015 | System shall create, update, and acknowledge portal notifications. |
| FR-VP-016 | System shall support message threads and messages between supplier accounts and internal employees. |
| FR-VP-017 | System shall support quality-issue response communications via threads / messages with Quality UUID refs only. |
| FR-VP-018 | System shall manage preferences and portal operational reports with read/export permissions. |
| FR-VP-019 | System shall enforce `vendor_portal.*` RBAC and Foundation workflow seeds listed in §15. |
| FR-VP-020 | System shall never ORM-write peer business schemas; Finance journals only via `PostingService.post_system_journal()`. |

---

## 13. Module Features

### Implemented aggregates (20 tables)

| # | Table | Feature |
|---|-------|---------|
| 1 | `vp_portal_account` | Supplier portal login identity |
| 2 | `vp_supplier_profile` | Self-service supplier profile surface |
| 3 | `vp_portal_session` | Authenticated sessions |
| 4 | `vp_dashboard` | Supplier / managed dashboards |
| 5 | `vp_dashboard_widget` | Dashboard widgets |
| 6 | `vp_rfq_view` | Procurement RFQ projections |
| 7 | `vp_quote_submission` | Quote submission envelopes |
| 8 | `vp_purchase_order_view` | Procurement PO projections |
| 9 | `vp_po_acknowledgement` | PO acknowledgement envelopes |
| 10 | `vp_delivery_schedule` | Promised delivery commitments |
| 11 | `vp_asn` | Advance shipping notice envelopes |
| 12 | `vp_invoice_submission` | Vendor invoice submission envelopes |
| 13 | `vp_payment_status` | Finance payment projections |
| 14 | `vp_document_access` | Document entitlement envelopes |
| 15 | `vp_notification` | Portal notifications |
| 16 | `vp_message_thread` | Conversation threads |
| 17 | `vp_message` | Message bodies |
| 18 | `vp_preference` | UX / locale preferences |
| 19 | `vp_login_audit` | Login security audit |
| 20 | `vp_report` | Portal operational reports |

---

## 14. Business Rules

1. Vendor Portal is **not** system of record for RFQ, quote, PO, receipt, invoice, payment, quality, documents, or vendor master.
2. **C-01:** only `master_vendor`, `master_employee`, `master_product`, `org_department` are authoritative masters.
3. Procurement remains RFQ / quote / PO / purchase-invoice authority — UUID / services only; no `proc_*` ORM writes.
4. Inventory remains receipt authority — ASN stores receipt / GRN UUID; no `inv_*` ORM writes.
5. Finance remains payment authority — payment UUID; journals only via `PostingService.post_system_journal()`.
6. Quality remains quality authority — NCR / inspection UUID via service; no `qm_*` ORM writes.
7. Document remains document authority — `document_id` UUID only.
8. Soft delete + optimistic versioning on mutable `vp_*` tables.
9. Credentials stored as vault/hash refs only — never plaintext.
10. Analytics read-only; Integration Hub transport only.
11. No peer ORM writes.

---

## 15. Workflow

| Workflow Code | Document | Path |
|---------------|----------|------|
| `VP_ACCOUNT_APPROVAL` | Portal Account | Supplier User → Procurement Manager → Vendor Portal Admin |
| `VP_QUOTE_SUBMISSION` | Quote Submission | Supplier User → Procurement Manager → Vendor Portal Admin |
| `VP_PO_ACKNOWLEDGEMENT` | PO Acknowledgement | Supplier User → Procurement Manager |
| `VP_INVOICE_SUBMISSION` | Invoice Submission | Supplier User → Procurement Manager → Vendor Portal Admin |
| `VP_ASN_APPROVAL` | ASN | Supplier User → Procurement Manager → Quality Coordinator → Vendor Portal Admin |

Instances use Foundation `wf_instance`. Seed-only definitions; `is_parallel` only on `wf_step`.

---

## 16. Notifications

Portal notifications (`vp_notification`) support operational types including RFQ invite, quote decision, PO issued, PO ack required, delivery reminder, ASN update, invoice decision, payment update, quality issue, document shared, message, and system events.

Delivery statuses include pending / sent / failed / read; acknowledge action supported under `vendor_portal.notification:acknowledge`.

Platform Notification (Foundation) and Integration Hub may transport delivery; portal stores portal-scoped notification rows.

Celery: `vendor_portal.notification_dispatcher`.

---

## 17. Reports

Portal operational reports (`vp_report`) cover metrics such as active suppliers, login failures, open RFQs, quote volume, PO acknowledgements, ASN volume, invoice submissions, payment status, quality-open counts, and session metrics.

Analytics may consume portal metrics read-only.

Permissions: `vendor_portal.report:read`, `vendor_portal.report:export`.

---

## 18. Audit Requirements

- Soft-delete and version columns on mutable vendor portal tables.
- `vp_login_audit` for authentication events.
- Foundation Audit Service used by vendor portal services for significant mutations.
- Workflow instance linkage on approval-bearing entities (account, quote, PO ack, ASN, invoice, document access).

---

## 19. Security Requirements

- RBAC namespace `vendor_portal.*` with four seeded roles.
- Tenant and company isolation on vendor portal tables.
- Session expiry / revoke.
- Credential vault/hash refs only.
- No peer schema ORM writes; UUID/service boundaries enforced.
- Finance posting restricted to `PostingService.post_system_journal()`.

---

## 20. Integration Requirements

| Module | Pattern |
|--------|---------|
| Master Data | `master_vendor` · `master_employee` · `master_product` (C-01) |
| Organization | `org_department` FK (optional on account) |
| Procurement | RFQ / quote / PO / purchase-invoice authority via UUID / services — no `proc_*` ORM writes |
| Inventory | Receipt authority via ASN → receipt / GRN UUID — no `inv_*` ORM writes |
| Finance | Payment UUID + PostingService only — no `fin_*` ORM writes |
| Quality | NCR / inspection UUID via service — no `qm_*` ORM writes |
| Document Management | `document_id` UUID for access — no Document ORM writes |
| Analytics | Read-only consumer of portal metrics |
| Integration Hub | IdP / API transport UUID only |
| Foundation | Workflow, RBAC, Audit, Notification, Celery |

---

## 21. Non Functional Requirements

| Area | Requirement |
|------|-------------|
| Architecture | Clean Architecture · DDD · Modular Monolith · Architecture Lock v1.1 |
| Scalability | Stateless API; Celery for sync/dispatch/retention/polling |
| Reliability | Soft delete; optimistic locking (`version`) |
| Observability | Login audit + Foundation audit |
| Performance | Projection sync jobs for RFQ / PO / payment views |
| Extensibility | Adapter ports for peers (UUID/services) |
| Compliance | Tenant isolation; least-privilege RBAC |

---

## 22. Acceptance Criteria

1. Exactly 20 `vp_*` tables in schema `vendor_portal` as implemented.
2. Vendor Portal capabilities available under `/api/v1/vendor-portal` for all aggregates listed in ERD_24.
3. Roles and permissions seeded as `vendor_portal.*` with four roles: `VENDOR_PORTAL_ADMIN`, `PROCUREMENT_MANAGER`, `SUPPLIER_USER`, `QUALITY_COORDINATOR`.
4. Five `VP_*` workflows seeded and usable via Foundation.
5. RFQ / PO / payment views never mutate Procurement / Finance ORM tables.
6. Quote / PO ack / ASN / invoice envelopes store peer UUIDs only.
7. Document access stores Document UUID only.
8. Finance journal writes only through PostingService when portal fee configured.
9. Celery tasks registered: session_expiry_sweeper, rfq_view_sync, po_view_sync, payment_status_sync, notification_dispatcher, login_audit_retention, asn_status_poller, quality_issue_poller.
10. Architecture Lock v1.1 preserved; no redesign of prior modules.

---

## 23. Assumptions

1. One `master_vendor` may have one primary supplier profile and one or more portal accounts (delegates).
2. RFQ / PO / payment views are projections refreshed from authoritative modules.
3. Quote / PO ack / ASN / invoice submission invoke peer services and store returned UUIDs.
4. Quality issue responses use message threads / messages with Quality UUID refs — no separate quality SoR table in this 20-table set.
5. Message thread is parent of messages.
6. Sprint 24 implementation and ERP Core v1.19-beta release already completed; this FRD is documentation completion.

---

## 24. Constraints

1. Architecture Lock v1.1 immutable.
2. No new business capabilities beyond implemented Sprint 24 scope.
3. No new tables beyond locked ERD_24 set.
4. No peer ORM writes.
5. C-01 masters only.
6. Procurement / Inventory / Finance / Quality / Document authorities preserved.
7. Finance PostingService-only for journals.
8. Analytics read-only; Integration Hub transport-only.

---

## 25. Traceability

| Artifact | Reference |
|----------|-----------|
| BRD | Enterprise BRD v1.0 — Supplier / Vendor Portal capabilities |
| ERD | ERD_24 Supplier / Vendor Portal (Locked) |
| SDD / DBS | SDD v1.1 · DBS v1.1 |
| Implementation | `apps/api/src/modules/vendor_portal/` |
| Migrations | `0443`–`0464` · head `0464_seed_vp_workflows` |
| Release | ERP Core v1.19-beta |
| Sprint 24 Completion Report | Sprint 24 implementation completion |
| Sprint 24 Validation Report | Sprint 24 quality-gate validation |
| Architecture Lock | v1.1 |
| Peer Portal FRD | FRD-23 Customer Portal (Locked) |

---

## 26. Future Enhancements

- Full IdP / SSO federation via Foundation / Integration Hub
- Richer real-time push notification channels
- Expanded Analytics-driven supplier dashboards (still read-only)
- Deeper quality collaboration UX (UUID / services only; no portal SoR)
- Mobile-first UX product layer over existing APIs

*(Enhancements must not violate Architecture Lock or C-01.)*

---

## 27. Phase Gate

| # | Gate Criterion | Status |
|---|----------------|--------|
| 1 | Business tables = 20; schema = `vendor_portal`; prefix = `vp_` | ✅ |
| 2 | Documents implemented Supplier / Vendor Portal only (no redesign) | ✅ |
| 3 | C-01 masters consumed; no duplicates | ✅ |
| 4 | Procurement / Inventory / Finance / Quality / Document authorities preserved | ✅ |
| 5 | Finance PostingService-only; Analytics read-only; Hub transport-only | ✅ |
| 6 | Workflows `VP_*` and RBAC `vendor_portal.*` documented | ✅ |
| 7 | Architecture Lock v1.1 preserved | ✅ |
| 8 | Traceable to ERD_24 + Sprint 24 implementation / v1.19-beta | ✅ |

**Phase Gate: PASS — Ready for Architect Review**

---

## 28. Document Status

| Field | Value |
|-------|--------|
| **FRD Status** | Locked — Ready for Future Reference |
| **Design** | ERD_24 Locked |
| **Implementation** | Completed (Sprint 24) |
| **Release** | ERP Core v1.19-beta |
| **Next** | Documentation Complete |
| **Architecture Lock** | v1.1 — Unchanged |

---

**FRD-24 Supplier / Vendor Portal is locked and ready for future reference.**
