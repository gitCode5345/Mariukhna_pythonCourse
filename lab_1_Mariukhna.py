matrix = ([1, 10, 3, -4],
          [-2, 3, 1, -5],
          [-10, 12, 0, 10])

def task_var_1(matrix):
    "first task"
    count_matrix_row = len(matrix)

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                count_matrix_row = count_matrix_row - 1
                break

    print(count_matrix_row)

    "second task"
    numbers_set = set()

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] not in numbers_set:
                check_number(matrix, matrix[i][j], numbers_set)

    if numbers_set:
        print(f'The maximum number that occurs more than once: {max(numbers_set)}')
    else:
        print('No repeating numbers')

def check_number(matrix, number, numbers_set):
    counter = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == number:
                counter = counter + 1
        if counter > 1:
            numbers_set.add(number)
            return

if __name__ == '__main__':
    task_var_1(matrix)
