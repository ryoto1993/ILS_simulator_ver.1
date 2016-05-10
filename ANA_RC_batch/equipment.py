# coding: UTF-8

import random
from calculation import *


def update_sensors(light_list, sensor_list):
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

        self.sensor_list = []   # センサリスト

        self.lum_history = []     # 光度値履歴
        self.sensor_history = []  # 全センサの照度値履歴
        self.sensor_rc = []       # 各センサの相関係数
        self.power_meter = PowerMeter

        self.objective_cur = 0   # 現在の目的関数値
        self.objective_next = 0  # 次のステップの目的関数値

    def __str__(self):
        return "Light" + str(self.ID)

    def get_luminosity(self):
        return self.lum_cur

    def set_luminosity(self, lum):
        self.lum_cur = lum

    def set_random_luminosity(self):
        # self.lum_cur *= random.uniform(0.92, 1.06)
        self.lum_cur = self.lum_cur * random.randint(92, 106) / 100
        if self.lum_cur < self.lum_MIN:
            self.lum_cur = self.lum_MIN
        if self.lum_cur > self.lum_MAX:
            self.lum_cur = self.lum_MAX

    def set_sensor_list(self, sensor_list):
        self.sensor_list = sensor_list
        for i in range(0, len(sensor_list)):
            self.sensor_history.append([])
            self.sensor_rc.append(0)

    def set_power_meter(self, power_meter):
        self.power_meter = power_meter

    def calc_current_objective(self):
        print("test")

    def calc_rc(self):
        for index in range(len(self.sensor_list)):
            a, b = calc_regression_coefficient(self.lum_history, self.sensor_history[index])
            self.sensor_rc[index] = a
        print(self.sensor_rc)

    def append_history(self):
        self.lum_history.append(self.lum_cur)
        for index, s in enumerate(self.sensor_list):
            self.sensor_history[index].append(s.get_illuminance())
        print(self.lum_history)
        print(self.sensor_history)



class Sensor:
    ID = 0

    def __init__(self):
        self.ID = Sensor.ID
        Sensor.ID += 1
        self.ill_tar = -1  # target illuminance
        self.ill_cur = 0  # current illuminance
        self.influence = []  # influence

    def __str__(self):
        return "Sensor" + str(self.ID)

    def set_target_illuminance(self, target):
        self.ill_tar = target

    def set_influence(self, influence):
        self.influence = influence

    def get_illuminance(self):
        return self.ill_cur

    def reflect(self, light_list):
        ill_tmp = 0
        for index, l in enumerate(light_list):
            ill_tmp += l.get_luminosity() * float(self.influence[index+1])
        self.ill_cur = ill_tmp


class PowerMeter:
    ID = 0

    def __init__(self):
        self.ID = PowerMeter.ID
        PowerMeter.ID += 1
        self.current_power = 0
        self.light_list = []

    def __str__(self):
        return "Power Meter " + str(self.ID)

    def get_power(self):
        power = 0

        for l in self.light_list:
            power += l.get_luminosity()
        return power

    def set_light_list(self, light_list):
        self.light_list = light_list
