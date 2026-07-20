"""Vendor Portal permission constants per ERD_24."""

VENDOR_PORTAL_PERMISSIONS: list[tuple[str, str, str, str]] = [
    ("vendor_portal.account:read", "vendor_portal.account", "read", "vendor_portal"),
    ("vendor_portal.account:create", "vendor_portal.account", "create", "vendor_portal"),
    ("vendor_portal.account:update", "vendor_portal.account", "update", "vendor_portal"),
    ("vendor_portal.account:submit", "vendor_portal.account", "submit", "vendor_portal"),
    ("vendor_portal.account:approve", "vendor_portal.account", "approve", "vendor_portal"),
    ("vendor_portal.account:lock", "vendor_portal.account", "lock", "vendor_portal"),
    ("vendor_portal.profile:read", "vendor_portal.profile", "read", "vendor_portal"),
    ("vendor_portal.profile:create", "vendor_portal.profile", "create", "vendor_portal"),
    ("vendor_portal.profile:update", "vendor_portal.profile", "update", "vendor_portal"),
    ("vendor_portal.profile:submit", "vendor_portal.profile", "submit", "vendor_portal"),
    ("vendor_portal.profile:approve", "vendor_portal.profile", "approve", "vendor_portal"),
    ("vendor_portal.session:read", "vendor_portal.session", "read", "vendor_portal"),
    ("vendor_portal.session:create", "vendor_portal.session", "create", "vendor_portal"),
    ("vendor_portal.session:update", "vendor_portal.session", "update", "vendor_portal"),
    ("vendor_portal.session:revoke", "vendor_portal.session", "revoke", "vendor_portal"),
    ("vendor_portal.login_audit:read", "vendor_portal.login_audit", "read", "vendor_portal"),
    ("vendor_portal.login_audit:create", "vendor_portal.login_audit", "create", "vendor_portal"),
    ("vendor_portal.login_audit:update", "vendor_portal.login_audit", "update", "vendor_portal"),
    ("vendor_portal.dashboard:read", "vendor_portal.dashboard", "read", "vendor_portal"),
    ("vendor_portal.dashboard:create", "vendor_portal.dashboard", "create", "vendor_portal"),
    ("vendor_portal.dashboard:update", "vendor_portal.dashboard", "update", "vendor_portal"),
    ("vendor_portal.widget:read", "vendor_portal.widget", "read", "vendor_portal"),
    ("vendor_portal.widget:create", "vendor_portal.widget", "create", "vendor_portal"),
    ("vendor_portal.widget:update", "vendor_portal.widget", "update", "vendor_portal"),
    ("vendor_portal.rfq_view:read", "vendor_portal.rfq_view", "read", "vendor_portal"),
    ("vendor_portal.rfq_view:create", "vendor_portal.rfq_view", "create", "vendor_portal"),
    ("vendor_portal.rfq_view:update", "vendor_portal.rfq_view", "update", "vendor_portal"),
    ("vendor_portal.rfq_view:sync", "vendor_portal.rfq_view", "sync", "vendor_portal"),
    ("vendor_portal.purchase_order_view:read", "vendor_portal.purchase_order_view", "read", "vendor_portal"),  # noqa: E501
    ("vendor_portal.purchase_order_view:create", "vendor_portal.purchase_order_view", "create", "vendor_portal"),  # noqa: E501
    ("vendor_portal.purchase_order_view:update", "vendor_portal.purchase_order_view", "update", "vendor_portal"),  # noqa: E501
    ("vendor_portal.purchase_order_view:sync", "vendor_portal.purchase_order_view", "sync", "vendor_portal"),  # noqa: E501
    ("vendor_portal.payment_status:read", "vendor_portal.payment_status", "read", "vendor_portal"),
    ("vendor_portal.payment_status:create", "vendor_portal.payment_status", "create", "vendor_portal"),  # noqa: E501
    ("vendor_portal.payment_status:update", "vendor_portal.payment_status", "update", "vendor_portal"),  # noqa: E501
    ("vendor_portal.payment_status:sync", "vendor_portal.payment_status", "sync", "vendor_portal"),
    ("vendor_portal.quote_submission:read", "vendor_portal.quote_submission", "read", "vendor_portal"),  # noqa: E501
    ("vendor_portal.quote_submission:create", "vendor_portal.quote_submission", "create", "vendor_portal"),  # noqa: E501
    ("vendor_portal.quote_submission:submit", "vendor_portal.quote_submission", "submit", "vendor_portal"),  # noqa: E501
    ("vendor_portal.quote_submission:update", "vendor_portal.quote_submission", "update", "vendor_portal"),  # noqa: E501
    ("vendor_portal.quote_submission:approve", "vendor_portal.quote_submission", "approve", "vendor_portal"),  # noqa: E501
    ("vendor_portal.po_acknowledgement:read", "vendor_portal.po_acknowledgement", "read", "vendor_portal"),  # noqa: E501
    ("vendor_portal.po_acknowledgement:create", "vendor_portal.po_acknowledgement", "create", "vendor_portal"),  # noqa: E501
    ("vendor_portal.po_acknowledgement:submit", "vendor_portal.po_acknowledgement", "submit", "vendor_portal"),  # noqa: E501
    ("vendor_portal.po_acknowledgement:update", "vendor_portal.po_acknowledgement", "update", "vendor_portal"),  # noqa: E501
    ("vendor_portal.po_acknowledgement:approve", "vendor_portal.po_acknowledgement", "approve", "vendor_portal"),  # noqa: E501
    ("vendor_portal.delivery_schedule:read", "vendor_portal.delivery_schedule", "read", "vendor_portal"),  # noqa: E501
    ("vendor_portal.delivery_schedule:create", "vendor_portal.delivery_schedule", "create", "vendor_portal"),  # noqa: E501
    ("vendor_portal.delivery_schedule:update", "vendor_portal.delivery_schedule", "update", "vendor_portal"),  # noqa: E501
    ("vendor_portal.asn:read", "vendor_portal.asn", "read", "vendor_portal"),
    ("vendor_portal.asn:create", "vendor_portal.asn", "create", "vendor_portal"),
    ("vendor_portal.asn:submit", "vendor_portal.asn", "submit", "vendor_portal"),
    ("vendor_portal.asn:approve", "vendor_portal.asn", "approve", "vendor_portal"),
    ("vendor_portal.asn:update", "vendor_portal.asn", "update", "vendor_portal"),
    ("vendor_portal.invoice_submission:read", "vendor_portal.invoice_submission", "read", "vendor_portal"),  # noqa: E501
    ("vendor_portal.invoice_submission:create", "vendor_portal.invoice_submission", "create", "vendor_portal"),  # noqa: E501
    ("vendor_portal.invoice_submission:submit", "vendor_portal.invoice_submission", "submit", "vendor_portal"),  # noqa: E501
    ("vendor_portal.invoice_submission:update", "vendor_portal.invoice_submission", "update", "vendor_portal"),  # noqa: E501
    ("vendor_portal.invoice_submission:approve", "vendor_portal.invoice_submission", "approve", "vendor_portal"),  # noqa: E501
    ("vendor_portal.document_access:read", "vendor_portal.document_access", "read", "vendor_portal"),  # noqa: E501
    ("vendor_portal.document_access:create", "vendor_portal.document_access", "create", "vendor_portal"),  # noqa: E501
    ("vendor_portal.document_access:submit", "vendor_portal.document_access", "submit", "vendor_portal"),  # noqa: E501
    ("vendor_portal.document_access:approve", "vendor_portal.document_access", "approve", "vendor_portal"),  # noqa: E501
    ("vendor_portal.document_access:revoke", "vendor_portal.document_access", "revoke", "vendor_portal"),  # noqa: E501
    ("vendor_portal.document_access:update", "vendor_portal.document_access", "update", "vendor_portal"),  # noqa: E501
    ("vendor_portal.notification:read", "vendor_portal.notification", "read", "vendor_portal"),
    ("vendor_portal.notification:create", "vendor_portal.notification", "create", "vendor_portal"),
    ("vendor_portal.notification:update", "vendor_portal.notification", "update", "vendor_portal"),
    ("vendor_portal.notification:acknowledge", "vendor_portal.notification", "acknowledge", "vendor_portal"),  # noqa: E501
    ("vendor_portal.message:read", "vendor_portal.message", "read", "vendor_portal"),
    ("vendor_portal.message:create", "vendor_portal.message", "create", "vendor_portal"),
    ("vendor_portal.message:update", "vendor_portal.message", "update", "vendor_portal"),
    ("vendor_portal.thread:read", "vendor_portal.thread", "read", "vendor_portal"),
    ("vendor_portal.thread:create", "vendor_portal.thread", "create", "vendor_portal"),
    ("vendor_portal.thread:update", "vendor_portal.thread", "update", "vendor_portal"),
    ("vendor_portal.preference:read", "vendor_portal.preference", "read", "vendor_portal"),
    ("vendor_portal.preference:create", "vendor_portal.preference", "create", "vendor_portal"),
    ("vendor_portal.preference:update", "vendor_portal.preference", "update", "vendor_portal"),
    ("vendor_portal.report:read", "vendor_portal.report", "read", "vendor_portal"),
    ("vendor_portal.report:export", "vendor_portal.report", "export", "vendor_portal"),
    ("vendor_portal.quality_response:read", "vendor_portal.quality_response", "read", "vendor_portal"),  # noqa: E501
    ("vendor_portal.quality_response:create", "vendor_portal.quality_response", "create", "vendor_portal"),  # noqa: E501
    ("vendor_portal.quality_response:update", "vendor_portal.quality_response", "update", "vendor_portal"),  # noqa: E501
]

