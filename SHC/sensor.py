# coding: UTF-8

class Sensor:
    ID = 0

    def __init__(self):
        self.ID = Sensor.ID
        Sensor.ID += 1
        self.tarIL = 0  # target illuminance
        self.curIL = 0  # current illuminance

    def __str__(self):
        return "Sensor" + set(self.ID)

    def setTargetIlluminance(self, target):
        self.tarIL = target