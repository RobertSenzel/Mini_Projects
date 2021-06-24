import numpy as np
import matplotlib.pyplot as plt
from seaborn import set_style

set_style('darkgrid')


def f(Theta, Omega, T):
    """ damped, driven, nonlinear d(omega)/dt. Amplitude is now a variable"""
    k = 0.5
    phi = 0.66667
    A = 1.5
    return -np.sin(Theta) - k * Omega + A * np.cos(phi * T)


def Runge_Kutta_algorithm(Theta, Omega):
    list_of_omega = []
    list_of_theta = []
    T = 0.0
    dt = (2 * np.pi) / (1000 * 0.66667)
    for i in range(0, 1000000):
        k1a = dt * Omega
        k1b = dt * f(Theta, Omega, T)
        k2a = dt * (Omega + k1b / 2)
        k2b = dt * f(Theta + k1a / 2, Omega + k1b / 2, T + dt / 2)
        k3a = dt * (Omega + k2b / 2)
        k3b = dt * f(Theta + k2a / 2, Omega + k2b / 2, T + dt / 2)
        k4a = dt * (Omega + k3b)
        k4b = dt * f(Theta + k3a, Omega + k3b, T + dt)

        Theta = Theta + (k1a + 2 * k2a + 2 * k3a + k4a) / 6
        Omega = Omega + (k1b + 2 * k2b + 2 * k3b + k4b) / 6
        T = T + dt

        if (Theta > np.pi) or (Theta < -np.pi):
            Theta -= 2 * np.pi * np.abs(Theta) / Theta
        if i % 1000 == 0:
            # print(i, (0.66667 * T) % (2 * np.pi))
            list_of_omega.append(Omega)
            list_of_theta.append(Theta)

    return list_of_theta, list_of_omega


# plot graphs

theta, omega = 3.0, 0.0
fig, ax = plt.subplots(dpi=200)
RK_theta, RK_omega = Runge_Kutta_algorithm(theta, omega)
ax.plot(RK_omega, RK_theta, 'b.', markersize=1)
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_position(('data', 0))
ax.spines['bottom'].set_position(('data', 0))
ax.set_xlabel(r'$\omega$', x=0.99, labelpad=-25)
ax.set_ylabel(r'$\theta$', y=0.96, labelpad=-25, rotation=0)
ax.set_title(f'Theta vs Omega  A = {1.5}')
plt.show()
