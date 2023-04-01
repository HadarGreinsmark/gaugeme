import os as _os
from typing import Any

import yaml as _yaml

__all__ = [
    "State",
    "Error",
    "LoadError",
    "ComponentMissingError",
]


class Error(Exception):
    pass


class LoadError(Error):
    pass


class ComponentMissingError(Error):
    pass


class State:
    """This ``config.State`` class parses a config object and provides
    methods to access the config structure properly.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        components = config.get("components", {})
        if not isinstance(components, dict):
            raise Error("'components' key must be a dictionary")
        for name, component in components.items():
            if not isinstance(component, dict):
                raise Error(f"Component '{name}' must be a dictionary")
        self._components = components

    def component(self, name: str) -> Any:
        if name not in self._components:
            raise ComponentMissingError(f"Component '{name}' is missing")
        return self._components[name]


def load() -> State:
    file = _os.environ.get("HOMEBOARD_CONFIG")
    if file is None:
        raise LoadError("Environment variable HOMEBOARD_CONFIG must be set")
    try:
        with open(file, encoding="utf-8") as f:
            return State(_yaml.safe_load(f))
    except Exception as e:
        raise LoadError(f"Exception when loading config file '{file}'") from e
