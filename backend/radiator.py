from backend.constants import *
from backend.entity import Entity
import numpy as np


# A class responsible for simulating the signal source as well as its characteristics
class Radiator:

    def __init__(self, coordinates: np.array, energy: float, impulse_count: int) -> None:
        self._power = energy ** 2
        self._wave_length = speed_of_light * plank_constant / energy
        self._coordinates = coordinates
        self._energy = energy
        self._impulse_count = impulse_count

    # Function for calculating the distance between the source and the object
    def calculate_distance(self, entity: Entity) -> float:
        return np.linalg.norm(entity.position - self._coordinates)

    @property
    def power(self) -> float:
        return self._power

    @property
    def wave_length(self) -> float:
        return self._wave_length

    @property
    def position(self) -> np.array:
        return self._coordinates

    @property
    def impulse_count(self) -> int:
        return self._impulse_count

    def emit_signal(self) -> None:
        pass
