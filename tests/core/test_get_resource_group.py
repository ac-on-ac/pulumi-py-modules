"""Unit tests for pulumi_azure_modules.core.get_resource_group.

``get_resource_group`` uses the Pulumi *invoke* path (a read-only data-source
lookup) rather than the resource-creation path, so the mock engine's ``call``
method must return realistic data.  A module-level ``autouse`` fixture overrides
the default conftest mocks with one that handles the ``getResourceGroup`` token.
"""

from __future__ import annotations

import pulumi
import pytest

from pulumi_azure_modules.core import get_resource_group

# ---------------------------------------------------------------------------
# Mock
# ---------------------------------------------------------------------------

_MOCK_LOCATION = "eastus"
_MOCK_TAGS = {"environment": "test", "managed_by": "pulumi"}


class _GetRGMocks(pulumi.runtime.Mocks):
    """Mock engine that handles getResourceGroup invoke calls."""

    def new_resource(
        self,
        args: pulumi.runtime.MockResourceArgs,
    ) -> tuple[str, dict]:
        return (f"{args.name}_id", args.inputs)

    def call(
        self,
        args: pulumi.runtime.MockCallArgs,
    ) -> tuple[dict, list]:
        if args.token == "azure-native:resources:getResourceGroup":
            rg_name = args.args.get("resourceGroupName", "mock-rg")
            return (
                {
                    "name": rg_name,
                    "location": _MOCK_LOCATION,
                    "id": (
                        "/subscriptions/00000000-0000-0000-0000-000000000000"
                        f"/resourceGroups/{rg_name}"
                    ),
                    "tags": _MOCK_TAGS,
                    "managedBy": "",
                    "type": "Microsoft.Resources/resourceGroups",
                    "azureApiVersion": "2024-03-01",
                    "properties": {"provisioningState": "Succeeded"},
                },
                [],
            )
        return ({}, [])


@pytest.fixture(autouse=True)
def rg_lookup_mocks() -> None:
    """Override conftest mocks so that getResourceGroup invokes return data."""
    pulumi.runtime.set_mocks(
        _GetRGMocks(),
        project="test-project",
        stack="test-stack",
        preview=False,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pulumi.runtime.test
def test_returns_output() -> None:
    """get_resource_group returns a non-None Output."""
    result = get_resource_group("rg-platform-dev")
    assert result is not None


@pulumi.runtime.test
def test_name_resolves() -> None:
    """The name attribute resolves to the looked-up resource group name."""
    result = get_resource_group("rg-platform-dev")

    def check(v: str) -> None:
        assert v == "rg-platform-dev"

    return result.name.apply(check)


@pulumi.runtime.test
def test_location_resolves() -> None:
    """The location attribute resolves to the resource group's region."""
    result = get_resource_group("rg-platform-dev")

    def check(v: str) -> None:
        assert v == _MOCK_LOCATION

    return result.location.apply(check)


@pulumi.runtime.test
def test_id_contains_rg_name() -> None:
    """The id attribute is a non-empty ARM resource ID containing the RG name."""
    result = get_resource_group("rg-platform-dev")

    def check(v: str) -> None:
        assert v
        assert "rg-platform-dev" in v

    return result.id.apply(check)


@pulumi.runtime.test
def test_tags_are_returned() -> None:
    """Tags from the existing resource group are surfaced in the output."""
    result = get_resource_group("rg-platform-dev")

    def check(v: dict) -> None:
        assert v == _MOCK_TAGS

    return result.tags.apply(check)


@pulumi.runtime.test
def test_different_rg_names_resolve_independently() -> None:
    """Two lookups with different names resolve to their respective names."""
    rg_a = get_resource_group("rg-network")
    rg_b = get_resource_group("rg-compute")

    def check_a(v: str) -> None:
        assert v == "rg-network"

    def check_b(v: str) -> None:
        assert v == "rg-compute"

    return pulumi.Output.all(
        rg_a.name.apply(check_a),
        rg_b.name.apply(check_b),
    )
