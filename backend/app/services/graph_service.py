"""
Dependency Graph reasoning.

Builds a directed graph from the mock dependency data using networkx and
exposes:
  - blocker chain detection ("what is blocking what, transitively")
  - downstream impact radius ("if X goes down, what breaks")
  - a simple critical-path / risk-propagation score

This is intentionally graph-native rather than keyword search: every answer
is derived by walking edges, not by matching text.
"""
import networkx as nx

from app.services.data_loader import store


def build_graph() -> nx.DiGraph:
    g = nx.DiGraph()
    data = store.dependency_graph
    for node in data["nodes"]:
        g.add_node(node["id"], **node)
    for edge in data["edges"]:
        g.add_edge(edge["source"], edge["target"], relation=edge["relation"])
    return g


def get_graph_payload():
    return store.dependency_graph


def find_blocker_chains():
    """Return chains of nodes connected by 'blocks' edges, ordered upstream -> downstream."""
    g = build_graph()
    blocks_edges = [(u, v) for u, v, d in g.edges(data=True) if d.get("relation") == "blocks"]
    bg = nx.DiGraph()
    bg.add_edges_from(blocks_edges)

    chains = []
    roots = [n for n in bg.nodes if bg.in_degree(n) == 0]
    for root in roots:
        for target in bg.nodes:
            if root == target:
                continue
            if nx.has_path(bg, root, target):
                pass
    # Build full simple paths from each root to each leaf
    leaves = [n for n in bg.nodes if bg.out_degree(n) == 0]
    for root in roots:
        for leaf in leaves:
            if root == leaf:
                continue
            if nx.has_path(bg, root, leaf):
                for path in nx.all_simple_paths(bg, root, leaf):
                    if len(path) > 1:
                        chains.append(path)
    # de-duplicate, keep longest chains
    chains = sorted({tuple(c) for c in chains}, key=len, reverse=True)
    node_lookup = {n["id"]: n for n in store.dependency_graph["nodes"]}
    return [
        {
            "chain": list(chain),
            "labels": [node_lookup.get(n, {}).get("label", n) for n in chain],
        }
        for chain in chains
    ]


def downstream_impact(node_id: str):
    """All nodes reachable from node_id via any edge type (what breaks if this breaks)."""
    g = build_graph()
    if node_id not in g:
        return []
    reachable = nx.descendants(g, node_id)
    node_lookup = {n["id"]: n for n in store.dependency_graph["nodes"]}
    return [node_lookup[n] for n in reachable if n in node_lookup]


def upstream_dependencies(node_id: str):
    """All nodes that node_id depends on, transitively."""
    g = build_graph()
    if node_id not in g:
        return []
    ancestors = nx.ancestors(g, node_id)
    node_lookup = {n["id"]: n for n in store.dependency_graph["nodes"]}
    return [node_lookup[n] for n in ancestors if n in node_lookup]


def risk_score_for_node(node_id: str) -> int:
    """
    Very simple heuristic risk score:
    base severity from node status + weighted by number of downstream dependents.
    """
    status_weight = {"blocked": 40, "delayed": 30, "at_risk": 25, "on_track": 5}
    node_lookup = {n["id"]: n for n in store.dependency_graph["nodes"]}
    node = node_lookup.get(node_id, {})
    base = status_weight.get(node.get("status", "on_track"), 5)
    downstream_count = len(downstream_impact(node_id))
    score = min(99, base + downstream_count * 8)
    return score


def critical_path():
    """
    Returns the single highest-risk blocker chain, used to power the
    'Dependency Risk Overview' panel and the scripted demo scenario.
    """
    chains = find_blocker_chains()
    if not chains:
        return None
    scored = [
        {**c, "risk_score": max(risk_score_for_node(n) for n in c["chain"])}
        for c in chains
    ]
    scored.sort(key=lambda c: (-len(c["chain"]), -c["risk_score"]))
    return scored[0]
