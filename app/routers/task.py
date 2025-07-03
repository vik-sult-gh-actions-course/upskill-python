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

from fastapi import APIRouter, Request, Depends, Path
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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class TaskCreate(BaseModel):
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
    title: str = Field(min_length=10)
    description: str | None
    status: TaskStatus
    due_date: datetime.date | None


class TaskUpdate(BaseModel):
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
async def get_task(request: Request, db: db_dependency):
    return db.query(Task).all()


@router.get('/{task_id}', status_code=status.HTTP_200_OK)
async def get_user(request: Request, task_id: int, db: db_dependency):
    return db.query(Task).filter(Task.id == task_id).first()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_task(user_request: TaskCreate, db: db_dependency):
    task_request_model_dump = user_request.model_dump()
    task_model = Task(**task_request_model_dump)
    db.add(task_model)
    db.commit()
    db.refresh(task_model)
    return task_model


# Update (PUT)
@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
async def update_task(task_id: int, user_request: TaskUpdate, db: db_dependency):
    task_model = db.query(Task).filter(Task.id == task_id).first()
    if user_request.title is not None:
        task_model.title = user_request.title

    if user_request.description is not None:
        task_model.description = user_request.description

    if user_request.status is not None:
        task_model.status = user_request.status

    if user_request.due_date is not None:
        task_model.due_date = user_request.due_date

    db.commit()

    db.refresh(task_model)
    return task_model


# Delete (DELETE)
@router.delete("/{task_id}")
async def delete_item(task_id: int, db: db_dependency):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(db_task)
    db.commit()
    return {"message": "Item deleted successfully"}
