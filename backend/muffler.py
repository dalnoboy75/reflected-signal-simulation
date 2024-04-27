import random

class Muffler:
    def __init__(self, noise_percent):
        self.noise_percent = noise_percent

    def noise_mc(self, power):
        fraction = random.uniform(0, 1)
        noise = power * fraction * (self.noise_percent / 100.0)
        sign = random.randint(0, 1)
        if sign == 0:
            power += abs(noise)
        else:
            power -= abs(noise)
        return power