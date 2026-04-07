import traceback
from threading import Thread, Lock

from serial import Serial

from utils import get_logger

DISTANCE_MAX_LOG = 4

LOG = get_logger("ArduinoHook")


class ArduinoHook:
    distance_log = [200 for _ in range(DISTANCE_MAX_LOG)]
    button = False
    _lock = Lock()

    def __init__(self, port: str, baud_rate: int = 9600):
        self.channel = Serial(port, baud_rate)
        self.thread = Thread(target=self._task, daemon=True)

    def start(self):
        self.thread.start()

    def send_running(self, running: bool):
        with self._lock:
            self.channel.write(b'1' if running else b'0')
            LOG.debug("Sent running: %s", running)

    def _task(self):
        while True:
            try:
                with self._lock:
                    incoming = str(self.channel.readline())[2:-5]

                if not incoming:
                    continue

                incoming = incoming.split(",")
                distance = int(incoming[0])

                self.distance_log.pop(0)
                self.distance_log.append(distance)
                self.button = incoming[1] == "1"

                if distance < 100:
                    LOG.debug("Incoming message: %s,%s", incoming[0], incoming[1])
            except BaseException:
                traceback.print_exc()


class ArduinoHookMock(ArduinoHook):
    distance_log = [10 for _ in range(DISTANCE_MAX_LOG)]

    def __init__(self):
        pass

    def start(self):
        pass

    def send_running(self, running: bool):
        LOG.debug("Sent running: %s", running)

