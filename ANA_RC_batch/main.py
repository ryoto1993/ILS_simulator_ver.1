# coding: utf-8

import csv

from ANA_RC_batch.equipment import *

print("知的照明システムシミュレーター ver.0.2")
print("最適化アルゴリズム：ANA/RC")

lightList = []
sensorList = []
useSensorList = []
f = open('../influenceKC111FL.csv', 'r')
save_csv = open('../data/ANA_RC/log.csv', 'w')
reader = csv.reader(f)
header = next(reader)
csvWriter = csv.writer(save_csv)

# 装置の準備
for var in range(0, 15):
    lightList.append(Light())

for var in range(0, 97):
    sensorList.append(Sensor())
    sensorList[var].set_influence(next(reader))

powerMeter = PowerMeter()
powerMeter.set_light_list(lightList)

# 使用するセンサを設定
sensorList[10].set_target_illuminance(300)
sensorList[56].set_target_illuminance(500)
sensorList[87].set_target_illuminance(700)
useSensorList.append(sensorList[10])
useSensorList.append(sensorList[56])
useSensorList.append(sensorList[87])

# 使用する照明を設定
for l in lightList:
    l.set_sensor_list(useSensorList)
    l.set_power_meter(powerMeter)
    l.set_weight(15)

# csvの作成
csvList = ["Step", "Power", "Sensor10", "Sensor56", "Sensor87"]
for l in lightList:
    csvList.append(l)
csvWriter.writerow(csvList)

# センサの更新
update_sensors(lightList, useSensorList)

# SHCを50回回す
for i in range(0, 50):
    for l in lightList:
        l.shc_calc_objective_function()
    for l in lightList:
        l.shc_set_random_luminosity()
    update_sensors(lightList, useSensorList)
    for l in lightList:
        l.shc_append_history()
    for l in lightList:
        l.shc_calc_next_objective_function()
    if lightList[0].shc_is_rollback():
        for l in lightList:
            l.shc_rollback()
        update_sensors(lightList, useSensorList)

# ここから1ステップ毎の処理を記述
for i in range(0, 1000):
    # 回帰係数計算
    for l in lightList:
        l.calc_rc()
    # 現在目的関数計算
    for l in lightList:
        l.calc_current_objective()
    # 近傍選択
    for l in lightList:
        l.decide_neighbor()
    # 光度値変動
    for l in lightList:
        l.set_random_luminosity()
    update_sensors(lightList, useSensorList)
    for l in lightList:
        l.append_history()
    # 変動後回帰係数計算
    for l in lightList:
        l.calc_rc()
    # 次の目的関数計算
    for l in lightList:
        l.calc_next_objective()
    # ロールバック
    for l in lightList:
        if l.is_rollback():
            l.rollback()
    update_sensors(lightList, useSensorList)
    print(i)

# ファイルクローズ
f.close()
save_csv.close()
