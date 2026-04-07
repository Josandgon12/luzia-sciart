from abc import ABC, abstractmethod

from arduino_hook import ArduinoHook


#
# BUTTON
#

class Button(ABC):

    @abstractmethod
    def is_pressed(self):
        return False


class ArduinoButton(Button):

    def __init__(self, arduino_hook: ArduinoHook):
        self.arduino_hook = arduino_hook

    def is_pressed(self):
        return self.arduino_hook.button


#
# DISTANCE SENSOR
#

class DistanceSensor(ABC):

    def __init__(self, distance: int):
        self.distance = distance

    @abstractmethod
    def trigger(self) -> bool:
        return False


class ArduinoDistanceSensor(DistanceSensor):

    def __init__(self, distance: int, arduino_hook: ArduinoHook):
        super().__init__(distance)
        self.arduino_hook = arduino_hook

    def trigger(self) -> bool:
        return all(distance <= self.distance for distance in self.arduino_hook.distance_log)

    def trigger_off(self) -> bool:
        return all(distance > self.distance for distance in self.arduino_hook.distance_log)
