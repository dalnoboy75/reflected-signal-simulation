from backend.muffler import Muffler
from backend.radiator import Radiator
from backend.receiver import Receiver
from backend.entity import Entity
from backend.lsm import *
from backend.constants import *


class RLS:
    velocity_measurements_amount = 10

    def __init__(self, coordinates: np.array, amplification_coefficient: float, fix_coefficient: float,
                 energy: float, impulse_count: int) -> None:
        # Receiver
        self.receiver = Receiver(coordinates, amplification_coefficient, fix_coefficient)

        # Radiator
        self.radiator = Radiator(coordinates, energy, impulse_count)

    def calculate_distance(self, entity: Entity, muffler: Muffler) -> float:
        self.receiver.get_signal(entity, self.radiator.power, self.radiator.wave_length)
        muffler.noise_signal(self)
        power_coefficient = self.radiator.power / self.receiver.power
        return ((power_coefficient * (
                self.receiver.amplification_coefficient ** 2) * entity.reflection_surface * self.radiator.wave_length ** 2) / (
                        64 * self.receiver.fix_coefficient * pi ** 3)) ** 0.25

    def _calculate_coordinate(self, entity: Entity, muffler: Muffler, direction_vector: np.array) -> float:
        unit_vector = direction_vector / np.linalg.norm(direction_vector)
        return self.receiver.position + unit_vector * self.calculate_distance(entity, muffler)

    def calculate_coordinate(self, entity: Entity, direction_vector: np.array, muffler: Muffler) -> np.array:
        unit_vector = direction_vector / np.linalg.norm(direction_vector)
        coordinates = []
        for i in range(self.radiator.impulse_count):
            coordinates.append(self.radiator.position + unit_vector * self.calculate_distance(entity, muffler))
        coordinates = np.array(coordinates)

        abscissa = coordinates[:, 0]
        ordinate = coordinates[:, 1]
        applicate = coordinates[:, 2]

        mean_coordinate = np.array([get_mse(abscissa).mean, get_mse(ordinate).mean, get_mse(applicate).mean])
        coordinate_error = np.array([get_mse(abscissa).error, get_mse(ordinate).error, get_mse(applicate).error])

        return np.array([mean_coordinate, coordinate_error])

    def calculate_velocity(self, entity: Entity, direction_vector: np.array, muffler: Muffler,
                           dt: float) -> np.array:
        time = np.arange(1, self.velocity_measurements_amount + 1) * dt
        coordinates = []

        for i in range(self.velocity_measurements_amount):
            self.receiver.get_signal(entity, self.radiator.power, self.radiator.wave_length)
            coordinates.append(self.calculate_coordinate(entity, direction_vector, muffler)[0])
            entity.update_position(dt)
        coordinates = np.array(coordinates)
        abscissa = get_lsm_description(time, coordinates[:, 0]).incline
        ordinate = get_lsm_description(time, coordinates[:, 1]).incline
        applicate = get_lsm_description(time, coordinates[:, 2]).incline

        return np.array([abscissa, ordinate, applicate])
