# coding: UTF-8


def calc_power(light_list):
    power = 0

    for l in light_list:
        power += l.get_luminosity()
    return power


def calc_objective_function(light_list, sensor_list, weight):
    light_weight = 0

    for s in sensor_list:
        light_weight += s.get_g()

    return calc_power(light_list) + weight * light_weight


class Light:
    ID = 0

    def __init__(self):
        self.ID = Light.ID
        Light.ID += 1
        self.name = ""
        self.lumMAX = 1000  # 最大光度
        self.lumMIN = 200   # 最小光度
        self.lumCUR = 1000   # 現在光度

    def __str__(self):
        return "Light" + str(self.ID)

    def set_luminosity_range(self, lum_max, lum_min):
        self.lumMAX = lum_max
        self.lumMIN = lum_min

    def get_luminosity(self):
        return self.lumCUR


class Sensor:
    ID = 0

    def __init__(self):
        self.ID = Sensor.ID
        Sensor.ID += 1
        self.tarIL = 0  # target illuminance
        self.curIL = 0  # current illuminance
        self.influence = []  # influence

    def __str__(self):
        return "Sensor" + set(self.ID)

    def set_target_illuminance(self, target):
        self.tarIL = target

    def set_influence(self, influence):
        self.influence = influence

    def get_g(self):
        if self.curIL - self.tarIL >= 0:
            return 0
        else:
            return (self.curIL - self.tarIL)**2
