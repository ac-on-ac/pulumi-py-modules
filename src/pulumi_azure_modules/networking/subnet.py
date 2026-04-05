"""Subnet component module."""

from __future__ import annotations

import dataclasses
from typing import Optional

import pulumi
import pulumi_azure_native.network as azure_network

from pulumi_azure_modules.networking.network_security_group import (
    NetworkSecurityGroup,
    SecurityRuleArgs,
)
from pulumi_azure_modules.networking.route_table import RouteArgs, RouteTable


@dataclasses.dataclass
class DelegationArgs:
    """Arguments for a single subnet service delegation.

    Attributes:
        name:         Azure resource name for the delegation entry, unique
                      within the subnet (e.g. ``"aks-delegation"``).
        service_name: The delegated service, e.g.
                      ``"Microsoft.ContainerService/managedClusters"`` or
                      ``"Microsoft.Sql/servers"``.
        actions:      Explicit list of permitted actions.  When ``None``, the
                      provider derives the correct actions from
                      ``service_name`` automatically.
    """

    name: pulumi.Input[str]
    service_name: pulumi.Input[str]
    actions: list[str] | None = None


class Subnet(pulumi.ComponentResource):
    """Creates an Azure Subnet with optional NSG and route table associations.

    The NSG and route table can each be supplied in one of two ways:

    * **Existing resource** — pass the Azure resource ID via ``nsg_id`` or
      ``route_table_id``.  No child NSG or route table resource is created.
    * **New resource** — pass ``security_rules`` to deploy a new
      :class:`~pulumi_azure_modules.networking.NetworkSecurityGroup` child, or
      ``routes`` to deploy a new
      :class:`~pulumi_azure_modules.networking.RouteTable` child.  Both
      require ``location`` to be set.

    When both ``nsg_id`` and ``security_rules`` are provided, ``nsg_id`` takes
    precedence and no child NSG is created.  Likewise, ``route_table_id``
    takes precedence over ``routes``.

    Example — deploy a new NSG and route table::

        from pulumi_azure_modules.networking import (
            RouteArgs,
            SecurityRuleArgs,
            Subnet,
        )

        subnet = Subnet(
            "aks-subnet",
            resource_group_name="rg-platform",
            virtual_network_name="vnet-spoke",
            location="eastus",
            address_prefix="10.1.0.0/24",
            security_rules=[
                SecurityRuleArgs(
                    name="allow-https",
                    priority=100,
                    direction="Inbound",
                    access="Allow",
                    protocol="Tcp",
                    source_address_prefix="*",
                    source_port_range="*",
                    destination_address_prefix="*",
                    destination_port_range="443",
                ),
            ],
            routes=[
                RouteArgs(
                    name="to-internet",
                    next_hop_type="Internet",
                    address_prefix="0.0.0.0/0",
                ),
            ],
            service_endpoints=["Microsoft.Storage"],
            tags={"environment": "prod"},
        )

    Example — associate existing NSG and route table by resource ID::

        subnet = Subnet(
            "aks-subnet",
            resource_group_name="rg-platform",
            virtual_network_name="vnet-spoke",
            address_prefix="10.1.0.0/24",
            nsg_id="/subscriptions/.../networkSecurityGroups/my-nsg",
            route_table_id="/subscriptions/.../routeTables/my-rt",
        )
    """

    id: pulumi.Output[str]
    """The fully-qualified Azure resource ID of the subnet.

    Format:
    ``/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/
    virtualNetworks/{vnet}/subnets/{name}``
    """

    name: pulumi.Output[str]
    """The Azure resource name of the subnet."""

    address_prefix: pulumi.Output[Optional[str]]  # noqa: UP045
    """The primary address-prefix CIDR of the subnet (e.g. ``"10.1.0.0/24"``).

    This output is populated when ``address_prefix`` was passed at construction
    time.  It may be ``None`` when only ``address_prefixes`` was used.
    """

    resource_group_name: pulumi.Output[str]
    """The resource group the subnet was deployed into."""

    def __init__(
        self,
        resource_name: str,
        resource_group_name: pulumi.Input[str],
        virtual_network_name: pulumi.Input[str],
        address_prefix: pulumi.Input[str] | None = None,
        address_prefixes: list[str] | None = None,
        subnet_name: pulumi.Input[str] | None = None,
        location: pulumi.Input[str] | None = None,
        nsg_id: pulumi.Input[str] | None = None,
        security_rules: list[SecurityRuleArgs] | None = None,
        route_table_id: pulumi.Input[str] | None = None,
        routes: list[RouteArgs] | None = None,
        service_endpoints: list[str] | None = None,
        delegations: list[DelegationArgs] | None = None,
        default_outbound_access: pulumi.Input[bool] | None = None,
        tags: pulumi.Input[dict[str, str]] | None = None,
        opts: pulumi.ResourceOptions | None = None,
    ) -> None:
        """Create a subnet, optionally wiring up an NSG and/or route table.

        Args:
            resource_name:       Pulumi logical name (used as the state key and
                                 name prefix for child resources).
            resource_group_name: Resource group that contains the virtual
                                 network.
            virtual_network_name: The name of the parent virtual network.
            address_prefix:      Single CIDR block for the subnet, e.g.
                                 ``"10.1.0.0/24"``.  Mutually exclusive with
                                 ``address_prefixes``; at least one must be
                                 provided.
            address_prefixes:    List of CIDR blocks when the subnet spans
                                 multiple address ranges.  Mutually exclusive
                                 with ``address_prefix``; at least one must be
                                 provided.
            subnet_name:         Explicit Azure resource name for the subnet.
                                 Auto-generated by the provider when ``None``.
            location:            Azure region (e.g. ``"eastus"``).  Required
                                 when ``security_rules`` or ``routes`` are
                                 supplied so that child resources can be
                                 created.
            nsg_id:              Resource ID of a **pre-existing** NSG to
                                 associate with this subnet.  Takes precedence
                                 over ``security_rules`` when both are set.
            security_rules:      Security rules for a **new** NSG child
                                 resource.  Requires ``location``.  Ignored
                                 when ``nsg_id`` is also provided.
            route_table_id:      Resource ID of a **pre-existing** route table
                                 to associate with this subnet.  Takes
                                 precedence over ``routes`` when both are set.
            routes:              Routes for a **new** route table child
                                 resource.  Requires ``location``.  Ignored
                                 when ``route_table_id`` is also provided.
            service_endpoints:   List of Azure service names to enable service
                                 endpoints for, e.g.
                                 ``["Microsoft.Storage", "Microsoft.Sql"]``.
            delegations:         List of :class:`DelegationArgs` describing
                                 service delegations for the subnet.  When
                                 ``None``, no delegations are configured.
            default_outbound_access: When ``False``, disables default outbound
                                 connectivity for all VMs in the subnet.
                                 **This flag can only be set at subnet creation
                                 time and cannot be changed afterwards.**
                                 Defaults to ``None`` (provider default —
                                 currently ``True``).
            tags:                Azure resource tags applied to the subnet and,
                                 when created, to any child NSG or route table.
            opts:                Pulumi resource options.

        Raises:
            ValueError: When ``security_rules`` are provided without
                        ``location``, or when ``routes`` are provided without
                        ``location``.
        """
        super().__init__(
            "pulumi-azure-modules:networking:Subnet",
            resource_name,
            {},
            opts,
        )

        # ------------------------------------------------------------------
        # Resolve effective NSG reference.
        # ------------------------------------------------------------------
        nsg_args: azure_network.NetworkSecurityGroupArgs | None = None
        if nsg_id is not None:
            nsg_args = azure_network.NetworkSecurityGroupArgs(id=nsg_id)
        elif security_rules is not None:
            if location is None:
                raise ValueError("location is required when security_rules are provided")
            child_nsg = NetworkSecurityGroup(
                f"{resource_name}-nsg",
                resource_group_name=resource_group_name,
                location=location,
                security_rules=security_rules,
                tags=tags,
                opts=pulumi.ResourceOptions(parent=self),
            )
            nsg_args = azure_network.NetworkSecurityGroupArgs(id=child_nsg.id)

        # ------------------------------------------------------------------
        # Resolve effective route table reference.
        # ------------------------------------------------------------------
        rt_args: azure_network.RouteTableArgs | None = None
        if route_table_id is not None:
            rt_args = azure_network.RouteTableArgs(id=route_table_id)
        elif routes is not None:
            if location is None:
                raise ValueError("location is required when routes are provided")
            child_rt = RouteTable(
                f"{resource_name}-rt",
                resource_group_name=resource_group_name,
                location=location,
                routes=routes,
                tags=tags,
                opts=pulumi.ResourceOptions(parent=self),
            )
            rt_args = azure_network.RouteTableArgs(id=child_rt.id)

        # ------------------------------------------------------------------
        # Build service endpoint properties list.
        # ------------------------------------------------------------------
        svc_ep_args: list[azure_network.ServiceEndpointPropertiesFormatArgs] | None = None
        if service_endpoints:
            svc_ep_args = [
                azure_network.ServiceEndpointPropertiesFormatArgs(service=svc)
                for svc in service_endpoints
            ]

        # ------------------------------------------------------------------
        # Build delegation args list.
        # ------------------------------------------------------------------
        delegation_args: list[azure_network.DelegationArgs] | None = None
        if delegations:
            delegation_args = [
                azure_network.DelegationArgs(
                    name=d.name,
                    service_name=d.service_name,
                    actions=d.actions,
                )
                for d in delegations
            ]

        # ------------------------------------------------------------------
        # Deploy the subnet.
        # ------------------------------------------------------------------
        subnet = azure_network.Subnet(
            f"{resource_name}-subnet",
            resource_group_name=resource_group_name,
            virtual_network_name=virtual_network_name,
            subnet_name=subnet_name,
            address_prefix=address_prefix,
            address_prefixes=address_prefixes,
            network_security_group=nsg_args,
            route_table=rt_args,
            service_endpoints=svc_ep_args,
            delegations=delegation_args,
            default_outbound_access=default_outbound_access,
            opts=pulumi.ResourceOptions(parent=self),
        )

        self.id = subnet.id
        self.name = subnet.name  # type: ignore[assignment]
        self.resource_group_name = pulumi.Output.from_input(resource_group_name)
        self.address_prefix = subnet.address_prefix

        self.register_outputs(
            {
                "id": self.id,
                "name": self.name,
                "address_prefix": self.address_prefix,
                "resource_group_name": self.resource_group_name,
            }
        )
