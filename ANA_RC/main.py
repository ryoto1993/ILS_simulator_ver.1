# coding: utf-8

import csv

from ANA_RC.equipment import *

print("知的照明システムシミュレーター ver.0.2")
print("最適化アルゴリズム：ANA/RC")

lightList = []
sensorList = []
f = open('../influenceKC111FL.csv', 'r')
save_csv = open('../data/log.csv', 'w')
reader = csv.reader(f)
header = next(reader)
csvWriter = csv.writer(save_csv)

# 照明とセンサの準備
for var in range(0, 15):
    lightList.append(Light())

for var in range(0, 97):
    sensorList.append(Sensor())
    sensorList[var].set_influence(next(reader))

# csvの作成
csvList = ["Step", "Power", "Sensor10", "Sensor56", "Sensor87"]
for l in lightList:
    csvList.append(l)
csvWriter.writerow(csvList)

# センサに目標照度値を設定
sensorList[10].set_target_illuminance(300)
sensorList[56].set_target_illuminance(500)
sensorList[87].set_target_illuminance(700)

for s in sensorList:
    s.reflect(lightList)

# ここから1ステップ毎の処理を記述
for i in range(0, 4000):
    # 移動検知した場合回帰係数リセット
    print("移動検知")

    # 目的関数値計算

    # 近傍計算

    # 光度をランダムに計算

    # 回帰係数計算

    # 目的関数値計算

    # ロールバック


# ファイルクローズ
f.close()
save_csv.close()
