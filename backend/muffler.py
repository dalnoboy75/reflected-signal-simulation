import random

from rls import RLS


class Muffler:
    def __init__(self, noise_share: float) -> None:
        self._noise_share = noise_share

    def noise_signal(self, rls: RLS) -> None:
        distribution = random.uniform(-1, 1)
        noise = rls.get_received_power() * distribution * self._noise_share
        rls.update_received_power(noise)
