import numpy as np
from project.backend.entity import Entity
from project.backend.muffler import Muffler
from project.backend.rls import RLS
from random import randint


##@package simulation
# Contains function simulate()
def simulate(data: dict) -> dict:
    """
    Main function for running a simulation based on input data.

    :param data: Dictionary containing simulation parameters.
    :return: Dictionary with simulation results.
    """
    # Extracting parameters from the input data
    rls_coordinates = np.array(list(data["RLS"]["COORD"]))
    rls_amplification_coefficient = data["RLS"]["AMPL"]
    rls_energy = data["RLS"]["ENERGY"]
    entity_coordinates = np.array(list(data["OBJ"]["COORD"]))
    entity_radius = data["OBJ"]["RADIUS"]
    entity_speed = np.array(list(data["OBJ"]["SPEED"]))
    noise_share = data["DISTORTION"]
    dt = data["DT"]
    impulse = data["INPC"]

    # Initializing objects
    station = RLS(coordinates=rls_coordinates, amplification_coefficient=rls_amplification_coefficient,
                  fix_coefficient=1, energy=rls_energy, impulse_count=impulse)
    entity = Entity(coordinates=entity_coordinates, radius=entity_radius, velocity=entity_speed)
    muffler = Muffler(noise_share=noise_share)
    noise = muffler.generate_noise()

    # Simulation steps
    station.receiver.get_signal(entity, station.radiator.power, station.radiator.wave_length)
    muffled_distance = station.calculate_distance(entity, noise)

    entity_coords = station.calculate_coordinate(entity, noise)[0]
    velocity_vector = station.calculate_velocity(entity, noise, dt)
    velocity = np.linalg.norm(velocity_vector)

    random_int = -1 if randint(0, 1) == 0 else 1
    # Preparing the result dictionary
    res = {
        "MUFDIST": muffled_distance,
        "SPEED": velocity + random_int * velocity * noise_share / 100,
        "SIGMA": entity.reflection_surface,
        "WAVEL": station.radiator.wave_length,
        "L": 1,
        "OBJCOORD": entity_coords,
        "PREDICT": station.testing_prediction_on_different_noise(muffler, entity),
        "COORD": entity_coordinates + random_int * entity_coordinates * noise_share / 100
    }
    return res
