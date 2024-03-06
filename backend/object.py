from models import Point


class Object:
    def __init__(self, coordinate: Point, velocity: Point) -> None:
        self.coordinate = coordinate
        self.velocity = velocity

    def change_location(self, new_cord) -> None:
        self.coordinate = new_cord

    def change_velocity(self, new_velocity) -> None:
        self.velocity = new_velocity

    def get_location(self) -> Point:
        return self.coordinate
