from movie_api import MovieAPI


def main():
    movies_information = MovieAPI(5)
    movies_information.fetch_movies()

    movies_information.fetch_genres()
    movies_information.fetch_movies()

    print(f'All data: {movies_information.get_all_data()}')
    print(f'All genres: {movies_information.get_all_genres()}')
    print(f'All data with step 4: {movies_information.get_all_data_with_step()}')
    print(f'Most popular film: {movies_information.get_most_popular_title_movie()}')
    print(f'Movies get by description: '
          f'{movies_information.get_title_of_movies_by_description('embarks', 'car', 'LoVE')}')
    print(movies_information.get_unique_collection_of_present_genres())
    movies_information.delete_movies_by_genre('War')
    print(f'All data after delete by genre: {movies_information.get_all_data()}')
    print(f'Most popular genres: {movies_information.get_names_of_most_popular_genres().most_common(5)}')
    print(f'Collection by common genres: {movies_information.get_collection_of_movies_by_similar_genres()[:5]}')
    initial_movies, copy_movies = movies_information.replace_first_genre_index_in_movies()
    print(f'Original unmodified data: {initial_movies[:5]} \n'
          f'Modified data: {copy_movies[:5]}')
    test_data = movies_information.get_compact_movie_collection()[:5]
    print(f'Collection of structures: {test_data[:5]}')
    movies_information.save_collection_to_csv(test_data, 'test', file_path='/Users/dmitrijmaruhna/Desktop')


if __name__ == '__main__':
    main()
