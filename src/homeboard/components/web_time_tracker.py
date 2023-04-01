import datetime
import json
from typing import Annotated, Any

import fastapi

import homeboard.component
import homeboard.config

__all__ = [
    "Component",
]

router = fastapi.APIRouter(
    prefix="/web_time_tracker",
    tags=["web_time_tracker"],
    responses={404: {"description": "Not found"}},
)


class Component(homeboard.component.Base):
    def __init__(self) -> None:
        pass

    def router(self) -> fastapi.APIRouter:
        return router

    def html(self) -> bytes:
        return b"ahaaa"


def summarize_todays_browsing_statistics(
    statistics: list[dict[str, Any]], domains: list[str]
) -> int:
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

        for d in domains:
            if website["url"].endswith(d):
                aggregate_time_visited += day["summary"]
                break

    return aggregate_time_visited


@router.post("/browsing_statistics")
def browsing_statistics(statistics: list[dict[str, Any]]) -> dict[str, str]:
    with open("browsing_statistics.json", "w") as f:
        f.write(json.dumps(statistics))
    return {"status": "ok"}


@router.get("/kpi")
def kpi(config: Annotated[Any, fastapi.Depends(homeboard.config.cached)]) -> Any:
    domains = config.component("web_time_tracker").get("domains")
    if domains is None:
        raise fastapi.HTTPException(status_code=500, detail="No domains configured")

    with open("browsing_statistics.json", "r") as f:
        statistics = json.loads(f.read())
    time_visited = summarize_todays_browsing_statistics(statistics, domains)
    return {"undesirable_time_visited": time_visited}
