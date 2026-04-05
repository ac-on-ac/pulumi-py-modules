"""Unit tests for pulumi_azure_modules.networking.get_virtual_network."""

from __future__ import annotations

import pulumi
import pytest

from pulumi_azure_modules.networking import get_virtual_network

_LOCATION = "eastus"
_VNET_NAME = "vnet-platform"
_RG = "rg-platform"
_ADDRESS_PREFIXES = ["10.0.0.0/16"]
_RESOURCE_ID = (
    "/subscriptions/00000000-0000-0000-0000-000000000000"
    f"/resourceGroups/{_RG}"
    f"/providers/Microsoft.Network/virtualNetworks/{_VNET_NAME}"
)


class _GetVNetMocks(pulumi.runtime.Mocks):
    """Mock engine that handles getVirtualNetwork invoke calls."""

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
        """Return realistic data for the getVirtualNetwork invoke token."""
        if args.token == "azure-native:network:getVirtualNetwork":
            vnet_name = args.args.get("virtualNetworkName", "mock-vnet")
            rg_name = args.args.get("resourceGroupName", "mock-rg")
            return (
                {
                    "name": vnet_name,
                    "location": _LOCATION,
                    "id": (
                        "/subscriptions/00000000-0000-0000-0000-000000000000"
                        f"/resourceGroups/{rg_name}"
                        f"/providers/Microsoft.Network/virtualNetworks/{vnet_name}"
                    ),
                    "addressSpace": {"addressPrefixes": _ADDRESS_PREFIXES},
                    "subnets": [],
                    "tags": {},
                    "provisioningState": "Succeeded",
                    "etag": 'W/"00000000-0000-0000-0000-000000000001"',
                    "type": "Microsoft.Network/virtualNetworks",
                    "azureApiVersion": "2024-05-01",
                },
                [],
            )
        return ({}, [])


@pytest.fixture(autouse=True)
def vnet_lookup_mocks() -> None:
    """Override mocks so getVirtualNetwork invokes return realistic data."""
    pulumi.runtime.set_mocks(
        _GetVNetMocks(),
        project="test-project",
        stack="test-stack",
        preview=False,
    )


@pulumi.runtime.test
def test_returns_output() -> None:
    """get_virtual_network returns a non-None Output."""
    result = get_virtual_network(_VNET_NAME, _RG)
    assert result is not None


@pulumi.runtime.test
def test_name_resolves() -> None:
    """Name attribute resolves to the looked-up virtual network name."""
    result = get_virtual_network(_VNET_NAME, _RG)

    def check(v: str) -> None:
        assert v == _VNET_NAME

    return result.name.apply(check)


@pulumi.runtime.test
def test_location_resolves() -> None:
    """Location attribute resolves to the Azure region of the VNet."""
    result = get_virtual_network(_VNET_NAME, _RG)

    def check(v: str) -> None:
        assert v == _LOCATION

    return result.location.apply(check)


@pulumi.runtime.test
def test_id_is_populated() -> None:
    """Id attribute resolves to a non-empty resource ID string."""
    result = get_virtual_network(_VNET_NAME, _RG)

    def check(v: str) -> None:
        assert v
        assert "Microsoft.Network/virtualNetworks" in v

    return result.id.apply(check)


@pulumi.runtime.test
def test_address_space_resolves() -> None:
    """Address space contains the expected CIDR prefixes."""
    result = get_virtual_network(_VNET_NAME, _RG)

    def check(v: dict) -> None:
        assert v.get("address_prefixes") == _ADDRESS_PREFIXES

    return result.address_space.apply(check)
