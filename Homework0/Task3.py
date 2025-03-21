import random

matrix = []

MATRIX_MIN_NUM = -20
MATRIX_MAX_NUM = 100

MATRIX_HEIGHT = 4
MATRIX_WIDTH = 3


def main():
    fill_matrix(matrix)
    print_matrix(matrix)
    start_var_3(matrix)


def fill_matrix(m):
    for i in range(MATRIX_HEIGHT):
        row_matrix = []
        for j in range(MATRIX_WIDTH):
            row_matrix.append(random.randint(MATRIX_MIN_NUM, MATRIX_MAX_NUM))

        m.append(row_matrix)


def print_matrix(m):
    for i in m:
        print(i, end='\n')


def start_var_3(m):
    counter_zero_cols = count_cols_zero_element(m)
    print(f"Number of columns that have at least one zero element: {counter_zero_cols}")

    index = find_index_row(m)

    if index != -1:
        print(f"The row index with the longest series of elements: {index}")
    else:
        print('Failed to find longest series of identical elements')


def count_cols_zero_element(m):
    counter = 0
    for i in range(MATRIX_WIDTH):
        for j in range(MATRIX_HEIGHT):
            if m[j][i] == 0:
                counter = counter + 1
                break

    return counter


def find_index_row(m):
    max_length = 1
    row_index = -1

    for i in range(MATRIX_HEIGHT):
        current_length = 1
        max_row_series = 1

        for j in range(1, MATRIX_WIDTH):
            if m[i][j] == m[i][j - 1]:
                current_length += 1
            else:
                current_length = 1

            max_row_series = max(max_row_series, current_length)

        if max_row_series > max_length:
            max_length = max_row_series
            row_index = i

    return row_index


if __name__ == '__main__':
    main()
