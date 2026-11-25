import numpy as np
import matplotlib.pyplot as plt

import solar
from solar import *
from params import *


beta = math.radians(BETA) # Угол наклона панели

times = []
powers = []
E_day = 0
E_ideal = 0

delta = declination(DAY)

sunrise = None
sunset = None
prev_h = None

for hour in np.arange(0, 24, DT):
    omega = utc_time(hour,DAY)
    h = solar_height(delta, omega)
    if prev_h is not None:
        if prev_h <= 0 < h and sunrise is None:
            sunrise = hour
        if prev_h > 0 >= h and sunset is None:
            sunset = hour
    prev_h = h
    if h > -0.8:
        A_sun = solar.azimuth(delta,h,hour)

        cos_theta = angle_of_incidence(beta, h, A_sun)
        E = power(h, cos_theta)
        E_ideal += ideal_power(h) * DT
        E_day += E*DT
        print(f'time: {time(hour)}, h =  {round(h,2)}°, A_sun = {round(math.degrees(A_sun),1)}°,cos_theta = {round(math.degrees(cos_theta),3)}° E = {round(E,4)}, Ideal = {round(E_ideal)}, E_Day = {round(E_day)}')
    else:
        E = 0
        print(f'time = {time(hour)} Солнце под горизонтом, h={round(h,2)},omega = {round(math.degrees(omega),2)},')

    times.append(hour)
    powers.append(E)

if sunrise:
    print(f"Восход: {time(sunrise)}")
if sunset:
    print(f"Закат: {time(sunset)}")

print(f"Энергия за день: {round(E_day, 2)} Вт·ч")
print(f"Идеальная панель: {round(E_ideal, 2)} Вт·ч")
print(f"Потери: {round((E_ideal - E_day) / E_ideal * 100, 2)}%")

fig, ax = plt.subplots(figsize=(11, 6.5), dpi=150)

ax.plot(
    times, powers,
    linewidth=2.8,
    color="#E67E22",
    solid_capstyle="round",
    label="Мощность панели"
)
ax.fill_between(times, powers, 0, color="#E67E22", alpha=0.12)

max_idx = int(np.argmax(powers))
max_time = times[max_idx]
max_power = powers[max_idx]
sun_times = [t for t, p in zip(times, powers) if p > 0]

if sun_times:
    ax.axvspan(min(sun_times), max(sun_times), color="#F5C542", alpha=0.07, zorder=0)
    ax.axvline(min(sun_times), color="0.45", linestyle="--", linewidth=1.0, alpha=0.7)
    ax.axvline(max(sun_times), color="0.45", linestyle="--", linewidth=1.0, alpha=0.7)

ax.scatter(
    [max_time], [max_power],
    s=55, color="#C0392B", zorder=5,
    edgecolor="white", linewidth=1.2
)
ax.annotate(
    f"Максимум: {max_power:.1f} Вт\n{time(max_time)} ч",
    xy=(max_time, max_power),
    xytext=(-53, -60),
    textcoords="offset points",
    fontsize=10,
    bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="0.75", alpha=0.95),
    arrowprops=dict(arrowstyle="->", color="0.35", lw=1.0)
)

ax.text(
    0.985, 0.97,
    f"Энергия за день: {E_day:.2f} Вт·ч\nПотери: {(E_ideal - E_day) / E_ideal * 100:.2f}%\n Восход {time(sunrise)}, Закат {time(sunset)}",
    transform=ax.transAxes,
    ha="right", va="top", fontsize=10,
    bbox=dict(boxstyle="round,pad=0.45", facecolor="white", edgecolor="0.8", alpha=0.95)
)

ax.set_xlabel("Местное солнечное время, ч", fontsize=11)
ax.set_ylabel("Мощность, Вт", fontsize=11)
ax.set_title(
    f"Мощность солнечной панели в течение дня {DAY}\n"
    f"Наклон панели: {math.degrees(beta):.0f}°",
    fontsize=14, fontweight="bold", pad=12
)

ax.set_xlim(0, 24)
ax.set_xticks(np.arange(0, 25, 2))
ax.set_ylim(bottom=0)
ax.grid(True, which="major", linestyle="--", linewidth=0.7, alpha=0.35)
ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.18)
ax.minorticks_on()
ax.legend(loc="upper left", frameon=True, framealpha=0.9)

fig.tight_layout()
fig.savefig("daily_power.png", dpi=300, bbox_inches="tight")
plt.show()
print("График сохранён: daily_power.png")
