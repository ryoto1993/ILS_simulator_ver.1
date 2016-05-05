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
        return str(self.ID)

    def setluminocity(self, lumMAX, lumMIN):
        self.lumMAX = lumMAX
        self.lumMIN = lumMIN
