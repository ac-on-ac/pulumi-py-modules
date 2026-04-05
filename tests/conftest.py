"""Shared Pytest fixtures for the pulumi-azure-modules test suite.

Pulumi unit tests run entirely in-process against a mock engine so no real
Azure credentials or a live Pulumi backend are required.  The ``pulumi_mocks``
fixture below wires that up automatically for every test in the suite.

Usage
-----
Because the fixture is marked ``autouse=True`` you don't need to reference it
in individual test functions – just write normal ``async`` test functions and
decorate them with ``@pulumi.runtime.test``:

    import pulumi
    import pytest

    @pulumi.runtime.test
    def test_something():
        # arrange / act
        result = my_module.deploy(...)

        # assert on Output values
        def check(value):
            assert value == "expected"

        result.some_output.apply(check)

See https://www.pulumi.com/docs/using-pulumi/testing/unit/ for the full guide.
"""

from __future__ import annotations

import pulumi
import pytest


class _PulumiMocks(pulumi.runtime.Mocks):
    """Minimal Pulumi mock engine used by all unit tests.

    Behaviour:
    - ``new_resource`` – returns ``<name>_id`` as the resource id and passes
      through all input properties as outputs.  SDK resources pass their name
      via a type-specific input key (e.g. ``resourceGroupName``) but expose it
      as ``name`` in outputs; this mock normalises that so tests can assert on
      ``.name`` without extra wiring.
    - ``call``         – returns an empty dict; override in individual tests when
      you need to mock a specific provider function call.
    """

    # Ordered list of SDK input keys that represent the resource's own name.
    # Ordering invariant: a key must come AFTER all keys that are more specific
    # than it.  Keys that double as parent-resource references (e.g.
    # ``virtualNetworkName`` for Subnet, ``resourceGroupName`` for everything)
    # must appear AFTER the child resource's own name key, so that child
    # resources resolve to their own name rather than their parent's.
    #
    # Concretely:
    #   - Subnet has both ``subnetName`` (own) and ``virtualNetworkName`` (parent)
    #     → ``subnetName`` must precede ``virtualNetworkName``
    #   - Most resources have ``resourceGroupName`` (parent) as well as their own
    #     name key → ``resourceGroupName`` must remain last
    _NAME_INPUT_KEYS: tuple[str, ...] = (
        "networkWatcherName",
        "subnetName",
        "networkSecurityGroupName",
        "accountName",
        "vaultName",
        "clusterName",
        "workspaceName",
        "serverName",
        "registryName",
        "databaseName",
        "virtualNetworkName",  # parent ref for subnets/peerings; own name for VNets — after child-resource keys
        "resourceGroupName",   # must remain last — parent ref for almost every resource
    )

    def new_resource(
        self,
        args: pulumi.runtime.MockResourceArgs,
    ) -> tuple[str, dict]:
        outputs = dict(args.inputs)
        # Map the SDK-specific name input to the common ``name`` output key so
        # that tests can assert on ``.name`` without needing per-resource mocks.
        if "name" not in outputs:
            for key in self._NAME_INPUT_KEYS:
                if key in outputs:
                    outputs["name"] = outputs[key]
                    break
        return (f"{args.name}_id", outputs)

    def call(
        self,
        args: pulumi.runtime.MockCallArgs,
    ) -> tuple[dict, list[tuple[str, str]]]:
        return ({}, [])


@pytest.fixture(autouse=True)
def pulumi_mocks() -> None:
    """Install Pulumi mock engine before each test and reset afterwards."""
    pulumi.runtime.set_mocks(
        _PulumiMocks(),
        project="test-project",
        stack="test-stack",
        preview=False,
    )
