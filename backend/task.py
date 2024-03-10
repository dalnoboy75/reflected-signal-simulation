import math

import matplotlib.pyplot as plt


class Interface:
    adopted_power: float
    emitter_power: float
    amplification_coefficient: float
    wavelength: float
    reflective_area: float
    damage_coefficient: float

    def __int__(self, adopted_power: float,
                emitter_power: float,
                amplification_coefficient: float,
                wavelength: float,
                reflective_area: float, damage_coefficient: float) -> None:
        self.adopted_power = adopted_power
        self.emitter_power = emitter_power
        self.amplification_coefficient = amplification_coefficient
        self.wavelength = wavelength
        self.reflective_area = reflective_area
        self.damage_coefficient = damage_coefficient

    def get_distance(self) -> float:
        numeral = self.emitter_power * self.reflective_area * (self.amplification_coefficient * self.wavelength) ** 2
        denominator = 48 * self.damage_coefficient * self.adopted_power * math.pi ** 3
        if denominator == 0 or denominator * numeral < 0:
            return None
        return (numeral / denominator) ** 0.25


class GraphData:
    _abscissa = []
    _ordinates = []

    def append_x(self, num: float) -> None:
        self._abscissa.append(num)

    def append_y(self, num: float) -> None:
        self._ordinates.append(num)

    def get_abscissa(self) -> list:
        return self._abscissa

    def get_ordinate(self) -> list:
        return self._ordinates


def draw_chart(lines: GraphData, path_to_save: str, abscissa_label: str):
    _, ax = plt.subplots(figsize=(16, 9))
    plt.plot(lines.get_abscissa(), lines.get_ordinate())
    plt.ylabel('distance')
    plt.xlabel(abscissa_label)
    ax.grid(True)
    plt.savefig(path_to_save)
