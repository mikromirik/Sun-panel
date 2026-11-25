import math
# КОНСТАНТЫ

I = 1000 # интенсивность солнца
ETA = 0.2 # КПД панели
A = 1 # Площадь панели
DAY = 180 # День в году по счету
DT = 0.05 # Шаг часа
BETA = 25 # Угол наклона панели
TIMEZONE = 5 # UTC
LONGITUDE = 56 # Долгота


PHI = math.radians(58) # Географическая широта
GAMMA_PANEL = math.radians(180) if PHI > 0 else math.radians(0) # азимут панели: 180° = юг