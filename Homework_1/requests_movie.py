import csv
import requests
import copy
from collections import defaultdict, namedtuple
from datetime import datetime, timedelta


class MovieInformation:
    HEADERS = {
        'accept': 'application/json',
        'Authorization': ('Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYz'
                          'RlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4'
                          'OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0'
                          'mUmP-zQpNAMCw_h-oaudAJB6Cn5c8')
    }
    MOVIE_URL = ('https://api.themoviedb.org/3/discover/'
                 'movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={})')
    GENRE_URL = 'https://api.themoviedb.org/3/genre/movie/list?language=en'

    def __init__(self, pages):
        self.pages = pages
        self.initial_list = []
        self.list_movies = []
        self.genre_dict = {}
        self.fetch_genres_information()

    def fetch_movie_information(self):
        self.list_movies.clear()
        for page in range(1, self.pages + 1):
            response = requests.get(self.MOVIE_URL.format(page), headers=self.HEADERS)
            if response.status_code == 200:
                self.list_movies.extend(response.json().get('results', []))
        self.initial_list = [copy.deepcopy(movie) for movie in self.list_movies]

    def fetch_genres_information(self):
        self.genre_dict.clear()
        response = requests.get(self.GENRE_URL, headers=self.HEADERS)
        self.genre_dict = {genre['id']: genre['name'] for genre in response.json().get('genres', [])}

    def get_all_data(self):
        return self.list_movies

    def get_information_about_movies_with_step(self):
        return self.list_movies[3:min(len(self.list_movies), 20):4]

    def get_most_popular_title_of_movie(self):
        return max(self.list_movies, key=lambda x: x['popularity'])['title']

    def get_title_by_description(self, *description):
        description = [word.lower() for word in description]
        return [movie['title'] for movie in self.list_movies
                if any(k in (movie.get('overview') or '').lower() for k in description)]

    def get_unique_genres(self):
        g_id_set = {genre_id for movie in self.list_movies for genre_id in movie.get('genre_ids', [])}
        return frozenset(self.genre_dict[genre_id] for genre_id in g_id_set if genre_id in self.genre_dict)

    def delete_movies_by_genre(self, genre_name):
        genre_id = next((genre_id for genre_id, name in self.genre_dict.items()
                         if name.lower() == genre_name.lower()), None)
        if genre_id is not None:
            self.list_movies = [movie for movie in self.list_movies if genre_id not in movie.get('genre_ids', [])]

    def get_popular_genres(self):
        counter = defaultdict(int)
        for movie in self.list_movies:
            for genre_id in movie.get('genre_ids', []):
                name_genre = self.genre_dict.get(genre_id)
                if name_genre:
                    counter[name_genre] += 1
        return dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))

    def get_pairs_by_genre(self):
        genre_map = defaultdict(list)
        for movie in self.list_movies:
            for genre_id in movie.get('genre_ids', []):
                genre_map[genre_id].append(movie['title'])

        result = set()
        for titles in genre_map.values():
            for i in range(0, len(titles) - 1, 2):
                result.add((titles[i], titles[i + 1]))
        return frozenset(result)

    def get_data_with_modified_genres(self):
        modified_films = copy.deepcopy(self.initial_list)
        for movie in modified_films:
            if movie.get('genre_ids'):
                movie['genre_ids'][0] = 22
        return self.initial_list, modified_films

    def get_custom_structure(self):
        result = []
        FilmStruct = namedtuple('FilmStruct',
                                ['title', 'popularity', 'score', 'last_day_in_cinema'])

        for movie in self.initial_list:
            try:
                title = movie['title']
                popularity = round(movie['popularity'], 1)
                score = int(movie['vote_average'])
                release_date = datetime.strptime(movie['release_date'], '%Y-%m-%d')
                last_day = release_date + timedelta(weeks=10)  # 2 months and 2 weeks
                result.append(FilmStruct(title, popularity, score, last_day.date()))
            except (KeyError, ValueError):
                continue

        return sorted(result, key=lambda x: (x.score, x.popularity), reverse=True)

    def write_to_csv(self, path):
        rows = self.get_custom_structure()
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Popularity', 'Score', 'Last_day_in_cinema'])
            for row in rows:
                writer.writerow(row)


def main():
    print('Hello! Please, enter count a pages you want fetch:')
    pages = int(input())

    movies_data = MovieInformation(pages)
    movies_data.fetch_movie_information()

    print(f'Information about all received movies: {movies_data.get_all_data()}')
    print(f'Movies with step 4: {movies_data.get_information_about_movies_with_step()}')
    print(f'Title of the most popular movie: {movies_data.get_most_popular_title_of_movie()}')
    print(f'Movie titles according to the given description: {movies_data.get_title_by_description('Chill')}')
    print(f'Unique genres: {movies_data.get_unique_genres()}')

    movies_data.delete_movies_by_genre('Horror')

    print(f'List of genres, with their number of uses: {movies_data.get_popular_genres()}')
    print(f'Movie titles grouped by genre: {movies_data.get_pairs_by_genre()}')

    original, modified = movies_data.get_data_with_modified_genres()
    print('Original first genre_ids:', original[0].get('genre_ids'))
    print('Modified first genre_ids:', modified[0].get('genre_ids'))

    struct_data = movies_data.get_custom_structure()
    print('Structured data example:', struct_data[:3])

    movies_data.write_to_csv('films_data.csv')


if __name__ == '__main__':
    main()
