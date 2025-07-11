"""Database models for the Sites API.

This module contains SQLAlchemy model definitions for the Sites API,
including the main Sites table structure.
"""

from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Sites(Base):
    """SQLAlchemy model representing sites in the system.

    Attributes:
        id: Primary key
        source_id: External source identifier
        name: Site name
        cid: Client ID
        manager: Site manager
        submanager: Assistant manager
        host: Hosting status flag
        devteam: Development team
        lifetime: Site lifetime
        state: Current state
        url: Site URL
    """
    __tablename__ = "sites"
    __table_args__ = {"schema": "raw"}

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String(50))
    name = Column(String(200))
    cid = Column(String(26))
    manager = Column(String(36))
    submanager = Column(String(36))
    host = Column(Boolean, default=False)
    devteam = Column(String(100))
    lifetime = Column(Integer)
    state = Column(String(100))
    url = Column(Text)

    def __repr__(self) -> str:
        """String representation of the Sites model."""
        return f"<Site(name='{self.name}', id={self.id})>"

    def get_display_name(self) -> str:
        """Returns a formatted display name for the site.

        Returns:
            str: A formatted string combining site name and ID
        """
        return f"{self.name} (ID: {self.source_id})" # pylint: disable=missing-final-newline