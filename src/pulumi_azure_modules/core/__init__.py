"""Core modules – foundational Azure resource primitives.

This sub-package covers resources in the ``azure_native.resources`` namespace:
resource groups, management groups, subscriptions, resource locks, tags, and
policy assignments.  These are typically the first resources created in any
deployment and are depended on by every other sub-package.

Exports
-------
- :class:`~pulumi_azure_modules.core.resource_group.ResourceGroup`
- :func:`~pulumi_azure_modules.core.get_resource_group.get_resource_group`
"""

from pulumi_azure_modules.core.get_resource_group import get_resource_group
from pulumi_azure_modules.core.resource_group import ResourceGroup

__all__ = ["ResourceGroup", "get_resource_group"]
