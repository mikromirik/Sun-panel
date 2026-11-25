import numpy as np
import matplotlib.pyplot as plt

import solar
from params import *
from solar import *


beta = math.radians(BETA)

sum_theYear = 0
idealYear = 0

days_list = []
real_cum = []
ideal_cum = []

for day in range(1, 366):
    delta = declination(day)
    sum_theDay = 0
    ideal_day = 0

    for hour in np.arange(0, 24, DT):
        omega = utc_time(hour, day)
        h = solar_height(delta, omega)

        if h > -0.8:
            A_sun = solar.azimuth(delta, h, hour)
            cos_theta = angle_of_incidence(beta, h, A_sun)

            I_max = np.interp(day, [105, 180, 290, 355], [700, 1000, 500, 300], period=365)

            sum_theDay += power(h, cos_theta, I_max)
            ideal_day += ideal_power(h, I_max)

    sum_theYear += sum_theDay * DT
    idealYear += ideal_day * DT

    days_list.append(day)
    real_cum.append(sum_theYear)
    ideal_cum.append(idealYear)

print(f"\nСуммарно за год: {round(sum_theYear, 2)} Вт·ч")
print(f"Идеальный год: {round(idealYear, 2)} Вт·ч")
print(f"Потери за год: {round((idealYear - sum_theYear) / 1000, 2)} кВт·ч")
print(f"Потери в %: {round((idealYear - sum_theYear) / idealYear * 100, 2)}%")

plt.figure(figsize=(11, 5))
plt.plot(days_list, real_cum, label=f'Реальная панель ({BETA}°)', color='orange', linewidth=2)
plt.plot(days_list, ideal_cum, label='Идеальная следящая панель', color='green', linewidth=2)


season_days = [105, 180, 290, 355]
season_names = ['Весна', 'Лето', 'Осень', 'Зима']

for d, name in zip(season_days, season_names):
    plt.axvline(x=d, color='black', linestyle='--', alpha=0.6)
    plt.text(d, max(real_cum) * 0.95, name, rotation=90,
             verticalalignment='top', horizontalalignment='right',
             fontsize=10, color='black')

plt.xlabel('День года')
plt.ylabel('Накопленная энергия, Вт·ч')
plt.title('Накопленная энергия за год: реальная и идеальная панель')
plt.legend()
plt.grid(True)
plt.show()
plt.savefig('yearly_cumulative.png')
print("График сохранён: yearly_cumulative.png")