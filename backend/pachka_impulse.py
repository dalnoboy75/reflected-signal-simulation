class Impulse:
    def __init__(self, x: float, y: float, z: float, power: int) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.power = power

    def get_vector(self) -> tuple:
        return self.x, self.y, self.z

    def change_vector(self, x: int, y: int, z: int):
        self.x += x
        self.y += y
        self.z += z

    def change_power(self, new_power) -> None:
        self.power = new_power

    def get_power(self) -> int:
        return self.power

class PackOfImpulse:
    def __init__(self, dtime: int, type_of_sygnal: str, lis: list):
        self.dtime = dtime
        self.type = type_of_sygnal
        self.lis = lis

    def add_impulse(self, new_impulse: Impulse):
        self.lis.append(new_impulse)

    def get_list(self):
        return self.lis

class signal:
    def __init__(self, sig: list):
        self.sig = sig

    def add_pack(self, k: int, time: int, type_of_sygnal: str):
        p = PackOfImpulse(time, type_of_sygnal, [])
        for i in range(k):
            im = Impulse(input())
            p.add_impulse(im)
        self.sig.append(p)
