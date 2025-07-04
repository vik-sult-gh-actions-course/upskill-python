"""
SQLAlchemy models for the task management application.

Defines the database schema for tasks and their statuses.

Classes:
    Status: Enum representing possible task statuses.
    Task: SQLAlchemy model for the 'task' table.
"""
import enum

from sqlalchemy import Column, Integer, String, Enum

from .database import Base


class Status(enum.Enum):
    """
    Enumeration of possible statuses for a task.
    """
    PENDING = 'pending'
    IN_PROGRESS = 'progress'
    FAILED = 'failed'
    COMPLETED = 'completed'

class Task(Base): # pylint: disable=too-few-public-methods
    """
    SQLAlchemy model representing a task.

    Attributes:
        id (int): Primary key.
        title (str): Title of the task.
        description (str): Description of the task.
        status (Status): Current status of the task.
        due_date (str): Due date of the task.
    """
    __tablename__ = 'task'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(Enum(Status))
    due_date = Column(String)
