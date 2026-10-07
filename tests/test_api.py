from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Bulk Certificate Generator API is running"


def test_invalid_empty_recipients():
    response = client.post(
        "/api/generation-jobs/",
        json={
            "event_name": "Python Workshop",
            "issue_date": "2026-10-07",
            "recipients": [],
        },
    )

    assert response.status_code == 422


def test_invalid_email():
    response = client.post(
        "/api/generation-jobs/",
        json={
            "event_name": "Python Workshop",
            "issue_date": "2026-10-07",
            "recipients": [
                {
                    "name": "Chaitra",
                    "email": "invalid-email",
                }
            ],
        },
    )

    assert response.status_code == 422


def test_create_generation_job():
    response = client.post(
        "/api/generation-jobs/",
        json={
            "event_name": "Aereo Backend Workshop",
            "issue_date": "2026-10-07",
            "recipients": [
                {
                    "name": "Chaitra",
                    "email": "chaitra-test@example.com",
                },
                {
                    "name": "Test User",
                    "email": "test-user@example.com",
                },
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "job_id" in data
    assert data["status"] == "COMPLETED"
    assert data["total_count"] == 2
    assert data["success_count"] == 2
    assert data["failure_count"] == 0


def test_generation_job_not_found():
    response = client.get(
        "/api/generation-jobs/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 200
    assert response.json()["error"] == "Generation job not found"