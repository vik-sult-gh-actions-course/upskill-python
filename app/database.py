"""
Database Configuration Module

This module is responsible for setting up the database connection using SQLAlchemy.
It loads environment variables from a `.env` file to configure the database engine,
creates a session factory for interacting with the database, and prepares the base
class for declarative models.

Key components:
- `engine`: SQLAlchemy engine connected to the database specified in the environment variables.
- `SessionLocal`: Factory for creating database sessions.
- `Base`: Declarative base class with an explicit schema set to 'public' for model definitions.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

db_url = os.getenv("DATABASE_URL")
if db_url is None:
    raise RuntimeError("DATABASE_URL environment variable is not set")

engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(metadata=MetaData(schema="public"))
