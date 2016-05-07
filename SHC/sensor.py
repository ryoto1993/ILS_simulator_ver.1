# coding: UTF-8


class Sensor:
    ID = 0

    def __init__(self):
        self.ID = Sensor.ID
        Sensor.ID += 1
        self.tarIL = 0  # target illuminance
        self.curIL = 0  # current illuminance
        self.influence = []  # influence

    def __str__(self):
        return "Sensor" + set(self.ID)

    def set_target_illuminance(self, target):
        self.tarIL = target

    def set_influence(self, influence):
        self.influence = influence
