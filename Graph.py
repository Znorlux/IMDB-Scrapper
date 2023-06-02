from OldScrapper import Movie
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
    
    def find_person_and_movie(self, name):
        result = []
        
        if name in self.adj_list:
            # Si el nombre es una película
            if self.adj_list[name]['type'] == 'movie':
                result.append("Película: " + name)
                
                # Obtener los actores, escritores y director de la película
                actors = []
                writers = []
                director = ""
                for neighbor in self.adj_list[name]['neighbors']:
                    neighbor_attr = self.adj_list[neighbor]
                    if neighbor_attr['type'] == 'actor':
                        actors.append(neighbor)
                    elif neighbor_attr['type'] == 'writer':
                        writers.append(neighbor)
                    elif neighbor_attr['type'] == 'director':
                        director = neighbor
                
                if actors:
                    result.append("Actores: " + ", ".join(actors))
                else:
                    result.append("No se encontraron actores para la película")
                
                if writers:
                    result.append("Escritores: " + ", ".join(writers))
                else:
                    result.append("No se encontraron escritores para la película")

                if director:
                    result.append("Director: " + director)
                else:
                    result.append("No se encontró director para la película")
            else:  # Si el nombre corresponde a un actor, escritor o director
                result.append("Persona: " + name)
                
                # Obtener las películas en las que la persona ha actuado, escrito o dirigido
                movies = []
                for neighbor in self.adj_list[name]['neighbors']:
                    neighbor_attr = self.adj_list[neighbor]
                    if neighbor_attr['type'] == 'movie':
                        movies.append(neighbor)
                if movies:
                    result.append("Películas: " + ", ".join(movies))
                else:
                    result.append("No se encontraron películas para la persona")
        else:
            result.append("No se encontró ninguna persona o película con ese nombre")

        return result

    def relation_V1_V2(self, v1, v2):
        # Verificar si los nodos v1 y v2 existen en el grafo
        if v1 not in self.adj_list or v2 not in self.adj_list:
            return "Al menos uno de los nodos no existe en el grafo"

        # Verificar si v2 es un vecino directo de v1
        if v2 in self.adj_list[v1]['neighbors']:
            return f"{v1} y {v2} están directamente relacionados en el grafo"

        # Buscar una ruta de relación indirecta
        visited = set()
        queue = [(v1, [])]  # Cola para realizar

        while queue:
            current_node, path = queue.pop(0)

            # Si se encuentra v2, se devuelve la ruta de relación indirecta
            if current_node == v2:
                return f"Se encontró una ruta de relación indirecta entre {v1} y {v2}: {' -> '.join(path + [current_node])}"

            visited.add(current_node)
            neighbors = self.get_neighbors(current_node)

            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [current_node]))

        # No se encontró ninguna relación entre v1 y v2
        return f"No se encontró una relación entre {v1} y {v2} en el grafo"

    def find_person_movies_and_relationships(self, person):
        result = ()
    
        if person in self.adj_list:
            result += ("Persona: " + person,)
    
            # Obtener las películas en las que la persona ha actuado, escrito o dirigido
            movies = set()
            for neighbor in self.adj_list[person]['neighbors']:
                if 'type' in self.adj_list[neighbor]:
                    neighbor_attr = self.adj_list[neighbor]
                    if neighbor_attr['type'] == 'movie':
                        movies.add(neighbor)
            if movies:
                result += ("Películas: " + ", ".join(movies),)
            else:
                result += ("No se encontraron películas para la persona",)
        else:
            result += ("No se encontró ninguna persona con ese nombre",)
    
        return result
    
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

def save_graph():
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

def user_menu():

    print("\nBienvenido al grafo de peliculas de IMDB!")
    print("Puedes realizar las siguientes acciones:")
    print('''
1. Guardar el grafo en archiv .GRAPHML.
2. Buscar a una persona o película por nombre.
3. Conocer el tipo de una persona, si existe en el grafo: actriz, director o escritor.
4. Conocer la relación directa o indirecta de dos nodos v1 y v2.
5. Conocer el actor que ha actuado en más películas.
6. Conocer el director que más películas ha dirigido.
7. Conocer si todas las películas en las que ha trabajado una persona y su relación con la misma.                                                    
8. Salir.
    ''')
    while True:
        option = input("\nIngresa tu opción: ")
        if option == "1":
            save_graph()
            print("El grafo se ha guardado correctamente! Puedes verlo en Cytoscape")

        elif option == "2":
            name = input("Ingresa el nombre de la pelicula, director, escritor o actor que quieres buscar: ")
            print(g.find_person_and_movie(name))

        elif option == "3":
            name = input("Ingresa el nombre de la persona: ")
            print(g.get_neighbors(name))

        elif option == "4":
            v1 = input("Ingresa el primer nodo (v1): ")
            v2 = input("Ingresa el segundo nodo (v2): ")
            print(g.relation_V1_V2(v1,v2))

        elif option == "5":
            most_frequent_actor, movie_count = g.find_most_frequent_actor()
            print("El actor que ha actuado en más películas es:", most_frequent_actor)
            print("Número de películas en las que actuó:", movie_count)

        elif option == "6":
            most_frequent_director, director_movies = g.find_most_frequent_director()
            print("El director que ha dirigido en más películas es:", most_frequent_director)
            print("Numero de peliculas que ha dirigido :", director_movies)

        elif option == "7":
            person = input("Ingrese el nombre de la persona: ")
            movies_info = g.find_person_movies_and_relationships(person)
            print("\n".join(movies_info))
            
        elif option == "8":
            break
        else:
            print("Ingresa un valor validoo!")
user_menu()