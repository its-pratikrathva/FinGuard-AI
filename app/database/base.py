"""
SQLAlchemy declarative base for all ORM models.

Every model inherits from Base so SQLAlchemy can track metadata
and generate tables via Base.metadata.create_all().
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared declarative base class for FinGuard AI models."""

    pass
