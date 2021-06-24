import numpy as np
import matplotlib.pyplot as plt
from seaborn import set_style

set_style('darkgrid')

''' simulating a damped, driven, nonlinear pendulum'''


def f(Theta, Omega, T, A):
    """ damped, driven, nonlinear d(omega)/dt. Amplitude is now a variable"""
    k = 0.5
    phi = 0.66667
    return -np.sin(Theta) - k * Omega + A * np.cos(phi * T)


def Runge_Kutta_algorithm(Theta, Omega, A, transient, a):
    """ creates a lists of theta, omega and t using the Runge-kutta method for a time interval starting at 0 and
        incremented by 0.01 (20000 + transient) times. Inputs are initial conditions for omega and theta, the driving
        amplitude, the transient which is the point where points start to be collected and a which is the offset to the
        range """
    list_of_t = []
    list_of_omega = []
    list_of_theta = []
    T = 0.0
    dt = 0.01
    for i in range(transient + 20000):
        k1a = dt * Omega
        k1b = dt * f(Theta, Omega, T, A)
        k2a = dt * (Omega + k1b / 2)
        k2b = dt * f(Theta + k1a / 2, Omega + k1b / 2, T + dt / 2, A)
        k3a = dt * (Omega + k2b / 2)
        k3b = dt * f(Theta + k2a / 2, Omega + k2b / 2, T + dt / 2, A)
        k4a = dt * (Omega + k3b)
        k4b = dt * f(Theta + k3a, Omega + k3b, T + dt, A)

        Theta = Theta + (k1a + 2 * k2a + 2 * k3a + k4a) / 6
        Omega = Omega + (k1b + 2 * k2b + 2 * k3b + k4b) / 6
        T = T + dt

        if Theta > (a + np.pi) or Theta < (a - np.pi):
            Theta -= 2 * np.pi * np.abs(Theta) / Theta

        if i > transient:
            list_of_t.append(T)
            list_of_omega.append(Omega)
            list_of_theta.append(Theta)
    return list_of_theta, list_of_omega, list_of_t


# plot graphs
initial_A = [[0.90, 5000, 0], [1.07, 5000, 0.1], [1.35, 5000, 0], [1.47, 7000, 0], [1.5, 0, 0]]
theta, omega = 3.0, 0.0
for amp, trans, aa in initial_A:
    fig, ax = plt.subplots(figsize=(8, 7), dpi=200)
    RK_theta, RK_omega, RKT = Runge_Kutta_algorithm(theta, omega, amp, trans, aa)
    ax.plot(RK_omega, RK_theta, linewidth=0.8)
    xrange = np.arange(-4, 4, 0.01)
    ax.plot(xrange, np.ones(len(xrange)) * np.pi, 'g--', linewidth=0.8)
    ax.plot(xrange, np.ones(len(xrange)) * -np.pi, 'g--', linewidth=0.8)
    ax.text(-3, 3.2, r'$\theta$ = $\pi$', color='green')
    ax.text(-3, -3.1, r'$\theta$ = -$\pi$', color='green')
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_position(('data', 0))
    ax.spines['bottom'].set_position(('data', 0))
    ax.set_xlabel(r'$\omega$', x=0.99, labelpad=-25)
    ax.set_ylabel(r'$\theta$', y=0.96, labelpad=-25, rotation=0)
    ax.set_title(f'Theta [rad] vs Omega [rad/s] A = {amp}')
    ax.set_ylim([-np.pi - 1, np.pi + 1])
    ax.set_xlim([-np.pi, np.pi])
    plt.show()
