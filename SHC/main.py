# coding: utf-8

from SHC.light import Light
from SHC.sensor import Sensor

print("知的照明システムシミュレーター ver.0.1")

lightList = []
sensorList = []

for var in range(0, 15):
    lightList.append(Light())

for var in range(0, 97):
    sensorList.append(Sensor())