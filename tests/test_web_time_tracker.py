import fastapi.testclient

import gaugeme.config
import gaugeme.main

client = fastapi.testclient.TestClient(gaugeme.main.app)


def fake_config() -> gaugeme.config.State:
    return gaugeme.config.State(
        {
            "components": {
                "web_time_tracker": {
                    "domains": [
                        "alpha.example.com",
                        "beta.example.com",
                    ],
                },
            },
        }
    )


gaugeme.main.app.dependency_overrides[gaugeme.config.cached] = fake_config


def test_only_tracked_domains_are_summarized() -> None:
    resp_post = client.post(
        "/web_time_tracker/browsing_statistics",
        json=[
            {
                "counter": 2,
                "days": [
                    {"counter": 1, "date": "1/1/2023", "summary": 5},
                    {"counter": 1, "date": "1/2/2023", "summary": 30},
                    {"counter": 1, "date": "1/3/2023", "summary": 60},
                ],
                "summaryTime": 90,
                "url": "alpha.example.com",
            },
            {
                "counter": 1,
                "days": [
                    {"counter": 1, "date": "1/3/2023", "summary": 15},
                    {"counter": 1, "date": "1/4/2023", "summary": 33},
                ],
                "summaryTime": 15,
                "url": "beta.example.com",
            },
            {
                "counter": 1,
                "days": [
                    {"counter": 1, "date": "1/3/2023", "summary": 120},
                ],
                "summaryTime": 120,
                "url": "gamma.example.com",
            },
        ],
    )
    resp_post.raise_for_status()

    resp_get = client.get("/web_time_tracker/kpi?start=2023-01-02&forward=1")
    resp_post.raise_for_status()
    assert resp_get.json()["visited_secs"] == [30, 75]
