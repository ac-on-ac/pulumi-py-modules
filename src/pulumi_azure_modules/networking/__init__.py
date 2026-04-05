"""Networking modules – VNets, Subnets, NSGs, Private Endpoints, DNS, etc.

Exports
-------
- :class:`~pulumi_azure_modules.networking.network_watcher.NetworkWatcher`
- :func:`~pulumi_azure_modules.networking.get_network_watcher.get_network_watcher`

Planned
-------
- ``VirtualNetwork``      – Deploy a VNet with a configurable address space.
- ``Subnet``              – Deploy a Subnet with optional service endpoints.
- ``NetworkSecurityGroup`` – Deploy an NSG with a set of rules.
- ``PrivateEndpoint``     – Wire up a Private Endpoint for a PaaS resource.
- ``PrivateDnsZone``      – Deploy and link a Private DNS Zone to a VNet.
"""

from pulumi_azure_modules.networking.get_network_watcher import get_network_watcher
from pulumi_azure_modules.networking.network_watcher import NetworkWatcher

__all__ = ["NetworkWatcher", "get_network_watcher"]
