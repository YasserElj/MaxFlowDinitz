import matplotlib.pyplot as plt
import networkx as nx
import os
from matplotlib.patches import Patch

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
        self.pos = None
        self.iteration = 1
        self.current_path = []

    def addEdge(self, u, v, C):
        a = Edge(v, 0, C, len(self.adj[v]))
        b = Edge(u, 0, 0, len(self.adj[u]))
        self.adj[u].append(a)
        self.adj[v].append(b)

    def draw_graph_with_path(self):
        if not os.path.exists("dfs_paths"):
            os.makedirs("dfs_paths")

        G = nx.DiGraph()
        path_edges = []
        saturated_edges = []
        available_edges = []

        # Create edges and classify them
        for u in range(self.V):
            for e in self.adj[u]:
                if e.C > 0:  # Only add forward edges
                    G.add_edge(u, e.v, capacity=e.C, flow=e.flow)
                    if e.flow == e.C:
                        saturated_edges.append((u, e.v))
                    else:
                        available_edges.append((u, e.v))

        # Get current path edges
        for i in range(len(self.current_path) - 1):
            path_edges.append((self.current_path[i], self.current_path[i + 1]))

        # Generate positions if not already generated
        if self.pos is None:
            self.pos = nx.spring_layout(G, seed=42)

        edge_labels = {(u, v): f"{d['flow']}/{d['capacity']}" for u, v, d in G.edges(data=True)}
        
        # Color nodes based on their level
        node_colors = []
        for n in G.nodes():
            if n == 0:  # source
                node_colors.append('lightgreen')
            elif n == self.V - 1:  # sink
                node_colors.append('lightcoral')
            elif self.level[n] == -1:
                node_colors.append('lightgray')  # unreachable nodes
            else:
                # Create a color gradient based on level
                intensity = max(0.2, 1 - (self.level[n] / (self.V * 0.8)))
                node_colors.append(f'#{int(intensity*255):02x}{int(intensity*255):02x}ff')

        plt.figure(figsize=(15, 10))
        
        # Draw the base graph with all available edges
        nx.draw_networkx_edges(G, self.pos, edgelist=available_edges, edge_color='gray', width=1.5)
        
        # Draw saturated edges
        nx.draw_networkx_edges(G, self.pos, edgelist=saturated_edges, edge_color='red', width=2)
        
        # Draw current path
        nx.draw_networkx_edges(G, self.pos, edgelist=path_edges, edge_color='blue', width=3)

        # Draw nodes and labels
        nx.draw_networkx_nodes(G, self.pos, node_color=node_colors, node_size=500)
        nx.draw_networkx_labels(G, self.pos, 
                              {n: f'{n}\n(L:{self.level[n]})' if self.level[n] != -1 else f'{n}\n(-)' 
                               for n in G.nodes()})
        nx.draw_networkx_edge_labels(G, self.pos, edge_labels=edge_labels, font_size=8)

        # Create legend
        legend_elements = [
            Patch(facecolor='lightgreen', label='Source'),
            Patch(facecolor='lightcoral', label='Sink'),
            Patch(facecolor='lightblue', label='Intermediate Node'),
            Patch(facecolor='lightgray', label='Unreachable Node'),
            Patch(facecolor='white', edgecolor='gray', label='Available Edge'),
            Patch(facecolor='red', label='Saturated Edge'),
            Patch(facecolor='blue', label='Current Path')
        ]
        
        # Add level information to title
        plt.title(f"Flow Network - Iteration {self.iteration}\nNode format: 'node_id\\n(L:level)' where L is the BFS level", 
                 pad=20)
        
        # Position legend outside the plot
        plt.legend(handles=legend_elements, 
                  loc='center left', 
                  bbox_to_anchor=(1, 0.5),
                  title='Legend')

        # Adjust layout to prevent legend overlap
        plt.tight_layout()
        plt.subplots_adjust(right=0.85)
        
        plt.savefig(f"dfs_paths/path{self.iteration}.png", bbox_inches='tight', dpi=300)
        plt.close()
        self.iteration += 1

    def BFS(self, s, t):
        for i in range(self.V):
            self.level[i] = -1
        self.level[s] = 0
        q = [s]
        while q:
            u = q.pop(0)
            for e in self.adj[u]:
                if self.level[e.v] < 0 and e.flow < e.C:
                    self.level[e.v] = self.level[u] + 1
                    q.append(e.v)
        return False if self.level[t] < 0 else True

    def DFS(self, u, flow, t, start):
        self.current_path.append(u)
        
        if u == t:
            self.draw_graph_with_path()
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
        
        self.current_path.pop()
        return 0

    def DinicMaxflow(self, s, t):
        if s == t:
            return -1
        total = 0
        while self.BFS(s, t):
            start = [0] * (self.V + 1)
            self.current_path = []
            while True:
                flow = self.DFS(s, float('inf'), t, start)
                if flow == 0:
                    break
                total += flow
                self.current_path = []
        return total

# Example usage with a complex graph
g = Graph(10)  # 10 nodes (0-9)

# Layer 1: Source connections
g.addEdge(0, 1, 20)
g.addEdge(0, 2, 15)
g.addEdge(0, 3, 18)

# Layer 2: Intermediate connections
g.addEdge(1, 4, 12)
g.addEdge(1, 5, 10)
g.addEdge(2, 4, 8)
g.addEdge(2, 5, 14)
g.addEdge(2, 6, 11)
g.addEdge(3, 5, 9)
g.addEdge(3, 6, 16)

# Cross connections
g.addEdge(4, 5, 7)
g.addEdge(5, 6, 8)
g.addEdge(4, 7, 13)
g.addEdge(5, 7, 15)
g.addEdge(5, 8, 12)
g.addEdge(6, 8, 10)

# Layer 3: Pre-sink connections
g.addEdge(7, 9, 25)
g.addEdge(8, 9, 20)

# Backward edges
g.addEdge(5, 4, 6)
g.addEdge(6, 5, 5)
g.addEdge(8, 7, 4)

print("Maximum flow:", g.DinicMaxflow(0, 9))