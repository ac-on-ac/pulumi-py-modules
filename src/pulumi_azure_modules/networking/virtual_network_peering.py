"""VirtualNetworkPeering component module."""

from __future__ import annotations

import pulumi
import pulumi_azure_native.network as azure_network


class VirtualNetworkPeering(pulumi.ComponentResource):
    """Creates a bidirectional Azure Virtual Network Peering.

    Two ``VirtualNetworkPeering`` child resources are created — one in each
    direction — so that traffic can flow between the networks without the caller
    needing to declare both directions manually.

    Example::

        from pulumi_azure_modules.networking import VirtualNetwork, VirtualNetworkPeering

        hub = VirtualNetwork(
            "hub",
            resource_group_name="rg-hub",
            location="eastus",
            address_prefixes=["10.0.0.0/16"],
        )
        spoke = VirtualNetwork(
            "spoke",
            resource_group_name="rg-spoke",
            location="eastus",
            address_prefixes=["10.1.0.0/16"],
        )

        # Basic peering — no gateway transit
        peering = VirtualNetworkPeering(
            "hub-spoke",
            local_vnet_name=hub.name,
            local_vnet_id=hub.id,
            local_resource_group_name=hub.resource_group_name,
            remote_vnet_name=spoke.name,
            remote_vnet_id=spoke.id,
            remote_resource_group_name=spoke.resource_group_name,
        )

        # Hub-and-spoke with gateway transit
        peering = VirtualNetworkPeering(
            "hub-spoke-gw",
            local_vnet_name=hub.name,
            local_vnet_id=hub.id,
            local_resource_group_name=hub.resource_group_name,
            remote_vnet_name=spoke.name,
            remote_vnet_id=spoke.id,
            remote_resource_group_name=spoke.resource_group_name,
            allow_gateway_transit=True,   # hub advertises its gateway
            use_remote_gateways=True,     # spoke routes through hub's gateway
        )

    Note:
        For cross-subscription peering where only one side is managed in this
        stack, use ``pulumi_azure_native.network.VirtualNetworkPeering``
        directly.
    """

    local_peering_id: pulumi.Output[str]
    """Resource ID of the local → remote peering.

    Format:
    ``/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/virtualNetworks/{vnet}/virtualNetworkPeerings/{name}``
    """

    remote_peering_id: pulumi.Output[str]
    """Resource ID of the remote → local peering."""

    def __init__(
        self,
        resource_name: str,
        local_vnet_name: pulumi.Input[str],
        local_vnet_id: pulumi.Input[str],
        local_resource_group_name: pulumi.Input[str],
        remote_vnet_name: pulumi.Input[str],
        remote_vnet_id: pulumi.Input[str],
        remote_resource_group_name: pulumi.Input[str],
        allow_forwarded_traffic: pulumi.Input[bool] = False,
        allow_virtual_network_access: pulumi.Input[bool] = True,
        allow_gateway_transit: pulumi.Input[bool] = False,
        use_remote_gateways: pulumi.Input[bool] = False,
        opts: pulumi.ResourceOptions | None = None,
    ) -> None:
        """Create a bidirectional VNet peering.

        Args:
            resource_name:              Pulumi logical name (used as the state
                                        key and name prefix for child peerings).
            local_vnet_name:            Name of the local virtual network.
            local_vnet_id:              Fully-qualified resource ID of the local
                                        virtual network.
            local_resource_group_name:  Resource group of the local VNet.
            remote_vnet_name:           Name of the remote virtual network.
            remote_vnet_id:             Fully-qualified resource ID of the remote
                                        virtual network.
            remote_resource_group_name: Resource group of the remote VNet.
            allow_forwarded_traffic:    Allow traffic forwarded from (i.e. not
                                        originating in) either VNet to flow
                                        across the peering.  Defaults to
                                        ``False``.
            allow_virtual_network_access: Allow VMs in each VNet to communicate
                                        with VMs in the other.  Defaults to
                                        ``True``.
            allow_gateway_transit:      Applied to the **local → remote**
                                        peering.  Set ``True`` when the local
                                        VNet contains a VPN/ExpressRoute gateway
                                        that the remote VNet should use.
                                        Defaults to ``False``.
            use_remote_gateways:        Applied to the **remote → local**
                                        peering.  Set ``True`` when the remote
                                        VNet (spoke) should route through the
                                        local VNet's (hub's) gateway.  Requires
                                        ``allow_gateway_transit=True``.
                                        Defaults to ``False``.
            opts:                       Pulumi resource options.
        """
        super().__init__(
            "pulumi-azure-modules:networking:VirtualNetworkPeering",
            resource_name,
            {},
            opts,
        )

        # local → remote
        local_to_remote = azure_network.VirtualNetworkPeering(
            f"{resource_name}-local-to-remote",
            virtual_network_name=local_vnet_name,
            resource_group_name=local_resource_group_name,
            remote_virtual_network=azure_network.SubResourceArgs(id=remote_vnet_id),
            allow_forwarded_traffic=allow_forwarded_traffic,
            allow_virtual_network_access=allow_virtual_network_access,
            allow_gateway_transit=allow_gateway_transit,
            use_remote_gateways=False,
            opts=pulumi.ResourceOptions(parent=self),
        )

        # remote → local
        remote_to_local = azure_network.VirtualNetworkPeering(
            f"{resource_name}-remote-to-local",
            virtual_network_name=remote_vnet_name,
            resource_group_name=remote_resource_group_name,
            remote_virtual_network=azure_network.SubResourceArgs(id=local_vnet_id),
            allow_forwarded_traffic=allow_forwarded_traffic,
            allow_virtual_network_access=allow_virtual_network_access,
            allow_gateway_transit=False,
            use_remote_gateways=use_remote_gateways,
            opts=pulumi.ResourceOptions(parent=self),
        )

        self.local_peering_id = local_to_remote.id
        self.remote_peering_id = remote_to_local.id

        self.register_outputs(
            {
                "local_peering_id": self.local_peering_id,
                "remote_peering_id": self.remote_peering_id,
            }
        )
