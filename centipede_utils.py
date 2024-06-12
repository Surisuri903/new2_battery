def set_centipede_payoff_structure(start_a, start_b, num_nodes, steps):
    nodes_a = [start_a]
    nodes_b = [start_b]
    for n in range(num_nodes - 1):
        new_node_a = nodes_a[n] + steps[0] if len(nodes_a) % 2 == 1 else nodes_a[n] + steps[1]
        new_node_b = nodes_b[n] + steps[1] if len(nodes_b) % 2 == 1 else nodes_b[n] + steps[0]
        nodes_a.append(new_node_a)
        nodes_b.append(new_node_b)
    return list(zip(nodes_a, nodes_b))

