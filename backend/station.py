from models import Point


class Emitter:
    _power: float
    _amplification: float
    _direction: Point

    def __int__(self, power: float, amplification: float, direction: Point) -> None:
        self._power = power
        self._amplification = amplification
        self._direction = direction

    def set_power(self, power) -> None:
        self._power = power

    def get_power(self) -> float:
        return self._power

    def get_amplification(self) -> float:
        return self._amplification

    def get_direction(self) -> Point:
        return self._direction

    def set_direction(self, direction: Point) -> None:
        self._direction = direction

    def get_line(self) -> tuple:
        return (self._direction.y / self._direction.x, 1) if self._direction.x != 0 else (0, 1)


class Receiver:
    _amplification: float

    def __int__(self, amplification: float) -> None:
        self._amplification = amplification

    def get_amplification(self) -> float:
        return self._amplification


class Station:
    _position: Point
    emitter: Emitter
    receiver: Receiver

    def get_position(self) -> Point:
        return self._position

    def set_position(self, position: Point) -> None:
        self._position = position
