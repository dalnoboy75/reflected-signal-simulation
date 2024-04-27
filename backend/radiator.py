import math

class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Signal:
    def __init__(self, coordinates, direction_vector, energy):
        self.coordinates = coordinates
        self.direction_vector = direction_vector
        self.energy = energy

class Receiver:
    def receive_signals(self, total_energy, received_power, L, wave_length, sigma, amplification_coefficient):
        pass # Реализация метода

class Object:
    def sigma(self):
        pass # Реализация метода

class Radiator:
    def __init__(self, energy, coordinates, direction_vector, L, amplification_coefficient):
        self.base_energy = energy
        self.current_energy = energy
        self.coordinates = coordinates
        self.direction_vector = direction_vector
        self.wave_length = (speed_of_light * plank_constant) / energy
        self.L = L
        self.amplification_coefficient = amplification_coefficient

    def emit_signal(self, signal_vector):
        signal_vector.append(Signal(self.coordinates, self.direction_vector, self.current_energy))

    def emit_signal(self, receiver, object):
        R = self.distance(object, receiver)

        member_1 = (self.current_energy * self.current_energy * self.amplification_coefficient) / (4 * math.pi * R * R)
        member_2 = (object.sigma()) / (4 * math.pi * R * R)
        member_3 = (self.amplification_coefficient * self.wave_length * self.wave_length) / (4 * math.pi)
        member_4 = 1 / self.L

        received_power = member_1 * member_2 * member_3 * member_4

        receiver.receive_signals(self.current_energy * self.current_energy, received_power, self.L, self.wave_length, object.sigma(), self.amplification_coefficient)

        increase = distribution / number_of_measurements / 100
        self.current_energy += increase * self.base_energy
        self.wave_length = (speed_of_light * plank_constant) / self.current_energy

    def reset_energy(self):
        self.current_energy = self.base_energy
        self.wave_length = (speed_of_light * plank_constant) / self.current_energy

    def distance(object, receiver):
        return abs(object.val_coordinates - receiver.coordinates)

# Глобальные константы
speed_of_light = 299792458 # m/s
plank_constant = 6.62607015e-34 # Js
distribution = 0 # Пример значения, замените на реальное
number_of_measurements = 0 # Пример значения, замените на реальное
