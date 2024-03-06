from backend.models import Point
from backend.station import Station
from backend.object import Object

station = Station()
positions = [Point(1, 2, 0), Point(5, 5, 0), Point(7, 2, 0)]

object = Object(positions[0], Point(1, 1, 0))

signal_direction = Point(1, 1, 0)

station.set_position(Point(0, 0, 0))
station.emitter.set_direction(signal_direction)

line = station.emitter.get_line()

for i in range(1, len(positions)):
    if positions[i].x*line[0] == line[1]:
        print("yes", positions[i].x, positions[i].y)
    else:
        print("no")

