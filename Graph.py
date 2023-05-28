import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, directed=True):
        self.adj_list = {}
        self.directed = directed

    def get_neighbors(self, node_label):
        if node_label in self.adj_list:
            return self.adj_list[node_label]
        else:
            return []

    def add_vertex(self, node_label):
        if node_label not in self.adj_list:
            self.adj_list[node_label] = []

    def add_edge(self, v1, v2):
        if v1 not in self.adj_list:
            self.add_vertex(v1)
        if v2 not in self.adj_list:
            self.add_vertex(v2)

        self.adj_list[v1].append(v2)
        if not self.directed:
            self.adj_list[v2].append(v1)

    def DFS(self, start, visited=None):
        if visited is None:
            visited = []

        if start not in self.adj_list:
            return "No existe el nodo inicial en el grafo."
        else:
            if start not in visited:
                visited.append(start)
                neighbors = self.get_neighbors(start)
                for n in neighbors:
                    self.DFS(n, visited)
        return visited
    

g = Graph()
g.add_vertex("A")
g.add_vertex("B")
g.add_vertex("C")
g.add_vertex("D")
g.add_vertex("E")
g.add_vertex("X")
g.add_vertex("R")


g.add_edge("A", "B")
g.add_edge("A", "E")
g.add_edge("B", "C")
g.add_edge("X", "R")
g.add_edge("B", "D")
g.add_edge("E", "X")
g.DFS("A")

G = nx.Graph()
for node in g.adj_list:
    G.add_node(node)
    for neighbor in g.get_neighbors(node):
        G.add_edge(node, neighbor)

nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray')
plt.show()