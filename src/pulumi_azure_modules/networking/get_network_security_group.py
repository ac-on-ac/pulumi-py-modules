"""get_network_security_group data-source lookup."""

from __future__ import annotations

from typing import Any

import pulumi
import pulumi_azure_native.network as azure_network


def get_network_security_group(
    name: str,
    resource_group_name: str,
    expand: str | None = None,
    opts: pulumi.InvokeOptions | None = None,
) -> pulumi.Output[Any]:
    """Look up an existing Azure Network Security Group by name and resource group.

    Equivalent Terraform::

        data "azurerm_network_security_group" "example" {
          name                = "web-nsg"
          resource_group_name = "rg-platform"
        }

    Args:
        name:                The name of the network security group.
        resource_group_name: The resource group the NSG lives in.
        expand:              OData ``$expand`` expression — pass
                             ``"defaultSecurityRules"`` to include the
                             platform default rules in the response.
                             ``None`` omits the parameter.
        opts:                Pulumi invoke options.

    Returns:
        An ``Output`` with the following lifted attributes:

        - ``.name``               – ``Output[str]``        – NSG name
        - ``.location``           – ``Output[str]``        – Azure region
        - ``.id``                 – ``Output[str]``        – fully-qualified resource ID
        - ``.provisioning_state`` – ``Output[str]``        – provisioning state
        - ``.security_rules``     – ``Output[list]``       – user-defined security rules
        - ``.default_security_rules`` – ``Output[list]``   – platform default rules
        - ``.tags``               – ``Output[dict]``       – resource tags
    """
    return azure_network.get_network_security_group_output(
        network_security_group_name=name,
        resource_group_name=resource_group_name,
        expand=expand,
        opts=opts,
    )
