class Point:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y, self.z + other.z)
    def __mul__(self, other):
        return Point(self.x*other, self.y*other, self.z*other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"
    def __repr__(self):
        return self.__str__()

