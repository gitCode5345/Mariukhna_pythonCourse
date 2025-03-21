import random

matrix = []

MATRIX_MIN_NUM = -20
MATRIX_MAX_NUM = 100

MATRIX_HEIGHT = 4
MATRIX_WIDTH = 3


def main():
    fill_matrix(matrix)
    print_matrix(matrix)
    start_var_1(matrix)


def fill_matrix(m):
    for i in range(MATRIX_HEIGHT):
        row_matrix = []
        for j in range(MATRIX_WIDTH):
            row_matrix.append(random.randint(MATRIX_MIN_NUM, MATRIX_MAX_NUM))

        m.append(row_matrix)


def print_matrix(m):
    for i in m:
        print(i, end='\n')


def start_var_1(m):
    count_matrix_row = count_no_zero_rows(m)
    print(f"Number of rows that do not contain zeros = {count_matrix_row}")

    "second task"
    numbers_set = find_matrix_max_num(m)

    if numbers_set:
        print(f'The maximum number that occurs more than once: {max(numbers_set)}')
    else:
        print('No repeating numbers')


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


def check_number(m, number, numbers_set):
    counter = 0
    for i in range(MATRIX_HEIGHT):
        for j in range(MATRIX_WIDTH):
            if m[i][j] == number:
                counter = counter + 1
        if counter > 1:
            numbers_set.add(number)
            return


if __name__ == '__main__':
    main()
