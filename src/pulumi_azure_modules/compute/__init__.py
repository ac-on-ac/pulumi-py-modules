"""Compute modules – Virtual Machines, VM Scale Sets, and related resources.

Planned functions
-----------------
- ``linux_vm``         – Deploy a Linux Virtual Machine with sensible defaults.
- ``windows_vm``       – Deploy a Windows Virtual Machine with sensible defaults.
- ``vm_scale_set``     – Deploy a VM Scale Set with auto-scaling rules.

All functions in this sub-package return a Pulumi ``ComponentResource`` so
that they appear as a logical unit in the Pulumi state tree and outputs are
easily consumed by callers.
"""

__all__: list[str] = []
