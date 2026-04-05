"""get_route_table data-source lookup."""

from __future__ import annotations

from typing import Any

import pulumi
import pulumi_azure_native.network as azure_network


def get_route_table(
    name: str,
    resource_group_name: str,
    expand: str | None = None,
    opts: pulumi.InvokeOptions | None = None,
) -> pulumi.Output[Any]:
    """Look up an existing Azure Route Table by name and resource group.

    Equivalent Terraform::

        data "azurerm_route_table" "example" {
          name                = "spoke-rt"
          resource_group_name = "rg-platform"
        }

    Args:
        name:                The name of the route table.
        resource_group_name: The resource group the route table lives in.
        expand:              OData ``$expand`` expression — pass
                             ``"routes"`` to expand the routes collection in
                             the response.  ``None`` omits the parameter.
        opts:                Pulumi invoke options.

    Returns:
        An ``Output`` with the following lifted attributes:

        - ``.name``                          – ``Output[str]``   – route table name
        - ``.location``                      – ``Output[str]``   – Azure region
        - ``.id``                            – ``Output[str]``   – fully-qualified resource ID
        - ``.provisioning_state``            – ``Output[str]``   – provisioning state
        - ``.routes``                        – ``Output[list]``  – routes in the table
        - ``.disable_bgp_route_propagation`` – ``Output[bool]``  – BGP propagation flag
        - ``.tags``                          – ``Output[dict]``  – resource tags
    """
    return azure_network.get_route_table_output(
        route_table_name=name,
        resource_group_name=resource_group_name,
        expand=expand,
        opts=opts,
    )
