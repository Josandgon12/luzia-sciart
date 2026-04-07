from abc import ABC, abstractmethod
from time import sleep

import microcontroller
import neopixel
import numpy as np
import cv2


class Screen(ABC):

    def __init__(self, width=30, height=13, frequency=20):
        self.current = np.zeros((width, height))
        self.frequency = frequency
        self.width = width
        self.height = height

    @abstractmethod
    def _draw(self, matrix: np.ndarray):
        pass

    def draw(self, matrix: np.ndarray):
        self._draw(matrix)
        self.current = matrix

    def draw_fade(self, matrix: np.ndarray, time: float = 5):
        frames = round(time * self.frequency)
        current = self.current
        difference = (matrix - current) / frames

        for _ in range(frames - 1):
            current += difference
            self._draw(current)
            sleep(1 / self.frequency)

        self.draw(matrix)


class CV2Screen(Screen):
    def __init__(self, window: str, width=30, height=13, frequency=20):
        super().__init__(width, height, frequency)
        self.window = window

    def _draw(self, matrix: np.ndarray):
        cv2.imshow(self.window, matrix)
        cv2.waitKey(1)


class NeoPixelScreen(Screen):

    def __init__(self, width: int, height: int, frequency: int, brightness: tuple[int, int, int], pin: microcontroller.Pin):
        super().__init__(width, height, frequency)
        self.brightness = brightness
        self.pixels = neopixel.NeoPixel(pin, width * height, auto_write=False, pixel_order="GBR")

    def _draw(self, matrix: np.ndarray):
        for x in range(matrix.shape[0]):
            for y in range(matrix.shape[1]):
                color = matrix[y, x]
                pixel_y = y if x % 2 == 1 else self.height - y
                pixel_number = x * self.height + pixel_y

                r = color * self.brightness[0]
                g = color * self.brightness[1]
                b = color * self.brightness[2]

                self.pixels[pixel_number] = (
                    255 if r > 255 else r,
                    255 if g > 255 else g,
                    255 if b > 255 else b
                )
        self.pixels.show()
