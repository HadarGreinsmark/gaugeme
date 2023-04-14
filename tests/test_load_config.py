from pathlib import Path

import pytest

import gaugeme.config


def test_invalid_yaml(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "config.yaml").write_bytes(b"!!!! broken_yaml")
    monkeypatch.setenv("GAUGEME_CONFIG", str(tmp_path / "config.yaml"))
    with pytest.raises(gaugeme.config.LoadError):
        gaugeme.config.load()


def test_missing_component_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "config.yaml").write_bytes(b"components: {}")
    monkeypatch.setenv("GAUGEME_CONFIG", str(tmp_path / "config.yaml"))
    with pytest.raises(gaugeme.config.ComponentMissingError):
        gaugeme.config.load().component("not_existing")


def test_component_config_accessible(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "config.yaml").write_bytes(
        b""" \
components:
  dummy_component:
    foo: bar
"""
    )
    monkeypatch.setenv("GAUGEME_CONFIG", str(tmp_path / "config.yaml"))
    assert gaugeme.config.load().component("dummy_component") == {"foo": "bar"}
