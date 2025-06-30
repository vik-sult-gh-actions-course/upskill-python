import enum

from sqlalchemy import Column, Integer, String, Enum

from .database import Base


class Status(enum.Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'progress'
    FAILED = 'failed'
    COMPLETED = 'completed'

class Task(Base):
    __tablename__ = 'task'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(Enum(Status))
    due_date = Column(String)
