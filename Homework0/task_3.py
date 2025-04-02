from consts import MATRIX_HEIGHT, MATRIX_WIDTH
from matrix_utils import fill_matrix, output_matrix


def count_cols_zero_element(matrix):
    counter = 0
    for i in range(MATRIX_WIDTH):
        if any(matrix[j][i] == 0 for j in range(MATRIX_HEIGHT)):
            counter += 1

    return counter


def find_index_row(matrix):
    max_length = 1
    row_index = -1

    for i in range(MATRIX_HEIGHT):
        current_length = 1
        max_row_series = 1

        for j in range(1, MATRIX_WIDTH):
            current_length = 1 if matrix[i][j] != matrix[i][j - 1] else current_length + 1
            max_row_series = max(max_row_series, current_length)

        if max_row_series > max_length:
            max_length = max_row_series
            row_index = i

    return row_index


def main():
    matrix = []

    fill_matrix(matrix)
    output_matrix(matrix)

    counter_zero_cols = count_cols_zero_element(matrix)
    print(f"Number of columns that have at least one zero element: {counter_zero_cols}")

    index = find_index_row(matrix)

    if index != -1:
        print(f"The row index with the longest series of elements: {index}")
    else:
        print('Failed to find longest series of identical elements')


if __name__ == '__main__':
    main()
