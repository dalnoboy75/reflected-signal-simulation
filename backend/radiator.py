from backend.constants import *
from backend.entity import Entity
import numpy as np


class Radiator:

    def __init__(self, coordinates: np.array, energy: float, impulse_count: int) -> None:
        self._power = energy ** 2
        self._wave_length = speed_of_light * plank_constant / energy
        self._coordinates = coordinates
        self._energy = energy
        self._impulse_count = impulse_count

    def calculate_distance(self, entity: Entity) -> float:
        return np.linalg.norm(entity.position - self._coordinates)

    @property
    def power(self):
        return self._power

    @property
    def wave_length(self):
        return self._wave_length

    @property
    def position(self):
        return self._coordinates

    @property
    def impulse_count(self):
        return self._impulse_count

    def emit_signal(self):
        pass
