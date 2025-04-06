from consts import MATRIX_HEIGHT, MATRIX_WIDTH
from matrix_utils import fill_matrix, print_matrix
from collections import defaultdict


def count_matrix_rows_without_zero(matrix):
    return sum(1 for row in matrix if 0 not in row)


def find_max_repeated_element(matrix):
    dict_nums = defaultdict(int)
    for i in range(MATRIX_HEIGHT):
        for j in range(MATRIX_WIDTH):
            dict_nums[matrix[i][j]] += 1

    value_max_element, count_max_element = max(dict_nums.items(), key=lambda x: x[1])

    return value_max_element, count_max_element


def main():
    matrix = fill_matrix()
    print_matrix(matrix)

    if matrix:
        counter_rows_without_zero_element = count_matrix_rows_without_zero(matrix)
        print(f'Number of rows that do not contain zeros = {counter_rows_without_zero_element}')

        value_max_element, count_max_element = find_max_repeated_element(matrix)
        x = (f'The maximum number that occurs more than once. Number: {value_max_element}, '
             f'number of repetitions: {count_max_element}') \
            if count_max_element > 1 else 'No repeating numbers'

        print(x)
    else:
        print('Please, fill your matrix')


if __name__ == '__main__':
    main()
