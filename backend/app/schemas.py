from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .models import CASE_STATUSES, TASK_STATUSES

CaseStatus = Literal[CASE_STATUSES]  # type: ignore[valid-type]
TaskStatus = Literal[TASK_STATUSES]  # type: ignore[valid-type]


class ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LoginIn(BaseModel):
    email: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(ORM):
    id: int
    email: str
    full_name: str
    role: str
    organization_id: int | None


class OrgIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    country: str | None = Field(default=None, min_length=2, max_length=2)
    status: Literal["Prospect", "Intake", "Active", "Inactive", "Archived"] = "Prospect"


class OrgOut(ORM, OrgIn):
    id: int


class CaseIn(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    organization_id: int
    owner_id: int | None = None


class CasePatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    status: CaseStatus | None = None
    owner_id: int | None = None


class CaseOut(ORM):
    id: int
    reference: str
    title: str
    organization_id: int
    status: str
    owner_id: int | None
    created_at: datetime


class TaskIn(BaseModel):
    client_case_id: int
    title: str = Field(min_length=1, max_length=300)
    description: str | None = None
    assignee_id: int | None = None
    internal_target_date: datetime | None = None


class TaskPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    status: TaskStatus | None = None
    assignee_id: int | None = None


class TaskOut(ORM):
    id: int
    client_case_id: int
    title: str
    description: str | None
    status: str
    assignee_id: int | None
    internal_target_date: datetime | None


class Page(BaseModel):
    items: list
    total: int
    page: int
    size: int
