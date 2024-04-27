import math


class Vector3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Object:
    def __init__(self, coordinates, radius_, refractive_index_, speed_vector_):
        self.effective_reflection_surface = None
        self.val_coordinates = coordinates
        self.radius = radius_
        self.refractive_index = refractive_index_
        self.speed_vector = speed_vector_

    def coordinates(self):
        return self.val_coordinates

    def set_effective_reflection_surface(self, receiver):
        R = distance(self, receiver)
        self.effective_reflection_surface = math.pi * self.radius * math.sqrt(4 * R ** 2 - self.radius ** 2)

    def update_position(self, dt):
        self.val_coordinates.x += self.speed_vector.x * dt
        self.val_coordinates.y += self.speed_vector.y * dt
        self.val_coordinates.z += self.speed_vector.z * dt

    def reflect(self, v_sign):
        for i in range(len(v_sign) - 1, -1, -1):
            if not self.can_collide(self.val_coordinates - v_sign[i].coordinates, v_sign[i].direction_vector):
                v_sign.pop(i)
            else:
                v_sign[i].change_direction(self)

def distance(object, receiver):
    return abs(object.val_coordinates - receiver.coordinates)


def dir_to_obj(object, receiver):
    return object.val_coordinates - receiver.coordinates
