import numpy as np
from project.backend.constants import pi

##@package entity
# Contains class Entity
class Entity:
    """The class responsible for simulation of the object, its characteristics and behavior."""
    __slots__ = ('_coordinates', '_radius', '_velocity', '_reflection_surface')

    def __init__(self, coordinates: np.array, radius: float, velocity: np.array) -> None:
        """
        Initialization of the object.

        :param coordinates: Initial coordinates of the object.
        :param radius: Radius of the object.
        :param velocity: Velocity vector of the object.
        """
        self._coordinates = coordinates
        self._radius = radius
        self._velocity = velocity
        self._reflection_surface = 2 * pi * radius ** 2

    @property
    def position(self) -> np.array:
        """Returns the current coordinates of the object."""
        return self._coordinates

    def update_position(self, dt: float) -> None:
        """
        Updates the position of the object based on its velocity and time delta.

        :param dt: Time delta for updating the position.
        """
        self._coordinates += self._velocity * dt

    @property
    def reflection_surface(self) -> float:
        """Returns the reflection surface area of the object."""
        return self._reflection_surface
