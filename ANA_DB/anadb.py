# coding: utf-8

import os
import datetime
from initial import *


class AnaDb:

    def __init__(self):
        self.lightList = Initial.lightList  # 照明
        self.useSensorList = Initial.useSensorList  # センサ
        self.powerMeter = Initial.powerMeter[0]  # 電力計

        # csvの作成
        time = datetime.datetime.today()
        year = str(time.year)
        month = str(time.month).zfill(2)
        date = str(time.day).zfill(2)
        hour = str(time.hour).zfill(2)
        minute = str(time.minute).zfill(2)
        file_dir = "log/" + year + month + date + "_" + hour + minute + "_" + "DB_" + Initial.sim_name
        os.mkdir(file_dir)
        log_dir = file_dir + "/log.csv"
        ill_log_dir = file_dir + "/ill_log.csv"
        lum_log_dir = file_dir + "/lum_log.csv"
        self.save_csv = open(log_dir, 'w', newline='')
        self.ill_csv = open(ill_log_dir, 'w', newline='')
        self.lum_csv = open(lum_log_dir, 'w', newline='')
        self.csv_writer = csv.writer(self.save_csv)
        self.ill_writer = csv.writer(self.ill_csv)
        self.lum_writer = csv.writer(self.lum_csv)
        self.csv_list = ["Step", "Power"]
        self.lum_list = []
        self.ill_list = []
        for s in self.useSensorList:
            self.csv_list.append(s)
        for l in self.lightList:
            self.csv_list.append(l)
        self.csv_writer.writerow(self.csv_list)

    def start(self):
        # センサ更新
        update_sensors(self.lightList, self.useSensorList)

        # ランク計算
        for l in self.lightList:
            l.db_calc_rank()

        # ここから1ステップ毎の処理を記述
        for i in range(0, 2000):
            # CSV出力
            self.csv_list.clear()
            self.lum_list.clear()
            self.ill_list.clear()
            self.csv_list.append(i)
            self.csv_list.append(str(int(self.powerMeter.get_power())))
            for s in self.useSensorList:
                self.csv_list.append(str(int(s.get_illuminance())))
                self.ill_list.append(str(int(s.get_illuminance())))
            for l in self.lightList:
                self.csv_list.append(str(int(l.get_luminosity())))
                self.lum_list.append(str(int(l.get_luminosity())))
            self.csv_writer.writerow(self.csv_list)
            self.ill_writer.writerow(self.ill_list)
            self.lum_writer.writerow(self.lum_list)

            # 現在目的関数計算
            for l in self.lightList:
                l.db_calc_current_objective()
            # 近傍選択
            for l in self.lightList:
                l.decide_neighbor()
            # 光度値変動
            for l in self.lightList:
                l.set_random_luminosity()
            update_sensors(self.lightList, self.useSensorList)
            for l in self.lightList:
                l.db_append_history()

            # CSV
            self.csv_list.clear()
            self.lum_list.clear()
            self.ill_list.clear()
            self.csv_list.append(i)
            self.csv_list.append(str(int(self.powerMeter.get_power())))
            for s in self.useSensorList:
                self.csv_list.append(str(int(s.get_illuminance())))
                self.ill_list.append(str(int(s.get_illuminance())))
            for l in self.lightList:
                self.csv_list.append(str(int(l.get_luminosity())))
                self.lum_list.append(str(int(l.get_luminosity())))
            self.csv_writer.writerow(self.csv_list)
            self.ill_writer.writerow(self.ill_list)
            self.lum_writer.writerow(self.lum_list)

            # 次の目的関数計算
            for l in self.lightList:
                l.db_calc_next_objective()
            # ロールバック
            for l in self.lightList:
                if l.is_rollback():
                    l.rollback()
            update_sensors(self.lightList, self.useSensorList)
            for l in self.lightList:
                if l.is_rollback():
                    l.db_append_history()

        # ファイルクローズ
        self.save_csv.close()
        self.ill_csv.close()
        self.lum_csv.close()
