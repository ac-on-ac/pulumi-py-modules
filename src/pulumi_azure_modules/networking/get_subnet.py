"""get_subnet data-source lookup."""

from __future__ import annotations

from typing import Any

import pulumi
import pulumi_azure_native.network as azure_network


def get_subnet(
    name: str,
    resource_group_name: str,
    virtual_network_name: str,
    expand: str | None = None,
    opts: pulumi.InvokeOptions | None = None,
) -> pulumi.Output[Any]:
    """Look up an existing Azure Subnet by name, virtual network, and resource group.

    Equivalent Terraform::

        data "azurerm_subnet" "example" {
          name                 = "aks-subnet"
          virtual_network_name = "vnet-spoke"
          resource_group_name  = "rg-platform"
        }

    Args:
        name:                 The name of the subnet.
        resource_group_name:  The resource group the virtual network lives in.
        virtual_network_name: The name of the parent virtual network.
        expand:               OData ``$expand`` expression — pass
                              ``"networkSecurityGroup"`` to expand the NSG
                              details in the response.  ``None`` omits the
                              parameter.
        opts:                 Pulumi invoke options.

    Returns:
        An ``Output`` with the following lifted attributes:

        - ``.name``                  – ``Output[str]``   – subnet name
        - ``.id``                    – ``Output[str]``   – fully-qualified resource ID
        - ``.address_prefix``        – ``Output[str]``   – primary CIDR block
        - ``.address_prefixes``      – ``Output[list]``  – all CIDR blocks
        - ``.provisioning_state``    – ``Output[str]``   – provisioning state
        - ``.network_security_group`` – ``Output``       – associated NSG (if any)
        - ``.route_table``           – ``Output``        – associated route table (if any)
        - ``.service_endpoints``     – ``Output[list]``  – service endpoint entries
    """
    return azure_network.get_subnet_output(
        subnet_name=name,
        resource_group_name=resource_group_name,
        virtual_network_name=virtual_network_name,
        expand=expand,
        opts=opts,
    )
