from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import schemas as s
from ..db import get_db
from ..deps import admin_only, audit, current_user, paginate, staff
from ..models import AuditEvent, ClientCase, Organization, Task, User
from ..security import make_token, verify_password

router = APIRouter(prefix="/api/v1")
MAX_FAILS = 5


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/auth/login", response_model=s.TokenOut)
def login(body: s.LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == body.email.lower()))
    now = datetime.now(timezone.utc)
    if user and user.locked_until and user.locked_until.replace(tzinfo=timezone.utc) > now:
        raise HTTPException(429, "Account temporarily locked")
    if not user or not user.is_active or not verify_password(body.password, user.password_hash):
        if user:
            user.failed_logins += 1
            if user.failed_logins >= MAX_FAILS:
                user.locked_until = now + timedelta(minutes=15)
                user.failed_logins = 0
        audit(db, user, "login", "user", user.id if user else None, "failure")
        db.commit()
        raise HTTPException(401, "Invalid credentials")
    user.failed_logins = 0
    audit(db, user, "login", "user", user.id)
    db.commit()
    return s.TokenOut(access_token=make_token(user.id))


@router.get("/auth/me", response_model=s.UserOut)
def me(user: User = Depends(current_user)):
    return user


# ---- organizations (staff only) ----
@router.post("/organizations", response_model=s.OrgOut, status_code=201)
def create_org(body: s.OrgIn, db: Session = Depends(get_db), user: User = Depends(staff)):
    org = Organization(**body.model_dump())
    db.add(org)
    db.flush()
    audit(db, user, "create", "organization", org.id, diff=body.model_dump())
    db.commit()
    return org


@router.get("/organizations")
def list_orgs(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100),
              q: str | None = None, db: Session = Depends(get_db), user: User = Depends(staff)):
    query = db.query(Organization).order_by(Organization.id)
    if q:
        query = query.filter(Organization.name.ilike(f"%{q}%"))
    r = paginate(query, page, size)
    r["items"] = [s.OrgOut.model_validate(o) for o in r["items"]]
    return r


@router.get("/organizations/{org_id}", response_model=s.OrgOut)
def get_org(org_id: int, db: Session = Depends(get_db), user: User = Depends(staff)):
    org = db.get(Organization, org_id)
    if not org:
        raise HTTPException(404, "Not found")
    return org


# ---- client cases ----
def _visible_case(db: Session, user: User, case_id: int) -> ClientCase:
    case = db.get(ClientCase, case_id)
    # 404 (not 403) for out-of-scope objects to avoid leaking existence.
    if not case or (user.role == "client" and case.organization_id != user.organization_id):
        raise HTTPException(404, "Not found")
    return case


@router.post("/client-cases", response_model=s.CaseOut, status_code=201)
def create_case(body: s.CaseIn, db: Session = Depends(get_db), user: User = Depends(staff)):
    if not db.get(Organization, body.organization_id):
        raise HTTPException(422, "Unknown organization_id")
    case = ClientCase(reference="pending", **body.model_dump())
    db.add(case)
    db.flush()
    case.reference = f"CC-{datetime.now(timezone.utc).year}-{case.id:05d}"
    audit(db, user, "create", "client_case", case.id, diff=body.model_dump())
    db.commit()
    return case


@router.get("/client-cases")
def list_cases(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100),
               status: str | None = None, q: str | None = None,
               db: Session = Depends(get_db), user: User = Depends(current_user)):
    query = db.query(ClientCase).order_by(ClientCase.id)
    if user.role == "client":
        query = query.filter(ClientCase.organization_id == user.organization_id)
    if status:
        query = query.filter(ClientCase.status == status)
    if q:
        query = query.filter(ClientCase.title.ilike(f"%{q}%"))
    r = paginate(query, page, size)
    r["items"] = [s.CaseOut.model_validate(c) for c in r["items"]]
    return r


@router.get("/client-cases/{case_id}", response_model=s.CaseOut)
def get_case(case_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    return _visible_case(db, user, case_id)


@router.patch("/client-cases/{case_id}", response_model=s.CaseOut)
def patch_case(case_id: int, body: s.CasePatch, db: Session = Depends(get_db),
               user: User = Depends(staff)):
    case = _visible_case(db, user, case_id)
    changes = body.model_dump(exclude_unset=True)
    diff = {k: [getattr(case, k), v] for k, v in changes.items()}
    for k, v in changes.items():
        setattr(case, k, v)
    audit(db, user, "update", "client_case", case.id, diff=diff)
    db.commit()
    return case


# ---- tasks (internal; staff only) ----
@router.post("/tasks", response_model=s.TaskOut, status_code=201)
def create_task(body: s.TaskIn, db: Session = Depends(get_db), user: User = Depends(staff)):
    if not db.get(ClientCase, body.client_case_id):
        raise HTTPException(422, "Unknown client_case_id")
    task = Task(**body.model_dump())
    db.add(task)
    db.flush()
    audit(db, user, "create", "task", task.id)
    db.commit()
    return task


@router.get("/tasks")
def list_tasks(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=100),
               client_case_id: int | None = None, status: str | None = None,
               db: Session = Depends(get_db), user: User = Depends(staff)):
    query = db.query(Task).order_by(Task.id)
    if client_case_id:
        query = query.filter(Task.client_case_id == client_case_id)
    if status:
        query = query.filter(Task.status == status)
    r = paginate(query, page, size)
    r["items"] = [s.TaskOut.model_validate(t) for t in r["items"]]
    return r


@router.patch("/tasks/{task_id}", response_model=s.TaskOut)
def patch_task(task_id: int, body: s.TaskPatch, db: Session = Depends(get_db),
               user: User = Depends(staff)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Not found")
    changes = body.model_dump(exclude_unset=True)
    diff = {k: [getattr(task, k), v] for k, v in changes.items()}
    for k, v in changes.items():
        setattr(task, k, v)
    audit(db, user, "update", "task", task.id, diff=diff)
    db.commit()
    return task


# ---- audit (admin only) ----
@router.get("/audit-events")
def list_audit(page: int = Query(1, ge=1), size: int = Query(50, ge=1, le=200),
               db: Session = Depends(get_db), user: User = Depends(admin_only)):
    r = paginate(db.query(AuditEvent).order_by(AuditEvent.id.desc()), page, size)
    r["items"] = [
        {"id": e.id, "at": e.at, "actor_id": e.actor_id, "action": e.action,
         "object_type": e.object_type, "object_id": e.object_id, "result": e.result, "diff": e.diff}
        for e in r["items"]
    ]
    return r
