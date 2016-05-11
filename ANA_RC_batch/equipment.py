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
        self.lum_next = 0    # 次の光度
        self.weight = 15     # 評価値の重み

        self.sensor_list = []   # センサリスト
        self.power_meter = []  # 電力計

        self.lum_history = []     # 光度値履歴
        self.sensor_history = []  # 全センサの照度値履歴
        self.sensor_rc = []       # 各センサの相関係数
        self.sensor_rank = []     # 近傍決定のためのセンサのランク
        self.neighbor = Neighbor()  # 近傍設計

        self.objective_cur = 0   # 現在の目的関数値
        self.objective_next = 0  # 次のステップの目的関数値

    def __str__(self):
        return "Light" + str(self.ID)

    def get_luminosity(self):
        return self.lum_cur

    def set_luminosity(self, lum):
        self.lum_cur = lum

    def set_weight(self, weight):
        self.weight = weight

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
            self.sensor_rank.append(10)
            self.sensor_rc.append(0)

    def set_power_meter(self, power_meter):
        self.power_meter.append(power_meter)

    def calc_current_objective(self):
        efunc = 0

        for index, s in enumerate(self.sensor_list):
            if (0.06 * s.get_illuminance() <= s.get_illuminance() -s.get_target()) or (s.get_illuminance() - s.get_target()):
                if self.sensor_rc[index] >= 0.8:
                    efunc += self.sensor_rc[index] * (s.get_illuminance() - s.get_target())**2

        self.objective_cur = self.power_meter[0].get_power() + self.weight * efunc
        # print(self.objective_cur)

    def calc_rc(self):
        for index in range(len(self.sensor_list)):
            a, b = calc_regression_coefficient(self.lum_history, self.sensor_history[index])
            self.sensor_rc[index] = a

            if a >= 3.0:
                self.sensor_rank[index] = 1
            elif a >= 2.0:
                self.sensor_rank[index] = 2
            elif a >= 1.5:
                self.sensor_rank[index] = 3
            else:
                self.sensor_rank[index] = 0

    def append_history(self):
        self.lum_history.append(self.lum_cur)
        for index, s in enumerate(self.sensor_list):
            self.sensor_history[index].append(s.get_illuminance())
        # print(self.lum_history)
        # print(self.sensor_history)

    def calc_shc_objective_function(self, weight):
        light_weight = 0

        for s in self.sensor_list:
            add = 0
            if s.get_illuminance() - s.get_target() >= 0:
                add = 0
            else:
                add = (s.get_illuminance() - s.get_target()) ** 2
            light_weight += add

        return self.power_meter.get_power() + weight * light_weight


# 近傍設計
class Neighbor:
    def __init__(self):
        self.upper = 0
        self.lower = 0
        self.neighbor_type = "N/A"
        self.neighbor_design = 0

    def __str__(self):
        return self.type

    def set_neighbor_type(self, neighbor_type):
        if neighbor_type == "a":
            self.upper = 1
            self.lower = -10
        elif neighbor_type == "b":
            self.upper = 3
            self.lower = -7
        elif neighbor_type == "c":
            self.upper = 3
            self.lower = -5
        elif neighbor_type == "d":
            self.upper = 2
            self.lower = -2
        elif neighbor_type == "e":
            self.upper = 5
            self.lower = -3
        elif neighbor_type == "f":
            self.upper = 7
            self.lower = -2
        elif neighbor_type == "g":
            self.upper = 12
            self.lower = -1

    def set_neighbor(self, light_list, sensor_list, rank_list):
        # node1
        if not ((1 in rank_list) or (2 in rank_list) or (3 in rank_list)):
            print("Set design 1")
            self.neighbor_design = 1
        else:
            # node2
            inf_count = 0
            inf_sensor_list = []
            for index, r in enumerate(rank_list):
                if (1 in r) or (2 in r) or (3 in r):
                    inf_count += 1
                    inf_sensor_list.append(sensor_list[index])
            if inf_count == 1:
                # node3
                if inf_sensor_list[0].get_illuminance() > inf_sensor_list[0].get_target():
                    # node5
                    if inf_sensor_list[0].get_illuminance() > 1.06 * inf_sensor_list[0].get_target:
                        print("Set design 3")
                        self.neighbor_design = 3
                    else:
                        print("Set design 2")
                        self.neighbor_design = 2
                else:
                    # node6
                    if 0.98 * inf_sensor_list[0].get_target() <= inf_sensor_list[0].get_illuminance() < inf_sensor_list[0].get_target():
                        print("Set design 6")
                        self.neighbor_design = 6
                    else:
                    # node7
                        if 0.92 * inf_sensor_list[0].get_target() < inf_sensor_list[0].get_illuminance() < 0.98 * inf_sensor_list[0].get_target:
                            print("Set design 5")
                            self.neighbor_design = 5
                        else:
                            print("Set design 4")
                            self.neighbor_design = 4
            else:
                # node4
                unsatisfy_sensor_list = []
                for s in inf_sensor_list:
                    if s.get_illuminance() < s.get_target():
                        unsatisfy_sensor_list.append(s)
                if len(unsatisfy_sensor_list) == 0:
                    # node5
                    flag = False
                    for s in inf_sensor_list:
                        if s.get_illuminance() > 1.06 * s.get_target():
                            flag = True
                    if flag:
                        print("Set design 3")
                        self.neighbor_design = 3
                    else:
                        print("Set design 2")
                        self.neighbor_design = 2
                else:
                    # node6
                    flag = False
                    for s in unsatisfy_sensor_list:
                        if not (0.98 * s.get_target() <= s.get_illuminance() < s.get_target()):
                            flag = True
                    if flag:
                        # node7
                        flag2 = False
                        for s in unsatisfy_sensor_list:
                            if not (0.92 * s.get_target() < s.get_illuminance() < 0.98 * s.get_target()):
                                flag2 = True
                        if flag2:
                            print("Set design 4")
                            self.neighbor_design = 4
                        else:
                            print("Set design 5")
                            self.neighbor_design = 5
                    else:
                        print("Set design 6")
                        self.neighbor_design = 6

    def get_upper(self):
        return self.upper

    def get_lower(self):
        return self.lower



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

    def get_target(self):
        return self.ill_tar

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
