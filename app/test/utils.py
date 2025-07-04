"""
Utility functions and test client setup for FastAPI application testing.

This module sets up a test database, provides a database override dependency,
and initializes a FastAPI TestClient for use in test cases.
"""
import os

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..database import Base
from ..main import app

load_dotenv()
engine = create_engine(
    os.getenv("SQLALCHEMY_DATABASE_URI"),
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    """
    Dependency override for providing a SQLAlchemy session
    connected to the test database for use in tests.
    Yields:
        db (Session): SQLAlchemy session for the test database.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)
