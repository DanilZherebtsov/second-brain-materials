from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "version": "0.4.2"}


def test_chat_returns_answer_with_citations():
    resp = client.post("/api/chat", json={"message": "Как оформить претензию о повреждении груза?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["answer"]
    assert data["citations"], "ответ без ссылки на регламент"
    assert data["citations"][0]["doc_id"] == "R-04"
    assert 0.0 <= data["confidence"] <= 1.0
    assert isinstance(data["latency_ms"], int)


def test_regulation_found():
    resp = client.get("/api/regulations/R-04")
    assert resp.status_code == 200
    data = resp.json()
    assert data["doc_id"] == "R-04"
    assert "претенз" in data["text"].lower()


def test_regulation_not_found():
    assert client.get("/api/regulations/R-99").status_code == 404


def test_empty_message_rejected():
    assert client.post("/api/chat", json={"message": ""}).status_code == 422
