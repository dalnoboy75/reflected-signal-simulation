import numpy as np
from backend.entity import Entity
from backend.muffler import Muffler
from backend.rls import RLS


def simulate(data: dict) -> dict:
    rl = RLS(coordinates=np.array(list(data["RLS"]["COORD"])), amplification_coefficient=data["RLS"]["AMPL"],
             fix_coefficient=1, energy=data["RLS"]["ENERGY"], impulse_count=data["IMPC"])
    obj = Entity(coordinates=np.array(list(data["OBJ"]["COORD"])), radius=data["OBJ"]["RADIUS"],
                 velocity=np.array(list(data["OBJ"]["SPEED"])))
    muf = Muffler(noise_share=data["DISTORTION"])
    rl.receiver.get_signal(obj, rl.radiator.power, rl.radiator.wave_length)

    dt = data["DT"]
    muffled_distance = rl.calculate_distance(obj, muf)
    dir_to_obj_vector = rl.receiver.get_direction(obj)
    obj_coords = rl.calculate_coordinate(obj, dir_to_obj_vector, muf)[0]
    speed_vector = rl.calculate_velocity(obj, dir_to_obj_vector, muf, dt)
    speed = np.linalg.norm(speed_vector)
    res = {"MUFDIST": muffled_distance, "SPEED": speed, "SIGMA": obj.reflection_surface,
           "WAVEL": rl.radiator.wave_length, "L": 1, "OBJCOORD": obj_coords}
    return res
