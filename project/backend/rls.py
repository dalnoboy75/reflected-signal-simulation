from project.backend.muffler import Muffler
from project.backend.radiator import Radiator
from project.backend.receiver import Receiver
from project.backend.entity import Entity
from project.backend.lsm import get_lsm_description, get_mse
from project.backend.constants import pi

import numpy as np

##@package rls
#Contains class RLS
class RLS:
    """The class responsible for simulating the operation of the entire radar station."""
    __slots__ = ('receiver', 'radiator')
    velocity_measurements_amount = 10

    def __init__(self, coordinates: np.array, amplification_coefficient: float, fix_coefficient: float,
                 energy: float, impulse_count: int) -> None:
        """
        Initialization of the radar station.

        :param coordinates: Coordinates of the station.
        :param amplification_coefficient: Amplification coefficient of the receiver.
        :param fix_coefficient: Fix coefficient of the receiver.
        :param energy: Energy of the radiator.
        :param impulse_count: Number of impulses for the radiator.
        """
        self.receiver = Receiver(coordinates, amplification_coefficient, fix_coefficient)
        self.radiator = Radiator(coordinates, energy, impulse_count)

    def noise_signal(self, noise: float) -> None:
        """
        Squeezes the signal based on the given noise level.

        :param noise: Noise level.
        """
        power = self.receiver.power * noise
        self.receiver.modify_power(power)

    def calculate_distance(self, entity: Entity, noise: float) -> float:
        """
        Calculates the distance based on the received and radiated signal power.

        :param entity: The object to which the distance is calculated.
        :param noise: Noise level.
        :return: Calculated distance.
        """
        self.radiator.emit_signal()
        self.receiver.get_signal(entity, self.radiator.power, self.radiator.wave_length)
        self.noise_signal(noise)
        if self.receiver.power == 0 or self.radiator.power == 0:
            raise ValueError("Radiator power cannot be zero.")
        power_coefficient = self.radiator.power / self.receiver.power
        return ((power_coefficient * (
                self.receiver.amplification_coefficient ** 2) * entity.reflection_surface * self.radiator.wave_length ** 2) / (
                        64 * self.receiver.fix_coefficient * pi ** 3)) ** 0.25

    def _calculate_coordinate(self, entity: Entity, noise: float) -> float:
        """
        Calculates coordinates based on the predicted distance to the object.

        :param entity: The object to which the coordinates are calculated.
        :param noise: Noise level.
        :return: Calculated coordinates.
        """
        if np.linalg.norm(self.receiver.get_direction(entity)) == 0:
            raise ValueError("Direction vector cannot be zero.")
        unit_vector = self.receiver.get_direction(entity) / np.linalg.norm(self.receiver.get_direction(entity))

        return self.receiver.position + unit_vector * self.calculate_distance(entity, noise)

    def calculate_coordinate(self, entity: Entity, noise: float) -> np.array:
        """
        Calculates coordinates based on several measurements, taking an average value.

        :param entity: The object to which the coordinates are calculated.
        :param noise: Noise level.
        :return: Array of mean coordinates and coordinate errors.
        """
        coordinates = []
        for i in range(self.radiator.impulse_count):
            coordinates.append(self._calculate_coordinate(entity, noise))
        coordinates = np.array(coordinates)

        abscissa = coordinates[:, 0]
        ordinate = coordinates[:, 1]
        applicate = coordinates[:, 2]

        mean_coordinate = np.array([get_mse(abscissa).mean, get_mse(ordinate).mean, get_mse(applicate).mean])
        coordinate_error = np.array([get_mse(abscissa).error, get_mse(ordinate).error, get_mse(applicate).error])

        return np.array([mean_coordinate, coordinate_error])

    def calculate_velocity(self, entity: Entity, noise: float, dt: float) -> np.array:
        """
        Calculates the speed based on several measurements, taking an average value.

        :param entity: The object to which the velocity is calculated.
        :param noise: Noise level.
        :param dt: Time delta.
        :return: Array of velocities.
        """
        time = np.arange(1, self.velocity_measurements_amount + 1) * dt
        coordinates = []

        for i in range(self.velocity_measurements_amount):
            self.radiator.emit_signal()
            self.receiver.get_signal(entity, self.radiator.power, self.radiator.wave_length)
            coordinates.append(self.calculate_coordinate(entity, noise)[0])
            entity.update_position(dt)
        coordinates = np.array(coordinates)

        abscissa = get_lsm_description(time, coordinates[:, 0]).incline
        ordinate = get_lsm_description(time, coordinates[:, 1]).incline
        applicate = get_lsm_description(time, coordinates[:, 2]).incline

        return np.array([abscissa, ordinate, applicate])

    def testing_prediction_on_different_noise(self, muffler: Muffler, entity: Entity) -> list:
        """
        Tests the prediction accuracy on different noise levels.

        :param muffler: Muffler object for generating noise levels.
        :param entity: The object to which the prediction is tested.
        :return: List of generated noise levels and corresponding prediction errors.
        """
        noises = muffler.generate_noises_set()
        relative_error = []
        real_distance = self.receiver.calculate_distance(entity)

        for i in range(len(noises)):
            distance = self.calculate_distance(entity, noises[i])
            relative_error.append((distance / real_distance) * 100)
            noises[i] *= 100
        return [noises, relative_error]
