import random

from consts import MATRIX_MIN_NUM
from consts import MATRIX_MAX_NUM
from consts import MATRIX_HEIGHT
from consts import MATRIX_WIDTH


def fill_matrix():
    return [[random.randint(MATRIX_MIN_NUM, MATRIX_MAX_NUM) for j in range(MATRIX_WIDTH)] for i in range(MATRIX_HEIGHT)]


def print_matrix(matrix):
    matrix_elements = [row for row in matrix] if matrix else 'Please, fill your matrix'
    print(matrix_elements)


def check_columns_for_zeros(matrix):
    return [any(matrix[j][i] == 0 for j in range(MATRIX_HEIGHT)) for i in range(MATRIX_WIDTH)]
