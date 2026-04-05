"""Unit tests for pulumi_azure_modules.core.resource_group."""

from __future__ import annotations

import pulumi

from pulumi_azure_modules.core import ResourceGroup


@pulumi.runtime.test
def test_location_output() -> None:
    """Location output resolves to the value supplied."""
    rg = ResourceGroup("test-rg", location="uksouth", name="rg-test")

    def check(v: str) -> None:
        assert v == "uksouth"

    return rg.location.apply(check)


@pulumi.runtime.test
def test_name_output() -> None:
    """Name output resolves to the provided resource group name."""
    rg = ResourceGroup("test-rg", location="eastus", name="rg-platform-dev")

    def check(v: str) -> None:
        assert v == "rg-platform-dev"

    return rg.name.apply(check)


@pulumi.runtime.test
def test_id_is_populated() -> None:
    """Id output is non-empty after resource creation."""
    rg = ResourceGroup("test-rg", location="eastus", name="rg-test")

    def check(v: str) -> None:
        assert v

    return rg.id.apply(check)


@pulumi.runtime.test
def test_name_is_optional() -> None:
    """ResourceGroup can be constructed without an explicit name."""
    rg = ResourceGroup("auto-named-rg", location="westeurope")
    assert rg is not None


@pulumi.runtime.test
def test_accepts_tags() -> None:
    """Tags are accepted without error."""
    rg = ResourceGroup(
        "tagged-rg",
        location="eastus",
        name="rg-tagged",
        tags={"environment": "dev", "owner": "platform-team"},
    )
    assert rg is not None


@pulumi.runtime.test
def test_accepts_managed_by() -> None:
    """managed_by is forwarded without error."""
    rg = ResourceGroup(
        "managed-rg",
        location="eastus",
        name="rg-managed",
        managed_by="/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mgmt-rg",
    )
    assert rg is not None
