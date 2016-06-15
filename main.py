# coding: utf-8

from ANA_RC.anarc import *
from ANA_DB.anadb import *

if __name__ == "__main__":
    print("知的照明システムシミュレーター ver.0.3")
    print("最適化アルゴリズム：ANA/DB")

    Initial.set()

    # ANA/RCを実行
    # ana = AnaRc()
    # ANA/DBを実行
    ana = AnaDb()

    ana.start()
