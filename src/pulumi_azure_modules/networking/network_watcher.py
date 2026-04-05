"""NetworkWatcher component module."""

from __future__ import annotations

from typing import Optional

import pulumi
import pulumi_azure_native.network as azure_network


class NetworkWatcher(pulumi.ComponentResource):
    """Creates an Azure Network Watcher.

    Network Watchers are regional singletons — one per subscription per region.
    Azure auto-creates one (named ``NetworkWatcher_{region}`` in
    ``NetworkWatcherRG``) the first time a VNet is deployed in a region, so in
    most cases you should use :func:`get_network_watcher` to look up the
    existing one rather than creating a new one.

    If you *do* need to bring an auto-created watcher under Pulumi management,
    pass ``opts=pulumi.ResourceOptions(import_="<resource-id>")`` on the first
    run — this avoids Pulumi trying to create a duplicate.

    Example::

        from pulumi_azure_modules.networking import NetworkWatcher

        nw = NetworkWatcher(
            "platform-nw",
            resource_group_name="rg-network",
            location="eastus",
            name="nw-eastus",
        )

        # Pass to a flow log (future module)
        # flow_log = NsgFlowLog(
        #     "platform-flow-log",
        #     network_watcher_name=nw.name,
        #     resource_group_name=nw.resource_group_name,
        #     ...
        # )
    """

    name: pulumi.Output[str]
    """The name of the network watcher."""

    location: pulumi.Output[str]
    """The Azure region the network watcher was deployed to."""

    id: pulumi.Output[str]
    """The fully-qualified Azure resource ID.

    Format:
    ``/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/networkWatchers/{name}``
    """

    resource_group_name: pulumi.Output[str]
    """The resource group the network watcher was deployed into.

    Retained as an output because downstream resources (NSG Flow Logs,
    Connection Monitors) require both ``network_watcher_name`` and
    ``resource_group_name``.
    """

    def __init__(
        self,
        resource_name: str,
        resource_group_name: pulumi.Input[str],
        location: pulumi.Input[str],
        name: Optional[pulumi.Input[str]] = None,
        tags: Optional[pulumi.Input[dict[str, str]]] = None,
        opts: Optional[pulumi.ResourceOptions] = None,
    ) -> None:
        """Create a Network Watcher.

        Args:
            resource_name:       Pulumi logical name (used as the state key).
            resource_group_name: Resource group to deploy the watcher into.
            location:            Azure region, e.g. ``"eastus"``.
            name:                Explicit resource name.  Auto-generated if
                                 omitted.  Azure convention is
                                 ``NetworkWatcher_{region}``.
            tags:                Tags to assign to the resource.
            opts:                Pulumi resource options.  Pass
                                 ``import_="<resource-id>"`` to adopt an
                                 existing auto-created watcher.
        """
        super().__init__(
            "pulumi-azure-modules:networking:NetworkWatcher",
            resource_name,
            {
                "name": None,
                "location": None,
                "id": None,
                "resource_group_name": None,
            },
            opts,
        )

        nw = azure_network.NetworkWatcher(
            resource_name,
            resource_group_name=resource_group_name,
            location=location,
            network_watcher_name=name,
            tags=tags,
            opts=pulumi.ResourceOptions(parent=self),
        )

        self.name = nw.name
        self.location = nw.location
        self.id = nw.id
        self.resource_group_name = pulumi.Output.from_input(resource_group_name)

        self.register_outputs(
            {
                "name": self.name,
                "location": self.location,
                "id": self.id,
                "resource_group_name": self.resource_group_name,
            }
        )
