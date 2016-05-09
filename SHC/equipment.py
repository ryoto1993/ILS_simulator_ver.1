# coding: UTF-8

import random


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


def change_luminosity_random(light_list):
    for l in light_list:
        l.set_random_luminosity()


def update_sensor(light_list, sensor_list):
    for s in sensor_list:
        s.reflect(light_list)


class Light:
    ID = 0

    def __init__(self):
        self.ID = Light.ID
        Light.ID += 1
        self.name = ""
        self.lum_MAX = 1000  # 最大光度
        self.lum_MIN = 200   # 最小光度
        self.lum_cur = 200   # 現在光度

    def __str__(self):
        return "Light" + str(self.ID)

    def set_luminosity_range(self, lum_max, lum_min):
        self.lum_MAX = lum_max
        self.lum_MIN = lum_min

    def get_luminosity(self):
        return self.lum_cur

    def set_luminosity(self, lum):
        self.lum_cur = lum

    def set_random_luminosity(self):
        self.lum_cur *= random.uniform(0.92, 1.06)
        if self.lum_cur < self.lum_MIN:
            self.lum_cur = self.lum_MIN
        if self.lum_cur > self.lum_MAX:
            self.lum_cur = self.lum_MAX


class Sensor:
    ID = 0

    def __init__(self):
        self.ID = Sensor.ID
        Sensor.ID += 1
        self.ill_tar = -1  # target illuminance
        self.ill_cur = 0  # current illuminance
        self.influence = []  # influence

    def __str__(self):
        return "Sensor" + set(self.ID)

    def set_target_illuminance(self, target):
        self.ill_tar = target

    def set_influence(self, influence):
        self.influence = influence

    def get_g(self):
        if self.ill_cur - self.ill_tar >= 0:
            return 0
        else:
            return (self.ill_cur - self.ill_tar) ** 2

    def get_illuminance(self):
        return self.ill_cur

    def reflect(self, light_list):
        ill_tmp = 0
        for index, l in enumerate(light_list):
            ill_tmp += l.get_luminosity() * float(self.influence[index+1])
        self.ill_cur = ill_tmp
