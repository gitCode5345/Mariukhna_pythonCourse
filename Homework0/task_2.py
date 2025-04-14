from consts import MATRIX_HEIGHT, MATRIX_WIDTH
from matrix_utils import fill_matrix, print_matrix, check_columns_for_zeros
from collections import defaultdict


def sort_rows_by_even_positive_sum(matrix):
    dict_matrix_characteristic = defaultdict(int)

    for i in range(MATRIX_HEIGHT):
        counter_sum = 0
        for j in range(MATRIX_WIDTH):
            if matrix[i][j] > 0 and matrix[i][j] % 2 == 0:
                counter_sum += matrix[i][j]
        dict_matrix_characteristic[i] = counter_sum

    return [matrix[i] for i, _ in sorted(dict_matrix_characteristic.items(), key=lambda x: x[1])]


def main():
    matrix = fill_matrix()
    print_matrix(matrix)

    if matrix:
        counter_cols_without_zero_element = check_columns_for_zeros(matrix)
        print(f'Number of cols that do not contain zeros = {counter_cols_without_zero_element.count(False)}')

        sorted_matrix_by_characteristic = sort_rows_by_even_positive_sum(matrix)

        print('Sorted matrix by characteristic')
        print_matrix(sorted_matrix_by_characteristic)
    else:
        print('Please, fill your matrix')


if __name__ == '__main__':
    main()
