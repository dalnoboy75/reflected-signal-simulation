import numpy as np
from backend.entity import Entity
from backend.muffler import Muffler
from backend.rls import RLS


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

    # Initializing objects
    station = RLS(coordinates=rls_coordinates, amplification_coefficient=rls_amplification_coefficient,
                  fix_coefficient=1, energy=rls_energy, impulse_count=5)
    entity = Entity(coordinates=entity_coordinates, radius=entity_radius, velocity=entity_speed)
    muffler = Muffler(noise_share=noise_share)
    noise = muffler.generate_noise()

    # Simulation steps
    station.receiver.get_signal(entity, station.radiator.power, station.radiator.wave_length)
    muffled_distance = station.calculate_distance(entity, noise)

    direction_vector = station.receiver.get_direction(entity)
    entity_coords = station.calculate_coordinate(entity, direction_vector, noise)[0]
    velocity_vector = station.calculate_velocity(entity, direction_vector, noise, dt)
    velocity = np.linalg.norm(velocity_vector)

    # Preparing the result dictionary
    res = {
        "MUFDIST": muffled_distance,
        "SPEED": velocity,
        "SIGMA": entity.reflection_surface,
        "WAVEL": station.radiator.wave_length,
        "L": 1,
        "OBJCOORD": entity_coords,
        "PREDICT": station.testing_prediction_on_different_noise(muffler, entity)
    }
    return res
