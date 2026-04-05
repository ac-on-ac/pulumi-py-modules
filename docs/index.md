# pulumi-azure-modules

> Reusable Pulumi Python modules for deploying Azure resources — the Python
> equivalent of a Terraform module repository.

[![CI](https://github.com/ac-on-ac/pulumi-py-modules/actions/workflows/ci.yml/badge.svg)](https://github.com/ac-on-ac/pulumi-py-modules/actions/workflows/ci.yml)

---

## Installation

**From GitHub** (before the first PyPI release):

```bash
pip install git+https://github.com/ac-on-ac/pulumi-py-modules.git
```

**Pin a specific version or commit:**

```bash
pip install git+https://github.com/ac-on-ac/pulumi-py-modules.git@v0.1.0
```

---

## Quick start

```python
import pulumi
from pulumi_azure_modules.core import ResourceGroup
from pulumi_azure_modules.networking import (
    VirtualNetwork,
    PrivateDnsZone,
    VnetLinkArgs,
)

rg = ResourceGroup(
    "platform",
    location="eastus",
    name="rg-platform",
)

vnet = VirtualNetwork(
    "platform-vnet",
    resource_group_name=rg.name,
    location=rg.location,
    address_prefixes=["10.0.0.0/16"],
)

zone = PrivateDnsZone(
    "blob-dns",
    resource_group_name=rg.name,
    zone_name="privatelink.blob.core.windows.net",
    vnet_links=[VnetLinkArgs(vnet_id=vnet.id)],
)

pulumi.export("vnet_id", vnet.id)
pulumi.export("zone_name", zone.name)
```

---

## Modules

| Module | Contents |
|--------|----------|
| [`core`](core.md) | `ResourceGroup`, `get_resource_group` |
| [`networking`](networking.md) | `VirtualNetwork`, `PrivateDnsZone`, `NetworkWatcher`, and data-source lookups |
