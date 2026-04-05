"""Unit tests for pulumi_azure_modules.networking.get_route_table."""

from __future__ import annotations

import pulumi
import pytest

from pulumi_azure_modules.networking import get_route_table

_RT_NAME = "spoke-rt"
_RG = "rg-platform"
_RESOURCE_ID = (
    "/subscriptions/00000000-0000-0000-0000-000000000000"
    f"/resourceGroups/{_RG}"
    f"/providers/Microsoft.Network/routeTables/{_RT_NAME}"
)


class _GetRtMocks(pulumi.runtime.Mocks):
    """Mock engine that handles getRouteTable invoke calls."""

    def new_resource(
        self,
        args: pulumi.runtime.MockResourceArgs,
    ) -> tuple[str, dict]:
        """Return a synthetic resource id and pass inputs through as outputs."""
        return (f"{args.name}_id", args.inputs)

    def call(
        self,
        args: pulumi.runtime.MockCallArgs,
    ) -> tuple[dict, list]:
        """Return realistic data for the getRouteTable invoke token."""
        if args.token == "azure-native:network:getRouteTable":
            rt_name = args.args.get("routeTableName", "mock-rt")
            rg_name = args.args.get("resourceGroupName", "mock-rg")
            return (
                {
                    "name": rt_name,
                    "location": "eastus",
                    "id": (
                        "/subscriptions/00000000-0000-0000-0000-000000000000"
                        f"/resourceGroups/{rg_name}"
                        f"/providers/Microsoft.Network/routeTables/{rt_name}"
                    ),
                    "tags": {},
                    "provisioningState": "Succeeded",
                    "etag": 'W/"00000000-0000-0000-0000-000000000001"',
                    "type": "Microsoft.Network/routeTables",
                    "azureApiVersion": "2024-05-01",
                    "resourceGuid": "00000000-0000-0000-0000-000000000002",
                    "routes": [],
                    "subnets": [],
                    "disableBgpRoutePropagation": False,
                },
                [],
            )
        return ({}, [])


@pytest.fixture(autouse=True)
def rt_lookup_mocks() -> None:
    """Override mocks so getRouteTable invokes return realistic data."""
    pulumi.runtime.set_mocks(
        _GetRtMocks(),
        project="test-project",
        stack="test-stack",
        preview=False,
    )


@pulumi.runtime.test
def test_returns_output() -> None:
    """get_route_table returns a non-None Output."""
    result = get_route_table(_RT_NAME, _RG)
    assert result is not None


@pulumi.runtime.test
def test_name_matches_input() -> None:
    """The returned name matches the name argument."""
    result = get_route_table(_RT_NAME, _RG)

    def check(r: object) -> None:
        assert getattr(r, "name", None) == _RT_NAME

    return result.apply(check)


@pulumi.runtime.test
def test_id_is_populated() -> None:
    """The returned id is a non-empty string."""
    result = get_route_table(_RT_NAME, _RG)

    def check(r: object) -> None:
        assert getattr(r, "id", None)

    return result.apply(check)


@pulumi.runtime.test
def test_id_contains_resource_group() -> None:
    """The returned id embeds the resource group name."""
    result = get_route_table(_RT_NAME, _RG)

    def check(r: object) -> None:
        assert _RG in (getattr(r, "id", "") or "")

    return result.apply(check)


@pulumi.runtime.test
def test_accepts_expand_parameter() -> None:
    """The expand parameter is accepted without error."""
    result = get_route_table(_RT_NAME, _RG, expand="routes")
    assert result is not None
