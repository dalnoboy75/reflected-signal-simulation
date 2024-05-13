from random import uniform


class Muffler:
    def __init__(self, noise_share: float) -> None:
        self._noise_share = noise_share

    def generate_noise(self) -> float:
        distribution = uniform(-0.99, 1)
        return distribution * self._noise_share

    def generate_noises_set(self) -> list:
        noises = [(i * self._noise_share / 1000) for i in range(-999, 1000)]
        return noises
