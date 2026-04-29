from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_api_health_endpoint_works():
    response = client.get("/api/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert data["message"] == "PawPal AI Planner backend is running"


def test_api_schedule_endpoint_returns_required_fields():
    response = client.post(
        "/api/schedule",
        json={
            "text": "I have a dog named Bruno. Feed him at 8 AM and give medicine at 8 PM."
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert "schedule" in data
    assert "confidence" in data
    assert "warnings" in data
    assert "agent_steps" in data
    assert isinstance(data["schedule"], list)
    assert isinstance(data["warnings"], list)
    assert isinstance(data["agent_steps"], list)