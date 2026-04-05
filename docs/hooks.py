"""MkDocs event hooks for pulumi-azure-modules documentation."""

from __future__ import annotations

from typing import Any


def on_page_context(context: dict[str, Any], *, page: Any, **kwargs: Any) -> dict[str, Any]:
    """Remove mkdocstrings member entries from the on-page table of contents.

    mkdocstrings registers every documented member (attributes, methods, etc.)
    as a separate TOC entry using the fully-qualified Python path as the anchor
    ID, e.g. ``pulumi_azure_modules.core.resource_group.ResourceGroup.name``.
    These entries clutter the right-side TOC sidebar.

    In the built TOC tree, the page H1 heading (e.g. ``core``) is the root
    item, and both the manual ``## Section`` headings and mkdocstrings member
    headings are its direct children.  Manual section IDs never contain dots;
    mkdocstrings member IDs always use the full Python dotted path.  This hook
    removes any child entry whose anchor ID contains a dot.
    """
    for item in page.toc.items:
        item.children = [c for c in item.children if "." not in c.id]
        for child in item.children:
            child.children = []
    return context
