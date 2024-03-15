import math

import matplotlib.pyplot as plt

class Interfaces:
    initial_phase_of_the_received_pulse: float
    initial_frequency: float
    wavelength_of_the_emitted_signal: float
    radial_velocity_of_the_target: float
    intermediate_frequency_of_the_receiver: float
    amplitude: float
    frequency_deviation: float
    pulse_duration: float

    def __int__(self, initial_phase_of_the_received_pulse: float,
                initial_frequency: float,
                wavelength_of_the_emitted_signal: float,
                radial_velocity_of_the_target: float, intermediate_frequency_of_the_receiver: float,
                amplitude: float, frequency_deviation: float, pulse_duration: float) -> None:
        self.initial_phase_of_the_received_pulse = initial_phase_of_the_received_pulse
        self.initial_frequency = initial_frequency
        self.wavelength_of_the_emitted_signal = wavelength_of_the_emitted_signal
        self.radial_velocity_of_the_target = radial_velocity_of_the_target
        self.intermediate_frequency_of_the_receiver = intermediate_frequency_of_the_receiver
        self.amplitude = amplitude
        self.frequency_deviation = frequency_deviation
        self.pulse_duration = pulse_duration

    def __int__(self, initial_phase_of_the_received_pulse: float,
                initial_frequency: float,
                wavelength_of_the_emitted_signal: float,
                radial_velocity_of_the_target: float, intermediate_frequency_of_the_receiver: float,
                amplitude: float) -> None:
        self.initial_phase_of_the_received_pulse = initial_phase_of_the_received_pulse
        self.initial_frequency = initial_frequency
        self.wavelength_of_the_emitted_signal = wavelength_of_the_emitted_signal
        self.radial_velocity_of_the_target = radial_velocity_of_the_target
        self.intermediate_frequency_of_the_receiver = intermediate_frequency_of_the_receiver
        self.amplitude = amplitude

    def get_frequency_1(self, time: float) -> float:
        function = self.intermediate_frequency_of_the_receiver + ((2 * self.initial_frequency * self.radial_velocity_of_the_target) / (self.wavelength_of_the_emitted_signal))
        frequency = self.amplitude * math.cos(4 * math.pi * function * time + self.initial_phase_of_the_received_pulse)
        return frequency
    
    def get_frequency_2(self, time: float) -> float:
        frequency = self.intermediate_frequency_of_the_receiver + self.frequency_deviation + (self.frequency_deviation / self.pulse_duration) * time + 2 * (self.radial_velocity_of_the_target / 299792458) * (self.initial_frequency - self.frequency_deviation + (self.frequency_deviation / self.pulse_duration) * time)
        return frequency 


class GraphDate:
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

class GraphDate_2:
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

def drawchart(lines: GraphDate, path_to_save: str):
    _, ax = plt.subplots(figsize=(16, 9))
    plt.plot(lines.get_abscissa(), lines.get_ordinate())
    plt.ylabel('frequency')
    plt.xlabel('time')
    ax.grid(True)
    plt.savefig(path_to_save)