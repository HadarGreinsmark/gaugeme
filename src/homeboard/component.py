import abc

import fastapi


class Base(abc.ABC):
    "This is an interface to be inherited by components"

    @abc.abstractmethod
    def __init__(self) -> None:
        "Loads component"

    @abc.abstractmethod
    def router(self) -> fastapi.APIRouter | None:
        "Returns FastAPI router for this component"

    @abc.abstractmethod
    def html(self) -> str:
        "Returns the HTML for showing this component"
