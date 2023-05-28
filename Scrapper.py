from bs4 import BeautifulSoup
import requests
import mysql.connector

class Movie:
    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.actors = None
        self.director = None
        self.writers = None

url = 'https://www.imdb.com/chart/top/'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')


table = soup.find('tbody', class_='lister-list')
rows = table.find_all('tr')
movie_list = []

for row in rows:
    title_column = row.find('td', class_='titleColumn')
    title_link = title_column.find('a')
    title = title_link.get_text(strip=True)
    href = title_link['href']
    #print(f"Title: {title}")
    #print(f"Href: www.imdb.com/{href}")
    movie = Movie(title, "https://www.imdb.com"+href)
    movie_list.append(movie)


class ShowScrapper:

    def Scrapper(self,movie):

        link = movie.link

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(link, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        cast_list = soup.find_all('a', attrs={'data-testid': 'title-cast-item__actor'})
        actors = [actor.get_text(strip=True) for actor in cast_list]
        movie.actors = actors
        #print("ACTORES:")
        #print(actors)
        #for actor in actors:
        #    print(actor)

        #El primer elemento con ese nombre de clase, es el director, el resto tendrá a los escritores
        director = soup.find('a', class_='ipc-metadata-list-item__list-content-item').get_text(strip=True)
        movie.director = director
        #print("\nDirector:")
        #print(director)


        writers_list = soup.find_all('a', class_='ipc-metadata-list-item__list-content-item')
        writers = []
        for writer in writers_list[1:-1]:
            if writer.get_text(strip=True) in actors:
                break
            else:
                writers.append(writer.get_text(strip=True))

        movie.writers = writers
        #print("\nEscritores:")
        #print(writers)


#Realizar web scrapping a las 250 peliculas
ShowScrapper = ShowScrapper()
#for i in range(len(movie_list)):
#    ShowScrapper.Scrapper(movie_list[i])
    #A este punto tendre una lista con 250 objetos de tipo Movie los cuales tienen toda la informacion que necesito, asi que aqui ya debo
    #mandar esos datos a la base de datos
    #print(movie_list[i].title)


# Establecer la conexión a la base de datos
conn = mysql.connector.connect(
    host='localhost',
    user='tu_usuario',
    password='tu_contraseña',
    database='nombre_de_la_base_de_datos'
)


