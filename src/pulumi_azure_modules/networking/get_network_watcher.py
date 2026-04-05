"""get_network_watcher data-source lookup."""

from __future__ import annotations

from typing import Any

import pulumi
import pulumi_azure_native.network as azure_network


def get_network_watcher(
    name: str,
    resource_group_name: str,
    opts: pulumi.InvokeOptions | None = None,
) -> pulumi.Output[Any]:
    """Look up an existing Azure Network Watcher by name and resource group.

    Because Azure auto-creates a Network Watcher for every region a VNet is
    deployed in (placed in ``NetworkWatcherRG`` and named
    ``NetworkWatcher_{region}``), this function is typically the right choice
    over creating a new one.

    Equivalent Terraform::

        data "azurerm_network_watcher" "example" {
          name                = "NetworkWatcher_eastus"
          resource_group_name = "NetworkWatcherRG"
        }

    Args:
        name:                The name of the network watcher to look up.
        resource_group_name: The resource group the watcher lives in.
        opts:                Pulumi invoke options.

    Returns:
        An ``Output`` with the following lifted attributes:

        - ``.name``        – ``Output[str]`` – network watcher name
        - ``.location``    – ``Output[str]`` – Azure region
        - ``.id``          – ``Output[str]`` – fully-qualified resource ID
        - ``.tags``        – ``Output[dict]`` – tags on the watcher

    Example::

        from pulumi_azure_modules.networking import get_network_watcher
        from pulumi_azure_modules.networking import NsgFlowLog  # future module

        nw = get_network_watcher(
            name="NetworkWatcher_eastus",
            resource_group_name="NetworkWatcherRG",
        )

        # nw.name and nw.id feed directly into flow log / connection monitor args
    """
    return azure_network.get_network_watcher_output(
        network_watcher_name=name,
        resource_group_name=resource_group_name,
        opts=opts,
    )
