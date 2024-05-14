from random import uniform

##@package muffler
class Muffler:
    """Class for simulating the signal attenuator and its characteristics."""
    __slots__ = ('_noise_share',)

    def __init__(self, noise_share: float) -> None:
        """
        Initialization of the signal attenuator.

        :param noise_share: Share of noise in the signal.
        """
        self._noise_share = noise_share

    def generate_noise(self) -> float:
        """
        Generates a single noise value based on the noise share.

        :return: A single noise value.
        """
        distribution = uniform(-1, 1)
        return distribution * self._noise_share

    def generate_noises_set(self) -> list:
        """
        Generates a set of noise values based on the noise share.

        :return: A list of noise values.
        """
        noises = [(i * self._noise_share / 1000) for i in range(-1000, 1000)]
        return noises
