"""Database operations and utilities for the SFTP API service.

Handles all PostgreSQL/MySQL database interactions including:
- Connection pooling
- CRUD operations
- Schema migrations
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_SCHEMA = "raw"

load_dotenv()

engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URI"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(metadata=MetaData(schema=DB_SCHEMA))
