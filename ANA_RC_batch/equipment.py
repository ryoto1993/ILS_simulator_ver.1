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
        self.lum_bef = 0    # 前の光度
        self.objective_cur = 0  # 現在の目的関数値
        self.objective_next = 0  # 次のステップの目的関数値
        self.weight = 15     # 評価値の重み
        self.shc_weight = 15  # SHCの評価値の重み

        self.sensor_list = []   # センサリスト
        self.power_meter = []  # 電力計

        self.lum_history = []     # 光度値履歴
        self.sensor_history = []  # 全センサの照度値履歴
        self.sensor_rc = []       # 各センサの相関係数
        self.sensor_rank = []     # 近傍決定のためのセンサのランク
        self.neighbor = Neighbor()  # 近傍設計

    def __str__(self):
        return "Light" + str(self.ID)

    def get_luminosity(self):
        return self.lum_cur

    def get_rc(self):
        return self.sensor_rc

    def set_luminosity(self, lum):
        self.lum_cur = lum

    def set_weight(self, weight):
        self.weight = weight

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
            if 0.06 * s.get_illuminance() <= s.get_illuminance() -s.get_target() < s.get_illuminance() - s.get_target():
                if self.sensor_rc[index] >= 0.02:
                    efunc += self.sensor_rc[index] * (s.get_illuminance() - s.get_target())**2

        self.objective_cur = self.power_meter[0].get_power() + self.weight * efunc
        # print(self.objective_cur)

    def calc_rc(self):
        for index in range(len(self.sensor_list)):
            a, b = calc_regression_coefficient(self.lum_history, self.sensor_history[index])
            self.sensor_rc[index] = a

            if a >= 0.2:
                self.sensor_rank[index] = 1
            elif a >= 0.1:
                self.sensor_rank[index] = 2
            elif a >= 0.06:
                self.sensor_rank[index] = 3
            else:
                self.sensor_rank[index] = 0

    def shc_append_history(self):
        self.lum_history.append(self.lum_cur - self.lum_bef)
        for index, s in enumerate(self.sensor_list):
            self.sensor_history[index].append(s.get_illuminance() - s.get_before())

    def shc_calc_objective_function(self):
        light_weight = 0

        for s in self.sensor_list:
            if s.get_illuminance() - s.get_target() >= 0:
                light_weight += 0
            else:
                light_weight += (s.get_illuminance() - s.get_target()) ** 2

        self.objective_cur = self.power_meter[0].get_power() + self.shc_weight * light_weight

    def shc_calc_next_objective_function(self):
        light_weight = 0

        for s in self.sensor_list:
            if s.get_illuminance() - s.get_target() >= 0:
                light_weight += 0
            else:
                light_weight += (s.get_illuminance() - s.get_target()) ** 2

        self.objective_next = self.power_meter[0].get_power() + self.shc_weight * light_weight

    def shc_set_random_luminosity(self):
        next_lum = self.lum_cur

        next_lum += (self.lum_MAX - self.lum_MIN) * random.randint(-8, 6) / 100
        if next_lum < self.lum_MIN:
            next_lum = self.lum_MIN
        if next_lum > self.lum_MAX:
            next_lum = self.lum_MAX

        self.lum_bef = self.lum_cur
        self.lum_cur = next_lum

    def shc_is_rollback(self):
        if self.objective_cur < self.objective_next:
            return True
        else:
            return False

    def shc_rollback(self):
        self.lum_cur = self.lum_bef


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
        self.ill_bef = 0
        self.influence = []  # influence

    def __str__(self):
        return "Sensor" + str(self.ID)

    def set_target_illuminance(self, target):
        self.ill_tar = target

    def set_influence(self, influence):
        self.influence = influence

    def get_illuminance(self):
        return self.ill_cur

    def get_before(self):
        return self.ill_bef

    def get_target(self):
        return self.ill_tar

    def reflect(self, light_list):
        ill_tmp = 0
        for index, l in enumerate(light_list):
            ill_tmp += l.get_luminosity() * float(self.influence[index+1])
        self.ill_bef = self.ill_cur
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
