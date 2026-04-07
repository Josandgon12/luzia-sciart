import sys

import board

sys.path.append('../luzia')

from time import sleep
import cv2
from luzia.matrix import Matrix
from luzia.screen import CV2Screen, NeoPixelScreen


def test_neopixel_screen():
    screen = NeoPixelScreen(20, 20, 60, brightness=(127, 150, 180), pin=board.D12)

    factors = [0.97, 0.01, 0.04, 0.60, 0.20, 0.05, 0.43]

    screen.draw(Matrix.from_factors((20, 20), factors, 2).to_numpy())
    sleep(2)
    while True:
        screen.draw_fade(Matrix.from_factors((20, 20), factors, 2).to_numpy(), time=2)


MAIN_WINDOW = "Ventana principal"
INITIAL_MATRIX = "Matriz inicial de la transición"
FINAL_MATRIX = "Matriz final de la transición"


def test_cv2screen():
    screen = CV2Screen(MAIN_WINDOW)
    create_windows()

    factors = [0.97, 0.01, 0.04, 0.60, 0.20, 0.05, 0.43]

    matrix1 = Matrix.from_factors((30, 13), factors, 5)
    screen.draw(matrix1.to_numpy())
    sleep(2)

    while True:
        matrix2 = Matrix.from_factors((30, 13), factors, 5)

        cv2.imshow(INITIAL_MATRIX, matrix1.to_numpy())
        cv2.imshow(FINAL_MATRIX, matrix2.to_numpy())

        screen.draw_fade(matrix2.to_numpy())
        matrix1 = matrix2


def create_windows():
    cv2.namedWindow(MAIN_WINDOW, cv2.WINDOW_GUI_EXPANDED)
    cv2.resizeWindow(MAIN_WINDOW, 1200, 520)

    cv2.namedWindow(INITIAL_MATRIX, cv2.WINDOW_GUI_EXPANDED)
    cv2.resizeWindow(INITIAL_MATRIX, 600, 260)

    cv2.namedWindow(FINAL_MATRIX, cv2.WINDOW_GUI_EXPANDED)
    cv2.resizeWindow(FINAL_MATRIX, 600, 260)


if __name__ == "__main__":
    test_neopixel_screen()
