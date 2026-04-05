"""Unit tests for pulumi_azure_modules.networking.get_subnet."""

from __future__ import annotations

import pulumi
import pytest

from pulumi_azure_modules.networking import get_subnet

_SUBNET_NAME = "aks-subnet"
_VNET_NAME = "vnet-spoke"
_RG = "rg-platform"
_RESOURCE_ID = (
    "/subscriptions/00000000-0000-0000-0000-000000000000"
    f"/resourceGroups/{_RG}"
    f"/providers/Microsoft.Network/virtualNetworks/{_VNET_NAME}"
    f"/subnets/{_SUBNET_NAME}"
)


class _GetSubnetMocks(pulumi.runtime.Mocks):
    """Mock engine that handles getSubnet invoke calls."""

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
        """Return realistic data for the getSubnet invoke token."""
        if args.token == "azure-native:network:getSubnet":
            subnet_name = args.args.get("subnetName", "mock-subnet")
            vnet_name = args.args.get("virtualNetworkName", "mock-vnet")
            rg_name = args.args.get("resourceGroupName", "mock-rg")
            return (
                {
                    "name": subnet_name,
                    "id": (
                        "/subscriptions/00000000-0000-0000-0000-000000000000"
                        f"/resourceGroups/{rg_name}"
                        f"/providers/Microsoft.Network/virtualNetworks/{vnet_name}"
                        f"/subnets/{subnet_name}"
                    ),
                    "addressPrefix": "10.1.0.0/24",
                    "addressPrefixes": [],
                    "provisioningState": "Succeeded",
                    "etag": 'W/"00000000-0000-0000-0000-000000000001"',
                    "type": "Microsoft.Network/virtualNetworks/subnets",
                    "azureApiVersion": "2024-05-01",
                    "privateEndpointNetworkPolicies": "Disabled",
                    "privateLinkServiceNetworkPolicies": "Enabled",
                    "ipConfigurations": [],
                    "ipConfigurationProfiles": [],
                    "serviceAssociationLinks": [],
                    "resourceNavigationLinks": [],
                    "delegations": [],
                    "privateEndpoints": [],
                    "ipAllocations": [],
                },
                [],
            )
        return ({}, [])


@pytest.fixture(autouse=True)
def subnet_lookup_mocks() -> None:
    """Override mocks so getSubnet invokes return realistic data."""
    pulumi.runtime.set_mocks(
        _GetSubnetMocks(),
        project="test-project",
        stack="test-stack",
        preview=False,
    )


@pulumi.runtime.test
def test_returns_output() -> None:
    """get_subnet returns a non-None Output."""
    result = get_subnet(_SUBNET_NAME, _RG, _VNET_NAME)
    assert result is not None


@pulumi.runtime.test
def test_name_matches_input() -> None:
    """The returned name matches the name argument."""
    result = get_subnet(_SUBNET_NAME, _RG, _VNET_NAME)

    def check(r: object) -> None:
        assert getattr(r, "name", None) == _SUBNET_NAME

    return result.apply(check)


@pulumi.runtime.test
def test_id_is_populated() -> None:
    """The returned id is a non-empty string."""
    result = get_subnet(_SUBNET_NAME, _RG, _VNET_NAME)

    def check(r: object) -> None:
        assert getattr(r, "id", None)

    return result.apply(check)


@pulumi.runtime.test
def test_vnet_name_in_id() -> None:
    """The virtual network name appears in the returned resource ID."""
    result = get_subnet(_SUBNET_NAME, _RG, _VNET_NAME)

    def check(r: object) -> None:
        resource_id = getattr(r, "id", "") or ""
        assert _VNET_NAME in resource_id

    return result.apply(check)


@pulumi.runtime.test
def test_resource_group_in_id() -> None:
    """The resource group name appears in the returned resource ID."""
    result = get_subnet(_SUBNET_NAME, _RG, _VNET_NAME)

    def check(r: object) -> None:
        resource_id = getattr(r, "id", "") or ""
        assert _RG in resource_id

    return result.apply(check)
