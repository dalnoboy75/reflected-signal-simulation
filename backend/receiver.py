import numpy as np
from backend.entity import Entity
from backend.constants import *


class Receiver:

    def __init__(self, coordinates: np.array, amplification_coefficient: float, fix_coefficient: float) -> None:
        self._coordinates = coordinates
        self._amplification_coefficient = amplification_coefficient
        self._fix_coefficient = fix_coefficient
        self._power = 0

    @property
    def position(self):
        return self._coordinates

    @property
    def amplification_coefficient(self):
        return self._amplification_coefficient

    @property
    def fix_coefficient(self):
        return self._fix_coefficient

    @property
    def power(self):
        return self._power

    def get_direction(self, entity: Entity) -> np.array:
        return np.linalg.norm(entity.position - self._coordinates)

    def modify_power(self, power: float) -> None:
        self._power += power

    def calculate_distance(self, entity: Entity) -> float:
        return np.linalg.norm(entity.position - self._coordinates)

    def get_signal(self, entity: Entity, radiated_power: float, wave_length: float):
        distance = self.calculate_distance(entity)
        self._power = ((radiated_power * self._amplification_coefficient) / (
                4 * pi * distance ** 2)) * (entity.reflection_surface / (4 * pi * distance ** 2)) * ((
                                                                                                             self._amplification_coefficient * wave_length ** 2) / (
                                                                                                             4 * pi)) * (
                              1 / self._fix_coefficient)
