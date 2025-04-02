import random

from consts import MATRIX_MIN_NUM
from consts import MATRIX_MAX_NUM
from consts import MATRIX_HEIGHT
from consts import MATRIX_WIDTH


def fill_matrix(matrix):
    for i in range(MATRIX_HEIGHT):
        row_matrix = [random.randint(MATRIX_MIN_NUM, MATRIX_MAX_NUM) for j in range(MATRIX_WIDTH)]
        matrix.append(row_matrix)


def output_matrix(matrix):
    for i in matrix:
        print(i, end='\n')
