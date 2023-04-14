import fastapi.testclient

import gaugeme.config
import gaugeme.main

client = fastapi.testclient.TestClient(gaugeme.main.app)


def fake_config() -> gaugeme.config.State:
    return gaugeme.config.State({})


gaugeme.main.app.dependency_overrides[gaugeme.config.cached] = fake_config


def test_get_dashboard() -> None:
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert len(response.content) > 0
