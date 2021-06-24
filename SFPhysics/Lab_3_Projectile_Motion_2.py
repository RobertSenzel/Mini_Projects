import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error

sns.set_style('darkgrid')
density = 2e3  # kg/m^3
diameter = 1e-4  # m
m = (4 / 3) * np.pi * (diameter / 2) ** 3 * density  # kg


def numerical_vel(mass, tmax):
    """ simulates a falling object using a numerical solution returns values for velocity at time t, using
        linear dependent air resistance"""
    g = 9.81  # m/s^2
    b = 1.6e-4 * diameter  # Ns/m
    t = 0  # s
    V = 0  # m/s
    dt = 0.001  # s

    v_list = []
    t_list = []
    for i in range(int(tmax * (1 / dt))):
        v_list.append(V)
        t_list.append(t)
        dV = - g * dt - (b / mass) * V * dt
        V += dV
        t += dt

    return v_list, t_list


fig, ax = plt.subplots(dpi=200)
for M in [m, 3e-9, 5e-9, 7e-9, 9e-9]:
    list_of_v, list_of_t = numerical_vel(M, 0.4)
    ax.plot(list_of_t, list_of_v, label=f'm = {round(M, 9)}kg')
ax.set_xlabel('time [s]')
ax.set_ylabel('vertical velocity [m/s]')
ax.set_xlim([-0.01, 0.4])
ax.set_title('vertical velocity versus time')
ax.plot(list_of_t, - 9.81 * np.array(list_of_t), label='no air resistance')
ax.legend()


def analytic_vel(mass, t):
    """ analytic solution for linear dependent air resistance"""
    g = 9.81                # m/s^2
    b = 1.6e-4 * diameter   # Ns/m
    return ((mass * g)/b) * (np.exp((-b*t)/mass) - 1)


fig1, ax1 = plt.subplots(dpi=200)
for M in [m, 3e-9, 5e-9, 7e-9, 9e-9]:
    num_v, list_of_t = numerical_vel(M, 1)
    ana_v = list(map(analytic_vel, np.ones(len(list_of_t)) * M, list_of_t))
    error = mean_absolute_error(ana_v, num_v)
    ax1.plot(list_of_t, np.array(ana_v) - np.array(num_v), label=f'm = {round(M, 9)}kg, MAE = {error:.3}')
ax1.set_xlabel('time [s]')
ax1.set_ylabel('error [m/s]')
ax1.set_title('difference in analytical and numerical methods')
ax1.legend(loc=4, facecolor='white', framealpha=1)


def numerical_distance(mass):
    """ simulates a falling object using a numerical solution returns values for time to fall, using
            linear dependent air resistance"""
    g = 9.81  # m/s^2
    b = 1.6e-4 * diameter  # Ns/m
    t = 0  # s
    V = 0  # m/s
    dt = 0.01  # s
    Y = 5
    while Y > 0:
        dV = - g * dt - (b / mass) * V * dt
        V += dV
        dy = V * dt
        Y += dy
        t += dt
    return t


list_of_mass = [x*10**-8 for x in np.arange(0.1, 3, 0.1)]
list_of_time = np.array(list(map(numerical_distance, list_of_mass)))
fig2, ax2 = plt.subplots(dpi=200)
ax2.plot(list_of_mass, list_of_time, 'b.-', label='with air resistance')
mrange = np.arange(0, 4e-8, 1e-8)
ax2.plot(mrange, np.ones(len(mrange)) * np.sqrt(10/9.91), color='red', label='without air resistance (t=1.01s]')
ax2.set_ylabel('time [s]')
ax2.set_xlabel('mass [kg]')
ax2.set_title('time to fall 5m')
ax2.legend()
plt.show()
