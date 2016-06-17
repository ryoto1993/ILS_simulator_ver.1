# coding: utf-8

import csv

from ILS_common.equipment import *


class Initial:
    # 実験名
    sim_name = "Sim.A-01"
    # 照明の数
    light = 12
    # センサの数
    sensor = 54
    # 使用するセンサのリスト
    sensorConfig = [[23, 300], [41, 500]]
    # 重み
    weight = 0.1
    # 初期光度値
    initLum = 200
    # 最小，最大光度値
    minLum = 200
    maxLum = 1200
    # 影響度ファイル
    coefficient_file = "coefficient/coefficient1_reverse.csv"

    # 設定用変数
    lightList = []
    sensorList = []
    useSensorList = []
    powerMeter = []

    @staticmethod
    def set():
        f = open(Initial.coefficient_file, 'r')
        reader = csv.reader(f)
        next(reader)  # ヘッダを読み飛ばす

        # 装置の準備
        for var in range(0, Initial.light):
            Initial.lightList.append(Light())

        for var in range(0, Initial.sensor):
            Initial.sensorList.append(Sensor())
            Initial.sensorList[var].set_influence(next(reader))

        Initial.powerMeter.append(PowerMeter())
        Initial.powerMeter[0].set_light_list(Initial.lightList)

        # 使用するセンサを設定
        for s in Initial.sensorConfig:
            Initial.sensorList[s[0]-1].set_target_illuminance(s[1])
            Initial.useSensorList.append(Initial.sensorList[s[0]-1])

        # 使用する照明を設定
        for l in Initial.lightList:
            l.set_sensor_list(Initial.useSensorList)
            l.set_weight(Initial.weight)
            l.set_power_meter(Initial.powerMeter[0])
            l.set_luminosity(Initial.initLum)
            l.set_min_max(Initial.minLum, Initial.maxLum)
