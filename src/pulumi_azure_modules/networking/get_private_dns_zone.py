"""get_private_dns_zone data-source lookup."""

from __future__ import annotations

from typing import Any

import pulumi
import pulumi_azure_native.privatedns as azure_privatedns


def get_private_dns_zone(
    name: str,
    resource_group_name: str,
    opts: pulumi.InvokeOptions | None = None,
) -> pulumi.Output[Any]:
    """Look up an existing Azure Private DNS Zone by name and resource group.

    Equivalent Terraform::

        data "azurerm_private_dns_zone" "example" {
          name                = "privatelink.blob.core.windows.net"
          resource_group_name = "rg-platform"
        }

    Args:
        name:                The name of the private DNS zone (without a
                             terminating dot), e.g.
                             ``"privatelink.blob.core.windows.net"``.
        resource_group_name: The resource group the zone lives in.
        opts:                Pulumi invoke options.

    Returns:
        An ``Output`` with the following lifted attributes:

        - ``.name``                – ``Output[str]``  – zone name
        - ``.location``            – ``Output[str]``  – always ``"Global"``
        - ``.id``                  – ``Output[str]``  – fully-qualified resource ID
        - ``.provisioning_state``  – ``Output[str]``  – provisioning state
        - ``.number_of_record_sets`` – ``Output[int]`` – current record-set count
        - ``.number_of_virtual_network_links`` – ``Output[int]`` – linked VNet count
        - ``.tags``                – ``Output[dict]`` – resource tags
    """
    return azure_privatedns.get_private_zone_output(
        private_zone_name=name,
        resource_group_name=resource_group_name,
        opts=opts,
    )
