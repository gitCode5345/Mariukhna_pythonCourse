from consts import MATRIX_HEIGHT, MATRIX_WIDTH
from matrix_utils import fill_matrix, output_matrix


def count_no_zero_cols(matrix):
    counter = 0
    for i in range(MATRIX_WIDTH):
        if any(matrix[j][i] != 0 for j in range(MATRIX_HEIGHT)):
            counter += 1

    return counter


def find_matrix_characteristic(matrix):
    matrix_characteristic = []

    for i in range(MATRIX_HEIGHT):
        counter_sum = 0
        for j in range(MATRIX_WIDTH):
            if matrix[i][j] > 0 and matrix[i][j] % 2 == 0:
                counter_sum += matrix[i][j]
        matrix_characteristic.append((counter_sum, i))

    matrix_characteristic.sort()
    sorted_matrix = [matrix[i] for _, i in matrix_characteristic]

    return sorted_matrix


def main():
    matrix = []

    fill_matrix(matrix)
    output_matrix(matrix)

    count_matrix_cols = count_no_zero_cols(matrix)
    print(f"Number of cols that do not contain zeros = {count_matrix_cols}")

    characteristic = find_matrix_characteristic(matrix)

    print('Sorted matrix by characteristic')
    output_matrix(characteristic)


if __name__ == '__main__':
    main()
