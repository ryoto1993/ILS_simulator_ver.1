# coding: utf-8

from SHC.equipment import *
import csv
import copy

print("知的照明システムシミュレーター ver.0.1")

lightList = []
sensorList = []
weight = 15
f = open('../influenceKC111FL.csv', 'r')
save_csv = open('../data/log.csv', 'w')
reader = csv.reader(f)
header = next(reader)
csvWriter = csv.writer(save_csv)


# 照明とセンサの準備
for var in range(0, 15):
    lightList.append(Light())

for var in range(0, 97):
    sensorList.append(Sensor())
    sensorList[var].set_influence(next(reader))

# csvの作成
csvList = ["Step", "Sensor10", "Sensor56", "Sensor87"]
for l in lightList:
    csvList.append(l)
csvWriter.writerow(csvList)

# センサに目標照度値を設定
sensorList[10].set_target_illuminance(300)
sensorList[56].set_target_illuminance(500)
sensorList[87].set_target_illuminance(700)

for s in sensorList:
    s.reflect(lightList)

# ここから1ステップ分の処理を書く
for i in range(0, 1000):
    before_f = calc_objective_function(lightList, sensorList, weight)
    before_light_list = copy.deepcopy(lightList)
    change_luminosity_random(lightList)
    update_sensor(lightList, sensorList)
    after_f = calc_objective_function(lightList, sensorList, weight)
    if before_f < after_f:
        lightList = copy.deepcopy(before_light_list)

    csvList.clear()
    csvList.append(i)
    csvList.append(str(int(sensorList[10].get_illuminance())))
    csvList.append(str(int(sensorList[56].get_illuminance())))
    csvList.append(str(int(sensorList[87].get_illuminance())))
    csvWriter.writerow(csvList)

f.close()
save_csv.close()
