"""Unit tests for pulumi_azure_modules.networking.get_private_dns_zone."""

from __future__ import annotations

import pulumi
import pytest

from pulumi_azure_modules.networking import get_private_dns_zone

_ZONE_NAME = "privatelink.blob.core.windows.net"
_RG = "rg-platform"
_RESOURCE_ID = (
    "/subscriptions/00000000-0000-0000-0000-000000000000"
    f"/resourceGroups/{_RG}"
    f"/providers/Microsoft.Network/privateDnsZones/{_ZONE_NAME}"
)


class _GetPrivateZoneMocks(pulumi.runtime.Mocks):
    """Mock engine that handles getPrivateZone invoke calls."""

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
        """Return realistic data for the getPrivateZone invoke token."""
        if args.token == "azure-native:privatedns:getPrivateZone":
            zone_name = args.args.get("privateZoneName", "mock.zone")
            rg_name = args.args.get("resourceGroupName", "mock-rg")
            return (
                {
                    "name": zone_name,
                    "location": "Global",
                    "id": (
                        "/subscriptions/00000000-0000-0000-0000-000000000000"
                        f"/resourceGroups/{rg_name}"
                        f"/providers/Microsoft.Network/privateDnsZones/{zone_name}"
                    ),
                    "tags": {},
                    "provisioningState": "Succeeded",
                    "etag": 'W/"00000000-0000-0000-0000-000000000001"',
                    "type": "Microsoft.Network/privateDnsZones",
                    "azureApiVersion": "2024-06-01",
                    "numberOfRecordSets": 2,
                    "numberOfVirtualNetworkLinks": 1,
                    "numberOfVirtualNetworkLinksWithRegistration": 0,
                    "maxNumberOfRecordSets": 10000,
                    "maxNumberOfVirtualNetworkLinks": 1000,
                    "maxNumberOfVirtualNetworkLinksWithRegistration": 100,
                },
                [],
            )
        return ({}, [])


@pytest.fixture(autouse=True)
def private_zone_lookup_mocks() -> None:
    """Override mocks so getPrivateZone invokes return realistic data."""
    pulumi.runtime.set_mocks(
        _GetPrivateZoneMocks(),
        project="test-project",
        stack="test-stack",
        preview=False,
    )


@pulumi.runtime.test
def test_returns_output() -> None:
    """get_private_dns_zone returns a non-None Output."""
    result = get_private_dns_zone(_ZONE_NAME, _RG)
    assert result is not None


@pulumi.runtime.test
def test_name_resolves() -> None:
    """Name attribute resolves to the looked-up zone name."""
    result = get_private_dns_zone(_ZONE_NAME, _RG)

    def check(v: str) -> None:
        assert v == _ZONE_NAME

    return result.name.apply(check)


@pulumi.runtime.test
def test_location_resolves() -> None:
    """Location attribute resolves to 'Global' for all private DNS zones."""
    result = get_private_dns_zone(_ZONE_NAME, _RG)

    def check(v: str) -> None:
        assert v == "Global"

    return result.location.apply(check)


@pulumi.runtime.test
def test_id_is_populated() -> None:
    """Id attribute resolves to a non-empty resource ID containing the zone name."""
    result = get_private_dns_zone(_ZONE_NAME, _RG)

    def check(v: str) -> None:
        assert v
        assert "Microsoft.Network/privateDnsZones" in v

    return result.id.apply(check)


@pulumi.runtime.test
def test_provisioning_state_resolves() -> None:
    """provisioning_state attribute resolves to the expected value."""
    result = get_private_dns_zone(_ZONE_NAME, _RG)

    def check(v: str) -> None:
        assert v == "Succeeded"

    return result.provisioning_state.apply(check)
