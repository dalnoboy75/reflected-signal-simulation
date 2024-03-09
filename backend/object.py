from backend.models import Point

class Object:
    def __init__(self, coordinate: Point, velocity: Point) -> None:
        self.coordinate = coordinate
        self.velocity = velocity

    def change_location(self) -> None:
        self.coordinate += self.velocity

    def change_velocity(self, new_velocity) -> None:
        self.velocity = new_velocity

    def get_location(self) -> Point:
        return self.coordinate
