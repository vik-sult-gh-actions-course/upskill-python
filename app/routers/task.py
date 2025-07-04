"""
Task management API router for FastAPI.

This module defines the API endpoints for creating, retrieving, updating, and deleting tasks.
It uses FastAPI for routing, Pydantic for data validation, and SQLAlchemy for database interactions.

Endpoints:
    - GET /task/ : Retrieve all tasks.
    - GET /task/{task_id} : Retrieve a specific task by ID.
    - POST /task/ : Create a new task.
    - PUT /task/{task_id} : Update an existing task.
    - DELETE /task/{task_id} : Delete a task.

Models:
    - TaskCreate: Schema for creating a task.
    - TaskResponse: Schema for returning task data.
    - TaskUpdate: Schema for updating a task.

Dependencies:
    - Database session management via SQLAlchemy.

Requires:
    - FastAPI
    - SQLAlchemy
    - Pydantic
    - Starlette

"""
import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from ..database import SessionLocal
from ..models import Task, Status as TaskStatus

router = APIRouter(
    prefix='/task',
    tags=['task']
)


def get_db():
    """
        Dependency that provides a database session.

        Yields:
            Session: SQLAlchemy database session.
        """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)] # pylint: disable=invalid-name


class TaskCreate(BaseModel):
    """
        Schema for creating a new task.

        Fields:
            title (str): Title of the task (minimum 10 characters).
            description (str | None): Optional description of the task (max 200 characters).
            status (TaskStatus): Status of the task.
            due_date (datetime.date | None): Optional due date for the task.
        """
    title: str = Field(min_length=10)
    description: str | None = Field(
        default=None, title="The description of the task", max_length=200
    )
    status: TaskStatus
    due_date: datetime.date | None = Path(
        ...,
        description="Due date UTC date-time",
        examples=["2027-07-21"]
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Water a flower",
                    "description": "With pure water",
                    "due_date": "2027-07-21",
                    "status": "pending",
                }
            ]
        }
    }


class TaskResponse(BaseModel):
    """
        Schema for returning task data in API responses.

        Fields:
            title (str): Title of the task.
            description (str | None): Optional description of the task.
            status (TaskStatus): Status of the task.
            due_date (datetime.date | None): Optional due date for the task.
        """
    title: str = Field(min_length=10)
    description: str | None
    status: TaskStatus
    due_date: datetime.date | None


class TaskUpdate(BaseModel):
    """
        Schema for updating an existing task.

        Fields:
            title (str | None): Optional new title for the task.
            description (str | None): Optional new description.
            status (TaskStatus | None): Optional new status.
            due_date (datetime.date | None): Optional new due date.
        """
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None
    due_date: datetime.date | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Water a flower",
                    "description": "With pure water",
                    "due_date": "2027-07-21",
                    "status": "pending",
                }
            ]
        }
    }


@router.get('/', status_code=status.HTTP_200_OK)
async def get_task(db: db_dependency):
    """
        Retrieve all tasks.

        Args:
            db (Session): Database session dependency.

        Returns:
            list: List of all Task objects.
        """
    return db.query(Task).all()


@router.get('/{task_id}', status_code=status.HTTP_200_OK)
async def get_user(task_id: int, db: db_dependency):
    """
        Retrieve a specific task by its ID.

        Args:
            task_id (int): ID of the task to retrieve.
            db (Session): Database session dependency.

        Returns:
            Task | None: The Task object if found, else None.
        """
    return db.query(Task).filter(Task.id == task_id).first()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_task(user_request: TaskCreate, db: db_dependency):
    """
        Create a new task.

        Args:
            user_request (TaskCreate): Task creation data.
            db (Session): Database session dependency.

        Returns:
            Task: The created Task object.
        """
    task_request_model_dump = user_request.model_dump()
    task_model = Task(**task_request_model_dump)
    db.add(task_model)
    db.commit()
    db.refresh(task_model)
    return task_model


# Update (PUT)
@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def update_task(task_id: int, user_request: TaskUpdate, db: db_dependency):
    """
        Update an existing task by its ID.

        Args:
            task_id (int): ID of the task to update.
            user_request (TaskUpdate): Task update data.
            db (Session): Database session dependency.

        Returns:
            Task: The updated Task object.
        """
    task_model = db.query(Task).filter(Task.id == task_id).first()

    for field in ['title', 'description', 'status', 'due_date']:
        value = getattr(user_request, field)
        if value is not None:
            setattr(task_model, field, value)

    db.commit()

    db.refresh(task_model)
    return task_model


# Delete (DELETE)
@router.delete("/{task_id}")
async def delete_item(task_id: int, db: db_dependency):
    """
        Delete a task by its ID.

        Args:
            task_id (int): ID of the task to delete.
            db (Session): Database session dependency.

        Returns:
            dict: Message indicating successful deletion.
        """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(db_task)
    db.commit()
    return {"message": "Item deleted successfully"}
