# Implementation Plan

Sources read in full: master prompt, Master Spec, Deep Functional Spec, Complete AI Build Spec (converted from docx).

## Architecture (modular monolith)
- Backend: Python 3.11 + FastAPI + SQLAlchemy 2 + Alembic, `/api/v1`, OpenAPI at `/openapi.json`.
- DB: PostgreSQL in production (`DATABASE_URL`); SQLite for local dev/tests (Docker/Postgres are not available in the current sandbox).
- Auth: argon2 password hashes, signed JWT bearer tokens; OIDC/MFA is a later phase.
- Frontend (Phase 2): React + TypeScript + Vite, design tokens from the master prompt section 5.
- Jobs/storage (later): Redis worker, S3-compatible storage.

## Phases
| Phase | Scope | Status |
|---|---|---|
| 1 | Backend core: auth, roles, server-side scope checks, organizations, client cases, tasks, audit trail, pagination, tests | in progress |
| 2 | Frontend shell + login + list/detail/create for Phase 1 modules | not started |
| 3 | Documents (versioned), deadlines (rule-traced), workflow templates | not started |
| 4 | Reports (draft→published, snapshots), client portal | not started |
| 5 | Trade-case DB, sources/verification, risk screening | not started |
| 6 | Financial analysis, questionnaires, AI, automations, deployment | not started |

## Testing
pytest (unit + API integration) per phase; frontend tests and E2E from Phase 2. Results are recorded in `docs/REQUIREMENTS_TRACEABILITY.md` only after being run.
