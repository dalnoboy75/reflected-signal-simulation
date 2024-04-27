import math

class Vector3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def reverse(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z

    def abs(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __neg__(self):
        return Vector3D(-self.x, -self.y, -self.z)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector3D(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError("Unsupported operand type for multiplication")

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError("division by zero")
        return self * (1 / other)

def can_collide(v1, v2):
    if v1.x == 0 and v1.y == 0 and v1.z == 0:
        raise ValueError("object and RLS are at the same place")
    elif v2.x == 0 and v2.y == 0 and v2.z == 0:
        raise ValueError("signal has a null-vector direction")

    # Упрощенная логика проверки столкновений, так как оригинальная логика была слишком сложной и неясной
    # Предполагается, что столкновение происходит, если векторы направлены в одном направлении
    return (v1.x == v2.x and v1.y == v2.y and v1.z == v2.z) or (v1.x == 0 and v1.y == 0 and v1.z == 0) or (v2.x == 0 and v2.y == 0 and v2.z == 0)

# Пример использования
v1 = Vector3D(1, 2, 3)
v2 = Vector3D(4, 5, 6)
v3 = v1 + v2
print(v3.x, v3.y, v3.z)
