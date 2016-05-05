# coding: UTF-8

class Sensor:
    ID = 0

    def __init__(self):
        self.ID = Sensor.ID
        Sensor.ID += 1

    def __str__(self):
        return "Sensor" + self.ID