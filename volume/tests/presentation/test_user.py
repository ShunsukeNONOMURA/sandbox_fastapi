from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_get_user() -> None:
    user_id = '00'
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    # assert response.json() == {"user_id": user_id}
