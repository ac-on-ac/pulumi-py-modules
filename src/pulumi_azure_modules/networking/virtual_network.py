"""VirtualNetwork component module."""

from __future__ import annotations

from typing import Any

import pulumi
import pulumi_azure_native.network as azure_network


class VirtualNetwork(pulumi.ComponentResource):
    """Creates an Azure Virtual Network.

    Example::

        from pulumi_azure_modules.networking import VirtualNetwork

        vnet = VirtualNetwork(
            "platform-vnet",
            resource_group_name="rg-platform",
            location="eastus",
            address_prefixes=["10.0.0.0/16"],
            name="vnet-platform",
            dns_servers=["168.63.129.16"],
        )

        # Pass address space to downstream resources (e.g. Subnets)
        # subnet = Subnet(
        #     "app-subnet",
        #     resource_group_name=vnet.resource_group_name,
        #     virtual_network_name=vnet.name,
        #     address_prefix="10.0.1.0/24",
        # )
    """

    name: pulumi.Output[str]
    """The name of the virtual network."""

    location: pulumi.Output[str]
    """The Azure region the virtual network was deployed to."""

    id: pulumi.Output[str]
    """The fully-qualified Azure resource ID.

    Format:
    ``/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/virtualNetworks/{name}``
    """

    resource_group_name: pulumi.Output[str]
    """The resource group the virtual network was deployed into.

    Retained as an output so downstream resources (e.g. Subnets, NSGs) can
    reference it without repeating the value.
    """

    address_prefixes: pulumi.Output[list[Any]]
    """The CIDR address prefixes assigned to the virtual network.

    Retained as an output so downstream resources (e.g. Subnets) can
    reference the VNet's address space without repeating the values.
    """

    def __init__(
        self,
        resource_name: str,
        resource_group_name: pulumi.Input[str],
        location: pulumi.Input[str],
        address_prefixes: pulumi.Input[list[Any]],
        name: pulumi.Input[str] | None = None,
        dns_servers: pulumi.Input[list[Any]] | None = None,
        enable_ddos_protection: pulumi.Input[bool] | None = None,
        tags: pulumi.Input[dict[str, str]] | None = None,
        opts: pulumi.ResourceOptions | None = None,
    ) -> None:
        """Create a Virtual Network.

        Args:
            resource_name:          Pulumi logical name (used as the state key).
            resource_group_name:    Resource group to deploy the VNet into.
            location:               Azure region, e.g. ``"eastus"``.
            address_prefixes:       One or more CIDR blocks for the VNet address
                                    space, e.g. ``["10.0.0.0/16"]``.
            name:                   Explicit resource name.  Auto-generated if
                                    omitted.
            dns_servers:            Custom DNS server IP addresses.  Leave
                                    ``None`` to use Azure-provided DNS
                                    (``168.63.129.16``).
            enable_ddos_protection: Enable DDoS Network Protection.  Requires a
                                    DDoS Protection Plan to be associated with
                                    the resource.  Defaults to ``False``.
            tags:                   Azure resource tags.
            opts:                   Pulumi resource options.
        """
        super().__init__(
            "pulumi-azure-modules:networking:VirtualNetwork",
            resource_name,
            {},
            opts,
        )

        child_opts = pulumi.ResourceOptions(parent=self)

        dhcp_options = (
            azure_network.DhcpOptionsArgs(dns_servers=dns_servers)
            if dns_servers is not None
            else None
        )

        vnet = azure_network.VirtualNetwork(
            resource_name,
            resource_group_name=resource_group_name,
            location=location,
            virtual_network_name=name,
            address_space=azure_network.AddressSpaceArgs(
                address_prefixes=address_prefixes,
            ),
            dhcp_options=dhcp_options,
            enable_ddos_protection=enable_ddos_protection,
            tags=tags,
            opts=child_opts,
        )

        self.name = vnet.name
        self.location = pulumi.Output.from_input(location)
        self.id = vnet.id
        self.resource_group_name = pulumi.Output.from_input(resource_group_name)
        self.address_prefixes = pulumi.Output.from_input(address_prefixes)

        self.register_outputs(
            {
                "name": self.name,
                "location": self.location,
                "id": self.id,
                "resource_group_name": self.resource_group_name,
                "address_prefixes": self.address_prefixes,
            }
        )
