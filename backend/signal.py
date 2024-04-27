from vector3d import Vector3D
from object import Object

class Signal:
    def __init__(self, coordinates, starting_direction_vector, energy):
        self.coordinates = coordinates
        self.direction_vector = starting_direction_vector
        self.energy = energy
        self.passed_time = 0
        self.wave_length = (speed_of_light * plank_constant) / energy

    def change_direction(self, obj):
        self.passed_time += ((obj.coordinates - self.coordinates).abs()) / speed_of_light
        self.coordinates = obj.coordinates
        self.direction_vector.reverse()
