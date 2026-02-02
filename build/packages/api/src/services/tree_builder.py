"""
Generic tree-building service for hierarchical data.

Used by processes and portfolio endpoints to build tree structures
from flat database results.
"""

from typing import Any, Callable, Optional, Protocol, TypeVar


class HasTreeFields(Protocol):
    """Protocol for items that can be built into a tree."""
    id: str
    parent_id: Optional[str]
    sort_order: int


T = TypeVar("T", bound=HasTreeFields)
NodeT = TypeVar("NodeT")


def build_tree(
    items: list[T],
    node_factory: Callable[[T, list[NodeT]], NodeT],
    root_parent_id: Optional[str] = None,
) -> list[NodeT]:
    """
    Build a tree structure from a flat list of items.

    Args:
        items: List of items with id, parent_id, and sort_order attributes
        node_factory: Function that creates a tree node from an item and its children
        root_parent_id: Parent ID for root nodes (None for top-level)

    Returns:
        List of root nodes with nested children, sorted by sort_order
    """
    # Create a lookup for quick parent finding
    items_by_parent: dict[Optional[str], list[T]] = {}
    for item in items:
        parent_id = item.parent_id
        if parent_id not in items_by_parent:
            items_by_parent[parent_id] = []
        items_by_parent[parent_id].append(item)

    # Sort children by sort_order
    for children in items_by_parent.values():
        children.sort(key=lambda x: x.sort_order)

    def build_children(parent_id: Optional[str]) -> list[NodeT]:
        """Recursively build children for a given parent."""
        children = items_by_parent.get(parent_id, [])
        return [
            node_factory(item, build_children(item.id))
            for item in children
        ]

    return build_children(root_parent_id)


def build_tree_with_transform(
    items: list[T],
    transform: Callable[[T], dict[str, Any]],
    children_key: str = "children",
    root_parent_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    """
    Build a tree structure from a flat list, transforming items to dicts.

    Simpler alternative when you just need dict output.

    Args:
        items: List of items with id, parent_id, and sort_order attributes
        transform: Function that converts an item to a dict (excluding children)
        children_key: Key name for children in the output dict
        root_parent_id: Parent ID for root nodes (None for top-level)

    Returns:
        List of root dicts with nested children
    """
    def node_factory(item: T, children: list[dict]) -> dict[str, Any]:
        node = transform(item)
        node[children_key] = children
        return node

    return build_tree(items, node_factory, root_parent_id)
