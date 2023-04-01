import datetime
import json
from typing import Annotated, Any

import fastapi

import homeboard.component
import homeboard.config

__all__ = [
    "Component",
]

# undesirable_time_visited = homeboard.config.components["web_time_tracker"]

router = fastapi.APIRouter(
    prefix="/web_time_tracker",
    tags=["web_time_tracker"],
    responses={404: {"description": "Not found"}},
)

html = b"ahaaa"


class Component(homeboard.component.Base):
    def __init__(self):
        pass

    def router(self) -> fastapi.APIRouter:
        return router

    def html(self) -> bytes:
        return html


def summarize_todays_browsing_statistics(statistics: list) -> dict:
    """
    Summarize todays browsing statistics.
    """
    today = datetime.date.today().strftime("%-m/%-d/%Y")
    print(today)

    aggregate_time_visited = 0

    for website in statistics:
        day = website["days"][-1]
        if day["date"] != today:
            continue

        for undesirable in undesirable_time_visited:
            if website["url"].endswith(undesirable):
                aggregate_time_visited += day["summary"]
                break

    return aggregate_time_visited


@router.post("/browsing_statistics")
def browsing_statistics(statistics: list):
    with open("browsing_statistics.json", "w") as f:
        f.write(json.dumps(statistics))
    return {"status": "ok"}


@router.get("/kpi")
def kpi(component_config: Annotated[Any, fastapi.Depends(homeboard.config.cached)]):
    with open("browsing_statistics.json", "r") as f:
        statistics = json.loads(f.read())
    time_visited = summarize_todays_browsing_statistics(statistics)
    return {"undesirable_time_visited": time_visited}
