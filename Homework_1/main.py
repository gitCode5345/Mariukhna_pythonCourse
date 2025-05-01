from movie_information import MovieInformation


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
