"""Container modules – AKS, Azure Container Registry, Azure Container Apps.

Planned functions
-----------------
- ``container_registry``  – Deploy an Azure Container Registry with optional
                            geo-replication and private endpoint.
- ``aks_cluster``         – Deploy an AKS cluster with a system node pool,
                            workload identity, and OIDC issuer enabled.
- ``container_app``       – Deploy an Azure Container App on a managed environment.
- ``container_app_env``   – Deploy an Azure Container App Environment backed by
                            a Log Analytics Workspace.

All functions in this sub-package return a Pulumi ``ComponentResource`` so
that they appear as a logical unit in the Pulumi state tree and outputs are
easily consumed by callers.
"""

__all__: list[str] = []
