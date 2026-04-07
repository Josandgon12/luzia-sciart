from collections import defaultdict, Counter
from datetime import datetime
from typing import List, Callable

from deepface import DeepFace

import age_and_gender


class Analyzer:

    def __init__(self, camera, capture_seconds=10, sleep_seconds=3):
        self.camera = camera
        self.capture_seconds = capture_seconds
        self.sleep_seconds = sleep_seconds

    def analyze(self, stop: Callable[[], bool]):  # -> dict | None
        captures = []

        start = datetime.now()
        while (datetime.now() - start).total_seconds() < self.capture_seconds:
            if stop():
                return None

            try:
                captures.append(self._analyze_single_frame())
            except ValueError:
                pass

        return _calculate_average(captures)

    def _analyze_single_frame(self) -> dict:
        captured, image = self.camera.read()

        if not captured:
            raise ValueError("camera not working")

        result = DeepFace.analyze(image, actions=("emotion",))[0]
        result.update(age_and_gender.analyze(image))
        return result


def _calculate_average(captures: List[dict]):  # -> dict | None
    if not captures:
        return None

    average = {}
    for capture in captures:
        for characteristic, values in capture.items():
            _add_characteristic(average, characteristic, values)

    for characteristic, values in average.items():
        if characteristic == "emotion":
            for key, value in values.items():
                values[key] = value / len(captures)
        else:
            average[characteristic] = Counter(values).most_common()[0][0]

    return average


def _add_characteristic(average, characteristic, values) -> None:
    if characteristic == "region":
        return

    elif characteristic == "emotion":
        for key, value in values.items():
            if characteristic not in average:
                average[characteristic] = defaultdict(int)
            average[characteristic][key] += value

    else:
        if characteristic not in average:
            average[characteristic] = []
        average[characteristic].append(values)
