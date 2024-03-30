from backend.models import Point


class Object:
    def __init__(self, coordinate: Point, velocity: Point) -> None:
        self.coordinate = coordinate
        self.velocity = velocity

    def change_location(self) -> None:
        self.coordinate += self.velocity

    def change_velocity(self, new_velocity) -> None:
        self.velocity = new_velocity

    def get_location_at_time(self, time, time_step=1) -> list:
        coords = list()
        ind = 1
        coords.append(self.coordinate)
        for i in range(time_step, time + 1, time_step):
            coords.append(coords[ind - 1] + self.velocity * time_step)
            ind += 1
        return coords

    def get_location(self) -> Point:
        return self.coordinate
