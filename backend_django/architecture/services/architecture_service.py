"""Architecture graph analysis."""
from collections import defaultdict

from architecture.models import Component, Dependency


def would_create_cycle(source, target, ignore_pk=None):
    """True if adding ``source -> target`` would close a cycle (or is a self-loop)."""
    if source.pk == target.pk:
        return True
    edges = Dependency.objects.filter(source__architecture=source.architecture)
    if ignore_pk is not None:
        edges = edges.exclude(pk=ignore_pk)
    graph = defaultdict(set)
    for s, t in edges.values_list("source_id", "target_id"):
        graph[s].add(t)
    seen, stack = set(), [target.pk]
    while stack:  # can target already reach source?
        node = stack.pop()
        if node == source.pk:
            return True
        if node in seen:
            continue
        seen.add(node)
        stack.extend(graph.get(node, ()))
    return False


def build_graph(architecture):
    components = list(Component.objects.filter(architecture=architecture))
    dependencies = list(Dependency.objects.filter(source__architecture=architecture))
    outgoing, incoming = defaultdict(int), defaultdict(int)
    for dep in dependencies:
        outgoing[dep.source_id] += 1
        incoming[dep.target_id] += 1
    nodes = [
        {"id": c.pk, "name": c.name, "type": c.component_type, "technology": c.technology,
         "depends_on_count": outgoing[c.pk], "dependents_count": incoming[c.pk]}
        for c in components
    ]
    edges = [{"id": d.pk, "source": d.source_id, "target": d.target_id, "type": d.dependency_type} for d in dependencies]
    most_depended = sorted(nodes, key=lambda n: (-n["dependents_count"], n["name"]))[:1]
    return {
        "architecture": architecture.pk,
        "nodes": nodes,
        "edges": edges,
        "metrics": {
            "components": len(nodes),
            "dependencies": len(edges),
            "isolated": [n["id"] for n in nodes if not n["depends_on_count"] and not n["dependents_count"]],
            "most_depended_on": most_depended[0]["id"] if most_depended and most_depended[0]["dependents_count"] else None,
        },
    }
