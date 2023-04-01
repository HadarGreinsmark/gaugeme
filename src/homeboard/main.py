import importlib
import pkgutil
from typing import Annotated

from fastapi import Depends, FastAPI, Response

import homeboard.component
import homeboard.components
import homeboard.config


def import_components() -> dict[str, type[homeboard.component.Base]]:
    "Imports and returns all components from ``homeboard.components.*.Component``"
    components = {}
    for info in pkgutil.iter_modules(homeboard.components.__path__):
        mod_name = f"homeboard.components.{info.name}"
        mod = importlib.import_module(mod_name)
        class_name = f"{mod_name}.Component"
        if not hasattr(mod, "Component"):
            raise Exception(f"Required class {class_name} is missing")
        if not issubclass(mod.Component, homeboard.component.Base):
            raise Exception(f"{class_name} must subclass homeboard.component.Base")
        components[info.name] = mod.Component
    return components


components = import_components()

app = FastAPI()
_html_components = {}
for name in components:
    instance = components[name]()
    app.include_router(instance.router())
    _html_components[name] = instance.html()


@app.get("/dashboard")
def dashboard(
    config: Annotated[homeboard.config.State, Depends(homeboard.config.cached)]
) -> Response:
    page = []
    for html in _html_components.values():
        page.append(html)

    # with open("dashboard.html", "r") as f:
    return Response(b"".join(page), media_type="text/html")
