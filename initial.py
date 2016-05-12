# coding: utf-8

from equipment import *
import csv


class Initial:
    # 照明の数
    light = 16
    # センサの数
    sensor = 98
    # 使用するセンサのリスト
    sensorConfig = [[10, 300], [56, 500], [87, 700]]
    # 重み
    weight = 15

    # 設定用変数
    lightList = []
    sensorList = []
    useSensorList = []
    powerMeter = []

    @staticmethod
    def set():
        f = open('influenceKC111FL.csv', 'r')
        reader = csv.reader(f)
        next(reader)  # ヘッダを読み飛ばす

        # 装置の準備
        for var in range(0, Initial.light-1):
            Initial.lightList.append(Light())

        for var in range(0, Initial.sensor-1):
            Initial.sensorList.append(Sensor())
            Initial.sensorList[var].set_influence(next(reader))

        Initial.powerMeter.append(PowerMeter())
        Initial.powerMeter[0].set_light_list(Initial.lightList)

        # 使用するセンサを設定
        for s in Initial.sensorConfig:
            Initial.sensorList[s[0]].set_target_illuminance(s[1])
            Initial.useSensorList.append(Initial.sensorList[s[0]])

        # 使用する照明を設定
        for l in Initial.lightList:
            l.set_sensor_list(Initial.useSensorList)
            l.set_weight(Initial.weight)
            l.set_power_meter(Initial.powerMeter[0])
