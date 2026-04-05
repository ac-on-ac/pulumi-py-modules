"""get_resource_group data-source lookup.

This is the Pulumi equivalent of Terraform's ``data "azurerm_resource_group"``
block.  It performs a read-only lookup against the Azure API at deploy time and
returns an ``Output`` whose attributes can be passed directly to any resource
that accepts ``Input[str]`` — no ``.apply()`` unwrapping required.
"""

from __future__ import annotations

from typing import Any

import pulumi
import pulumi_azure_native.resources as azure_resources


def get_resource_group(
    name: str,
    opts: pulumi.InvokeOptions | None = None,
) -> pulumi.Output[Any]:
    """Look up an existing Azure Resource Group by name.

    This is the ``_output`` form of the SDK invoke, meaning the return value is
    an ``Output`` that stays inside Pulumi's dependency graph.  Downstream
    resources will automatically wait for this lookup to resolve before they
    are created.

    Equivalent Terraform::

        data "azurerm_resource_group" "example" {
          name = "rg-platform-dev"
        }

    Args:
        name: The name of the resource group to look up (case-insensitive).
        opts: Pulumi invoke options, e.g. to pin a specific provider instance
              or API version.

    Returns:
        An ``Output`` with the following lifted attributes:

        - ``.name``       – ``Output[str]`` – resource group name
        - ``.location``   – ``Output[str]`` – Azure region
        - ``.id``         – ``Output[str]`` – fully-qualified resource ID
        - ``.tags``       – ``Output[dict]`` – tags on the resource group
        - ``.managed_by`` – ``Output[str]`` – managing resource ID, if any

    Example::

        from pulumi_azure_modules.core import get_resource_group
        from pulumi_azure_modules.networking import VirtualNetwork

        rg = get_resource_group("rg-platform-dev")

        vnet = VirtualNetwork(
            "platform-vnet",
            location=rg.location,
            resource_group_name=rg.name,
            address_space=["10.0.0.0/16"],
        )
    """
    return azure_resources.get_resource_group_output(
        resource_group_name=name,
        opts=opts,
    )
