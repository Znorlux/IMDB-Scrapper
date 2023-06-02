from bs4 import BeautifulSoup
import requests
import json
import os

class Movie:
    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.actors = []
        self.director = None
        self.writers = []

def get_movie_info(movie):
    url = movie.link
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(url, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    
    cast_list = soup.find_all('a', attrs={'data-testid': 'title-cast-item__actor'})
    for actor in cast_list:
        movie.actors.append(actor.get_text(strip=True))
    
    director = soup.find('a', class_='ipc-metadata-list-item__list-content-item').get_text(strip=True)
    movie.director = director
    
    writers_list = soup.find_all('a', class_='ipc-metadata-list-item__list-content-item')
    for writer in writers_list[1:-1]:
        if writer.get_text(strip=True) in movie.actors and writer.get_text(strip=True) != "Charles Chaplin":
            break
        else:
            movie.writers.append(writer.get_text(strip=True))

def Scrapper():
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
        movie = Movie(title, "https://www.imdb.com"+href)
        movie_list.append(movie)

    for movie in movie_list:
        print(movie.title)
        get_movie_info(movie)

    if os.path.exists("movies.json"):
        os.remove("movies.json")

    data = []
    for movie in movie_list:
        movie_data = {
            "title": movie.title,
            "link": movie.link,
            "actors": movie.actors,
            "director": movie.director,
            "writers": movie.writers
        }
        data.append(movie_data)

    # Escribir la lista de datos en un archivo JSON
    with open("movies.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    Scrapper()