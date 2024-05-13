import numpy as np


class LSMDescription:

    def __init__(self, incline: float, shift: float) -> None:
        self.incline = incline
        self.shift = shift


class MSEDescription:
    def __init__(self, mean: float, error: float) -> None:
        self.mean = mean
        self.error = error


# LSM calculation function
def get_lsm_description(abscissa: np.array, ordinates: np.array) -> LSMDescription:
    avr_x = np.mean(abscissa)
    avr_y = np.mean(ordinates)
    avr_xy = np.mean(abscissa * ordinates)
    avr_x2 = np.mean(abscissa ** 2)
    incline = (avr_xy - avr_x * avr_y) / (avr_x2 - avr_x ** 2)
    shift = avr_y - incline * avr_x
    return LSMDescription(incline, shift)


# MSE calculation function
def get_mse(measurements: np.array) -> MSEDescription:
    mean = np.mean(measurements)
    error = np.mean((measurements - mean) ** 2)
    return MSEDescription(mean, error)
