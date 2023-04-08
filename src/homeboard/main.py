import importlib
import pkgutil
from pathlib import Path
from typing import Annotated

import chevron
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
_html_components = []
for name in components:
    if not homeboard.config.cached().has_component(name):
        continue
    instance = components[name]()
    if router := instance.router():
        app.include_router(router)
    _html_components.append({"article": instance.html()})


template_path = Path(__file__).parent.joinpath("index.html.mustache")

with open(template_path) as f:
    page = chevron.render(f, {"widgets": _html_components})


@app.get("/dashboard")
def dashboard(
    config: Annotated[homeboard.config.State, Depends(homeboard.config.cached)]
) -> Response:
    return Response(page, media_type="text/html")
