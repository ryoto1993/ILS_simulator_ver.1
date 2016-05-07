# coding: utf-8

from SHC.light import Light
from SHC.sensor import Sensor
import csv

print("知的照明システムシミュレーター ver.0.1")

lightList = []
sensorList = []
f = open('../influenceKC111FL.csv', 'r')
reader = csv.reader(f)
header = next(reader)

# 照明とセンサの準備
for var in range(0, 15):
    lightList.append(Light())

for var in range(0, 97):
    sensorList.append(Sensor())
    sensorList[var].set_influence(next(reader))

# センサに目標照度値を設定
sensorList[10].set_target_illuminance(300)
sensorList[56].set_target_illuminance(500)
sensorList[87].set_target_illuminance(700)

f.close()
