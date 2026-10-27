from fastapi import FastAPI

from .db import Base, engine
from .routers.api import router

app = FastAPI(title="Trade Defence Management Platform", version="0.1.0")
app.include_router(router)


@app.on_event("startup")
def _create_tables() -> None:
    # Dev convenience only; Alembic migrations are the production path (pending).
    Base.metadata.create_all(engine)
