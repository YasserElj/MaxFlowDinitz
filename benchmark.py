# benchmark.py

import time
import dinic_original
import dinic_pruned
import random

def generate_large_graph(num_nodes, num_edges, s, t, seed=42):
    """
    Generates a large, complex directed graph for testing Dinic's algorithm.

    Parameters:
    - num_nodes (int): Total number of nodes in the graph.
    - num_edges (int): Total number of edges in the graph.
    - s (int): Source node.
    - t (int): Sink node.
    - seed (int): Random seed for reproducibility.

    Returns:
    - edges (list of tuples): Each tuple represents an edge in the format (u, v, capacity).
    """
    random.seed(seed)
    edges = []
    existing_edges = set()

    # Ensure that there's at least one path from s to t
    # Create a backbone path
    backbone = list(range(s, t + 1))
    for i in range(len(backbone) - 1):
        u = backbone[i]
        v = backbone[i + 1]
        capacity = random.randint(10, 100)
        edges.append((u, v, capacity))
        existing_edges.add((u, v))

    # Add additional edges to increase complexity
    while len(edges) < num_edges:
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u == v:
            continue  # No self-loops
        if (u, v) in existing_edges:
            continue  # Avoid duplicate edges
        capacity = random.randint(1, 100)
        edges.append((u, v, capacity))
        existing_edges.add((u, v))

    return edges

def benchmark():
    versions = {
        "Original": dinic_original,
        "Pruned": dinic_pruned,
    }

    # Define the graph parameters
    num_nodes = 10000     # Number of nodes (adjust as needed) 100000
    num_edges = 100000   # Number of edges (adjust as needed) 1000000
    s = 0                 # Source node
    t = num_nodes - 1     # Sink node

    # Generate the large, complex graph
    edges = generate_large_graph(num_nodes, num_edges, s, t)

    print(f"Generated a graph with {num_nodes} nodes and {num_edges} edges.\n")

    for name, module in versions.items():
        print(f"Running {name} version...")
        start_time = time.perf_counter()
        max_flow = module.run_dinic(num_nodes, edges, s, t, visualize=True)  # Disable visualization during timing
        end_time = time.perf_counter()
        algorithm_time = end_time - start_time

        # Now generate plots (not included in timing)
        module.run_dinic(num_nodes, edges, s, t, visualize=False)

        print(f"{name} version: Maximum flow = {max_flow}")
        print(f"{name} version took {algorithm_time:.6f} seconds (algorithm only)\n")

if __name__ == "__main__":
    benchmark()
