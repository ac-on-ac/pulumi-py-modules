"""Key Vault modules – Vaults, Secrets, Keys, and Certificates.

Planned functions
-----------------
- ``key_vault``         – Deploy a Key Vault with RBAC authorization, soft-delete,
                          and purge protection enabled by default.
- ``key_vault_secret``  – Store a secret in a Key Vault and return a reference.
- ``key_vault_key``     – Create a cryptographic key in a Key Vault.
- ``key_vault_cert``    – Import or generate a certificate in a Key Vault.

All functions in this sub-package return a Pulumi ``ComponentResource`` so
that they appear as a logical unit in the Pulumi state tree and outputs are
easily consumed by callers.
"""

__all__: list[str] = []
