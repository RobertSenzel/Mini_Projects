import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import sys

sns.set_style('darkgrid')
density = 2e3  # kg/m^3
diameter = 0.01


def linear_traj(speed, angle, mass, vacuum=False):
    """ simulates a falling object using a numerical solution returns values (x, y) coordinates, using
           linear dependent air resistance"""
    g = 9.81  # m/s^2
    b = 1.6e-4 * diameter if not vacuum else 0
    Vx = speed * np.cos(np.deg2rad(angle))  # m/s
    Vy = speed * np.sin(np.deg2rad(angle))  # m/s
    Yx = 0
    Yy = 0
    t = 0  # s
    dt = 0.001  # s

    yx_list = []
    yy_list = []
    while Yy >= 0:
        yx_list.append(Yx)
        yy_list.append(Yy)
        dVy = - g * dt - (b / mass) * Vy * dt
        dVx = - (b / mass) * Vx * dt
        Vx += dVx
        Vy += dVy
        dyx = Vx * dt
        dyy = Vy * dt
        Yx += dyx
        Yy += dyy
        t += dt

    return yx_list, yy_list


def quadratic_traj(speed, angle, mass):
    """ simulates a falling object using a numerical solution returns values (x, y) coordinates, using
           quadratic dependent air resistance"""
    g = 9.81  # m/s^2
    c = 0.25 * diameter ** 2
    Vx = speed * np.cos(np.deg2rad(angle))  # m/s
    Vy = speed * np.sin(np.deg2rad(angle))  # m/s
    Yx = 0
    Yy = 0
    t = 0  # s
    dt = 0.001  # s

    yx_list = []
    yy_list = []
    while Yy >= 0:
        yx_list.append(Yx)
        yy_list.append(Yy)
        dVy = - g * dt - (c / mass) * speed * Vy * dt
        dVx = - (c / mass) * speed * Vx * dt
        Vx += dVx
        Vy += dVy
        dyx = Vx * dt
        dyy = Vy * dt
        Yx += dyx
        Yy += dyy
        t += dt

    return yx_list, yy_list


fig, ax = plt.subplots(nrows=3, ncols=3, dpi=300, figsize=(11, 12))
row1, row2, row3 = ax
ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9 = row1[0], row1[1], row1[2], row2[0], row2[1], \
                                              row2[2], row3[0], row3[1], row3[2]
data_list = [[4, 70, 1e-6, ax1], [2, 70, 1e-6, ax2], [1, 70, 1e-6, ax3],
             [4, 70, 1e-5, ax4], [2, 70, 1e-5, ax5], [1, 70, 1e-5, ax6],
             [4, 70, 1e-4, ax7], [2, 70, 1e-4, ax8], [1, 70, 1e-4, ax9]]
for data in data_list:
    Speed, Angle, Mass, ax = data
    if Speed * diameter < 10**-2:
        print('quadratic term is not dominant')
        sys.exit()

    linear_data = linear_traj(Speed, Angle, Mass)
    quadratic_data = quadratic_traj(Speed, Angle, Mass)
    vacuum_data = linear_traj(Speed, Angle, Mass, vacuum=True)
    ax.plot(linear_data[0], linear_data[1], color='blue', label='linear term', linestyle=(3, (3, 3)))
    ax.plot(quadratic_data[0], quadratic_data[1], 'r', label='quadratic term')
    ax.plot(vacuum_data[0], vacuum_data[1], color='orange', label='vacuum',  linestyle=(0, (3, 3)))
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    circ = r'$^\circ$'
    ax.set_title(f'initial speed = {Speed}m/s,\nlaunch angle = {Angle}{circ},\nmass = {Mass:.3}kg')
    ax.legend()
plt.show()
