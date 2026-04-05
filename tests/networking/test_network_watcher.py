"""Unit tests for pulumi_azure_modules.networking.NetworkWatcher."""

from __future__ import annotations

import pulumi

from pulumi_azure_modules.networking import NetworkWatcher

_RG = "rg-network"
_LOCATION = "eastus"
_NAME = "nw-eastus"


@pulumi.runtime.test
def test_name_output() -> None:
    """name output resolves to the value supplied."""
    nw = NetworkWatcher("test-nw", resource_group_name=_RG, location=_LOCATION, name=_NAME)

    def check(v: str) -> None:
        assert v == _NAME

    return nw.name.apply(check)


@pulumi.runtime.test
def test_location_output() -> None:
    """location output resolves to the region supplied."""
    nw = NetworkWatcher("test-nw", resource_group_name=_RG, location=_LOCATION, name=_NAME)

    def check(v: str) -> None:
        assert v == _LOCATION

    return nw.location.apply(check)


@pulumi.runtime.test
def test_id_is_populated() -> None:
    """id output is non-empty after resource creation."""
    nw = NetworkWatcher("test-nw", resource_group_name=_RG, location=_LOCATION, name=_NAME)

    def check(v: str) -> None:
        assert v

    return nw.id.apply(check)


@pulumi.runtime.test
def test_resource_group_name_output() -> None:
    """resource_group_name is surfaced so downstream resources can consume it."""
    nw = NetworkWatcher("test-nw", resource_group_name=_RG, location=_LOCATION, name=_NAME)

    def check(v: str) -> None:
        assert v == _RG

    return nw.resource_group_name.apply(check)


@pulumi.runtime.test
def test_name_is_optional() -> None:
    """NetworkWatcher can be constructed without an explicit name."""
    nw = NetworkWatcher("auto-named-nw", resource_group_name=_RG, location=_LOCATION)
    assert nw is not None


@pulumi.runtime.test
def test_accepts_tags() -> None:
    """Tags are accepted without error."""
    nw = NetworkWatcher(
        "tagged-nw",
        resource_group_name=_RG,
        location=_LOCATION,
        name=_NAME,
        tags={"environment": "dev"},
    )
    assert nw is not None
