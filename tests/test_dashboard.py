import fastapi.testclient

import homeboard.config
import homeboard.main

client = fastapi.testclient.TestClient(homeboard.main.app)


def fake_config() -> homeboard.config.State:
    return homeboard.config.State({})


homeboard.main.app.dependency_overrides[homeboard.config.cached] = fake_config


def test_get_dashboard() -> None:
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert len(response.content) > 0
