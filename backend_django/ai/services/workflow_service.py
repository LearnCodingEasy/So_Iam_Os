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
        for edge in edges:
            if not isinstance(edge, dict) or edge.get("source") not in known or edge.get("target") not in known:
                errors.append("Every edge must connect two existing nodes.")
                break
        return {"valid": not errors, "errors": errors, "node_count": len(nodes), "edge_count": len(edges)}
