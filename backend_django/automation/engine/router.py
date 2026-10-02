# automation/engine/router.py

def get_next_node(current_node, result):

    condition = "success" if result else "failed"

    edge = current_node.out_edges.filter(condition=condition).first()

    if not edge:
        return None

    return edge.target_node