from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .db import get_db
from .models import AuditEvent, User
from .security import decode_token

bearer = HTTPBearer(auto_error=False)


def current_user(
    cred: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    uid = decode_token(cred.credentials) if cred else None
    user = db.get(User, uid) if uid else None
    if not user or not user.is_active:
        raise HTTPException(401, "Not authenticated")
    return user


def require_roles(*roles: str):
    def dep(user: User = Depends(current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(403, "Forbidden")
        return user
    return dep


staff = require_roles("admin", "consultant")
admin_only = require_roles("admin")


def audit(db: Session, actor: User | None, action: str, obj_type: str,
          obj_id=None, result: str = "success", diff: dict | None = None) -> None:
    db.add(AuditEvent(actor_id=actor.id if actor else None, action=action,
                      object_type=obj_type, object_id=str(obj_id) if obj_id is not None else None,
                      result=result, diff=diff))


def paginate(query, page: int, size: int):
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {"items": items, "total": total, "page": page, "size": size}
