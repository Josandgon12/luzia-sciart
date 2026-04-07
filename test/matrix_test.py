import sys
sys.path.append('../luzia')

import cv2
from luzia.matrix import Matrix


def draw(matrix: Matrix):
    cv2.namedWindow("Imagen filtrada", cv2.WINDOW_GUI_EXPANDED)
    cv2.resizeWindow("Imagen filtrada", 1200, 520)
    cv2.imshow("Imagen filtrada", matrix.to_numpy())
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test_create():
    coords = [(20, 20, 0.76), (40, 60, 0.10), (60, 80, 0.04), (80, 40, 0.14), (90, 90, 0.01)]
    matrix = Matrix.create((100, 50), coords, 20)
    draw(matrix)


def test_from_factors():
    factors = [0.97, 0.01, 0.04, 0.60, 0.20, 0.05, 0.43]
    matrix = Matrix.from_factors((30, 13), factors, 6)
    draw(matrix)


if __name__ == "__main__":
    test_from_factors()
