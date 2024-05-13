import numpy as np
from backend.constants import pi


class Entity:
    def __init__(self, coordinates: np.array, radius: float, velocity: np.array) -> None:
        self._coordinates = coordinates
        self._radius = radius
        self._velocity = velocity
        self._reflection_surface = 2 * pi * radius ** 2

    @property
    def position(self) -> np.array:
        return self._coordinates

    def update_position(self, dt: float) -> None:
        self._coordinates += self._velocity * dt

    @property
    def reflection_surface(self):
        return self._reflection_surface
