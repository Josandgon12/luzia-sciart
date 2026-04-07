import random
from math import ceil
from random import shuffle
from typing import List, Tuple

import numpy as np

MIN_SIZE_FOR_GRID = 50


class Matrix:

    @staticmethod
    def from_analysis(matrix_size: Tuple[int, int], data: dict, sigma: float):
        factors = []
        is_male = data["gender"] == "male"

        factors += sorted(data["emotion"].values(), reverse=True)[:3]
        # factors += sorted(data["race"].values(), reverse=True)[:3]
        factors.append(random.randint(0 if is_male else 49, 50 if is_male else 100))
        factors.append(random.randint(data["age"][0], data["age"][1]))

        factors = [factor / 100 for factor in factors]

        return Matrix.from_factors(matrix_size, factors, sigma)

    @staticmethod
    def from_factors(matrix_size: Tuple[int, int], factors: List[float], sigma: float):
        use_grid = matrix_size[0] > MIN_SIZE_FOR_GRID and matrix_size[1] > MIN_SIZE_FOR_GRID
        coords = []

        if use_grid:
            grid_x = matrix_size[0] / ceil(len(factors) / 2)
            grid_y = matrix_size[1] / ceil(len(factors) / 2)

        shuffle(factors)

        for i in range(len(factors)):
            x = np.random.randint(i * grid_x, (i + 1) * grid_x) if use_grid else np.random.randint(0, matrix_size[0])
            y = np.random.randint(i * grid_y, (i + 1) * grid_y) if use_grid else np.random.randint(0, matrix_size[1])
            coords.append((x, y, factors[i]))

        return Matrix.create(matrix_size, coords, sigma)

    @staticmethod
    def create(matrix_size: Tuple[int, int], coords: List[Tuple[int, int, float]], sigma: float):
        square_size = max(matrix_size)

        matrix = np.zeros((square_size, square_size))
        X, Y = np.meshgrid(np.arange(square_size), np.arange(square_size))

        for coord in coords:
            matrix += np.exp(-(np.square(X - coord[0]) + np.square(Y - coord[1])) / (2 * np.square(sigma))) * coord[2]

        # return Matrix(matrix[:matrix_size[1] - 1, :] if square_size > matrix_size[1] else matrix[:, matrix_size[0] - 1])
        return Matrix(matrix)

    def __init__(self, matrix):
        self.matrix = matrix

    def to_numpy(self) -> np.ndarray:
        return self.matrix
