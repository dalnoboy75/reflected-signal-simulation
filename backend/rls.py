from backend.muffler import Muffler
from backend.radiator import Radiator
from backend.receiver import Receiver
from backend.entity import Entity
from backend.lsm import *
from backend.constants import *


# The class responsible for simulating the operation of the entire radar station.
# It connects the receiver and the signal source, as well as calculates all the required values here
class RLS:
    velocity_measurements_amount = 10

    def __init__(self, coordinates: np.array, amplification_coefficient: float, fix_coefficient: float,
                 energy: float, impulse_count: int) -> None:
        # Receiver
        self.receiver = Receiver(coordinates, amplification_coefficient, fix_coefficient)

        # Radiator
        self.radiator = Radiator(coordinates, energy, impulse_count)

    # A function that squelches the signal
    def noise_signal(self, noise: float):
        power = self.receiver.power * noise
        self.receiver.modify_power(power)

    # Function that calculates the distance based on the received and radiated signal power
    def calculate_distance(self, entity: Entity, noise) -> float:
        self.radiator.emit_signal()
        self.receiver.get_signal(entity, self.radiator.power, self.radiator.wave_length)
        self.noise_signal(noise)
        power_coefficient = self.radiator.power / self.receiver.power
        return ((power_coefficient * (
                self.receiver.amplification_coefficient ** 2) * entity.reflection_surface * self.radiator.wave_length ** 2) / (
                        64 * self.receiver.fix_coefficient * pi ** 3)) ** 0.25

    # Function that calculates coordinates based on the predicted distance to the object
    def _calculate_coordinate(self, entity: Entity, noise: float, direction_vector: np.array) -> float:
        unit_vector = direction_vector / np.linalg.norm(direction_vector)
        return self.receiver.position + unit_vector * self.calculate_distance(entity, noise)

    # A function that calculates coordinates based on several measurements, it takes an average value
    def calculate_coordinate(self, entity: Entity, direction_vector: np.array, noise: float) -> np.array:
        coordinates = []
        for i in range(self.radiator.impulse_count):
            coordinates.append(self._calculate_coordinate(entity, direction_vector, noise))
        coordinates = np.array(coordinates)

        abscissa = coordinates[:, 0]
        ordinate = coordinates[:, 1]
        applicate = coordinates[:, 2]

        mean_coordinate = np.array([get_mse(abscissa).mean, get_mse(ordinate).mean, get_mse(applicate).mean])
        coordinate_error = np.array([get_mse(abscissa).error, get_mse(ordinate).error, get_mse(applicate).error])

        return np.array([mean_coordinate, coordinate_error])

    # A function that calculates the speed based on several measurements, it takes an average value
    def calculate_velocity(self, entity: Entity, direction_vector: np.array, noise: float, dt: float) -> np.array:
        time = np.arange(1, self.velocity_measurements_amount + 1) * dt
        coordinates = []

        for i in range(self.velocity_measurements_amount):
            self.radiator.emit_signal()
            self.receiver.get_signal(entity, self.radiator.power, self.radiator.wave_length)
            coordinates.append(self.calculate_coordinate(entity, direction_vector, noise)[0])
            entity.update_position(dt)
        coordinates = np.array(coordinates)
        abscissa = get_lsm_description(time, coordinates[:, 0]).incline
        ordinate = get_lsm_description(time, coordinates[:, 1]).incline
        applicate = get_lsm_description(time, coordinates[:, 2]).incline

        return np.array([abscissa, ordinate, applicate])

    # Auxiliary function for plotting the dependence of distance prediction accuracy on noise
    def testing_prediction_on_different_noise(self, muffler: Muffler, enity: Entity) -> list:
        noises = muffler.generate_noises_set()
        predict_distances_error = []
        real_distance = self.receiver.calculate_distance(enity)

        for i in range(len(noises)):
            distance = self.calculate_distance(enity, noises[i])
            predict_distances_error.append((min(distance, real_distance) / max(distance, real_distance)) * 100)
            noises[i] *= 100
        return [noises, predict_distances_error]
