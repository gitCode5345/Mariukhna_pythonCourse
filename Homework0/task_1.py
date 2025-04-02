from consts import MATRIX_HEIGHT, MATRIX_WIDTH
from matrix_utils import fill_matrix, output_matrix


def count_no_zero_rows(matrix):
    counter_rows = 0
    counter_rows += sum(1 for row in matrix if 0 not in row)

    return counter_rows


def find_matrix_max_num(matrix):
    dict_nums = {}
    for i in range(MATRIX_HEIGHT):
        for j in range(MATRIX_WIDTH):
            if matrix[i][j] not in dict_nums:
                dict_nums[matrix[i][j]] = 1
            else:
                dict_nums[matrix[i][j]] += 1

    max_key, value_key = max(dict_nums.items(), key=lambda x: x[1])

    return max_key, value_key


def main():
    matrix = []

    fill_matrix(matrix)
    output_matrix(matrix)

    count_matrix_row = count_no_zero_rows(matrix)
    print(f"Number of rows that do not contain zeros = {count_matrix_row}")

    max_key, max_value_key = find_matrix_max_num(matrix)
    print(f'The maximum number that occurs more than once: {max_key}, value {max_value_key}') \
        if max_key and max_value_key > 1 \
        else print('No repeating numbers')


if __name__ == '__main__':
    main()
