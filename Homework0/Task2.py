import random

matrix = []

MATRIX_MIN_NUM = -20
MATRIX_MAX_NUM = 100

MATRIX_HEIGHT = 4
MATRIX_WIDTH = 3


def main():
    fill_matrix(matrix)
    print_matrix(matrix)
    start_var_2(matrix)


def fill_matrix(m):
    for i in range(MATRIX_HEIGHT):
        row_matrix = []
        for j in range(MATRIX_WIDTH):
            row_matrix.append(random.randint(MATRIX_MIN_NUM, MATRIX_MAX_NUM))

        m.append(row_matrix)


def print_matrix(m):
    for i in m:
        print(i, end='\n')


def start_var_2(m):
    count_matrix_cols = count_no_zero_cols(m)
    print(f"Number of cols that do not contain zeros = {count_matrix_cols}")

    characteristic = find_matrix_characteristic(m)

    print('Sorted matrix by characteristic')
    print_matrix(characteristic)


def count_no_zero_cols(m):
    count_matrix_cols = MATRIX_WIDTH

    for i in range(MATRIX_WIDTH):
        for j in range(MATRIX_HEIGHT):
            if m[j][i] == 0:
                count_matrix_cols = count_matrix_cols - 1
                break

    return count_matrix_cols


def find_matrix_characteristic(m):
    matrix_characteristic = []

    for i in range(MATRIX_HEIGHT):
        counter_sum = 0
        for j in range(MATRIX_WIDTH):
            if m[i][j] > 0 and m[i][j] % 2 == 0:
                counter_sum += m[i][j]
        matrix_characteristic.append(counter_sum)

    swap_matrix_row(m, matrix_characteristic)

    return m


def swap_matrix_row(m, characteristic):
    for i in range(len(characteristic)):
        for j in range(len(characteristic) - 1 - i):
            if characteristic[j] > characteristic[j + 1]:
                characteristic[j + 1], characteristic[j] = characteristic[j], characteristic[j + 1]
                m[j + 1], m[j] = m[j], m[j + 1]


if __name__ == '__main__':
    main()
