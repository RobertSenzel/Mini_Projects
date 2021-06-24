import numpy as np
import matplotlib.pyplot as plt
from seaborn import set_style

set_style('darkgrid')

''' solving the linear and nonlinear pendulum equations '''

theta = 0.2
omega = 0.0
t = 0.0


def f_linear(Theta, Omega, T):
    """ linear d(omega)/dt """
    k = 0.0
    phi = 0.66667
    A = 0.0
    return -Theta - k * Omega + A * np.cos(phi * T)


def f_nonlinear(Theta, Omega, T):
    """ non-linear d(omega)/dt """
    k = 0.0
    phi = 0.66667
    A = 0.0
    return -np.sin(Theta) - k * Omega + A * np.cos(phi * T)


print(f_linear(theta, omega, t))
print(f_linear(1, 1, 1))
print(f_linear(0.5, 2.1, 3))
iterations = 50000


def trapezoid_rule(Theta, Omega, function):
    """ creates a lists of theta and omega using the trapezoid method for a time interval starting at 0 and incremented
        by 0.01 a 50000 times. Inputs are initial conditions for omega and theta and the d(omega)/dt """

    global iterations
    list_of_t = []
    list_of_omega = []
    list_of_theta = []
    T = 0.0
    Dt = 0.01
    iterations = 50000 if Theta != 0.2 else 100000
    for nsteps in range(iterations):
        theta_term_1 = Dt * Omega
        omega_term_1 = Dt * function(Theta, Omega, T)
        theta_term_2 = Dt * (Omega + omega_term_1)
        omega_term_2 = Dt * function(Theta + theta_term_1, Omega + omega_term_1, T + Dt)

        Theta = Theta + (theta_term_1 + theta_term_2) / 2
        Omega = Omega + (omega_term_1 + omega_term_2) / 2
        T += Dt

        list_of_t.append(T)
        list_of_omega.append(Omega)
        list_of_theta.append(Theta)
    return list_of_theta, list_of_omega, list_of_t, iterations


def plot_against_time(int_theta, int_omega):
    """ Inputs are the initial theta and omega, plots theta Vs. time and omega Vs. time for both linear and nonlinear
        pendulums"""

    l_theta, l_omega, l_t, l_n = trapezoid_rule(int_theta, int_omega, f_linear)
    nl_theta, nl_omega, nl_t, nl_n = trapezoid_rule(int_theta, int_omega, f_nonlinear)
    fig, axis = plt.subplots(nrows=4, dpi=300, figsize=(12, 8))
    ax1, ax2, ax3, ax4 = axis
    fig.suptitle(fr'Initial conditions: $\theta_0$={int_theta}, $\omega_0$={int_omega}')

    ax1.plot(l_t, l_theta, 'b-', label=r'linear $\theta$', linewidth=0.7)
    ax1.plot(nl_t, nl_theta, 'r-', label=r'nonlinear $\theta$', linewidth=0.7)
    superpos_theta = np.array(l_theta) + np.array(nl_theta)
    ax2.plot(l_t, superpos_theta, 'g-', linewidth=0.7)

    ax3.plot(l_t, l_omega, 'b-', label=r'linear $\omega$', linewidth=0.7)
    ax3.plot(nl_t, nl_omega, 'r-', label=r'nonlinear $\omega$', linewidth=0.7)
    superpos_omega = np.array(l_omega) + np.array(nl_omega)
    ax4.plot(l_t, superpos_omega, 'g-', linewidth=0.7)

    for ax in axis:
        ax.spines['left'].set_color('black')
        ax.spines['bottom'].set_color('black')
        ax.spines['left'].set_position(('data', 0))
        ax.spines['bottom'].set_position(('data', 0))
        ax.set_xlim([0, iterations / 100])
        ax.set_xlabel(f't', x=1.01, labelpad=-65)
        ax.tick_params(axis='x', which='major', pad=50)
    for ax in [ax1, ax3]:
        ax.set_title('theta [rad] versus time [s]' if ax == ax1 else 'omega [rad/s] versus time [s]')
        ax.set_ylabel(r'$\theta$' if ax == ax1 else r'$\omega$', rotation=0)
        ax.legend(loc=1, facecolor='white', framealpha=1)
    for ax in [ax2, ax4]:
        ax.set_title('superposed theta [rad] versus time [s]' if ax == ax2 else
                     'superposed omega [rad/s] versus time [s]')
        ax.set_ylabel(r'$\theta_l$ + $\theta_n$$_l$' if ax == ax2 else r'$\omega_l$ + $\omega_n$$_l$', rotation=0, y=0.6
                      )
    plt.show()


# to check that the plots of 𝜃 vs nsteps and 𝜔 vs nsteps are sinusoidal.
figure1, axis1 = plt.subplots(nrows=2, dpi=200)
axis_data = {axis1[0]: trapezoid_rule(theta, omega, f_linear), axis1[1]: trapezoid_rule(theta, omega, f_nonlinear)}
for axi in axis_data.keys():
    figure1.suptitle('fig1: linear, fig2: nonlinear')
    axi.plot(list(range(axis_data[axi][3])), axis_data[axi][1], color='purple', label='omega vs nsteps')
    axi.plot(list(range(axis_data[axi][3])), axis_data[axi][0], color='orange', label='theta vs nsteps')
    axi.set_xlim([0, 1000])
    axi.legend()
figure1.show()


# plot graphs
initial_values = [[0.2, 0.0], [1.0, 0.0], [3.1, 0.0], [0.0, 1.0]]
for theta, omega in initial_values:
    plot_against_time(theta, omega)
