class Point:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        if isinstance(self,other):
            self.x += other.x
            self.y += other.y
            self.z += other.z

