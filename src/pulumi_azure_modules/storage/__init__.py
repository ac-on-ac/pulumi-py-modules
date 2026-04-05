"""Storage modules – Storage Accounts, Blob Containers, File Shares, etc.

Planned functions
-----------------
- ``storage_account``       – Deploy a Storage Account with secure defaults
                              (HTTPS-only, TLS 1.2 minimum, CMK optional).
- ``blob_container``        – Deploy a Blob Container with optional lifecycle
                              management policies.
- ``file_share``            – Deploy an Azure File Share.
- ``static_website``        – Enable static website hosting on a Storage Account.

All functions in this sub-package return a Pulumi ``ComponentResource`` so
that they appear as a logical unit in the Pulumi state tree and outputs are
easily consumed by callers.
"""

__all__: list[str] = []
