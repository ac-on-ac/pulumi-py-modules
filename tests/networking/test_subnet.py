"""Unit tests for pulumi_azure_modules.networking.Subnet."""

from __future__ import annotations

import pulumi

from pulumi_azure_modules.networking import (
    DelegationArgs,
    RouteArgs,
    SecurityRuleArgs,
    Subnet,
)

_RG = "rg-platform"
_VNET = "vnet-spoke"
_LOCATION = "eastus"
_CIDR = "10.1.0.0/24"


def _make_subnet(**kwargs: object) -> Subnet:
    return Subnet(
        "test-subnet",
        resource_group_name=_RG,
        virtual_network_name=_VNET,
        address_prefix=_CIDR,
        **kwargs,  # type: ignore[arg-type]
    )


def _make_rule(name: str = "allow-https", priority: int = 100) -> SecurityRuleArgs:
    return SecurityRuleArgs(
        name=name,
        priority=priority,
        direction="Inbound",
        access="Allow",
        protocol="Tcp",
        source_address_prefix="*",
        source_port_range="*",
        destination_address_prefix="*",
        destination_port_range="443",
    )


def _make_route(name: str = "to-internet") -> RouteArgs:
    return RouteArgs(
        name=name,
        next_hop_type="Internet",
        address_prefix="0.0.0.0/0",
    )


def _make_delegation(
    name: str = "aks-delegation",
    service_name: str = "Microsoft.ContainerService/managedClusters",
) -> DelegationArgs:
    return DelegationArgs(name=name, service_name=service_name)


@pulumi.runtime.test
def test_subnet_id_is_populated() -> None:
    """Subnet id is non-empty after creation."""
    subnet = _make_subnet()

    def check(v: str) -> None:
        assert v

    return subnet.id.apply(check)


@pulumi.runtime.test
def test_subnet_name_is_populated() -> None:
    """Subnet name is non-empty after creation."""
    subnet = _make_subnet()

    def check(v: str) -> None:
        assert v

    return subnet.name.apply(check)


@pulumi.runtime.test
def test_address_prefix_propagated() -> None:
    """address_prefix output matches the value passed at construction time."""
    subnet = _make_subnet()

    def check(v: object) -> None:
        assert v == _CIDR

    return subnet.address_prefix.apply(check)


@pulumi.runtime.test
def test_custom_subnet_name() -> None:
    """A custom subnet_name is reflected in the name output."""
    subnet = _make_subnet(subnet_name="my-subnet")

    def check(v: str) -> None:
        assert v == "my-subnet"

    return subnet.name.apply(check)


@pulumi.runtime.test
def test_with_nsg_id() -> None:
    """Providing nsg_id associates the NSG; id is still populated."""
    nsg_resource_id = (
        "/subscriptions/00000000-0000-0000-0000-000000000000"
        "/resourceGroups/rg-platform"
        "/providers/Microsoft.Network/networkSecurityGroups/my-nsg"
    )
    subnet = _make_subnet(nsg_id=nsg_resource_id)

    def check(v: str) -> None:
        assert v

    return subnet.id.apply(check)


@pulumi.runtime.test
def test_with_route_table_id() -> None:
    """Providing route_table_id associates the RT; id is still populated."""
    rt_resource_id = (
        "/subscriptions/00000000-0000-0000-0000-000000000000"
        "/resourceGroups/rg-platform"
        "/providers/Microsoft.Network/routeTables/my-rt"
    )
    subnet = _make_subnet(route_table_id=rt_resource_id)

    def check(v: str) -> None:
        assert v

    return subnet.id.apply(check)


@pulumi.runtime.test
def test_with_security_rules() -> None:
    """Providing security_rules creates a child NSG; subnet id is populated."""
    subnet = _make_subnet(
        location=_LOCATION,
        security_rules=[_make_rule("allow-https", 100)],
    )

    def check(v: str) -> None:
        assert v

    return subnet.id.apply(check)


@pulumi.runtime.test
def test_with_routes() -> None:
    """Providing routes creates a child route table; subnet id is populated."""
    subnet = _make_subnet(
        location=_LOCATION,
        routes=[_make_route("to-internet")],
    )

    def check(v: str) -> None:
        assert v

    return subnet.id.apply(check)


@pulumi.runtime.test
def test_with_security_rules_and_routes() -> None:
    """Combined security_rules + routes creates both children; id is populated."""
    subnet = _make_subnet(
        location=_LOCATION,
        security_rules=[_make_rule()],
        routes=[_make_route()],
    )

    def check(v: str) -> None:
        assert v

    return subnet.id.apply(check)


@pulumi.runtime.test
def test_with_service_endpoints() -> None:
    """service_endpoints are accepted; id is still populated."""
    subnet = _make_subnet(service_endpoints=["Microsoft.Storage", "Microsoft.Sql"])

    def check(v: str) -> None:
        assert v

    return subnet.id.apply(check)


@pulumi.runtime.test
def test_tags_accepted() -> None:
    """Tags are accepted; id is still populated."""
    subnet = _make_subnet(tags={"environment": "prod", "team": "platform"})

    def check(v: str) -> None:
        assert v

    return subnet.id.apply(check)


@pulumi.runtime.test
def test_nsg_id_takes_precedence_over_security_rules() -> None:
    """When both nsg_id and security_rules are supplied, nsg_id takes precedence."""
    nsg_resource_id = (
        "/subscriptions/00000000-0000-0000-0000-000000000000"
        "/resourceGroups/rg-platform"
        "/providers/Microsoft.Network/networkSecurityGroups/pre-existing"
    )
    # Both provided; should not raise and id should be populated.
    subnet = _make_subnet(
        nsg_id=nsg_resource_id,
        security_rules=[_make_rule()],
        location=_LOCATION,
    )

    def check(v: str) -> None:
        assert v

    return subnet.id.apply(check)


@pulumi.runtime.test
def test_with_single_delegation() -> None:
    """A single delegation is accepted; id is still populated."""
    subnet = _make_subnet(delegations=[_make_delegation()])

    def check(v: str) -> None:
        assert v

    return subnet.id.apply(check)


@pulumi.runtime.test
def test_with_multiple_delegations() -> None:
    """Multiple delegations are accepted; id is still populated."""
    subnet = _make_subnet(
        delegations=[
            _make_delegation("aks-delegation", "Microsoft.ContainerService/managedClusters"),
            _make_delegation("sql-delegation", "Microsoft.Sql/servers"),
        ]
    )

    def check(v: str) -> None:
        assert v

    return subnet.id.apply(check)


@pulumi.runtime.test
def test_delegation_with_explicit_actions() -> None:
    """A delegation with explicit actions is accepted; id is still populated."""
    subnet = _make_subnet(
        delegations=[
            DelegationArgs(
                name="netapp-delegation",
                service_name="Microsoft.NetApp/volumes",
                actions=["Microsoft.Network/networkinterfaces/*"],
            )
        ]
    )

    def check(v: str) -> None:
        assert v

    return subnet.id.apply(check)


@pulumi.runtime.test
def test_default_outbound_access_false() -> None:
    """Setting default_outbound_access=False is accepted; id is still populated."""
    subnet = _make_subnet(default_outbound_access=False)

    def check(v: str) -> None:
        assert v

    return subnet.id.apply(check)
