import numpy as np
from backend.entity import Entity
from backend.muffler import Muffler
from backend.rls import RLS


# Main function for running a simulation based on input data
def simulate(data: dict) -> dict:
    station = RLS(coordinates=np.array(list(data["RLS"]["COORD"])), amplification_coefficient=data["RLS"]["AMPL"],
                  fix_coefficient=1, energy=data["RLS"]["ENERGY"], impulse_count=data["INPC"])
    entity = Entity(coordinates=np.array(list(data["OBJ"]["COORD"])), radius=data["OBJ"]["RADIUS"],
                    velocity=np.array(list(data["OBJ"]["SPEED"])))
    muffler = Muffler(noise_share=data["DISTORTION"])
    dt = data["DT"]
    noise = muffler.generate_noise()

    station.receiver.get_signal(entity, station.radiator.power, station.radiator.wave_length)
    muffled_distance = station.calculate_distance(entity, noise)

    direction_vector = station.receiver.get_direction(entity)
    entity_coords = station.calculate_coordinate(entity, direction_vector, noise)[0]
    velocity_vector = station.calculate_velocity(entity, direction_vector, noise, dt)
    velocity = np.linalg.norm(velocity_vector)

    res = {"MUFDIST": muffled_distance, "SPEED": velocity, "SIGMA": entity.reflection_surface,
           "WAVEL": station.radiator.wave_length, "L": 1, "OBJCOORD": entity_coords,
           "PREDICT": station.testing_prediction_on_different_noise(muffler, entity)}
    return res
