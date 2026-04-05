"""Unit tests for pulumi_azure_modules.networking.VirtualNetwork."""

from __future__ import annotations

import pulumi

from pulumi_azure_modules.networking import VirtualNetwork

_RG = "rg-platform"
_LOCATION = "eastus"
_NAME = "vnet-platform"
_ADDRESS_PREFIXES = ["10.0.0.0/16"]


@pulumi.runtime.test
def test_name_output() -> None:
    """Name output resolves to the value supplied."""
    vnet = VirtualNetwork(
        "test-vnet",
        resource_group_name=_RG,
        location=_LOCATION,
        address_prefixes=_ADDRESS_PREFIXES,
        name=_NAME,
    )

    def check(v: str) -> None:
        assert v == _NAME

    return vnet.name.apply(check)


@pulumi.runtime.test
def test_location_output() -> None:
    """Location output resolves to the region supplied."""
    vnet = VirtualNetwork(
        "test-vnet",
        resource_group_name=_RG,
        location=_LOCATION,
        address_prefixes=_ADDRESS_PREFIXES,
        name=_NAME,
    )

    def check(v: str) -> None:
        assert v == _LOCATION

    return vnet.location.apply(check)


@pulumi.runtime.test
def test_id_is_populated() -> None:
    """Id output is non-empty after resource creation."""
    vnet = VirtualNetwork(
        "test-vnet",
        resource_group_name=_RG,
        location=_LOCATION,
        address_prefixes=_ADDRESS_PREFIXES,
        name=_NAME,
    )

    def check(v: str) -> None:
        assert v

    return vnet.id.apply(check)


@pulumi.runtime.test
def test_resource_group_name_output() -> None:
    """resource_group_name is surfaced so downstream resources can consume it."""
    vnet = VirtualNetwork(
        "test-vnet",
        resource_group_name=_RG,
        location=_LOCATION,
        address_prefixes=_ADDRESS_PREFIXES,
        name=_NAME,
    )

    def check(v: str) -> None:
        assert v == _RG

    return vnet.resource_group_name.apply(check)


@pulumi.runtime.test
def test_address_prefixes_output() -> None:
    """Address prefixes output resolves to the list supplied."""
    vnet = VirtualNetwork(
        "test-vnet",
        resource_group_name=_RG,
        location=_LOCATION,
        address_prefixes=_ADDRESS_PREFIXES,
        name=_NAME,
    )

    def check(v: list) -> None:
        assert v == _ADDRESS_PREFIXES

    return vnet.address_prefixes.apply(check)


@pulumi.runtime.test
def test_accepts_optional_params() -> None:
    """VirtualNetwork accepts dns_servers, enable_ddos_protection, and tags."""
    vnet = VirtualNetwork(
        "optional-params-vnet",
        resource_group_name=_RG,
        location=_LOCATION,
        address_prefixes=_ADDRESS_PREFIXES,
        name=_NAME,
        dns_servers=["168.63.129.16"],
        enable_ddos_protection=False,
        tags={"environment": "dev"},
    )
    assert vnet is not None
