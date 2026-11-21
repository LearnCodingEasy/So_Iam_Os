"""Validate workflow graphs before any executor is allowed to run them."""
class WorkflowService:
    MAX_NODES = 100
    @classmethod
    def validate(cls, graph):
        if not isinstance(graph, dict):
            return {"valid": False, "errors": ["Workflow must be an object."]}
        nodes, edges = graph.get("nodes", []), graph.get("edges", [])
        errors = []
        if not isinstance(nodes, list) or not isinstance(edges, list):
            return {"valid": False, "errors": ["nodes and edges must be lists."]}
        if len(nodes) > cls.MAX_NODES:
            errors.append(f"Workflow exceeds {cls.MAX_NODES} nodes.")
        ids = [n.get("id") for n in nodes if isinstance(n, dict)]
        if len(ids) != len(nodes) or any(not x for x in ids):
            errors.append("Every node must be an object with an id.")
        if len(set(ids)) != len(ids):
            errors.append("Node ids must be unique.")
        known = set(ids)
        adjacency = {node_id: [] for node_id in known}
        for node in nodes:
            if not isinstance(node, dict):
                continue
            node_type = node.get("type") or node.get("data", {}).get("type")
            if node_type and not isinstance(node_type, str):
                errors.append("Node type must be a string.")
        for edge in edges:
            if not isinstance(edge, dict) or edge.get("source") not in known or edge.get("target") not in known:
                errors.append("Every edge must connect two existing nodes.")
                continue
            adjacency[edge["source"]].append(edge["target"])
        # A workflow is a DAG. Detect cycles with DFS coloring.
        visiting, visited = set(), set()
        def visit(node_id):
            if node_id in visiting:
                return True
            if node_id in visited:
                return False
            visiting.add(node_id)
            if any(visit(child) for child in adjacency.get(node_id, [])):
                return True
            visiting.remove(node_id)
            visited.add(node_id)
            return False
        if any(visit(node_id) for node_id in known):
            errors.append("Workflow graph contains a cycle.")
        return {"valid": not errors, "errors": errors, "node_count": len(nodes), "edge_count": len(edges)}
