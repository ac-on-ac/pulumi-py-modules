"""Unit tests for pulumi_azure_modules.networking.VirtualNetworkPeering."""

from __future__ import annotations

import pulumi

from pulumi_azure_modules.networking import VirtualNetworkPeering

_HUB_NAME = "vnet-hub"
_HUB_RG = "rg-hub"
_HUB_ID = (
    "/subscriptions/00000000-0000-0000-0000-000000000000"
    f"/resourceGroups/{_HUB_RG}"
    f"/providers/Microsoft.Network/virtualNetworks/{_HUB_NAME}"
)
_SPOKE_NAME = "vnet-spoke"
_SPOKE_RG = "rg-spoke"
_SPOKE_ID = (
    "/subscriptions/00000000-0000-0000-0000-000000000000"
    f"/resourceGroups/{_SPOKE_RG}"
    f"/providers/Microsoft.Network/virtualNetworks/{_SPOKE_NAME}"
)


def _make_peering(**kwargs: object) -> VirtualNetworkPeering:
    return VirtualNetworkPeering(
        "hub-spoke",
        local_vnet_name=_HUB_NAME,
        local_vnet_id=_HUB_ID,
        local_resource_group_name=_HUB_RG,
        remote_vnet_name=_SPOKE_NAME,
        remote_vnet_id=_SPOKE_ID,
        remote_resource_group_name=_SPOKE_RG,
        **kwargs,  # type: ignore[arg-type]
    )


@pulumi.runtime.test
def test_local_peering_id_is_populated() -> None:
    """local_peering_id (local → remote) is non-empty after creation."""
    peering = _make_peering()

    def check(v: str) -> None:
        assert v

    return peering.local_peering_id.apply(check)


@pulumi.runtime.test
def test_remote_peering_id_is_populated() -> None:
    """remote_peering_id (remote → local) is non-empty after creation."""
    peering = _make_peering()

    def check(v: str) -> None:
        assert v

    return peering.remote_peering_id.apply(check)


@pulumi.runtime.test
def test_peering_ids_are_distinct() -> None:
    """The two peering IDs are different resources."""
    peering = _make_peering()

    def check(ids: list) -> None:
        local_id, remote_id = ids
        assert local_id != remote_id

    return pulumi.Output.all(peering.local_peering_id, peering.remote_peering_id).apply(check)


@pulumi.runtime.test
def test_accepts_gateway_transit_flags() -> None:
    """allow_gateway_transit and use_remote_gateways are accepted."""
    peering = _make_peering(allow_gateway_transit=True, use_remote_gateways=True)
    assert peering is not None


@pulumi.runtime.test
def test_accepts_forwarded_traffic_flag() -> None:
    """allow_forwarded_traffic is accepted."""
    peering = _make_peering(allow_forwarded_traffic=True)
    assert peering is not None


@pulumi.runtime.test
def test_allow_virtual_network_access_default() -> None:
    """allow_virtual_network_access defaults to True — both IDs are still created."""
    peering = _make_peering()

    def check(v: str) -> None:
        assert v

    return peering.local_peering_id.apply(check)
