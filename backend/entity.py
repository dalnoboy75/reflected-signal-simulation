import numpy as np
from rls import RLS
from math import pi, sqrt


class Entity:
    def __init__(self, coordinates: np.array, radius: float, velocity: np.array) -> None:
        self._coordinates = coordinates
        self._radius = radius
        self._velocity = velocity
        self._reflection_surface = None

    def get_position(self) -> np.array:
        return self._coordinates

    def set_reflection_surface(self, rls: RLS) -> None:
        distance = rls.calculate_distance(self)
        self._reflection_surface = pi * self._radius * sqrt(4 * distance ** 2 - self._radius ** 2)

    def update_position(self, dt: float) -> None:
        self._coordinates += self._velocity * dt

    def get_reflection_surface(self):
        return self._reflection_surface





