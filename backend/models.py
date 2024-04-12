from math import sqrt


class Point:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"

    def __repr__(self):
        return self.__str__()

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __neg__(self):
        p = Point(-self.x, -self.y, -self.z)
        return p

    def __sub__(self, other):
        return self.__add__(other.__neg__())

    def __rsub__(self, other):
        return self.__sub__(other)
