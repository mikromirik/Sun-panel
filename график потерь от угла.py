import numpy as np
import matplotlib.pyplot as plt

from solar import *
from params import *


delta = declination(DAY)

def energy_for_beta(beta_deg):
    beta = math.radians(beta_deg)
    sum_day = 0
    ideal_day = 0
    for hour in np.arange(0, 24.25, DT):
        omega = utc_time(hour, DAY)
        h = solar_height(delta, omega)
        if h > -0.8:
            A_sun = azimuth(delta, h, hour)
            cos_theta = angle_of_incidence(beta, h, A_sun)
            cos_theta = max(0, cos_theta)
            sum_day += power(h, cos_theta)
            ideal_day += ideal_power(h)
    E_day = sum_day * DT
    E_ideal = ideal_day * DT
    return E_day, E_ideal

angles = list(range(0, 91, 1))
losses = []

for a in angles:
    E_day, E_ideal = energy_for_beta(a)
    loss = (E_ideal - E_day) / E_ideal * 100
    losses.append(loss)
    print(f"Угол {a}°: потери {round(loss, 2)}%")
print(f'Лучший угол: {angles[losses.index(min(losses))]}°')


fig, ax = plt.subplots(figsize=(11, 6.5), dpi=150)

best_idx = int(np.argmin(losses))
best_angle = angles[best_idx]
best_loss = losses[best_idx]

ax.plot(
    angles, losses,
    linewidth=2.8,
    color="#C0392B",
    solid_capstyle="round",
    label="Расчётные потери"
)

marker_idx = np.arange(0, len(angles), 5)
if marker_idx[-1] != len(angles) - 1:
    marker_idx = np.append(marker_idx, len(angles) - 1)
ax.scatter(
    np.array(angles)[marker_idx],
    np.array(losses)[marker_idx],
    s=24, color="#C0392B", zorder=4
)

ax.scatter(
    [best_angle], [best_loss],
    s=75, color="#1F618D", zorder=5,
    edgecolor="white", linewidth=1.4
)
ax.axvline(best_angle, color="#1F618D", linestyle="--", linewidth=1.2, alpha=0.7)
ax.annotate(
    f"Оптимальный угол: {best_angle}°\nПотери: {best_loss:.2f}%",
    xy=(best_angle, best_loss),
    xytext=(14, 18),
    textcoords="offset points",
    fontsize=10,
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="0.75", alpha=0.95),
    arrowprops=dict(arrowstyle="->", color="0.35", lw=1.0)
)

ax.set_xlabel("Угол наклона панели, °", fontsize=11)
ax.set_ylabel("Потери энергии, %", fontsize=11)
ax.set_title(
    f"Зависимость суточных потерь энергии от угла наклона\n"
    f"День {DAY}",
    fontsize=14, fontweight="bold", pad=12
)

ax.set_xlim(0, 90)
ax.set_xticks(np.arange(0, 91, 10))
ax.set_ylim(bottom=0)
ax.grid(True, which="major", linestyle="--", linewidth=0.7, alpha=0.35)
ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.18)
ax.minorticks_on()
ax.legend(loc="best", frameon=True, framealpha=0.9)

fig.tight_layout()
fig.savefig("loss_vs_angle.png", dpi=300, bbox_inches="tight")
plt.show()
print("График сохранён: loss_vs_angle.png")
