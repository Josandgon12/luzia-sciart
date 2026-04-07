import json
import os
import sys
import traceback
from threading import Thread, Timer
from time import sleep
from typing import List

import board
import cv2
import numpy as np

from analyzer import Analyzer
from arduino_hook import ArduinoHook, ArduinoHookMock
from matrix import Matrix
from screen import Screen, CV2Screen, NeoPixelScreen
from sensors import ArduinoDistanceSensor, ArduinoButton
from utils import get_random_element, play_sound, get_logger

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.getenv("LUZIA_DATA_PATH", os.path.join(os.path.expanduser("~"), ".luzia", "last-data.json"))
DATA_SAVE_DELAY_SECONDS = 60 * 5

ARDUINO_PORT = os.getenv("ARDUINO_PORT", "/dev/ttyACM0")
DISTANCE_SENSOR_TRIGGER = 65

RESTART_SECONDS = 60 * 60 * 3  # 3 hours

SCREEN_WIDTH = 20
SCREEN_HEIGHT = 20
SCREEN_FREQUENCY = 60
SCREEN_BRIGHTNESS = (180, 212, 255)
SCREEN_TRANSITION_SECONDS = 1

AUDIO_PATH = os.path.join(BASE_DIR, "..", "assets", "introduction.mp3")
CAPTURE_SECONDS = 25
SLEEP_SECONDS = 3
POST_ANALYSIS = 10

MAX_MATRICES = 10
MATRIX_SIGMA = 2.3

LOG = get_logger("main")


class Luzia:
    _data: List[dict] = []
    _last_chosen = None

    def __init__(self, screen: Screen, arduino_hook: ArduinoHook):
        self._load_data()
        self._arduino_hook = arduino_hook

        self._should_exit = False
        self._restart_scheduled = False
        self._restart_timer = Timer(RESTART_SECONDS, self._schedule_restart)

        self._screen = screen
        self._screen_thread = Thread(target=self._screen_task, daemon=True)

        self._analyzer = Analyzer(cv2.VideoCapture(0), CAPTURE_SECONDS, SLEEP_SECONDS)
        self._analyzer_thread = Thread(target=self._analyzer_task, daemon=True)

        self._distance_sensor = ArduinoDistanceSensor(DISTANCE_SENSOR_TRIGGER, self._arduino_hook)
        self._button = ArduinoButton(self._arduino_hook)

        self._save_data_thread = Thread(target=self._save_data_task, daemon=True)

    def start(self):
        self._arduino_hook.start()
        self._restart_timer.start()

        self._analyzer_thread.start()
        self._save_data_thread.start()
        self._screen_thread.start()

        while True:
            if self._should_exit:
                LOG.debug("Exiting...")
                sys.exit(0)
            sleep(1)

    def _schedule_restart(self):
        self._restart_scheduled = True
        LOG.debug("Restart scheduled")

    def _update_screen(self):
        if len(self._data) == 0:
            self._screen.draw(np.random.rand(SCREEN_HEIGHT, SCREEN_WIDTH))
            sleep(0.05)
            return

        chosen = get_random_element(self._data, (self._last_chosen,))
        self._last_chosen = chosen

        matrix = Matrix.from_analysis((SCREEN_WIDTH, SCREEN_HEIGHT), chosen, MATRIX_SIGMA).to_numpy()
        self._screen.draw_fade(matrix, SCREEN_TRANSITION_SECONDS)

    def _analyze(self):
        if self._restart_scheduled:
            self._should_exit = True
            return

        if not self._distance_sensor.trigger():
            sleep(0.1)
            return

        LOG.debug("Spectator detected! Started analyzing...")
        self._arduino_hook.send_running(True)
        sound = play_sound(AUDIO_PATH)
        data = None

        try:
            data = self._analyzer.analyze(self._is_quitting)
        except BaseException:
            traceback.print_exc()

        if self._is_quitting():
            LOG.debug("Spectator walked away or pressed the button. Quitting...")
            sound.terminate()
        else:
            if len(self._data) == 10:
                self._data.pop(0)

            if data is not None:
                self._data.append(data)

        self._arduino_hook.send_running(False)
        LOG.debug("Captured: %s", json.dumps(data, indent=2))
        sleep(POST_ANALYSIS)

    def _is_quitting(self) -> bool:
        return self._distance_sensor.trigger_off() or self._button.is_pressed()

    def _load_data(self):
        try:
            with open(DATA_PATH, encoding="utf-8") as file:
                self._data = json.load(file)
        except IOError:
            pass

    def _save(self):
        try:
            with open(DATA_PATH, "w+", encoding="utf-8") as file:
                file.write(json.dumps(self._data, indent=2))
        except FileNotFoundError:
            os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
            self._save()

    def _screen_task(self):
        while True:
            try:
                self._update_screen()
            except BaseException:
                traceback.print_exc()

    def _analyzer_task(self):
        while True:
            try:
                self._analyze()
            except BaseException:
                traceback.print_exc()

    def _save_data_task(self):
        while True:
            try:
                self._save()
            except BaseException:
                traceback.print_exc()
            sleep(DATA_SAVE_DELAY_SECONDS)


def main():
    # screen = CV2Screen("Screen", SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FREQUENCY)
    screen = NeoPixelScreen(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FREQUENCY, SCREEN_BRIGHTNESS, board.D12)

    # arduino_hook = ArduinoHookMock()
    arduino_hook = ArduinoHook(ARDUINO_PORT)

    Luzia(screen, arduino_hook).start()


if __name__ == "__main__":
    main()
