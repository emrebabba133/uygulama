# Requirements Traceability (honest status)

Status values: DONE-PARTIAL (implemented and tested, scope limited), NOT STARTED, BLOCKED.
Test evidence: `cd backend && ../.venv/bin/python -m pytest -q` -> 5 passed (Phase 1).

| Module (master prompt s.6) | Status | Location | Evidence / remaining |
|---|---|---|---|
| 1 Auth, users, roles | DONE-PARTIAL | backend/app/{security,deps}.py, routers/api.py | login, lockout, role checks tested. Missing: OIDC/MFA, user admin API, password change, rate limiting |
| 3 CRM (organizations) | DONE-PARTIAL | routers/api.py | create/list/get/pagination/validation tested. Missing: contacts, facilities, products, update/delete |
| 7 Consultancy files | DONE-PARTIAL | routers/api.py | create/list/get/patch, client scope isolation (IDOR) tested. Missing: trade-case links, lifecycle transition rules |
| 9 Tasks | DONE-PARTIAL | routers/api.py | create/list/patch tested. Missing: dependencies, approvals, comments |
| 21 Audit | DONE-PARTIAL | models.AuditEvent | create/update/login audited, admin-only read tested |
| 2,4,5,6,8,10-20 | NOT STARTED | - | - |
| Frontend, Docker, Alembic migrations, seed script | NOT STARTED | - | Docker/Postgres unavailable in sandbox; tables created via create_all in dev |
