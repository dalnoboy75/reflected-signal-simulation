import math
from vector3d import Vector3D


class Receiver:
    def __init__(self, coordinates_, critical_energy_):
        self.coordinates = coordinates_
        self.critical_energy = critical_energy_
        self.delay_sum = 0
        self.average_delay = 0
        self.current_energy = 0
        self.received_signals_count = 0
        self.dist = 0

    def distance(self):
        return self.dist

    def distance_using_power(self, radiator, object, muffler=None):
        radiator.emit_signal(self, object)
        if muffler:
            muffler.noise_mc(self.received_power)
        Pt_div_Pr = self.radiated_power / self.received_power
        return math.pow(Pt_div_Pr * ((math.pow(self.amplification_coefficient, 2) * self.sigma * math.pow(self.wave_length, 2)) / (64 * math.pow(math.pi, 3) * self.L)), 0.25)

    def distance_using_power_no_muffler(self, radiator, object):
        return self.distance_using_power(radiator, object)

    def coordinates_using_power(self, radiator, object, direction_vector, muffler=None):
        unit_vector = direction_vector / direction_vector.abs()
        return self.coordinates + unit_vector * self.distance_using_power(radiator, object, muffler)

    def coordinates_with_mse(self, radiator, object, direction_vector, muffler=None):
        unit_vector = direction_vector / direction_vector.abs()
        abscisses = []
        ordinates = []
        applicates = []

        for _ in range(self.number_of_measurements):
            coordinate = self.coordinates + unit_vector * self.distance_using_power(radiator, object, muffler)
            abscisses.append(coordinate.x)
            ordinates.append(coordinate.y)
            applicates.append(coordinate.z)

        answer = (Vector3D(0, 0, 0), Vector3D(0, 0, 0))
        answer[0].x, answer[1].x = self.mse(abscisses)
        answer[0].y, answer[1].y = self.mse(ordinates)
        answer[0].z, answer[1].z = self.mse(applicates)

        radiator.reset_energy()
        return answer

    def receive_signals(self, v_sign):
        for signal in reversed(v_sign):
            if self.can_collide(self.coordinates - signal.coordinates, signal.direction_vector):
                self.delay_sum += signal.passed_time + ((self.coordinates - signal.coordinates).abs()) / self.speed_of_light
                self.received_signals_count += 1
            v_sign.pop()
        self.dist = -1 if self.received_signals_count == 0 else self.delay_sum / self.received_signals_count * self.speed_of_light / 2

    def receive_signals_with_params(self, radiated_power_, received_power_, L_, wave_length_, sigma_, amplification_coefficient_):
        self.radiated_power = radiated_power_
        self.received_power = received_power_
        self.L = L_
        self.wave_length = wave_length_
        self.sigma = sigma_
        self.amplification_coefficient = amplification_coefficient_

    def mse(self, arr):
        mean = sum(arr) / len(arr)
        sum_squared_diff = sum((x - mean) ** 2 for x in arr)
        return mean, math.sqrt(sum_squared_diff / len(arr))

    def mnk(self, time, coord):
        n = len(time)
        sumX = sum(time)
        sumY = sum(coord)
        sumXY = sum(time[i] * coord[i] for i in range(n))
        sumX2 = sum(time[i] * time[i] for i in range(n))

        avrX = sumX / n
        avrY = sumY / n
        avrXY = sumXY / n
        avrX2 = sumX2 / n

        k = (avrXY - avrX * avrY) / (avrX2 - avrX * avrX)
        b = avrY - k * avrX

        return k, b

    def speed_calculation(self, rad, object, muffler, dt):
        l1 = self.distance_using_power(rad, object)
        object.update_position(dt)
        l2 = self.distance_using_power(rad, object)
        object.update_position(dt)
        l3 = self.distance_using_power(rad, object)
        object.update_position(dt)

        speed = math.sqrt(abs(l1*l1 + l3*l3 - 2*l2*l2)) / dt * math.sqrt(0.5)
        if muffler:
            muffler.noise_mc(speed)
        return speed

    def speed_vector_with_mse(self, rad, object, muffler, direction_vector, dt):
        abscisses = []
        ordinates = []
        applicates = []
        time_vector = []

        for i in range(1, self.speed_measurements_amount + 1):
            time_vector.append(i * dt)
            rad.emit_signal(self, object)
            coord = self.coordinates_with_mse(rad, object, direction_vector, muffler)[0]
            abscisses.append(coord.x)
            ordinates.append(coord.y)
            applicates.append(coord.z)
            object.update_position(dt)

        speed_vector = Vector3D(0, 0, 0)
        speed_vector.x, _ = self.mnk(time_vector, abscisses)
        speed_vector.y, _ = self.mnk(time_vector, ordinates)
        speed_vector.z, _ = self.mnk(time_vector, applicates)

        return speed_vector
