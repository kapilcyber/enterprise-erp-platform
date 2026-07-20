"""Idempotently create or reset the development Finance administrator.

The plaintext password must be supplied through FINANCE_SEED_PASSWORD and is
never persisted outside the normal bcrypt password hash.
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from database.session import SessionLocal  # noqa: E402
from security.password import PasswordHasher  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed the Finance development administrator")
    parser.add_argument("--email", default="finance.admin@example.com")
    parser.add_argument("--tenant-code", default="BOOTSTRAP")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    password = os.environ.get("FINANCE_SEED_PASSWORD")
    if not password:
        raise SystemExit("FINANCE_SEED_PASSWORD must be set")

    now = datetime.now(timezone.utc)
    password_hash = PasswordHasher.hash_password(password)

    with SessionLocal.begin() as db:
        tenant = db.execute(
            text(
                """
                SELECT id FROM foundation.sec_tenant
                WHERE tenant_code = :code AND status = 'active' AND is_deleted = false
                """
            ),
            {"code": args.tenant_code},
        ).first()
        if tenant is None:
            raise SystemExit(
                f"Active tenant {args.tenant_code!r} was not found; run migrations first"
            )
        tenant_id = tenant[0]

        existing = db.execute(
            text(
                """
                SELECT id FROM foundation.sec_user
                WHERE tenant_id = :tenant_id AND lower(email) = lower(:email)
                """
            ),
            {"tenant_id": tenant_id, "email": args.email},
        ).first()

        if existing:
            user_id = existing[0]
            db.execute(
                text(
                    """
                    UPDATE foundation.sec_user
                    SET password_hash = :password_hash, display_name = 'Finance Administrator',
                        user_type = 'super_admin', status = 'active', mfa_enabled = false,
                        failed_login_count = 0, locked_until = NULL, is_deleted = false,
                        updated_at = :now, version = version + 1
                    WHERE id = :user_id
                    """
                ),
                {"password_hash": password_hash, "now": now, "user_id": user_id},
            )
            action = "reset"
        else:
            user_id = uuid4()
            db.execute(
                text(
                    """
                    INSERT INTO foundation.sec_user
                    (id, tenant_id, email, password_hash, display_name, user_type, status,
                     mfa_enabled, failed_login_count, created_at, updated_at, version, is_deleted)
                    VALUES
                    (:id, :tenant_id, :email, :password_hash, 'Finance Administrator',
                     'super_admin', 'active', false, 0, :now, :now, 1, false)
                    """
                ),
                {
                    "id": user_id,
                    "tenant_id": tenant_id,
                    "email": args.email,
                    "password_hash": password_hash,
                    "now": now,
                },
            )
            action = "created"

        roles = db.execute(
            text(
                """
                SELECT id, role_code FROM foundation.sec_role
                WHERE tenant_id = :tenant_id
                  AND role_code IN ('SUPER_ADMIN', 'FINANCE_MANAGER', 'CFO')
                  AND status = 'active' AND is_deleted = false
                """
            ),
            {"tenant_id": tenant_id},
        ).all()
        role_codes = {row.role_code for row in roles}
        if "SUPER_ADMIN" not in role_codes:
            raise SystemExit("SUPER_ADMIN role was not found; run foundation migrations first")

        for role_id, _role_code in roles:
            assigned = db.execute(
                text(
                    """
                    SELECT 1 FROM foundation.sec_user_role
                    WHERE user_id = :user_id AND role_id = :role_id
                    """
                ),
                {"user_id": user_id, "role_id": role_id},
            ).first()
            if not assigned:
                db.execute(
                    text(
                        """
                        INSERT INTO foundation.sec_user_role
                        (id, tenant_id, user_id, role_id, assigned_at)
                        VALUES (:id, :tenant_id, :user_id, :role_id, :now)
                        """
                    ),
                    {
                        "id": uuid4(),
                        "tenant_id": tenant_id,
                        "user_id": user_id,
                        "role_id": role_id,
                        "now": now,
                    },
                )

    print(f"Finance administrator {action}")
    print(f"tenant_id={tenant_id}")
    print(f"user_id={user_id}")
    print(f"email={args.email}")
    print(f"roles={','.join(sorted(role_codes))}")


if __name__ == "__main__":
    main()
