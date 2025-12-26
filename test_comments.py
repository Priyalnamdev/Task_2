import pytest
from app import app, db, Task

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            task = Task(title="Test Task")
            db.session.add(task)
            db.session.commit()
        yield client

def test_create_comment(client):
    res = client.post("/tasks/1/comments", json={"content": "Test comment"})
    assert res.status_code == 201

def test_get_comments(client):
    client.post("/tasks/1/comments", json={"content": "Hello"})
    res = client.get("/tasks/1/comments")
    assert res.status_code == 200
    assert len(res.json) == 1

def test_update_comment(client):
    client.post("/tasks/1/comments", json={"content": "Old"})
    res = client.put("/comments/1", json={"content": "Updated"})
    assert res.json["content"] == "Updated"

def test_delete_comment(client):
    client.post("/tasks/1/comments", json={"content": "To delete"})
    res = client.delete("/comments/1")
    assert res.status_code == 200
