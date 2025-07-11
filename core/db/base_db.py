"""Shared database configuration for SQLAlchemy ORM."""
from typing import Optional, Dict, Any
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


def setup_database(schema: str = "public", db_url: Optional[str] = None) -> Dict[str, Any]:
    """Initialize and return database components.

    Args:
        db_url: Database URL (falls back to SQLALCHEMY_DATABASE_URI env var if None)
        schema: Database schema name

    Returns:
        Dictionary with 'engine', 'SessionLocal', and 'Base' components
    """
    load_dotenv()
    db_url = db_url or os.getenv("SQLALCHEMY_DATABASE_URI")

    if not db_url:
        raise RuntimeError("Database URL not provided and SQLALCHEMY_DATABASE_URI not set")

    engine = create_engine(db_url)
    # pylint: disable=invalid-name
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # pylint: disable=invalid-name
    Base = declarative_base(metadata=MetaData(schema=schema))

    return {
        'engine': engine,
        'SessionLocal': SessionLocal,
        'Base': Base
    }  # pylint: disable=missing-final-newline