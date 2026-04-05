"""pulumi-azure-modules: Reusable Pulumi Python modules for deploying Azure resources.

This package is the Python equivalent of a Terraform module repository.  Each
sub-package targets a logical grouping of Azure resource types and exposes
opinionated, composable functions (components) that wrap the low-level
``pulumi_azure_native`` SDK resources.

Sub-packages
------------
- :mod:`~pulumi_azure_modules.core`         – Resource Groups, Locks, Tags, Policy, etc.
- :mod:`~pulumi_azure_modules.compute`      – Virtual Machines, VMSS, etc.
- :mod:`~pulumi_azure_modules.networking`   – VNets, Subnets, NSGs, etc.
- :mod:`~pulumi_azure_modules.storage`      – Storage Accounts, Blobs, etc.
- :mod:`~pulumi_azure_modules.databases`    – SQL, CosmosDB, PostgreSQL, etc.
- :mod:`~pulumi_azure_modules.identity`     – Managed Identities, RBAC, etc.
- :mod:`~pulumi_azure_modules.keyvault`     – Key Vault, Secrets, Certs, etc.
- :mod:`~pulumi_azure_modules.monitoring`   – Log Analytics, App Insights, etc.
- :mod:`~pulumi_azure_modules.containers`   – AKS, ACR, Container Apps, etc.
"""

__version__ = "0.1.0"

__all__: list[str] = []
