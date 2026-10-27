# Assumptions and Decisions

- A-001 (DEC-001): Single-organization deployment first; schema keeps `organization_id` scoping so multi-tenant can be added.
- A-002: SQLite used for dev/tests because Docker/Postgres are unavailable in the build sandbox; models avoid DB-specific features.
- A-003: Roles for Phase 1: `admin`, `consultant`, `client`. Finer-grained permissions come later.
- A-004: Clients see only consultancy files of their own organization; tasks are internal-only (no client access).
- A-005: Legal data (deadlines, rates, scope) is never seeded or invented; no official-source connectors exist yet.
- A-006: Internal consultancy files and official trade cases are separate entities (trade cases arrive in a later phase).
