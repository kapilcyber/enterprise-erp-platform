# ERP Core v1.19-beta — Release Notes

| Field | Value |
|-------|--------|
| **Document Type** | Enterprise Release Notes |
| **Release Name** | ERP Core v1.19-beta |
| **Release Status** | Beta Development Release |
| **Architecture Lock** | v1.1 — Maintained |
| **Prepared As** | Enterprise Solution Architect · ERP Product Architect · Technical Documentation Lead · Release Manager · Principal Software Engineer |
| **Classification** | Internal — Confidential |
| **Predecessor** | [ERP Core v1.18-beta](./ERP_Core_v1.18-beta.md) |
| **Ready For** | Sprint 25 — Next domain per ERP roadmap |

---

## 1. Release Information

| Field | Value |
|-------|--------|
| **Version** | ERP Core v1.19-beta |
| **Status** | Beta Development Release |
| **Date** | 2026-07-20 |
| **Previous Release** | ERP Core v1.18-beta |
| **Architecture Lock** | v1.1 — Preserved |
| **Recommended Git Tag** | `v1.19-beta` |

---

## 2. Sprint 24 Highlights

Sprint 24 delivered the **Supplier / Vendor Portal** domain (ERD_24) as the enterprise external supplier self-service layer — portal accounts → supplier profiles → sessions → dashboards / widgets → RFQ views → quote submissions → purchase-order views → PO acknowledgements → delivery schedules → ASN envelopes → invoice submissions → payment-status projections → document access → notifications / messages / threads → preferences → login audit → reports — while **existing masters remain authoritative (C-01)**. No duplicate employee / vendor / product / department masters. This module **provides secure self-service access** and **never becomes the system of record**: **Procurement remains RFQ / PO / quote / purchase-invoice authority**, **Inventory remains receipt authority**, **Finance remains payment / accounting authority**, **Quality remains quality authority**, **Document remains document authority**, **Analytics** remains read-only, and **Integration Hub** owns external portal / IdP / API transport (UUID / API only). Peer bindings use **UUID / services only** — **no peer ORM writes**. Finance journals use **`PostingService.post_system_journal()`** only — **no `fin_*` ORM writes**.

| Capability | Delivery |
|------------|----------|
| **Vendor Portal Module** | `apps/api/src/modules/vendor_portal/` — Clean Architecture package (domain, models, repositories, engines, services, routers, adapters, tasks) |
| **Portal Accounts** | External login identities bound to `master_vendor` with submit / approve |
| **Supplier Profiles** | Self-service supplier profile surface (`master_vendor` = party identity) |
| **Portal Sessions** | Authenticated session lifecycle |
| **Dashboards / Widgets** | Supplier / manager portal dashboards |
| **RFQ Views** | Projected Procurement RFQ views (`proc_rfq_header_id` UUID) |
| **Quote Submissions** | Quote envelopes mapped to Procurement quotation UUID |
| **Purchase Order Views** | Projected Procurement PO views |
| **PO Acknowledgements** | Acknowledgement envelopes with submit / approve |
| **Delivery Schedules** | Supplier promised delivery commitments |
| **ASN** | Advance shipment notice envelopes (`inventory_receipt_id` / GRN UUID) |
| **Invoice Submissions** | Invoice envelopes mapped to Procurement / Finance AP UUID |
| **Payment Status** | Projected Finance payment snapshots |
| **Document Access** | Document grant envelopes (`document_id` UUID) |
| **Notifications / Messages / Threads** | Portal communications (quality / support UUID hooks) |
| **Preferences / Login Audit / Reports** | Personalization, security audit, operational reports |
| **Engines (20)** | PortalAccount · SupplierProfile · PortalSession · Dashboard · DashboardWidget · RfqView · QuoteSubmission · PurchaseOrderView · PoAcknowledgement · DeliverySchedule · Asn · InvoiceSubmission · PaymentStatus · DocumentAccess · Notification · MessageThread · Message · Preference · LoginAudit · Report |

**Services:** `VendorPortalApplicationService`, entity services for all 20 aggregates, **`VendorPortalIntegrationService`**, **`VendorPortalNumberService`**.

**Supporting delivered items:** document numbering (`ACC-` / `PRF-` / `SES-` / `DSH-` / `RFQ-` / `QTE-` / `POV-` / `ACK-` / `DLS-` / `ASN-` / `INV-` / `PAY-` / `DOC-` / `NTF-` / `THR-` / `MSG-` / `AUD-`), Celery jobs (`session_expiry_sweeper`, `rfq_view_sync`, `po_view_sync`, `payment_status_sync`, `notification_dispatcher`, `login_audit_retention`, `asn_status_poller`, `quality_issue_poller`), RBAC roles (`VENDOR_PORTAL_ADMIN`, `PROCUREMENT_MANAGER`, `SUPPLIER_USER`, `QUALITY_COORDINATOR`), and workflows (`VP_ACCOUNT_APPROVAL`, `VP_QUOTE_SUBMISSION`, `VP_PO_ACKNOWLEDGEMENT`, `VP_INVOICE_SUBMISSION`, `VP_ASN_APPROVAL`).

