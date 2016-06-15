# coding: utf-8

from initial import *


class AnaRc:

    def __init__(self):
        self.lightList = Initial.lightList  # 照明
        self.useSensorList = Initial.useSensorList  # センサ
        self.powerMeter = Initial.powerMeter[0]  # 電力計

        # csvの作成
        self.save_csv = open('log/ANA_RC/log.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.save_csv)
        self.csv_list = ["Step", "Power"]
        for s in self.useSensorList:
            self.csv_list.append(s)
        for l in self.lightList:
            self.csv_list.append(l)
        self.csv_writer.writerow(self.csv_list)

        # 回帰係数出力テスト
        self.rccsv = open('log/ANA_RC/rc.csv', 'w', newline='')
        self.rccsv_writer = csv.writer(self.rccsv)
        self.rccsv_list = ["Step"]
        for s in self.useSensorList:
            self.rccsv_list.append(s)
        self.rccsv_writer.writerow(self.rccsv_list)
        
    def start(self):
        # センサの更新
        update_sensors(self.lightList, self.useSensorList)

        # SHCを50回回す
        for i in range(0, 50):
            for l in self.lightList:
                l.shc_calc_objective_function()
            for l in self.lightList:
                l.shc_set_random_luminosity()
            update_sensors(self.lightList, self.useSensorList)
            for l in self.lightList:
                l.shc_append_history()
            for l in self.lightList:
                l.shc_calc_next_objective_function()
            if self.lightList[0].shc_is_rollback():
                for l in self.lightList:
                    l.shc_rollback()
                update_sensors(self.lightList, self.useSensorList)
            # CSV出力
            self.csv_list.clear()
            self.csv_list.append(i)
            self.csv_list.append(self.powerMeter.get_power())
            for s in self.useSensorList:
                self.csv_list.append(str(int(s.get_illuminance())))
            for l in self.lightList:
                self.csv_list.append(str(int(l.get_luminosity())))
            self.csv_writer.writerow(self.csv_list)

        for l in self.lightList:
            l.calc_rc()

        self.rccsv_list.clear()
        self.rccsv_list.append("SHC")
        self.rccsv_list.append(self.lightList[0].get_rc()[0])
        self.rccsv_list.append(self.lightList[0].get_rc()[1])
        # self.rccsv_list.append(self.lightList[0].get_rc()[2])
        self.rccsv_writer.writerow(self.rccsv_list)

        # 初期化
        for l in self.lightList:
            pass
            # l.set_luminosity(l.get_min())
        update_sensors(self.lightList, self.useSensorList)

        # ここから1ステップ毎の処理を記述
        for i in range(0, 2000):

            # ######## センサの変更ルール処理をここで記述！

            # CSV出力
            self.csv_list.clear()
            self.csv_list.append(i)
            self.csv_list.append(str(int(self.powerMeter.get_power())))
            for s in self.useSensorList:
                self.csv_list.append(str(int(s.get_illuminance())))
            for l in self.lightList:
                self.csv_list.append(str(int(l.get_luminosity())))
            self.csv_writer.writerow(self.csv_list)

            # 回帰係数計算
            for l in self.lightList:
                pass
                l.calc_rc()
            self.rccsv_list.clear()
            self.rccsv_list.append(i)
            self.rccsv_list.append(self.lightList[0].get_rc()[0])
            self.rccsv_list.append(self.lightList[0].get_rc()[1])
            # self.rccsv_list.append(self.lightList[0].get_rc()[2])
            self.rccsv_writer.writerow(self.rccsv_list)
            # 現在目的関数計算
            for l in self.lightList:
                l.calc_current_objective()
            # 近傍選択
            for l in self.lightList:
                l.decide_neighbor()
            # 光度値変動
            for l in self.lightList:
                l.set_random_luminosity()
            update_sensors(self.lightList, self.useSensorList)
            for l in self.lightList:
                l.append_history()

            # CSV
            self.csv_list.clear()
            self.csv_list.append(i)
            self.csv_list.append(str(int(self.powerMeter.get_power())))
            for s in self.useSensorList:
                self.csv_list.append(str(int(s.get_illuminance())))
            for l in self.lightList:
                self.csv_list.append(str(int(l.get_luminosity())))
            self.csv_writer.writerow(self.csv_list)

            # 変動後回帰係数計算
            for l in self.lightList:
                pass
                l.calc_rc()
            # 次の目的関数計算
            for l in self.lightList:
                l.calc_next_objective()
            # ロールバック
            for l in self.lightList:
                if l.is_rollback():
                    l.rollback()
            update_sensors(self.lightList, self.useSensorList)
            for l in self.lightList:
                if l.is_rollback():
                    l.append_history()

        # ファイルクローズ
        self.save_csv.close()