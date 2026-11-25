import numpy as np
import matplotlib.pyplot as plt

from params import *
from solar import utc_time, declination, solar_height, azimuth, angle_of_incidence, intensity

intensity_by_day = {
    105: 700,
    180: 1000,
    290: 500,
    355: 300
}



days = [105, 180, 290, 355]
angles = list(range(0, 91, 1))


def energy_for_day(day, beta_deg):
    beta = math.radians(beta_deg)

    delta = declination(day)

    sum_day = 0
    ideal_day = 0

    for hour in np.arange(0, 24, DT):
        omega = utc_time(hour, day)
        h = solar_height(delta, omega)

        if h > 0:
            A_sun = azimuth(delta, h, hour)
            cos_theta = angle_of_incidence(beta, h, A_sun)

            I_h = intensity(h, I)
            sum_day += I_h * A * ETA * cos_theta
            ideal_day += I_h * A * ETA

    E_day = sum_day * DT
    E_ideal = ideal_day * DT
    return E_day, E_ideal


results = {}
for d in days:
    results[d] = []
    for a in angles:
        E_day, E_ideal = energy_for_day(d, a)
        loss = (E_ideal - E_day) / E_ideal * 100
        results[d].append(loss)


fig, ax = plt.subplots(figsize=(11.5, 6.8), dpi=150)

colors = ["#1F77B4", "#E67E22", "#2CA02C", "#9467BD"]

for d, color in zip(days, colors):
    values = results[d]
    min_idx = int(np.argmin(values))
    best_angle = angles[min_idx]
    best_loss = values[min_idx]

    ax.plot(
        angles, values,
        linewidth=2.5,
        color=color,
        solid_capstyle="round",
        label=f"День {d}"
    )

    ax.scatter(
        [best_angle], [best_loss],
        s=58, color=color, zorder=5,
        edgecolor="white", linewidth=1.2
    )

    ax.annotate(
        f"{best_angle}°",
        xy=(best_angle, best_loss),
        xytext=(0, -18),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        color=color,
        fontweight="bold"
    )

ax.set_xlabel("Угол наклона панели, °", fontsize=11)
ax.set_ylabel("Потери энергии, %", fontsize=11)
ax.set_title(
    "Зависимость суточных потерь от угла наклона в разные дни года",
    fontsize=14, fontweight="bold", pad=12
)

ax.set_xlim(0, 90)
ax.set_xticks(np.arange(0, 91, 10))
ax.set_ylim(bottom=0)
ax.grid(True, which="major", linestyle="--", linewidth=0.7, alpha=0.35)
ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.18)
ax.minorticks_on()

ax.legend(
    title="Расчётный день",
    loc="upper center",
    bbox_to_anchor=(0.5, 1.0),
    ncol=4,
    frameon=True,
    framealpha=0.95
)

fig.tight_layout()
fig.savefig("seasonal_losses.png", dpi=300, bbox_inches="tight")
plt.show()
print("График сохранён: seasonal_losses.png")


print("\nЛучший угол по дням:")
for d in days:
    idx = results[d].index(min(results[d]))
    print(f"день {d}: угол {angles[idx]}°, потери {round(results[d][idx], 2)}%")
