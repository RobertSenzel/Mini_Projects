import numpy as np
import matplotlib.pyplot as plt
from seaborn import set_style

set_style('darkgrid')

''' simulating a damped nonlinear pendulum'''


def f(Theta, Omega, T):
    """ damped nonlinear d(omega)/dt """
    k = 0.5
    phi = 0.66667
    A = 0.0
    return -np.sin(Theta) - k * Omega + A * np.cos(phi * T)


def Runge_Kutta_algorithm(Theta, Omega):
    """ creates a lists of theta and omega using the Runge kutta method for a time interval starting at 0 and
        incremented by 0.01 3000 times. Inputs are initial conditions for omega and theta """
    list_of_t = []
    list_of_omega = []
    list_of_theta = []
    T = 0.0
    dt = 0.01
    for i in range(3000):
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
           by 0.01 3000 times. Inputs are initial conditions for omega and theta and the """
    list_of_t = []
    list_of_omega = []
    list_of_theta = []
    T = 0.0
    Dt = 0.01
    for i in range(3000):
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


theta, omega = 3.0, 0.0
# get data
RK_theta, RK_omega, RKT = Runge_Kutta_algorithm(theta, omega)
Tr_theta, Tr_omega, TrT = trapezoid_rule(theta, omega)

# plot graphs
fig, axis = plt.subplots(nrows=2, dpi=200)
fig.suptitle(r'Initial conditions: $\theta_0$=3.0, $\omega_0$=0.0')
ax1, ax2 = axis
ax1.plot(RKT, RK_theta, color='blue', label='Runge-Kutta')
ax1.plot(TrT, Tr_theta, color='red', label='Trapezoid', linestyle=(0, (5, 5)))
ax2.plot(RKT, RK_omega, color='purple', label='Runge-Kutta')
ax2.plot(TrT, Tr_omega, color='orange', label='Trapezoid', linestyle=(0, (5, 5)))
for ax in axis:
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_position(('data', 0))
    ax.spines['bottom'].set_position(('data', 0))
    ax.set_xlim([0, 30])
    ax.set_xlabel(f't', x=0.99, labelpad=-25)
    ax.set_ylabel(r'$\theta$' if ax == ax1 else r'$\omega$', rotation=0)
    ax.set_title('theta [rad] versus time [s]' if ax == ax1 else 'omega [rad/s] versus time [s]')
    ax.set_ylim([-3, 3] if ax == ax1 else [-1.5, 1.5])
    ax.legend()
plt.show()
