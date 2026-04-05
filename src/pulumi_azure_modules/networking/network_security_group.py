"""NetworkSecurityGroup component module."""

from __future__ import annotations

import dataclasses
from typing import Any

import pulumi
import pulumi_azure_native.network as azure_network


@dataclasses.dataclass
class SecurityRuleArgs:
    """Arguments for a single security rule within an NSG.

    All ``source_*`` and ``destination_*`` fields are optional individually, but
    the Azure API requires at least one address-prefix form and one port-range
    form to be supplied when the rule is deployed.

    Attributes:
        name:                         Azure resource name for the rule (used as
                                      ``security_rule_name`` within the NSG).
                                      Must be unique within the NSG.
        priority:                     Rule priority — 100 to 4096 (lower means
                                      higher priority).  Must be unique within
                                      the NSG.
        direction:                    ``"Inbound"`` or ``"Outbound"``.
        access:                       ``"Allow"`` or ``"Deny"``.
        protocol:                     ``"Tcp"``, ``"Udp"``, ``"Icmp"``,
                                      ``"Esp"``, ``"Ah"``, or ``"*"``.
        source_port_range:            Single source port / range, e.g. ``"*"``
                                      or ``"1024-65535"``.
        source_port_ranges:           List of source port ranges.  Use instead
                                      of ``source_port_range`` when multiple
                                      ranges are needed.
        source_address_prefix:        Source CIDR, IP, or service tag, e.g.
                                      ``"*"``, ``"10.0.0.0/8"``, or
                                      ``"VirtualNetwork"``.
        source_address_prefixes:      List of source CIDRs / service tags.
        destination_port_range:       Single destination port or range.
        destination_port_ranges:      List of destination port ranges.
        destination_address_prefix:   Destination CIDR, IP, or service tag.
        destination_address_prefixes: List of destination CIDRs / service tags.
        description:                  Optional free-text description (≤ 140
                                      chars).
    """

    name: pulumi.Input[str]
    priority: pulumi.Input[int]
    direction: pulumi.Input[str]
    access: pulumi.Input[str]
    protocol: pulumi.Input[str]
    source_port_range: pulumi.Input[str] | None = None
    source_port_ranges: list[str] | None = None
    source_address_prefix: pulumi.Input[str] | None = None
    source_address_prefixes: list[str] | None = None
    destination_port_range: pulumi.Input[str] | None = None
    destination_port_ranges: list[str] | None = None
    destination_address_prefix: pulumi.Input[str] | None = None
    destination_address_prefixes: list[str] | None = None
    description: pulumi.Input[str] | None = None


class NetworkSecurityGroup(pulumi.ComponentResource):
    """Creates an Azure Network Security Group with optional security rules.

    Each entry in ``security_rules`` is deployed as a standalone
    ``azure_network.SecurityRule`` child resource (not as an inline rule on the
    NSG resource itself).  This avoids the provider conflict that arises when
    both inline and standalone rules are mixed on the same NSG.

    Example::

        from pulumi_azure_modules.networking import (
            NetworkSecurityGroup,
            SecurityRuleArgs,
        )

        nsg = NetworkSecurityGroup(
            "web-nsg",
            resource_group_name="rg-platform",
            location="eastus",
            security_rules=[
                SecurityRuleArgs(
                    name="allow-https-inbound",
                    priority=100,
                    direction="Inbound",
                    access="Allow",
                    protocol="Tcp",
                    source_address_prefix="*",
                    source_port_range="*",
                    destination_address_prefix="*",
                    destination_port_range="443",
                ),
                SecurityRuleArgs(
                    name="deny-all-inbound",
                    priority=4096,
                    direction="Inbound",
                    access="Deny",
                    protocol="*",
                    source_address_prefix="*",
                    source_port_range="*",
                    destination_address_prefix="*",
                    destination_port_range="*",
                ),
            ],
            tags={"environment": "prod"},
        )

        # Associate the NSG with a subnet by its resource ID:
        # network_security_group=azure_network.SubResourceArgs(id=nsg.id)
    """

    id: pulumi.Output[str]
    """The fully-qualified Azure resource ID of the NSG.

    Format:
    ``/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/networkSecurityGroups/{name}``
    """

    name: pulumi.Output[str]
    """The Azure resource name of the NSG."""

    resource_group_name: pulumi.Output[str]
    """The resource group the NSG was deployed into."""

    rule_ids: pulumi.Output[list[Any]]
    """Resource IDs of all standalone security rules created for this NSG.

    Preserves the same order as ``security_rules``.  Empty list when no
    ``security_rules`` were supplied.  Useful for expressing ``depends_on``
    relationships in downstream resources that require rules to exist before
    traffic is permitted.
    """

    def __init__(
        self,
        resource_name: str,
        resource_group_name: pulumi.Input[str],
        location: pulumi.Input[str],
        nsg_name: pulumi.Input[str] | None = None,
        security_rules: list[SecurityRuleArgs] | None = None,
        tags: pulumi.Input[dict[str, str]] | None = None,
        opts: pulumi.ResourceOptions | None = None,
    ) -> None:
        """Create an NSG and its security rules.

        Args:
            resource_name:       Pulumi logical name (used as the state key and
                                 name prefix for child resources).
            resource_group_name: Resource group to deploy the NSG into.
            location:            Azure region (e.g. ``"eastus"``).
            nsg_name:            Explicit Azure resource name for the NSG.
                                 Auto-generated by the provider when ``None``.
            security_rules:      Zero or more :class:`SecurityRuleArgs` entries.
                                 Each entry creates one standalone
                                 ``SecurityRule`` child resource.
            tags:                Azure resource tags applied to the NSG.
            opts:                Pulumi resource options.
        """
        super().__init__(
            "pulumi-azure-modules:networking:NetworkSecurityGroup",
            resource_name,
            {},
            opts,
        )

        nsg = azure_network.NetworkSecurityGroup(
            f"{resource_name}-nsg",
            resource_group_name=resource_group_name,
            location=location,
            network_security_group_name=nsg_name,
            tags=tags,
            opts=pulumi.ResourceOptions(parent=self),
        )

        created_rules: list[azure_network.SecurityRule] = []
        for i, rule in enumerate(security_rules or []):
            sr = azure_network.SecurityRule(
                f"{resource_name}-rule-{i}",
                resource_group_name=resource_group_name,
                network_security_group_name=nsg.name,
                security_rule_name=rule.name,
                priority=rule.priority,
                direction=rule.direction,
                access=rule.access,
                protocol=rule.protocol,
                source_port_range=rule.source_port_range,
                source_port_ranges=rule.source_port_ranges,
                source_address_prefix=rule.source_address_prefix,
                source_address_prefixes=rule.source_address_prefixes,
                destination_port_range=rule.destination_port_range,
                destination_port_ranges=rule.destination_port_ranges,
                destination_address_prefix=rule.destination_address_prefix,
                destination_address_prefixes=rule.destination_address_prefixes,
                description=rule.description,
                opts=pulumi.ResourceOptions(parent=self),
            )
            created_rules.append(sr)

        self.id = nsg.id
        self.name = nsg.name
        self.resource_group_name = pulumi.Output.from_input(resource_group_name)

        no_rules: list[Any] = []
        self.rule_ids = (
            pulumi.Output.all(*[r.id for r in created_rules])
            if created_rules
            else pulumi.Output.from_input(no_rules)
        )

        self.register_outputs(
            {
                "id": self.id,
                "name": self.name,
                "resource_group_name": self.resource_group_name,
                "rule_ids": self.rule_ids,
            }
        )
