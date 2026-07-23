"""
Database engine configuration and table initialization.

Creates the SQLAlchemy engine, ensures the SQLite file directory exists,
and exposes init_db() to create all registered tables on startup.
"""

from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine

from app.config.settings import settings
from app.database.base import Base

# Resolve ./data relative to the backend root (where uvicorn is run from)
_BACKEND_ROOT = Path(__file__).resolve().parents[2]
_DATA_DIR = _BACKEND_ROOT / "data"


def _ensure_data_directory() -> None:
    """Create the data/ directory if it does not exist (required for SQLite)."""
    _DATA_DIR.mkdir(parents=True, exist_ok=True)


def _sqlite_file_path() -> Path | None:
    """
    Extract the SQLite file path from DATABASE_URL.

    Returns None for non-file SQLite URLs (e.g. :memory:).
    """
    url = settings.DATABASE_URL
    if url.startswith("sqlite:///"):
        relative_path = url.removeprefix("sqlite:///")
        if relative_path == ":memory:":
            return None
        return (_BACKEND_ROOT / relative_path).resolve()
    return None


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record) -> None:
    """Enable foreign key enforcement for SQLite connections."""
    if settings.DATABASE_URL.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def _create_engine() -> Engine:
    """Build the SQLAlchemy engine with SQLite-safe defaults."""
    connect_args: dict[str, object] = {}
    if settings.DATABASE_URL.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    _ensure_data_directory()
    return create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        echo=settings.DEBUG,
        future=True,
    )


engine: Engine = _create_engine()


def init_db() -> None:
    """
    Create all database tables if they do not exist.

    Must import models before calling so they register with Base.metadata.
    """
    # Import models here to register them with Base.metadata
    import app.models  # noqa: F401

    db_path = _sqlite_file_path()
    if db_path is not None:
        db_path.parent.mkdir(parents=True, exist_ok=True)

    Base.metadata.create_all(bind=engine)
