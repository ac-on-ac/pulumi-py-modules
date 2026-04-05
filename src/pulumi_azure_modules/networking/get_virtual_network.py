"""get_virtual_network data-source lookup."""

from __future__ import annotations

from typing import Any

import pulumi
import pulumi_azure_native.network as azure_network


def get_virtual_network(
    name: str,
    resource_group_name: str,
    opts: pulumi.InvokeOptions | None = None,
) -> pulumi.Output[Any]:
    """Look up an existing Azure Virtual Network by name and resource group.

    Equivalent Terraform::

        data "azurerm_virtual_network" "example" {
          name                = "vnet-platform"
          resource_group_name = "rg-platform"
        }

    Args:
        name:                The name of the virtual network to look up.
        resource_group_name: The resource group the VNet lives in.
        opts:                Pulumi invoke options.

    Returns:
        An ``Output`` with the following lifted attributes:

        - ``.name``               – ``Output[str]``   – virtual network name
        - ``.location``           – ``Output[str]``   – Azure region
        - ``.id``                 – ``Output[str]``   – fully-qualified resource ID
        - ``.address_space``      – ``Output[...]``   – address space (contains
            ``.address_prefixes``)
        - ``.subnets``            – ``Output[list]``  – subnets in the VNet
        - ``.provisioning_state`` – ``Output[str]``   – provisioning state
        - ``.tags``               – ``Output[dict]``  – resource tags
    """
    return azure_network.get_virtual_network_output(
        virtual_network_name=name,
        resource_group_name=resource_group_name,
        opts=opts,
    )
