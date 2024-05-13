import numpy as np


class LSMDescription:
    """Class for storing Least Squares Method description."""
    __slots__ = ('incline', 'shift')

    def __init__(self, incline: float, shift: float) -> None:
        self.incline = incline
        self.shift = shift


class MSEDescription:
    """Class for storing Mean Squared Error description."""
    __slots__ = ('mean', 'error')

    def __init__(self, mean: float, error: float) -> None:
        self.mean = mean
        self.error = error


def get_lsm_description(abscissa: np.array, ordinates: np.array) -> LSMDescription:
    """
    Calculate LSM (Least Squares Method) description.

    :param abscissa: Array of x-coordinates.
    :param ordinates: Array of y-coordinates.
    :return: LSMDescription object with incline and shift.
    """
    avr_x = np.average(abscissa)
    avr_y = np.average(ordinates)
    avr_xy = np.average(abscissa * ordinates)
    avr_x2 = np.average(abscissa ** 2)
    incline = (avr_xy - avr_x * avr_y) / (avr_x2 - avr_x ** 2)
    shift = avr_y - incline * avr_x
    return LSMDescription(incline, shift)


def get_mse(measurements: np.array) -> MSEDescription:
    """
    Calculate MSE (Mean Squared Error) description.

    :param measurements: Array of measurements.
    :return: MSEDescription object with mean and error.
    """
    mean = np.average(measurements)
    error = np.average((measurements - mean) ** 2)
    return MSEDescription(mean, error)
