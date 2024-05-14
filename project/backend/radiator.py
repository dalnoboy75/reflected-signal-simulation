from project.backend.entity import Entity
import numpy as np
from project.backend.constants import speed_of_light, plank_constant

## @package radiator
# Contains class Radiator
class Radiator:
    """Class for simulating the signal source and its characteristics."""
    __slots__ = ('_power', '_wave_length', '_coordinates', '_energy', '_impulse_count')

    def __init__(self, coordinates: np.array, energy: float, impulse_count: int) -> None:
        """
        Initialization of the signal source.

        :param coordinates: Coordinates of the signal source.
        :param energy: Energy of the signal source.
        :param impulse_count: Number of impulses.
        """
        self._power = energy ** 2
        self._wave_length = speed_of_light * plank_constant / energy
        self._coordinates = coordinates
        self._energy = energy
        self._impulse_count = impulse_count

    def calculate_distance(self, entity: Entity) -> float:
        """
        Calculation of the distance between the signal source and the object.

        :param entity: The object to which the distance is calculated.
        :return: Distance between the signal source and the object.
        """
        return np.linalg.norm(entity.position - self._coordinates)

    @property
    def power(self) -> float:
        """Returns the power of the signal source."""
        return self._power

    @property
    def wave_length(self) -> float:
        """Returns the wavelength of the signal source."""
        return self._wave_length

    @property
    def position(self) -> np.array:
        """Returns the coordinates of the signal source."""
        return self._coordinates

    @property
    def impulse_count(self) -> int:
        """Returns the number of impulses of the signal source."""
        return self._impulse_count

    def emit_signal(self) -> None:
        """Method for emitting the signal."""
        pass
