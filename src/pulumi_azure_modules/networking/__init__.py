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

Planned
-------
- ``Subnet``              – Deploy a Subnet with optional service endpoints.
- ``NetworkSecurityGroup`` – Deploy an NSG with a set of rules.
- ``PrivateEndpoint``     – Wire up a Private Endpoint for a PaaS resource.
"""

from pulumi_azure_modules.networking.get_network_watcher import get_network_watcher
from pulumi_azure_modules.networking.get_private_dns_zone import get_private_dns_zone
from pulumi_azure_modules.networking.get_virtual_network import get_virtual_network
from pulumi_azure_modules.networking.network_watcher import NetworkWatcher
from pulumi_azure_modules.networking.private_dns_zone import PrivateDnsZone, VnetLinkArgs
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
]
