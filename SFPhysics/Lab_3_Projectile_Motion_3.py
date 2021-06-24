import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

sns.set_style('darkgrid')
density = 2e3  # kg/m^3
diameter = 1e-4  # m
m = (4 / 3) * np.pi * (diameter / 2) ** 3 * density  # kg


def numerical_vel(b, angle, mass):
    """ simulates a falling object using a numerical solution returns values (x, y) coordinates, using
        linear dependent air resistance"""
    g = 9.81  # m/s^2
    Vx = np.cos(np.deg2rad(angle))  # m/s
    Vy = np.sin(np.deg2rad(angle))  # m/s
    Yx = 0
    Yy = 0
    t = 0  # s
    dt = 0.001  # s

    x_list = []
    y_list = []
    while Yy >= 0:
        x_list.append(Yx)
        y_list.append(Yy)
        dVy = - g * dt - (b / mass) * Vy * dt
        dVx = - (b / mass) * Vx * dt
        Vx += dVx
        Vy += dVy
        dyx = Vx * dt
        dyy = Vy * dt
        Yx += dyx
        Yy += dyy
        t += dt

    return x_list, y_list


air_resistance = numerical_vel(1.6e-4 * diameter, 45, m)
vacuum = numerical_vel(0, 45, m)
fig, ax = plt.subplots(dpi=200)
ax.plot(air_resistance[0], air_resistance[1], label='air resistance')
ax.plot(vacuum[0], vacuum[1], label='vacuum')
ax.legend()
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_ylim([0, 0.03])
ax.set_xlim([0, 0.11])
ax.text(0.015, 0.003, r'45$^\circ$', size=15)


angles = np.array([i for i in np.arange(0.1, 90, 0.001)])
xrange = []
for i in angles:
    xdata = numerical_vel(1.6e-4 * diameter, i, m)
    xrange.append(xdata[0][-1])
max_range = max(xrange)
print(max_range, angles[xrange.index(max_range)])


list_of_mass = [x*10**-8 for x in np.linspace(0.01, 2, 100)]
optimum_angles = []
for Mass in list_of_mass:
    angles = np.array([i for i in np.arange(10, 50, 0.01)])
    xrange = []
    for i in angles:
        xdata = numerical_vel(1.6e-4 * diameter, i, Mass)
        xrange.append(xdata[0][-1])     # appends last value in the x coordinate list which is the range
    optimum_angles.append(angles[xrange.index(max(xrange))])    # finds the corresponding angle

fig2, ax2 = plt.subplots(dpi=200)
ax2.plot(list_of_mass, optimum_angles, 'b.-')
ax2.set_xlabel('mass [kg]')
ax2.set_ylabel(r'angle [$\circ$]')
ax2.set_title('optimum launch angle')
plt.show()
