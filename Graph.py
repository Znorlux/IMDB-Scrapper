from Scrapper import Movie
import json
import networkx as nx
import os
class Graph:
    def __init__(self, directed=True):
        self.adj_list = {}
        self.directed = directed

    def get_neighbors(self, node_label):
        if node_label in self.adj_list:
            return self.adj_list[node_label]
        else:
            return []

    def add_vertex(self, node_label, node_type=None):
        if node_label not in self.adj_list:
            self.adj_list[node_label] = {'type': node_type, 'neighbors': []}

    def add_edge(self, v1, v2):
        if v1 not in self.adj_list:
            self.add_vertex(v1)
        if v2 not in self.adj_list:
            self.add_vertex(v2)

        self.adj_list[v1]['neighbors'].append(v2)
        if not self.directed:
            self.adj_list[v2]['neighbors'].append(v1)

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

    def find_most_frequent_actor(self):
        actor_counts = {}
        for node, attr in self.adj_list.items():
            if attr['type'] == 'actor':
                movies = set()  # Conjunto para almacenar las películas únicas en las que actúa el actor
                for neighbor in attr['neighbors']:
                    neighbor_attr = self.adj_list[neighbor]
                    if neighbor_attr['type'] == 'movie':
                        movies.add(neighbor)
                movie_count = len(movies)
                actor_counts[node] = movie_count

        if not actor_counts:
            return None, 0

        most_frequent_actor = max(actor_counts, key=actor_counts.get)
        max_movie_count = actor_counts[most_frequent_actor]

        return most_frequent_actor, max_movie_count
    
    def find_most_frequent_director(self):
        director_counts = {}
        for node, attr in self.adj_list.items():
            if attr['type'] == 'director':
                movies = set()  # Conjunto para almacenar las películas únicas que dirigió el director
                for neighbor in attr['neighbors']:
                    neighbor_attr = self.adj_list[neighbor]
                    if neighbor_attr['type'] == 'movie':
                        movies.add(neighbor)
                movie_count = len(movies)
                director_counts[node] = movie_count

        if not director_counts:
            return None, 0

        most_frequent_actor = max(director_counts, key=director_counts.get)
        max_movie_count = director_counts[most_frequent_actor]

        return most_frequent_actor, max_movie_count
    

with open("movies.json", "r") as json_file:
    data = json.load(json_file)

# Crear una lista de películas con los datos del archivo JSON
movie_list = []
for movie_data in data:
    title = movie_data["title"]
    link = movie_data["link"]
    actors = movie_data["actors"]
    director = movie_data["director"]
    writers = movie_data["writers"]
    movie = Movie(title, link)
    movie.actors = actors
    movie.director = director
    movie.writers = writers
    movie_list.append(movie)

# Crear el grafo y agregar nodos y aristas
g = Graph()

for movie in movie_list:
    g.add_vertex(movie.title, node_type='movie')
    for actor in movie.actors:
        g.add_vertex(actor, node_type='actor')
        g.add_edge(movie.title, actor)
        g.add_edge(actor, movie.title)
    if movie.director:
        g.add_vertex(movie.director, node_type='director')
        g.add_edge(movie.title, movie.director)
        g.add_edge(movie.director, movie.title)
    for writer in movie.writers:
        g.add_vertex(writer, node_type='writer')
        g.add_edge(movie.title, writer)
        g.add_edge(writer, movie.title)

most_frequent_actor, movie_count = g.find_most_frequent_actor()
print("El actor que ha actuado en más películas es:", most_frequent_actor)
print("Número de películas en las que actuó:", movie_count)

print()

most_frequent_director, director_movies = g.find_most_frequent_director()
print("El director que ha dirigido en más películas es:", most_frequent_director)
print("El director que ha dirigido en más películas es:", director_movies)

print(g.get_neighbors("Charles Chaplin"))

'''
# Crear el grafo de Networkx
G = nx.Graph()
for node, attr in g.adj_list.items():
    G.add_node(node, **attr)
    for neighbor in attr['neighbors']:
        G.add_edge(node, neighbor)

# Convertir los atributos a cadenas de texto
for node in G.nodes:
    attr = G.nodes[node]
    for key, value in attr.items():
        if isinstance(value, (list, type)):
            attr[key] = str(value)

if os.path.exists("graph.graphml"):
    os.remove("graph.graphml")

# Guardar el grafo en formato GraphML
nx.write_graphml(G, "graph.graphml")
'''
