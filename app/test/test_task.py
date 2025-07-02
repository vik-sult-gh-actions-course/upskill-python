from .utils import *
from ..routers.task import get_db

app.dependency_overrides[get_db] = override_get_db


def test_get_task():
    response = client.get("/task")
    assert response.status_code == 200
    assert type(response.json()) == type(list())
    assert len(response.json()) > 0


def test_get_task_by_id():
    tasks_list_response = client.get("/task")
    tasks_list_json = tasks_list_response.json()

    id = tasks_list_json[0]['id']
    response = client.get(f"/task/{id}")
    assert response.status_code == 200
    assert id == response.json()['id']


def test_post_task_no_body():
    response = client.post("/task/")
    assert response.status_code == 422


def test_post_task():
    headers = {"Content-Type": "application/json",
               "Accept": "text/plain"}
    payload = {
        "description": "With pure water",
        "due_date": "2027-07-21",
        "status": "pending",
        "title": "[TEST_TEST_TEST]"
    }
    response = client.post("/task/", headers=headers, json=payload)
    assert response.status_code == 201


def test_delete_test_task():
    tasks_list_response = client.get("/task")
    tasks_list_json = tasks_list_response.json()
    for task in tasks_list_json:
        if task['title'] == "[TEST_TEST_TEST]":
            response = client.delete(f"/task/{task['id']}")
            assert response.status_code == 200
