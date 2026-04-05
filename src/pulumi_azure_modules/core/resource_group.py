"""ResourceGroup component module."""

from __future__ import annotations

import pulumi
import pulumi_azure_native.resources as azure_resources


class ResourceGroup(pulumi.ComponentResource):
    """Creates an Azure Resource Group.

    Example::

        from pulumi_azure_modules.core import ResourceGroup

        rg = ResourceGroup(
            "platform-rg",
            location="eastus",
            name="rg-platform-dev",
            tags={"environment": "dev"},
        )

        pulumi.export("rg_name", rg.name)
        pulumi.export("rg_id",   rg.id)
    """

    name: pulumi.Output[str]
    """The name of the resource group."""

    location: pulumi.Output[str]
    """The Azure region the resource group was deployed to."""

    id: pulumi.Output[str]
    """The fully-qualified Azure resource ID.

    Format: ``/subscriptions/{subscriptionId}/resourceGroups/{name}``
    """

    def __init__(
        self,
        resource_name: str,
        location: pulumi.Input[str],
        name: pulumi.Input[str] | None = None,
        managed_by: pulumi.Input[str] | None = None,
        tags: pulumi.Input[dict[str, str]] | None = None,
        opts: pulumi.ResourceOptions | None = None,
    ) -> None:
        """Create a Resource Group.

        Args:
            resource_name: Pulumi logical name (used as the state key).
            location:      Azure region, e.g. ``"eastus"``.
            name:          Resource group name.  Auto-generated if omitted.
            managed_by:    Resource ID of the managing resource, if any.
            tags:          Tags to assign to the resource group.
            opts:          Pulumi resource options.
        """
        super().__init__(
            "pulumi-azure-modules:core:ResourceGroup",
            resource_name,
            {"name": None, "location": None, "id": None},
            opts,
        )

        rg = azure_resources.ResourceGroup(
            resource_name,
            location=location,
            resource_group_name=name,
            managed_by=managed_by,
            tags=tags,
            opts=pulumi.ResourceOptions(parent=self),
        )

        self.name = rg.name
        self.location = rg.location
        self.id = rg.id

        self.register_outputs({"name": self.name, "location": self.location, "id": self.id})
