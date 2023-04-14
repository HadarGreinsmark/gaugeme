import importlib
import pkgutil
from pathlib import Path
from typing import Annotated

import chevron
from fastapi import Depends, FastAPI, Response

import gaugeme.component
import gaugeme.components
import gaugeme.config


def import_components() -> dict[str, type[gaugeme.component.Base]]:
    "Imports and returns all components from ``gaugeme.components.*.Component``"
    components = {}
    for info in pkgutil.iter_modules(gaugeme.components.__path__):
        mod_name = f"gaugeme.components.{info.name}"
        mod = importlib.import_module(mod_name)
        class_name = f"{mod_name}.Component"
        if not hasattr(mod, "Component"):
            raise Exception(f"Required class {class_name} is missing")
        if not issubclass(mod.Component, gaugeme.component.Base):
            raise Exception(f"{class_name} must subclass gaugeme.component.Base")
        components[info.name] = mod.Component
    return components


components = import_components()

app = FastAPI()
_html_components = []
for name in components:
    if not gaugeme.config.cached().has_component(name):
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
    config: Annotated[gaugeme.config.State, Depends(gaugeme.config.cached)]
) -> Response:
    return Response(page, media_type="text/html")
