import numpy as np
from backend.entity import Entity
from backend.constants import pi


class Receiver:
    """Class for simulating the operation of the signal receiver and its characteristics."""
    __slots__ = ('_coordinates', '_amplification_coefficient', '_fix_coefficient', '_power')

    def __init__(self, coordinates: np.array, amplification_coefficient: float, fix_coefficient: float) -> None:
        """
        Initialization of the signal receiver.

        :param coordinates: Coordinates of the receiver.
        :param amplification_coefficient: Amplification coefficient of the receiver.
        :param fix_coefficient: Fix coefficient of the receiver.
        """
        self._coordinates = coordinates
        self._amplification_coefficient = amplification_coefficient
        self._fix_coefficient = fix_coefficient
        self._power = 0

    @property
    def position(self) -> np.array:
        """Returns the coordinates of the receiver."""
        return self._coordinates

    @property
    def amplification_coefficient(self) -> float:
        """Returns the amplification coefficient of the receiver."""
        return self._amplification_coefficient

    @property
    def fix_coefficient(self) -> float:
        """Returns the fix coefficient of the receiver."""
        return self._fix_coefficient

    @property
    def power(self) -> float:
        """Returns the current power of the receiver."""
        return self._power

    def get_direction(self, entity: Entity) -> np.array:
        """
        Calculates the direction vector from the receiver to the object.

        :param entity: The object to which the direction is calculated.
        :return: Direction vector from the receiver to the object.
        """
        return entity.position - self._coordinates

    def modify_power(self, power: float) -> None:
        """Modifies the current power of the receiver."""
        self._power += power

    def calculate_distance(self, entity: Entity) -> float:
        """
        Calculates the distance between the receiver and the object.

        :param entity: The object to which the distance is calculated.
        :return: Distance between the receiver and the object.
        """
        return np.linalg.norm(entity.position - self._coordinates)

    def get_signal(self, entity: Entity, radiated_power: float, wave_length: float) -> None:
        """
        Simulates receiver operation and calculates power based on the estimated received signal.

        :param entity: The object from which the signal is received.
        :param radiated_power: Power of the radiated signal.
        :param wave_length: Wavelength of the radiated signal.
        """
        distance = self.calculate_distance(entity)
        self._power = ((radiated_power * self._amplification_coefficient) / (
                4 * pi * distance ** 2)) * (entity.reflection_surface / (4 * pi * distance ** 2)) * (
                              (self._amplification_coefficient * wave_length ** 2) / (4 * pi)) * (
                              1 / self._fix_coefficient)
