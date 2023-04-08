import datetime
from pathlib import Path
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

statistics_store = []


class Component(homeboard.component.Base):
    def __init__(self) -> None:
        pass

    def router(self) -> fastapi.APIRouter:
        return router

    def html(self) -> str:
        return Path(__file__).parent.joinpath("index.html").read_text()


def summarize_todays_browsing_statistics(
    statistics: list[dict[str, Any]], domains: list[str], day: datetime.date
) -> int:
    """
    Summarize todays browsing statistics.
    """

    aggregate_time_visited = 0
    day_string = day.strftime("%-m/%-d/%Y")

    for website in statistics:
        web_day = website["days"][-1]
        if web_day["date"] != day_string:
            continue

        for d in domains:
            if website["url"].endswith(d):
                aggregate_time_visited += web_day["summary"]
                break

    return aggregate_time_visited


@router.post("/browsing_statistics")
def browsing_statistics(statistics: list[dict[str, Any]]) -> dict[str, str]:
    global statistics_store
    statistics_store = statistics
    return {"status": "ok"}


@router.get("/kpi")
def kpi(
    day: datetime.date,
    config: Annotated[Any, fastapi.Depends(homeboard.config.cached)],
) -> Any:
    domains = config.component("web_time_tracker").get("domains")
    if domains is None:
        raise fastapi.HTTPException(status_code=500, detail="No domains configured")

    time_visited = summarize_todays_browsing_statistics(statistics_store, domains, day)
    return {"visited_secs": time_visited}