_ALL = [p[0] for p in VENDOR_PORTAL_PERMISSIONS]

VENDOR_PORTAL_ADMIN_PERMISSIONS = list(_ALL)
PROCUREMENT_MANAGER_PERMISSIONS = [
    p for p in _ALL if ":lock" not in p
]
SUPPLIER_USER_PERMISSIONS = [
    p for p in _ALL
    if any(
        x in p
        for x in (
            "vendor_portal.profile",
            "vendor_portal.session",
            "vendor_portal.dashboard",
            "vendor_portal.widget",
            "vendor_portal.rfq_view",
            "vendor_portal.quote_submission",
            "vendor_portal.purchase_order_view",
            "vendor_portal.po_acknowledgement",
            "vendor_portal.delivery_schedule",
            "vendor_portal.asn",
            "vendor_portal.invoice_submission",
            "vendor_portal.payment_status",
            "vendor_portal.document_access:read",
            "vendor_portal.notification",
            "vendor_portal.message",
            "vendor_portal.thread",
            "vendor_portal.preference",
            "vendor_portal.report:read",
            "vendor_portal.quality_response",
        )
    )
    and ":approve" not in p
    and ":lock" not in p
]
QUALITY_COORDINATOR_PERMISSIONS = [
    p for p in _ALL
    if "quality_response" in p or "asn" in p or "document_access" in p or "thread" in p or "message" in p or "notification" in p  # noqa: E501
]
