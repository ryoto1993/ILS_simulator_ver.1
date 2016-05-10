# coding: utf-8

import csv

from ANA_RC_batch.equipment import *

print("知的照明システムシミュレーター ver.0.2")
print("最適化アルゴリズム：ANA/RC")

lightList = []
sensorList = []
useSensorList = []
f = open('../influenceKC111FL.csv', 'r')
save_csv = open('../data/ANA_RC/log.csv', 'w')
reader = csv.reader(f)
header = next(reader)
csvWriter = csv.writer(save_csv)

# 装置の準備
for var in range(0, 15):
    lightList.append(Light())

for var in range(0, 97):
    sensorList.append(Sensor())
    sensorList[var].set_influence(next(reader))

powerMeter = PowerMeter()
powerMeter.set_light_list(lightList)

# 使用するセンサを設定
sensorList[10].set_target_illuminance(300)
sensorList[56].set_target_illuminance(500)
sensorList[87].set_target_illuminance(700)
useSensorList.append(sensorList[10])
useSensorList.append(sensorList[56])
useSensorList.append(sensorList[87])

# 照明にセンサ情報と電力計を渡す
for l in lightList:
    l.set_sensor_list(useSensorList)

# csvの作成
csvList = ["Step", "Power", "Sensor10", "Sensor56", "Sensor87"]
for l in lightList:
    csvList.append(l)
csvWriter.writerow(csvList)

# センサの更新
update_sensors(lightList, useSensorList)

# テスト
for l in lightList:
    l.append_history()
    l.set_random_luminosity()

update_sensors(lightList, useSensorList)

for l in lightList:
    l.append_history()
    l.set_random_luminosity()

update_sensors(lightList, useSensorList)

for l in lightList:
    l.append_history()
    print(l)
    l.calc_rc()

# ここから1ステップ毎の処理を記述
for i in range(0, 4000):
    pass
    # 移動検知した場合回帰係数リセット

    # 目的関数値計算

    # 各センサのランク付け

    # 近傍設計の選択

    # 光度をランダムに計算

    # 回帰係数計算

    # 目的関数値計算

    # ロールバック


# ファイルクローズ
f.close()
save_csv.close()
