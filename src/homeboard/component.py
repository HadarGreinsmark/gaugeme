import abc
import io

import fastapi

import homeboard.config


class Base(abc.ABC):
    "This is an interface to be inherited by components"

    @abc.abstractmethod
    def __init__(self, *, config: homeboard.config.State):
        "Loads component with config injected"

    @abc.abstractmethod
    def router(self) -> fastapi.APIRouter:
        "Returns FastAPI router for this component"

    @abc.abstractmethod
    def html(self) -> bytes | io.BytesIO:
        "Returns the HTML for showing this component"
