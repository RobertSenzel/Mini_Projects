import numpy as np
import matplotlib.pyplot as plt
from seaborn import set_style

set_style('darkgrid')

''' simulating the nonlinear pendulum using the fourth order Runge-Kutta algorithm '''


def f(Theta, Omega, T):
    """ d(omega)/dt """
    k = 0.0
    phi = 0.66667
    A = 0.0
    return -np.sin(Theta) - k * Omega + A * np.cos(phi * T)


def Runge_Kutta_algorithm(Theta, Omega):
    """ creates a lists of theta and omega using the Runge kutta method for a time interval starting at 0 and
        incremented by 0.01 50000 times. Inputs are initial conditions for omega and theta """
    list_of_t = []
    list_of_omega = []
    list_of_theta = []
    T = 0.0
    dt = 0.01
    for i in range(10000):
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

        list_of_t.append(T)
        list_of_omega.append(Omega)
        list_of_theta.append(Theta)
    return list_of_theta, list_of_omega, list_of_t


def trapezoid_rule(Theta, Omega):
    """ creates a lists of theta and omega using the trapezoid method for a time interval starting at 0 and incremented
        by 0.01 50000 times. Inputs are initial conditions for omega and theta"""

    list_of_t = []
    list_of_omega = []
    list_of_theta = []
    T = 0.0
    Dt = 0.01
    for i in range(10000):
        theta_term_1 = Dt * Omega
        omega_term_1 = Dt * f(Theta, Omega, T)
        theta_term_2 = Dt * (Omega + omega_term_1)
        omega_term_2 = Dt * f(Theta + theta_term_1, Omega + omega_term_1, T + Dt)

        Theta = Theta + (theta_term_1 + theta_term_2) / 2
        Omega = Omega + (omega_term_1 + omega_term_2) / 2
        T += Dt

        list_of_t.append(T)
        list_of_omega.append(Omega)
        list_of_theta.append(Theta)
    return list_of_theta, list_of_omega, list_of_t


theta, omega = 3.14, 0.0
# get data
RK_theta, RK_omega, RKT = Runge_Kutta_algorithm(theta, omega)
Tr_theta, Tr_omega, TrT = trapezoid_rule(theta, omega)

# plot graphs
fig, [ax1, ax2] = plt.subplots(nrows=2, dpi=300, figsize=(12, 4))
ax1.plot(RKT, RK_theta, color='blue', label='Runge-Kutta', linewidth=0.7)
ax1.plot(TrT, Tr_theta, color='red', label='Trapezoid', linewidth=0.7)
ax1.legend(loc=1, facecolor='white', framealpha=1)
ax2.plot(TrT, np.array(RK_theta) + np.array(Tr_theta), color='green', linewidth=0.7)

for ax in [ax1, ax2]:
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_position(('data', 0))
    ax.spines['bottom'].set_position(('data', 0))
    ax.tick_params(axis='x', which='major', pad=50)
    ax.set_xlim([0, 100])
    ax.set_xlabel(f't', x=1.01, labelpad=-65)
    ax.set_ylabel(r'$\theta$' if ax == ax1 else r'$\theta_T$ + $\theta_R$', rotation=0, y=0.6)
    ax.set_title('theta [rad] versus time [s]' if ax == ax1 else 'superposed theta [rad] versus time [s]')
plt.show()
