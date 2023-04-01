import pkgutil

from fastapi import FastAPI, Response

import homeboard.components
import homeboard.config

app = FastAPI()

components_html = {}

# TODO: Fail without Python stack trace
_config = homeboard.config.load()

for component_info in pkgutil.iter_modules(homeboard.components.__path__):
    module = component_info.module_finder.find_module(component_info.name).load_module()
    if not hasattr(module, "Component"):
        raise Exception(
            f"Required class {component_info.name}.Component is missing"
        )
    print("module.Component", module.Component)
    print("homeboard.component.Base", homeboard.component.Base)
    if issubclass(module.Component, homeboard.component.Base):
        raise Exception(
            f"{component_info.name}.Component does not inherit from homeboard.component.Base"
        )
    component = module.Component(_config)
    app.include_router(component.router())
    components_html[component_info.name] = component.html()


@app.get("/dashboard")
def dashboard():
    page = []
    for html in components_html.values():
        page.append(html)

    # with open("dashboard.html", "r") as f:
    return Response(b"".join(page), media_type="text/html")
