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
      through all input properties as outputs.
    - ``call``         – returns an empty dict; override in individual tests when
      you need to mock a specific provider function call.
    """

    def new_resource(
        self,
        args: pulumi.runtime.MockResourceArgs,
    ) -> tuple[str, dict]:
        return (f"{args.name}_id", args.inputs)

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
