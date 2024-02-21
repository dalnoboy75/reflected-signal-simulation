class Object:
    def __init__(self, x: float, y: float, z: float, v: tuple) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.v = v

    def change_location(self) -> None:
        self.x += self.v[0]
        self.y += self.v[1]
        self.z += self.v[2]

    def change_velocity(self, new_v) -> None:
        self.v = new_v

    def get_location(self) -> tuple:
        return self.x, self.y, self.z
