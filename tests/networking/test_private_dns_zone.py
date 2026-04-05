"""Unit tests for pulumi_azure_modules.networking.PrivateDnsZone."""

from __future__ import annotations

from typing import Any

import pulumi

from pulumi_azure_modules.networking import PrivateDnsZone, VnetLinkArgs

_RG = "rg-platform"
_ZONE_NAME = "privatelink.blob.core.windows.net"
_VNET_ID_1 = (
    "/subscriptions/00000000-0000-0000-0000-000000000000"
    "/resourceGroups/rg-platform"
    "/providers/Microsoft.Network/virtualNetworks/vnet-spoke"
)
_VNET_ID_2 = (
    "/subscriptions/00000000-0000-0000-0000-000000000000"
    "/resourceGroups/rg-platform"
    "/providers/Microsoft.Network/virtualNetworks/vnet-hub"
)


@pulumi.runtime.test
def test_name_output() -> None:
    """Name output resolves to the zone_name supplied."""
    zone = PrivateDnsZone(
        "test-zone",
        resource_group_name=_RG,
        zone_name=_ZONE_NAME,
    )

    def check(v: str) -> None:
        assert v == _ZONE_NAME

    return zone.name.apply(check)


@pulumi.runtime.test
def test_id_is_populated() -> None:
    """Id output is non-empty after resource creation."""
    zone = PrivateDnsZone(
        "test-zone",
        resource_group_name=_RG,
        zone_name=_ZONE_NAME,
    )

    def check(v: str) -> None:
        assert v

    return zone.id.apply(check)


@pulumi.runtime.test
def test_resource_group_name_output() -> None:
    """resource_group_name output resolves to the value supplied."""
    zone = PrivateDnsZone(
        "test-zone",
        resource_group_name=_RG,
        zone_name=_ZONE_NAME,
    )

    def check(v: str) -> None:
        assert v == _RG

    return zone.resource_group_name.apply(check)


@pulumi.runtime.test
def test_no_links_by_default() -> None:
    """link_ids is an empty list when no vnet_links are supplied."""
    zone = PrivateDnsZone(
        "test-zone",
        resource_group_name=_RG,
        zone_name=_ZONE_NAME,
    )

    def check(v: list[Any]) -> None:
        assert v == []

    return zone.link_ids.apply(check)


@pulumi.runtime.test
def test_creates_vnet_links() -> None:
    """link_ids contains one ID per entry in vnet_links."""
    zone = PrivateDnsZone(
        "test-zone",
        resource_group_name=_RG,
        zone_name=_ZONE_NAME,
        vnet_links=[
            VnetLinkArgs(vnet_id=_VNET_ID_1),
            VnetLinkArgs(vnet_id=_VNET_ID_2, registration_enabled=True),
        ],
    )

    def check(v: list[Any]) -> None:
        assert len(v) == 2

    return zone.link_ids.apply(check)


@pulumi.runtime.test
def test_explicit_link_name() -> None:
    """A VnetLinkArgs with an explicit link_name is accepted."""
    zone = PrivateDnsZone(
        "test-zone",
        resource_group_name=_RG,
        zone_name=_ZONE_NAME,
        vnet_links=[
            VnetLinkArgs(vnet_id=_VNET_ID_1, link_name="spoke-link"),
        ],
    )

    def check(v: list[Any]) -> None:
        assert len(v) == 1

    return zone.link_ids.apply(check)


@pulumi.runtime.test
def test_accepts_optional_params() -> None:
    """PrivateDnsZone accepts tags and produces a non-None resource."""
    zone = PrivateDnsZone(
        "tagged-zone",
        resource_group_name=_RG,
        zone_name=_ZONE_NAME,
        tags={"environment": "dev"},
    )
    assert zone is not None
