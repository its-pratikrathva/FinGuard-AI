"""
SQLAlchemy ORM models.

Import all models here so Base.metadata is fully populated
before init_db() runs.
"""

from app.models.scan_history import ScanHistory
from app.models.user import User

__all__ = ["User", "ScanHistory"]
