"""Unit tests for pulumi_azure_modules.networking.RouteTable."""

from __future__ import annotations

import pulumi

from pulumi_azure_modules.networking import RouteArgs, RouteTable

_RG = "rg-platform"
_LOCATION = "eastus"


def _make_rt(**kwargs: object) -> RouteTable:
    return RouteTable(
        "test-rt",
        resource_group_name=_RG,
        location=_LOCATION,
        **kwargs,  # type: ignore[arg-type]
    )


def _make_route(name: str = "route-1", next_hop_type: str = "Internet") -> RouteArgs:
    return RouteArgs(
        name=name,
        next_hop_type=next_hop_type,
        address_prefix="0.0.0.0/0",
    )


@pulumi.runtime.test
def test_route_table_id_is_populated() -> None:
    """Route table id is non-empty after creation."""
    rt = _make_rt()

    def check(v: str) -> None:
        assert v

    return rt.id.apply(check)


@pulumi.runtime.test
def test_route_table_name_is_populated() -> None:
    """Route table name is non-empty after creation."""
    rt = _make_rt()

    def check(v: str) -> None:
        assert v

    return rt.name.apply(check)


@pulumi.runtime.test
def test_route_ids_empty_when_no_routes() -> None:
    """route_ids is an empty list when no routes are provided."""
    rt = _make_rt()

    def check(ids: list) -> None:
        assert ids == []

    return rt.route_ids.apply(check)


@pulumi.runtime.test
def test_route_ids_populated_with_single_route() -> None:
    """route_ids has one non-empty entry when one route is provided."""
    rt = _make_rt(routes=[_make_route("to-internet")])

    def check(ids: list) -> None:
        assert len(ids) == 1
        assert ids[0]

    return rt.route_ids.apply(check)


@pulumi.runtime.test
def test_route_ids_count_matches_routes() -> None:
    """Number of route_ids matches the number of routes supplied."""
    routes = [
        RouteArgs(
            name=f"route-{i}",
            next_hop_type="Internet",
            address_prefix=f"10.{i}.0.0/16",
        )
        for i in range(3)
    ]
    rt = _make_rt(routes=routes)

    def check(ids: list) -> None:
        assert len(ids) == 3

    return rt.route_ids.apply(check)


@pulumi.runtime.test
def test_accepts_custom_route_table_name() -> None:
    """A custom route_table_name is accepted and the id is still populated."""
    rt = _make_rt(route_table_name="my-custom-rt")

    def check(v: str) -> None:
        assert v

    return rt.id.apply(check)


@pulumi.runtime.test
def test_accepts_tags() -> None:
    """Tags are accepted without error."""
    rt = _make_rt(tags={"environment": "test", "team": "platform"})
    assert rt is not None


@pulumi.runtime.test
def test_accepts_virtual_appliance_route() -> None:
    """A VirtualAppliance route with next_hop_ip_address is accepted."""
    route = RouteArgs(
        name="to-nva",
        next_hop_type="VirtualAppliance",
        address_prefix="10.0.0.0/8",
        next_hop_ip_address="10.1.0.4",
    )
    rt = _make_rt(routes=[route])

    def check(ids: list) -> None:
        assert len(ids) == 1

    return rt.route_ids.apply(check)


@pulumi.runtime.test
def test_accepts_disable_bgp_route_propagation() -> None:
    """disable_bgp_route_propagation=True is accepted without error."""
    rt = _make_rt(disable_bgp_route_propagation=True)
    assert rt is not None
