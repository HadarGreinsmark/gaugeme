import fastapi.testclient

import homeboard.config
import homeboard.main

client = fastapi.testclient.TestClient(homeboard.main.app)


def fake_config() -> homeboard.config.State:
    return homeboard.config.State(
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


homeboard.main.app.dependency_overrides[homeboard.config.cached] = fake_config


def test_only_tracked_domains_are_summarized() -> None:
    resp_post = client.post(
        "/web_time_tracker/browsing_statistics",
        json=[
            {
                "counter": 2,
                "days": [
                    {"counter": 1, "date": "1/1/2023", "summary": 30},
                    {"counter": 1, "date": "1/2/2023", "summary": 60},
                ],
                "summaryTime": 90,
                "url": "alpha.example.com",
            },
            {
                "counter": 1,
                "days": [
                    {"counter": 1, "date": "1/2/2023", "summary": 15},
                ],
                "summaryTime": 15,
                "url": "beta.example.com",
            },
            {
                "counter": 1,
                "days": [
                    {"counter": 1, "date": "1/2/2023", "summary": 120},
                ],
                "summaryTime": 120,
                "url": "gamma.example.com",
            },
        ],
    )
    resp_post.raise_for_status()

    resp_get = client.get("/web_time_tracker/kpi?day=2023-01-02")
    resp_post.raise_for_status()
    assert resp_get.json()["visited_secs"] == 75
