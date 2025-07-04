"""
Unit tests for the task-related API endpoints in the FastAPI application.
"""

from .utils import app, client, override_get_db
from ..routers.task import get_db

app.dependency_overrides[get_db] = override_get_db


def test_get_task():
    """
    Test retrieving all tasks from the /task endpoint.
    Asserts that the response is a non-empty list and status code is 200.
    """
    response = client.get("/task")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  # pylint: disable=missing-final-newline


def test_get_task_by_id():
    """
    Test retrieving a task by its ID from the /task/{id} endpoint.
    Asserts that the returned task matches the requested ID and status code is 200.
    """
    tasks_list_response = client.get("/task")
    tasks_list_json = tasks_list_response.json()

    task_id = tasks_list_json[0]["id"]
    response = client.get(f"/task/{task_id}")
    assert response.status_code == 200
    assert task_id == response.json()["id"]  # pylint: disable=missing-final-newline


def test_post_task_no_body():
    """
    Test posting to /task/ with no body.
    Asserts that the response status code is 422 (Unprocessable Entity).
    """
    response = client.post("/task/")
    assert response.status_code == 422


def test_post_task():
    """
    Test creating a new task via the /task/ endpoint.
    Asserts that the response status code is 201 (Created).
    """
    headers = {"Content-Type": "application/json", "Accept": "text/plain"}
    payload = {
        "description": "With pure water",
        "due_date": "2027-07-21",
        "status": "pending",
        "title": "[TEST_TEST_TEST]",
    }
    response = client.post("/task/", headers=headers, json=payload)
    assert response.status_code == 201


def test_delete_test_task():
    """
    Test deleting a task with the title '[TEST_TEST_TEST]' via the /task/{id} endpoint.
    Asserts that the response status code is 200 upon successful deletion.
    """
    tasks_list_response = client.get("/task")
    tasks_list_json = tasks_list_response.json()
    for task in tasks_list_json:
        if task["title"] == "[TEST_TEST_TEST]":
            response = client.delete(f"/task/{task['id']}")
            assert response.status_code == 200
