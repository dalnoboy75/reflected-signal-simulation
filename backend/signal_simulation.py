import numpy as np
from backend.entity import Entity
from backend.muffler import Muffler
from backend.rls import RLS


def simulate(data: dict) -> dict:
    rl = RLS(coordinates=np.array(list(data["RLS"]["COORD"])), amplification_coefficient=data["RLS"]["AMPL"],
             fix_coefficient=1, energy=data["RLS"]["ENERGY"])
    obj = Entity(coordinates=np.array(list(data["OBJ"]["COORD"])), radius=data["OBJ"]["RADIUS"],
                 velocity=np.array(list(data["OBJ"]["SPEED"])))
    muf = Muffler(noise_share=data["DISTORTION"])

    obj.set_reflection_surface(rl)
    rl.emit_signal(obj)

    dt = data["DT"]

    muffled_distance = rl.calculate_distance_with_noise(obj, muf)
    rl.reset_energy()
    dir_to_obj_vector = rl.get_direction_to_entity(obj)
    obj_coords = rl.calculate_coordinates_with_mse(obj, dir_to_obj_vector, muf)[0]
    speed_vector = rl.calculate_velocity_with_lsm(obj, dir_to_obj_vector, muf, dt)

    speed = np.linalg.norm(speed_vector)
    res = {"MUFDIST": muffled_distance, "SPEED": speed, "SIGMA": rl.get_reflective_surface(),
           "WAVEL": rl.get_wave_length(), "L": 1, "OBJCOORD": obj_coords}
    return res