---

## 3. Supplier / Vendor Portal Module

| Item | Value |
|------|--------|
| **Schema** | `vendor_portal` |
| **Prefix** | `vp_` |
| **Business Tables** | **20** |
| **ERD** | ERD_24 Supplier / Vendor Portal (locked) |
| **API mount** | `/api/v1/vendor-portal` |

**Tables:** `vp_portal_account`, `vp_supplier_profile`, `vp_portal_session`, `vp_dashboard`, `vp_dashboard_widget`, `vp_rfq_view`, `vp_quote_submission`, `vp_purchase_order_view`, `vp_po_acknowledgement`, `vp_delivery_schedule`, `vp_asn`, `vp_invoice_submission`, `vp_payment_status`, `vp_document_access`, `vp_notification`, `vp_message_thread`, `vp_message`, `vp_preference`, `vp_login_audit`, `vp_report`.

**Coverage:** portal accounts · supplier profiles · portal sessions · dashboards · dashboard widgets · RFQ views · quote submissions · purchase-order views · PO acknowledgements · delivery schedules · ASN · invoice submissions · payment status · document access · notifications · message threads · messages · preferences · login audit · reports.

**API mount:** `/api/v1/vendor-portal` — portal-accounts (+ submit / approve), supplier-profiles (+ submit / approve), portal-sessions, dashboards, dashboard-widgets, rfq-views, quote-submissions (+ submit / approve), purchase-order-views, po-acknowledgements (+ submit / approve), delivery-schedules, asns (+ submit / approve), invoice-submissions (+ submit / approve), payment-statuses, document-accesses (+ submit / approve), notifications, message-threads, messages, preferences, login-audits, reports.

---

## 4. Cross Module Integrations

Vendor Portal **never** duplicates employee, vendor, product, or department masters. **Existing masters remain authoritative (C-01)**. **Procurement remains RFQ / PO authority**. **Inventory remains receipt authority**. **Finance remains payment authority**. **Quality remains quality authority**. **Document remains document authority**. Peers communicate via **services · events · REST / webhooks (Integration Hub) · UUID refs** — **never** via direct ORM writes outside `vp_*`. Finance journals use **`PostingService.post_system_journal()`** only — **no `fin_*` ORM writes**. Analytics remains **read-only**. Integration Hub is **UUID / API only**. **No duplicate masters**. **No peer ORM writes**.

| Module | Integration |
|--------|-------------|
| **Master Data** | **`master_vendor` · `master_employee` · `master_product` (C-01)** — **no duplicate masters** |
| **Organization** | **`org_department` only** — no Vendor Portal department master |
| **Procurement** | **RFQ / Quote / PO / purchase-invoice authority** — UUID only — **no `proc_*` ORM writes** |
| **Inventory** | **Receipt authority** — ASN → receipt / GRN UUID — **no Inventory ORM writes** |
| **Finance** | **Payment authority** + **`PostingService.post_system_journal()`** — store `finance_journal_id` — **no `fin_*` writes** |
| **Quality** | **Quality authority** — NCR / inspection UUID — **no `qm_*` ORM writes** |
| **Document** | **Document authority** — access stores `document_id` UUID — **no Document ORM writes** |
| **Analytics** | **Read-only** consumer of portal metrics — **no Analytics ORM writes** |
| **Integration Hub** | External portal / IdP / API **REST · events · webhooks** — connector UUID refs only |
| **Foundation** | **Workflow** (`VP_ACCOUNT_APPROVAL`, `VP_QUOTE_SUBMISSION`, `VP_PO_ACKNOWLEDGEMENT`, `VP_INVOICE_SUBMISSION`, `VP_ASN_APPROVAL`); **RBAC** (`vendor_portal.*` permissions; roles `VENDOR_PORTAL_ADMIN`, `PROCUREMENT_MANAGER`, `SUPPLIER_USER`, `QUALITY_COORDINATOR` with `status='active'`) |

---

## 5. APIs

| Metric | Value |
|--------|------:|
| **Total Routes** | **1727** |
| **OpenAPI Paths** | **1080** |
| **Vendor Portal Routes** | **94** |
| **Vendor Portal OpenAPI Paths** | **~54** |

Swagger (`/docs`) and OpenAPI (`/openapi.json`) register Vendor Portal APIs under `/api/v1/vendor-portal/*`.

---

## 6. Database

| Item | Value |
|------|--------|
| **Alembic Head** | `0464_seed_vp_workflows` |
| **Migration range (this release delta)** | `0443_create_vendor_portal_schema` → `0464_seed_vp_workflows` |
| **Approximate business tables** | Approximately **428** (~408 at v1.18-beta + 20 Vendor Portal) |
| **Schemas** | prior 25 + **`vendor_portal`** (**26**) |

