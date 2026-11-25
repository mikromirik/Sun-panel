import math
from params import GAMMA_PANEL,PHI,I,A,ETA,TIMEZONE,LONGITUDE


def solar_height(delta, omega):
    sin_h = (math.sin(PHI) * math.sin(delta) +
             math.cos(PHI) * math.cos(delta) * math.cos(omega))
    return math.degrees(math.asin(sin_h))

def declination(day):
    return math.radians(23.45 * math.sin(math.radians(360 * (284 + day) / 365)))

def azimuth(delta,h,hour):
    sin_h = math.sin(math.radians(h))
    cos_A = ((math.sin(delta) - math.sin(PHI) * sin_h) /
             (math.cos(PHI) * math.cos(math.radians(h))))
    cos_A = max(-1, min(1, cos_A))
    A_sun = math.acos(cos_A)
    if hour > 12:
        A_sun = 2 * math.pi - A_sun
    return A_sun

def angle_of_incidence(beta,h,A_sun):
    cos_theta = (math.cos(beta) * math.sin(math.radians(h)) +
                 math.sin(beta) * math.cos(math.radians(h)) *
                 math.cos(A_sun - GAMMA_PANEL)) #
    return max(0, cos_theta)

def utc_time(hour,day):
    t_utc = hour - TIMEZONE  # TIMEZONE - Местное время
    B = math.radians(360 * (day - 81) / 365) # Положение Земли на орбите
    E = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B) # Уравнение времени, E - поправка в минутах
    t_solar = t_utc + LONGITUDE / 15 + E / 60 # LONGITUDE - Долгота
    omega = math.radians(15 * (t_solar - 12)) # Часовой угол
    return omega

def time(hour):
    hours = int(hour)
    minutes = int((hour - hours) * 60)
    return f"{int(hour):02d}:{int(minutes):02d}"
def intensity(h, I_max=I):
    return I_max * math.sin(math.radians(h))

def power(h, cos_theta, I_max=I, eta=ETA):
    return intensity(h, I_max) * A * eta * cos_theta

def ideal_power(h, I_max=I, eta=ETA):
    return intensity(h, I_max) * A * eta