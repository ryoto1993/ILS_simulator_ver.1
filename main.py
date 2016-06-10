# coding: utf-8

from ANA_RC.anarc import *

if __name__ == "__main__":
    print("知的照明システムシミュレーター ver.0.2")
    print("最適化アルゴリズム：ANA/RC")

    Initial.set()
    ana_rc = AnaRc()

    ana_rc.start()
