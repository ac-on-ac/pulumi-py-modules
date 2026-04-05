"""Identity modules – Managed Identities, Role Assignments, Entra App Regs.

Planned functions
-----------------
- ``user_assigned_identity``  – Deploy a User-Assigned Managed Identity.
- ``role_assignment``         – Assign an Azure RBAC role to a principal.
- ``federated_credential``    – Wire up a Federated Identity Credential for
                                workload identity (e.g. GitHub Actions → Azure).

All functions in this sub-package return a Pulumi ``ComponentResource`` so
that they appear as a logical unit in the Pulumi state tree and outputs are
easily consumed by callers.
"""

__all__: list[str] = []