```text
0443_create_vendor_portal_schema
        ↓
0464_seed_vp_workflows
```

---

## 7. Quality Gates

| Gate | Status |
|------|--------|
| Alembic Head | PASS — `0464_seed_vp_workflows` (current=head; chain 0443→0464; no pending revisions) |
| FastAPI | PASS — startup successful |
| Swagger | PASS — `/docs` HTTP 200 |
| OpenAPI | PASS — `/openapi.json` generated successfully |
| Vendor Portal APIs | PASS — mounted under `/api/v1/vendor-portal` |
| Ruff | PASS |
| MyPy | PASS |
| Pytest | PASS — **189 passed (full suite)** |
| Architecture Lock v1.1 | PASS — preserved |

Validation completed for Sprint 24 Vendor Portal package wiring, ERD_24 table set, migrations 0443–0464, RBAC / workflow seeds, and hub tests.

---

## 8. Architecture Status

| Principle | Confirmation |
|-----------|--------------|
| **Architecture Lock v1.1** | **Preserved** — no Architecture Lock changes |
| **No redesign** | Prior sprints unmodified except required vendor_portal wiring (router / Celery / Alembic env) |
| **Clean Architecture** | Router → Service → Repository → Database maintained |
| **DDD** | Vendor Portal domain enums, exceptions, entities, value objects, engines |
| **Modular Monolith** | New `modules/vendor_portal` package; no service-boundary redesign |
| **Previous modules unchanged** | Confirmed — Foundation · Organization · Master Data · Finance · Sales · Procurement · Inventory · Manufacturing · Quality · CRM · HR · Payroll · Recruitment · Project · Asset · Service · Helpdesk · Document · GRC · Analytics · Integration · E-Commerce · Customer Portal untouched except required wiring |

Stack unchanged: FastAPI · SQLAlchemy 2.0 · Alembic · PostgreSQL · Redis · Celery.

---

## 9. Sprint 25 Roadmap

| Attribute | Value |
|-----------|--------|
| **Next Release** | ERP Core **v1.20-beta** (planned) |
| **Sprint** | **Sprint 25 — Next domain per ERP roadmap** |
| **Primary domain** | Per ERP product roadmap (post ERD_24) |

**Planned scope (planning only — no implementation in this release):**

- Next enterprise domain per approved ERP roadmap / FRD sequence
- Continuity with Master Data party / product masters (C-01)
- Optional cross-links to Vendor Portal · Customer Portal · Procurement · Finance via UUID / services only
- No redesign of Vendor Portal · Customer Portal · Procurement · Finance modules

---

## 10. Release Summary

| Item | Confirmation |
|------|----------------|
| Release document | `docs/07_RELEASES/ERP_Core_v1.19-beta.md` |
| Prior releases unmodified | `ERP_Core_v1.0-alpha.md` · `v1.1-beta` … · `v1.18-beta` unchanged |
| **Version** | **ERP Core v1.19-beta** |
| **Status** | Beta Development Release |
| **Modules** | Foundation · Organization · Master Data · Finance · Sales · Procurement · Inventory · Manufacturing · Quality · CRM · HR · Payroll · Recruitment · Project · Asset · Service · Helpdesk · Document · GRC · Analytics · Integration · E-Commerce · Customer Portal · **Vendor Portal** |
| **Alembic head** | **`0464_seed_vp_workflows`** |
| **Tests** | **189 passed** |
| **Routes** | **1727** FastAPI · **1080** OpenAPI · **94** Vendor Portal |
| **Quality gates** | Alembic head · Import · Router · Celery · Pytest — **PASS** |
| **Next** | **Sprint 25 — Next domain per ERP roadmap** |
| **Ready for Git Tag** | **`v1.19-beta`** |

---

## 11. Version Timeline

| Version | Date | Scope | Alembic Head | Tests |
|---------|------|--------|--------------|-------|
| **v1.18-beta** | 2026-07-16 | Sprints 0–23 (+ Customer Portal & Self-Service) | `0442_seed_portal_workflows` | 297 passed |
| **v1.19-beta** | 2026-07-20 | Sprints 0–24 (+ Supplier / Vendor Portal) | `0464_seed_vp_workflows` | +10 Vendor Portal hub |

```text
v1.18-beta ──(+ Sprint 24 Supplier / Vendor Portal)──► v1.19-beta ──► Sprint 25 (planned)
```

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-20 | Initial ERP Core v1.19-beta release notes after Sprint 24 Vendor Portal implementation |

---

**Confirmations**

- `ERP_Core_v1.19-beta.md` created successfully
- Previous release notes remain unchanged
- Ready for Git tag: **`v1.19-beta`**
- Ready to begin Sprint 25 planning
- Sprint 24 Validation completed successfully.
- Release Notes synchronized with final validation results.
- Ready for Git Tag: `v1.19-beta`.

**ERP Core v1.19-beta release documentation completed and ready for release approval.**
