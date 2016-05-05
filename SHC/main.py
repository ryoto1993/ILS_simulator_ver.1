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

sensorList[10].setTargetIlluminance(300)
sensorList[56].setTargetIlluminance(500)
sensorList[87].setTargetIlluminance(700)