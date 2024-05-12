from math import pi

import numpy as np

from entity import Entity
from muffler import Muffler
from lsm import *

speed_of_light = 299792458
plank_constant = 6.626 * (10 ** -34)


class RLS:
    base_distribution_share = 1
    base_measurements_amount = 25
    velocity_measurements_amount = 10

    def __init__(self, coordinates: np.array, amplification_coefficient: float, fix_coefficient: float,
                 energy: float) -> None:
        # Receiver
        self._coordinates = coordinates
        self._radiated_power = 0
        self._received_power = 0
        self._fix_coefficient = fix_coefficient
        self._wave_length = speed_of_light * plank_constant / energy
        self._reflective_surface = 0
        self._amplification_coefficient = amplification_coefficient

        # Radiator
        self._base_energy = energy
        self._current_energy = energy
        self._distribution = self.base_distribution_share
        self._number_of_measurements = self.base_measurements_amount
        self._current_percent = 0

    def get_reflective_surface(self):
        return self._reflective_surface

    def get_wave_length(self):
        return self._wave_length

    def reset_energy(self) -> None:
        self._current_energy = self._base_energy
        speed_of_light * plank_constant / self._current_energy

    def calculate_distance(self, entity: Entity) -> float:
        return np.linalg.norm(entity.get_position() - self._coordinates)

    def get_direction_to_entity(self, entity: Entity) -> np.array:
        return entity.get_position() - self._coordinates

    def emit_signal(self, entity: Entity) -> None:
        distance = self.calculate_distance(entity)
        self._received_power = (((self._current_energy ** 2) * self._amplification_coefficient) / (
                4 * pi * distance ** 2)) * ((entity.get_reflection_surface()) / (4 * pi * distance ** 2)) * (
                                       (self._amplification_coefficient * self._wave_length ** 2) / (4 * pi)) * (
                                       1 / self._fix_coefficient)
        self._reflective_surface = entity.get_reflection_surface()
        self._radiated_power = self._current_energy ** 2

        increase = self._distribution / self._number_of_measurements
        self._current_energy += increase * self._base_energy
        self._wave_length = (speed_of_light * plank_constant) / self._current_energy

    def get_received_power(self) -> float:
        return self._received_power

    def update_received_power(self, power: float) -> None:
        self._received_power += power

    def calculate_distance_with_noise(self, entity: Entity, muffler: Muffler) -> float:
        self.emit_signal(entity)
        muffler.noise_signal(self)
        power_coefficient = self._radiated_power / self._received_power
        return ((power_coefficient * (
                self._amplification_coefficient ** 2) * self._reflective_surface * self._wave_length ** 2) / (
                        64 * self._fix_coefficient * pi ** 3)) ** 0.25

    def calculate_coordinate_with_noise(self, entity: Entity, muffler: Muffler, direction_vector: np.array) -> float:
        unit_vector = direction_vector / np.linalg.norm(direction_vector)
        return self._coordinates + unit_vector * self.calculate_distance_with_noise(entity, muffler)

    def calculate_coordinates_with_mse(self, entity: Entity, direction_vector: np.array, muffler: Muffler) -> np.array:
        unit_vector = direction_vector / np.linalg.norm(direction_vector)
        coordinates = np.array([])
        for i in range(self._number_of_measurements):
            coordinates = np.append(coordinates,
                                    self._coordinates + unit_vector * self.calculate_distance_with_noise(entity,
                                                                                                         muffler))

        abscissa = coordinates[:, 0]
        ordinate = coordinates[:, 1]
        applicate = coordinates[:, 2]

        mean_coordinates = np.array([get_mse(abscissa).mean, get_mse(ordinate).mean, get_mse(applicate).mean])
        coordinates_error = np.array([get_mse(abscissa).error, get_mse(ordinate).error, get_mse(applicate).error])
        self.reset_energy()

        return np.array(mean_coordinates, coordinates_error)

    def calculate_velocity_with_lsm(self, entity: Entity, direction_vector: np.array, muffler: Muffler,
                                    dt: float) -> np.array:
        time = np.arange(1, self.velocity_measurements_amount + 1) * dt
        coordinates = np.array([])

        for i in range(self.velocity_measurements_amount):
            self.emit_signal(entity)
            coordinates = np.append(coordinates, self.calculate_coordinates_with_mse(entity, direction_vector, muffler))
            entity.update_position(dt)

        abscissa = get_lsm_description(time, coordinates[:, 0]).incline
        ordinate = get_lsm_description(time, coordinates[:, 1]).incline
        applicate = get_lsm_description(time, coordinates[:, 2]).incline

        return np.array([abscissa, ordinate, applicate])
