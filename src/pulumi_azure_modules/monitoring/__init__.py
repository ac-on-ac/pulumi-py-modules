"""Monitoring modules – Log Analytics Workspaces, Application Insights, Alerts.

Planned functions
-----------------
- ``log_analytics_workspace``  – Deploy a Log Analytics Workspace.
- ``application_insights``     – Deploy an Application Insights instance linked
                                 to a Log Analytics Workspace.
- ``diagnostic_setting``       – Attach a Diagnostic Setting to any resource to
                                 forward logs/metrics to a Log Analytics Workspace.
- ``metric_alert``             – Create an Azure Monitor metric alert rule.

All functions in this sub-package return a Pulumi ``ComponentResource`` so
that they appear as a logical unit in the Pulumi state tree and outputs are
easily consumed by callers.
"""

__all__: list[str] = []
