import time
import dinic_original
import dinic_pruned
import dinic_delete_edges
import random

def benchmark():
    import dinic_original
    import dinic_pruned

    versions = {
        "Original": dinic_original,
        "Pruned": dinic_pruned,
    }

    # Define the graph data
    V = 10  # Number of nodes
    edges = [
        # Layer 1: Source connections
        (0, 1, 20),
        (0, 2, 15),
        (0, 3, 18),

        # Layer 2: Intermediate connections
        (1, 4, 12),
        (1, 5, 10),
        (2, 4, 8),
        (2, 5, 14),
        (2, 6, 11),
        (3, 5, 9),
        (3, 6, 16),

        # Cross connections
        (4, 5, 7),
        (5, 6, 8),
        (4, 7, 13),
        (5, 7, 15),
        (5, 8, 12),
        (6, 8, 10),

        # Layer 3: Pre-sink connections
        (7, 9, 25),
        (8, 9, 20),

        # Backward edges
        (5, 4, 6),
        (6, 5, 5),
        (8, 7, 4)
    ]

    s = 0  # Source
    t = 9  # Sink

    for name, module in versions.items():
        start_time = time.perf_counter()
        module.run_dinic(V, edges, s, t, visualize=True)
        end_time = time.perf_counter()
        print(f"{name} version took {end_time - start_time:.6f} seconds\n")

if __name__ == "__main__":
    benchmark()
