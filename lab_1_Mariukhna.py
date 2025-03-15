import random

matrix = []

MATRIX_MIN = -20
MATRIX_MAX = 100

MATRIX_HEIGHT = 4
MATRIX_WIDTH = 3


def count_no_zero_rows(m):
    count_matrix_row = MATRIX_HEIGHT

    for i in range(MATRIX_HEIGHT):
        for j in range(MATRIX_WIDTH):
            if m[i][j] == 0:
                count_matrix_row = count_matrix_row - 1
                break

    return count_matrix_row


def find_matrix_max_num(m):
    numbers_set = set()

    for i in range(MATRIX_HEIGHT):
        for j in range(MATRIX_WIDTH):
            if m[i][j] not in numbers_set:
                check_number(m, m[i][j], numbers_set)

    return numbers_set


def start_var_1(m):
    count_matrix_row = count_no_zero_rows(matrix)
    print(f"Number of rows that do not contain zeros = {count_matrix_row}")

    "second task"
    numbers_set = find_matrix_max_num(matrix)

    if numbers_set:
        print(f'The maximum number that occurs more than once: {max(numbers_set)}')
    else:
        print('No repeating numbers')


def check_number(m, number, numbers_set):
    counter = 0
    for i in range(MATRIX_HEIGHT):
        for j in range(MATRIX_WIDTH):
            if m[i][j] == number:
                counter = counter + 1
        if counter > 1:
            numbers_set.add(number)
            return


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


def start_var_2(m):
    count_matrix_cols = count_no_zero_cols(m)
    print(f"Number of cols that do not contain zeros = {count_matrix_cols}")

    characteristic = find_matrix_characteristic(m)

    print('Sorted matrix by characteristic')
    print_matrix(characteristic)


def swap_matrix_row(m, characteristic):
    for i in range(len(characteristic)):
        for j in range(len(characteristic) - 1 - i):
            if characteristic[j] > characteristic[j + 1]:
                characteristic[j + 1], characteristic[j] = characteristic[j], characteristic[j + 1]
                m[j + 1], m[j] = m[j], m[j + 1]


def count_cols(m):
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


def start_var_3(m):
    counter_zero_cols = count_cols(m)
    print(f"Number of columns that have at least one zero element: {counter_zero_cols}")

    index = find_index_row(m)

    if index != -1:
        print(f"The row index with the longest series of elements: {index}")
    else:
        print('Failed to find longest series of identical elements')


def fill_matrix(m):
    for i in range(MATRIX_HEIGHT):
        row_matrix = []
        for j in range(MATRIX_WIDTH):
            row_matrix.append(random.randint(MATRIX_MIN, MATRIX_MAX))

        m.append(row_matrix)


def print_matrix(m):
    for i in m:
        print(i, end='\n')

if __name__ == '__main__':
    fill_matrix(matrix)
    print_matrix(matrix)
    #start_var_1(matrix)
    start_var_2(matrix)
    #start_var_3(matrix)
