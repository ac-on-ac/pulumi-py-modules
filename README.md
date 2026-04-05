# pulumi-azure-modules

> **Reusable Pulumi Python modules for deploying Azure resources** — the Python
> equivalent of a Terraform module repository.

[![CI](https://github.com/ac-on-ac/pulumi-py-modules/actions/workflows/ci.yml/badge.svg)](https://github.com/ac-on-ac/pulumi-py-modules/actions/workflows/ci.yml)

---

## Overview

This repository publishes the `pulumi-azure-modules` Python package.  Each
sub-package wraps low-level [`pulumi-azure-native`](https://www.pulumi.com/registry/packages/azure-native/)
resources into opinionated, composable **component functions** that:

- Apply sensible security defaults (HTTPS-only, TLS 1.2+, soft-delete, etc.).
- Accept a minimal set of required arguments plus optional keyword arguments for
  overrides — convention over configuration.
- Return a `pulumi.ComponentResource` so callers can consume typed outputs and
  the Pulumi state tree stays readable.

Think of each function as you would a Terraform module: `source` → pip install,
`inputs` → function arguments, `outputs` → component outputs.

---

## Repository structure

```
pulumi-py-modules/
├── src/
│   └── pulumi_azure_modules/   # Installable Python package
│       ├── compute/            # VMs, VMSS
│       ├── networking/         # VNets, Subnets, NSGs, Private Endpoints
│       ├── storage/            # Storage Accounts, Blob Containers
│       ├── databases/          # SQL, CosmosDB, PostgreSQL
│       ├── identity/           # Managed Identities, Role Assignments
│       ├── keyvault/           # Key Vault, Secrets, Keys, Certs
│       ├── monitoring/         # Log Analytics, App Insights, Alerts
│       └── containers/         # AKS, ACR, Container Apps
├── tests/                      # Pytest unit tests (mock engine, no live Azure)
├── .github/workflows/
│   ├── ci.yml                  # Lint + test on every PR / push to main
│   └── publish.yml             # Build + publish to PyPI on version tag
└── pyproject.toml              # Package metadata, deps, tool config
```

---

## Installation

### From PyPI _(once published)_

```bash
pip install pulumi-azure-modules
```

### From GitHub _(for development or before first release)_

```bash
pip install git+https://github.com/ac-on-ac/pulumi-py-modules.git
```

### Pinning a specific version / commit

```bash
pip install git+https://github.com/ac-on-ac/pulumi-py-modules.git@v0.1.0
```

---

## Usage

In a Pulumi program:

```python
import pulumi
from pulumi_azure_modules.networking import virtual_network
from pulumi_azure_modules.storage import storage_account

vnet = virtual_network(
    name="my-vnet",
    resource_group_name="my-rg",
    address_spaces=["10.0.0.0/16"],
)

sa = storage_account(
    name="mystorageaccount",
    resource_group_name="my-rg",
)

pulumi.export("vnet_id", vnet.id)
pulumi.export("storage_endpoint", sa.primary_blob_endpoint)
```

---

## Development

### Prerequisites

- Python ≥ 3.9
- [Pulumi CLI](https://www.pulumi.com/docs/install/)

### Set up a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -e ".[dev]"
```

### Run tests

Tests use Pulumi's built-in mock engine — no Azure credentials required.

```bash
pytest
```

### Lint & format

```bash
ruff check src/ tests/
ruff format src/ tests/
mypy src/
```

---

## Releasing a new version

1. Update `version` in `pyproject.toml` and in `src/pulumi_azure_modules/__init__.py`.
2. Commit and push.
3. Create and push a tag matching `v*.*.*` (e.g. `git tag v0.2.0 && git push --tags`).
4. The `publish.yml` workflow will build and publish to PyPI automatically via
   [trusted publishing (OIDC)](https://docs.pypi.org/trusted-publishers/) — no
   API token needed.

---

## Contributing

Pull requests are welcome.  Please open an issue first to discuss significant
changes.  All new functions must include:

- Type annotations on every parameter and return value.
- A Google-style docstring.
- At least one unit test using the mock engine in `tests/`.

---

## License

[MIT](LICENSE)
Pulumi modules for Azure Infrastructure - Python
