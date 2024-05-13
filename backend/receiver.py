import numpy as np
from backend.entity import Entity
from backend.constants import *


# A class responsible for simulating the operation of the signal receiver as well as its characteristics
class Receiver:

    def __init__(self, coordinates: np.array, amplification_coefficient: float, fix_coefficient: float) -> None:
        self._coordinates = coordinates
        self._amplification_coefficient = amplification_coefficient
        self._fix_coefficient = fix_coefficient
        self._power = 0

    @property
    def position(self) -> np.array:
        return self._coordinates

    @property
    def amplification_coefficient(self) -> float:
        return self._amplification_coefficient

    @property
    def fix_coefficient(self) -> float:
        return self._fix_coefficient

    @property
    def power(self) -> float:
        return self._power

    # Function calculating the direction vector from the receiver to the object
    def get_direction(self, entity: Entity) -> np.array:
        return entity.position - self._coordinates

    def modify_power(self, power: float) -> None:
        self._power += power

    # Function for calculating the distance between the receiver and the object
    def calculate_distance(self, entity: Entity) -> float:
        return np.linalg.norm(entity.position - self._coordinates)

    # Function that simulates receiver operation and calculates power based on the estimated received signal
    def get_signal(self, entity: Entity, radiated_power: float, wave_length: float) -> None:
        distance = self.calculate_distance(entity)
        self._power = ((radiated_power * self._amplification_coefficient) / (
                4 * pi * distance ** 2)) * (entity.reflection_surface / (4 * pi * distance ** 2)) * (
                              (self._amplification_coefficient * wave_length ** 2) / (4 * pi)) * (
                              1 / self._fix_coefficient)
