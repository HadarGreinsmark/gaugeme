import datetime
from pathlib import Path
from typing import Annotated, Any

import fastapi

import gaugeme.component
import gaugeme.config

__all__ = [
    "Component",
]

router = fastapi.APIRouter(
    prefix="/web_time_tracker",
    tags=["web_time_tracker"],
    responses={404: {"description": "Not found"}},
)

statistics_store = []


class Component(gaugeme.component.Base):
    def __init__(self) -> None:
        pass

    def router(self) -> fastapi.APIRouter:
        return router

    def html(self) -> str:
        return Path(__file__).parent.joinpath("index.html").read_text()


def sum_visited_secs(
    statistics: list[dict[str, Any]],
    domains: list[str],
    start: datetime.date,
    forward: int,
) -> list[int]:
    """
    Summarizes browsing statistics for the domains given and within the
    time interval.
    """
    visited_sums = [0] * (forward + 1)
    for website in statistics:
        tracked = False
        for d in domains:
            # Domain checking could be optimized
            if website["url"].endswith(d):
                tracked = True
                break
        if not tracked:
            continue

        # We only have to check the last `forward` days
        relevant_days = website["days"][-forward - 1 :]
        for day_stats in relevant_days:
            day = datetime.datetime.strptime(day_stats["date"], "%m/%d/%Y").date()
            day_index = (day - start).days
            if day_index < 0 or day_index > forward:
                continue
            visited_sums[day_index] += day_stats["summary"]
    return visited_sums


@router.post("/browsing_statistics")
def browsing_statistics(statistics: list[dict[str, Any]]) -> dict[str, str]:
    global statistics_store
    statistics_store = statistics
    return {"status": "ok"}


@router.get("/kpi")
def kpi(
    start: datetime.date,
    forward: int,
    config: Annotated[Any, fastapi.Depends(gaugeme.config.cached)],
) -> Any:
    domains = config.component("web_time_tracker").get("domains")
    if domains is None:
        raise fastapi.HTTPException(status_code=500, detail="No domains configured")
    return {"visited_secs": sum_visited_secs(statistics_store, domains, start, forward)}
