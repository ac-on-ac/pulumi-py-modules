"""Networking modules – VNets, Subnets, NSGs, Private Endpoints, DNS, etc.

Exports
-------
- :class:`~pulumi_azure_modules.networking.network_watcher.NetworkWatcher`
- :func:`~pulumi_azure_modules.networking.get_network_watcher.get_network_watcher`
- :class:`~pulumi_azure_modules.networking.virtual_network.VirtualNetwork`
- :func:`~pulumi_azure_modules.networking.get_virtual_network.get_virtual_network`
- :class:`~pulumi_azure_modules.networking.private_dns_zone.PrivateDnsZone`
- :class:`~pulumi_azure_modules.networking.private_dns_zone.VnetLinkArgs`
- :func:`~pulumi_azure_modules.networking.get_private_dns_zone.get_private_dns_zone`
- :class:`~pulumi_azure_modules.networking.virtual_network_peering.VirtualNetworkPeering`
- :class:`~pulumi_azure_modules.networking.network_security_group.NetworkSecurityGroup`
- :class:`~pulumi_azure_modules.networking.network_security_group.SecurityRuleArgs`
- :func:`~pulumi_azure_modules.networking.get_network_security_group.get_network_security_group`
- :class:`~pulumi_azure_modules.networking.route_table.RouteTable`
- :class:`~pulumi_azure_modules.networking.route_table.RouteArgs`
- :func:`~pulumi_azure_modules.networking.get_route_table.get_route_table`
- :class:`~pulumi_azure_modules.networking.subnet.Subnet`
- :class:`~pulumi_azure_modules.networking.subnet.DelegationArgs`
- :func:`~pulumi_azure_modules.networking.get_subnet.get_subnet`

Planned
-------
- ``PrivateEndpoint`` – Wire up a Private Endpoint for a PaaS resource.
"""

from pulumi_azure_modules.networking.get_network_security_group import (
    get_network_security_group,
)
from pulumi_azure_modules.networking.get_network_watcher import get_network_watcher
from pulumi_azure_modules.networking.get_private_dns_zone import get_private_dns_zone
from pulumi_azure_modules.networking.get_route_table import get_route_table
from pulumi_azure_modules.networking.get_subnet import get_subnet
from pulumi_azure_modules.networking.get_virtual_network import get_virtual_network
from pulumi_azure_modules.networking.network_security_group import (
    NetworkSecurityGroup,
    SecurityRuleArgs,
)
from pulumi_azure_modules.networking.network_watcher import NetworkWatcher
from pulumi_azure_modules.networking.private_dns_zone import PrivateDnsZone, VnetLinkArgs
from pulumi_azure_modules.networking.route_table import RouteArgs, RouteTable
from pulumi_azure_modules.networking.subnet import DelegationArgs, Subnet
from pulumi_azure_modules.networking.virtual_network import VirtualNetwork
from pulumi_azure_modules.networking.virtual_network_peering import VirtualNetworkPeering

__all__ = [
    "NetworkWatcher",
    "get_network_watcher",
    "VirtualNetwork",
    "get_virtual_network",
    "PrivateDnsZone",
    "VnetLinkArgs",
    "get_private_dns_zone",
    "VirtualNetworkPeering",
    "NetworkSecurityGroup",
    "SecurityRuleArgs",
    "get_network_security_group",
    "RouteTable",
    "RouteArgs",
    "get_route_table",
    "Subnet",
    "DelegationArgs",
    "get_subnet",
]
