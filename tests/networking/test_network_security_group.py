"""Unit tests for pulumi_azure_modules.networking.NetworkSecurityGroup."""

from __future__ import annotations

import pulumi

from pulumi_azure_modules.networking import NetworkSecurityGroup, SecurityRuleArgs

_RG = "rg-platform"
_LOCATION = "eastus"


def _make_nsg(**kwargs: object) -> NetworkSecurityGroup:
    return NetworkSecurityGroup(
        "test-nsg",
        resource_group_name=_RG,
        location=_LOCATION,
        **kwargs,  # type: ignore[arg-type]
    )


def _make_rule(name: str = "rule-1", priority: int = 100) -> SecurityRuleArgs:
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


@pulumi.runtime.test
def test_nsg_id_is_populated() -> None:
    """NSG id is non-empty after creation."""
    nsg = _make_nsg()

    def check(v: str) -> None:
        assert v

    return nsg.id.apply(check)


@pulumi.runtime.test
def test_nsg_name_is_populated() -> None:
    """NSG name is non-empty after creation."""
    nsg = _make_nsg()

    def check(v: str) -> None:
        assert v

    return nsg.name.apply(check)


@pulumi.runtime.test
def test_rule_ids_empty_when_no_rules() -> None:
    """rule_ids is an empty list when no security_rules are provided."""
    nsg = _make_nsg()

    def check(ids: list) -> None:
        assert ids == []

    return nsg.rule_ids.apply(check)


@pulumi.runtime.test
def test_rule_ids_populated_with_single_rule() -> None:
    """rule_ids has one non-empty entry when one rule is provided."""
    nsg = _make_nsg(security_rules=[_make_rule("allow-https", 100)])

    def check(ids: list) -> None:
        assert len(ids) == 1
        assert ids[0]

    return nsg.rule_ids.apply(check)


@pulumi.runtime.test
def test_rule_ids_count_matches_rules() -> None:
    """Number of rule_ids matches the number of security_rules supplied."""
    rules = [_make_rule(f"rule-{i}", 100 + i * 10) for i in range(3)]
    nsg = _make_nsg(security_rules=rules)

    def check(ids: list) -> None:
        assert len(ids) == 3

    return nsg.rule_ids.apply(check)


@pulumi.runtime.test
def test_accepts_custom_nsg_name() -> None:
    """A custom nsg_name is accepted and the NSG id is still populated."""
    nsg = _make_nsg(nsg_name="my-custom-nsg")

    def check(v: str) -> None:
        assert v

    return nsg.id.apply(check)


@pulumi.runtime.test
def test_accepts_tags() -> None:
    """Tags are accepted without error."""
    nsg = _make_nsg(tags={"environment": "test", "team": "platform"})
    assert nsg is not None


@pulumi.runtime.test
def test_accepts_multi_prefix_rule() -> None:
    """A rule with address_prefixes and port_ranges lists is accepted."""
    rule = SecurityRuleArgs(
        name="allow-multi",
        priority=200,
        direction="Inbound",
        access="Allow",
        protocol="Tcp",
        source_address_prefixes=["10.0.0.0/8", "192.168.0.0/16"],
        source_port_range="*",
        destination_address_prefix="*",
        destination_port_ranges=["80", "443", "8080"],
    )
    nsg = _make_nsg(security_rules=[rule])

    def check(ids: list) -> None:
        assert len(ids) == 1

    return nsg.rule_ids.apply(check)
