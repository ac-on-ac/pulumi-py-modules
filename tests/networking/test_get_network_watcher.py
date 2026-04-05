"""Unit tests for pulumi_azure_modules.networking.get_network_watcher."""

from __future__ import annotations

import pulumi
import pytest

from pulumi_azure_modules.networking import get_network_watcher

_LOCATION = "eastus"
_WATCHER_NAME = "NetworkWatcher_eastus"
_RG = "NetworkWatcherRG"


class _GetNWMocks(pulumi.runtime.Mocks):
    """Mock engine that handles getNetworkWatcher invoke calls."""

    def new_resource(
        self,
        args: pulumi.runtime.MockResourceArgs,
    ) -> tuple[str, dict]:
        return (f"{args.name}_id", args.inputs)

    def call(
        self,
        args: pulumi.runtime.MockCallArgs,
    ) -> tuple[dict, list]:
        if args.token == "azure-native:network:getNetworkWatcher":
            nw_name = args.args.get("networkWatcherName", "mock-nw")
            rg_name = args.args.get("resourceGroupName", "mock-rg")
            return (
                {
                    "name": nw_name,
                    "location": _LOCATION,
                    "id": (
                        "/subscriptions/00000000-0000-0000-0000-000000000000"
                        f"/resourceGroups/{rg_name}"
                        f"/providers/Microsoft.Network/networkWatchers/{nw_name}"
                    ),
                    "tags": {},
                    "provisioningState": "Succeeded",
                    "etag": 'W/"00000000-0000-0000-0000-000000000000"',
                    "type": "Microsoft.Network/networkWatchers",
                    "azureApiVersion": "2024-05-01",
                },
                [],
            )
        return ({}, [])


@pytest.fixture(autouse=True)
def nw_lookup_mocks() -> None:
    """Override mocks so getNetworkWatcher invokes return realistic data."""
    pulumi.runtime.set_mocks(
        _GetNWMocks(),
        project="test-project",
        stack="test-stack",
        preview=False,
    )


@pulumi.runtime.test
def test_returns_output() -> None:
    """get_network_watcher returns a non-None Output."""
    result = get_network_watcher(_WATCHER_NAME, _RG)
    assert result is not None


@pulumi.runtime.test
def test_name_resolves() -> None:
    """Name attribute resolves to the looked-up watcher name."""
    result = get_network_watcher(_WATCHER_NAME, _RG)

    def check(v: str) -> None:
        assert v == _WATCHER_NAME

    return result.name.apply(check)


@pulumi.runtime.test
def test_location_resolves() -> None:
    """Location attribute resolves to the watcher's region."""
    result = get_network_watcher(_WATCHER_NAME, _RG)

    def check(v: str) -> None:
        assert v == _LOCATION

    return result.location.apply(check)


@pulumi.runtime.test
def test_id_contains_watcher_name() -> None:
    """Id is a non-empty ARM resource ID containing both the watcher and RG names."""
    result = get_network_watcher(_WATCHER_NAME, _RG)

    def check(v: str) -> None:
        assert v
        assert _WATCHER_NAME in v
        assert _RG in v

    return result.id.apply(check)


@pulumi.runtime.test
def test_different_regions_resolve_independently() -> None:
    """Two lookups in different regions resolve to their respective names."""
    nw_east = get_network_watcher("NetworkWatcher_eastus", _RG)
    nw_west = get_network_watcher("NetworkWatcher_westeurope", _RG)

    def check_east(v: str) -> None:
        assert v == "NetworkWatcher_eastus"

    def check_west(v: str) -> None:
        assert v == "NetworkWatcher_westeurope"

    return pulumi.Output.all(
        nw_east.name.apply(check_east),
        nw_west.name.apply(check_west),
    )
