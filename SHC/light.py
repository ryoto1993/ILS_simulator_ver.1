# coding: UTF-8


class Light:
    ID = 0

    def __init__(self):
        self.ID = Light.ID
        Light.ID += 1
        self.name = ""
        self.lumMAX = 1000  # 最大光度
        self.lumMIN = 200  # 最小光度

    def __str__(self):
        return "Light" + str(self.ID)

    def set_luminosity(self, lum_max, lum_min):
        self.lumMAX = lum_max
        self.lumMIN = lum_min
