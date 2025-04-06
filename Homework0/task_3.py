from matrix_utils import fill_matrix, print_matrix, check_columns_for_zeros


def find_longest_series_index_row(matrix):
    max_length = 1
    row_index = -1

    for index, row in enumerate(matrix):
        current_length = 1
        max_row_series = 1

        for j in range(1, len(row)):
            current_length = 1 if matrix[index][j] != matrix[index][j - 1] else current_length + 1
            max_row_series = max(max_row_series, current_length)

        if max_row_series > max_length:
            max_length = max_row_series
            row_index = index

    return row_index


def main():
    matrix = fill_matrix()
    print_matrix(matrix)

    if matrix:
        counter_cols_with_zero_element = check_columns_for_zeros(matrix)
        print(f'Number of columns that have at least one zero element: {counter_cols_with_zero_element.count(True)}')

        longest_series_index_row = find_longest_series_index_row(matrix)

        answer = f'The row index with the longest series of elements: {longest_series_index_row}' \
                 if longest_series_index_row != -1 else 'Failed to find longest series of identical elements'

        print(answer)
    else:
        print('Please, fill your matrix')


if __name__ == '__main__':
    main()
