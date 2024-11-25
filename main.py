import matplotlib.pyplot as plt
import networkx as nx
import os

class Edge:
    def __init__(self, v, flow, C, rev):
        self.v = v
        self.flow = flow
        self.C = C
        self.rev = rev

class Graph:
    def __init__(self, V):
        self.adj = [[] for i in range(V)]
        self.V = V
        self.level = [0 for i in range(V)]
        self.pos = None  # Position for nodes

    def addEdge(self, u, v, C):
        a = Edge(v, 0, C, len(self.adj[v]))
        b = Edge(u, 0, 0, len(self.adj[u]))
        self.adj[u].append(a)
        self.adj[v].append(b)

    def draw_graph_with_level(self, iteration):
        # Create a directory to save BFS images if not exists
        if not os.path.exists("bfs"):
            os.makedirs("bfs")

        G = nx.DiGraph()
        level_edges = []

        for u in range(self.V):
            for e in self.adj[u]:
                if e.C > 0:
                    G.add_edge(u, e.v, capacity=e.C, flow=e.flow)
                    # Highlight level graph edges
                    if self.level[u] != -1 and self.level[e.v] == self.level[u] + 1 and e.flow < e.C:
                        level_edges.append((u, e.v))

        # Generate node positions once if not already done
        if self.pos is None:
            self.pos = nx.spring_layout(G, seed=42)  # Use a fixed seed for consistent layout

        edge_labels = {(u, v): f"{d['flow']}/{d['capacity']}" for u, v, d in G.edges(data=True)}
        node_colors = ['green' if n == 0 else 'red' if n == self.V - 1 else 'lightblue' for n in G.nodes]
        node_labels = {n: 's' if n == 0 else 't' if n == self.V - 1 else str(n) for n in G.nodes}

        plt.figure(figsize=(12, 8))
        # Draw the entire graph
        nx.draw(
            G,
            self.pos,
            with_labels=True,
            node_color=node_colors,
            node_size=500,
            font_size=10,
            font_weight='bold',
            arrows=True,
            labels=node_labels,
        )
        # Highlight level graph edges
        nx.draw_networkx_edges(
            G,
            self.pos,
            edgelist=level_edges,
            edge_color='blue',
            width=2.5,
        )
        nx.draw_networkx_edge_labels(G, self.pos, edge_labels=edge_labels, font_size=9)
        plt.title(f"Graph with Level Graph Highlighted (Iteration {iteration})")
        plt.savefig(f"bfs/bfs{iteration}.png")
        plt.close()  # Close the plot to avoid display in some environments

    def BFS(self, s, t):
        for i in range(self.V):
            self.level[i] = -1
        self.level[s] = 0
        q = [s]
        iteration = 1  # Track BFS iteration
        while q:
            u = q.pop(0)
            for e in self.adj[u]:
                if self.level[e.v] < 0 and e.flow < e.C:
                    self.level[e.v] = self.level[u] + 1
                    q.append(e.v)

            # Visualize the entire graph and highlight the level graph at this iteration
            self.draw_graph_with_level(iteration)
            iteration += 1

        return False if self.level[t] < 0 else True

    def DFS(self, u, flow, t, start):
        if u == t:
            return flow
        while start[u] < len(self.adj[u]):
            e = self.adj[u][start[u]]
            if self.level[e.v] == self.level[u] + 1 and e.flow < e.C:
                curr_flow = min(flow, e.C - e.flow)
                temp_flow = self.DFS(e.v, curr_flow, t, start)
                if temp_flow > 0:
                    e.flow += temp_flow
                    self.adj[e.v][e.rev].flow -= temp_flow
                    return temp_flow
            start[u] += 1
        return 0

    def DinicMaxflow(self, s, t):
        if s == t:
            return -1
        total = 0
        while self.BFS(s, t):
            start = [0] * (self.V + 1)
            while True:
                flow = self.DFS(s, float('inf'), t, start)
                if flow == 0:
                    break
                total += flow
        return total

# Example usage
g = Graph(6)
g.addEdge(0, 1, 16)
g.addEdge(0, 2, 13)
g.addEdge(1, 2, 10)
g.addEdge(1, 3, 12)
g.addEdge(2, 1, 4)
g.addEdge(2, 4, 14)
g.addEdge(3, 2, 9)
g.addEdge(3, 5, 20)
g.addEdge(4, 3, 7)
g.addEdge(4, 5, 10)

print("Maximum flow:", g.DinicMaxflow(0, 5))
