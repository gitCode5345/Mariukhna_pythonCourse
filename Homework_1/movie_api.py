import os
import string
import requests
import csv
from check_list_size_decorator import check_list_size
from datetime import timedelta, datetime
from copy import deepcopy
from dotenv import load_dotenv
from collections import Counter, namedtuple


class MovieAPI:
    load_dotenv()
    MOVIE_URL = 'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=\
                 popularity.desc&page={}'
    GENRES_URL = 'https://api.themoviedb.org/3/genre/movie/list?language=en'
    HEADERS_API = {'accept': 'application/json',
                   'Authorization': f'Bearer {os.getenv('API_KEY')}'}

    def __init__(self, pages):
        self.pages = pages
        self.init_list = []
        self.copy_list = []
        self.genres = {}
        self.fetch_genres()

    def fetch_genres(self):
        self.genres.clear()
        response = requests.get(self.GENRES_URL, headers=self.HEADERS_API)
        if response.status_code == 200:
            data = response.json().get('genres', [])
            for item in data:
                self.genres[item['id']] = item['name']
        else:
            print('Failed to load genres')
            return None

    def fetch_movies(self):
        self.copy_list.clear()
        for i in range(1, self.pages + 1):
            response = requests.get(self.MOVIE_URL.format(i), headers=self.HEADERS_API)
            if response.status_code == 200:
                self.copy_list.extend(response.json().get('results', []))
            else:
                print('Failed to download movies')
                return None
        self.init_list = deepcopy(self.copy_list)

    @check_list_size
    def get_all_data(self):
        return self.copy_list

    @check_list_size
    def get_all_genres(self):
        return self.genres

    @check_list_size
    def get_all_data_with_step(self):
        return self.copy_list[3:20:4]

    @check_list_size
    def get_most_popular_title_movie(self):
        return max(self.copy_list, key=lambda x: x['popularity'])['title']

    @check_list_size
    def get_title_of_movies_by_description(self, *description):
        description = [word.lower() for word in description]
        list_of_names = []
        for movie in self.copy_list:
            movie_overview = ''.join([s for s in movie['overview'].lower() if s not in string.punctuation]).split()
            for word in movie_overview:
                if word in description:
                    list_of_names.append(movie['title'])
                    break

        return list_of_names

    @check_list_size
    def get_unique_collection_of_present_genres(self):
        genres_id_set = {genre_id for movie in self.copy_list for genre_id in movie['genre_ids']}
        return frozenset(self.genres[genre_id] for genre_id in genres_id_set)

    @check_list_size
    def delete_movies_by_genre(self, *genre_names):
        genre_names = [word.lower() for word in genre_names]
        if self.copy_list:
            self.copy_list = [movie for movie in self.copy_list if not any(self.genres[g_id].lower() in genre_names
                                                                           for g_id in movie['genre_ids'])]

    @check_list_size
    def get_names_of_most_popular_genres(self):
        list_of_genres = []
        for movie in self.copy_list:
            for ids in movie['genre_ids']:
                list_of_genres.append(self.genres[ids])

        return Counter(list_of_genres)

    @check_list_size
    def get_collection_of_movies_by_similar_genres(self):
        list_collection = []

        for i in range(len(self.copy_list)):
            for j in range(i + 1, len(self.copy_list)):
                flag = any(first_index == second_index for first_index in self.copy_list[i]['genre_ids']
                           for second_index in self.copy_list[j]['genre_ids'])

                if flag:
                    pair_tuple = (self.copy_list[i]['title'], self.copy_list[j]['title'])
                    list_collection.append(pair_tuple)

        return tuple(list_collection)

    @check_list_size
    def replace_first_genre_index_in_movies(self):
        for movie in self.copy_list:
            if movie['genre_ids']:
                movie['genre_ids'][0] = 22

        return self.init_list, self.copy_list

    @check_list_size
    def get_compact_movie_collection(self):
        fieldnames_structure = ['title', 'popularity', 'score', 'last_day_in_cinema']
        film_structure = namedtuple(typename='FilmStructure', field_names=fieldnames_structure)
        list_structure = []

        for movie in self.copy_list:
            title_movie = movie['title']
            popularity_movie = round(movie['popularity'], 1)
            score_movie = round(movie['vote_average'])
            parse_datetime_movie = datetime.strftime(datetime.strptime(movie['release_date'], '%Y-%m-%d') +
                                                     timedelta(weeks=10), format='%Y-%m-%d')

            list_structure.append(film_structure(title_movie, popularity_movie, score_movie, parse_datetime_movie))

        return sorted(list_structure, key=lambda x: (x.score, x.popularity), reverse=True)

    @check_list_size
    def save_collection_to_csv(self, film_collection: namedtuple, filename: str, file_path='.'):
        full_save_path = file_path + '/' + filename + '.csv'
        headers = ['title', 'popularity', 'score', 'last_day_in_cinema']
        with open(full_save_path, mode='w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(headers)
            csv_writer.writerows(film_collection)
