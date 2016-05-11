# テスト
for l in lightList:
    l.append_history()
for l in lightList:
    l.set_random_luminosity()

update_sensors(lightList, useSensorList)

for l in lightList:
    l.append_history()
for l in lightList:
    l.set_random_luminosity()

update_sensors(lightList, useSensorList)

for l in lightList:
    l.append_history()
    #print(l)
    l.calc_rc()
    l.calc_current_objective()
