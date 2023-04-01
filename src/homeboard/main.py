import importlib
import pkgutil

from fastapi import FastAPI, Response

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

# TODO: Fail without Python stack trace
_config = homeboard.config.load()

app = FastAPI()
_html_components = {}
for name in components:
    instance = components[name](config=_config)
    app.include_router(instance.router())
    _html_components[name] = instance.html()


@app.get("/dashboard")
def dashboard() -> Response:
    page = []
    for html in _html_components.values():
        page.append(html)

    # with open("dashboard.html", "r") as f:
    return Response(b"".join(page), media_type="text/html")
