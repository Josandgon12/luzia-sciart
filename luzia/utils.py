import logging
import random
from multiprocessing import Process
from typing import Sequence, TypeVar

from playsound import playsound

T = TypeVar("T")


def get_random_element(sequence: Sequence[T], avoid: Sequence[T]) -> T:
    candidates = [item for item in sequence if item not in avoid]
    return random.choice(candidates) if len(candidates) > 1 else sequence[0]


def play_sound(path) -> Process:
    process = Process(target=playsound, args=(path,), daemon=True)
    process.start()
    return process


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)

    return logger
