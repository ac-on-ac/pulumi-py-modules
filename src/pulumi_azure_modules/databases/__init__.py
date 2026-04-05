"""Database modules – Azure SQL, CosmosDB, PostgreSQL Flexible Server, etc.

Planned functions
-----------------
- ``sql_server``                  – Deploy an Azure SQL Server + Database.
- ``cosmos_account``              – Deploy a Cosmos DB Account with configurable
                                    API and consistency policy.
- ``postgresql_flexible_server``  – Deploy a PostgreSQL Flexible Server.

All functions in this sub-package return a Pulumi ``ComponentResource`` so
that they appear as a logical unit in the Pulumi state tree and outputs are
easily consumed by callers.
"""

__all__: list[str] = []
