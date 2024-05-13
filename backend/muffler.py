from random import uniform


class Muffler:
    def __init__(self, noise_share: float) -> None:
        self._noise_share = noise_share

    def noise_signal(self, rls) -> None:
        from backend.rls import RLS
        distribution = uniform(-1, 1)
        power = rls.receiver.power * distribution * self._noise_share
        rls.receiver.modify_power(power)
