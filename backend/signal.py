class Signal:
    def __init__(self, x: float, y: float, z: float, power: int, time: int, distance: int) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.pow = power
        self.time = time
        self.dis = distance

    def change_power(self, new_power) -> None:
        self.pow = new_power

    def get_vector(self) -> tuple:
        return self.x, self.y, self.z

    def change_vector(self, x: int, y: int, z: int):
        self.x += x
        self.y += y
        self.z += z

    def get_power(self) -> int:
        return self.pow

    def get_distance(self) -> int:
        return self.dis

    def change_dis(self, new_distance) -> None:
        self.dis = new_distance
