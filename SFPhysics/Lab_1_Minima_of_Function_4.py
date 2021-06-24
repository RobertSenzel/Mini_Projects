import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

sns.set_style('darkgrid')
''' Exercise 4'''
R = 1


def V(O, q1, q2):
    """ potential energy of two charges """
    e0 = 8.854e-12
    A = (q1 * q2) / (8 * np.pi * e0 * np.abs(R))
    return A / np.abs(np.sin(O/2))


def F(O, q1, q2):
    """ force between two charges """
    e0 = 8.854e-12
    A = (q1 * q2) / (8 * np.pi * e0 * np.abs(R))
    return -((-A/4) * np.sin(O)) / np.abs(np.sin(O/2))**3


def der_F(O, q1, q2):
    """ derivative of force between two charges """
    e0 = 8.854e-12
    A = (q1 * q2) / (8 * np.pi * e0 * np.abs(R))
    term1 = (-3 * (np.sin(O))**2) / (4 * np.abs(np.sin(O/2))**5)
    term2 = np.cos(O) / np.abs(np.sin(O/2))**3
    return -(-A/4) * (term1 + term2)


xr = np.arange(0.01, 6.28, 0.01)
fig, ax = plt.subplots(dpi=200)
ax.plot(xr, V(xr, 1, 1), label=r'V($\theta$) (J)')
ax.plot(xr, F(xr, 1, 1), label=r'F($\theta$) (N)')
ax.set_ylim([-1e11, 1e11])
ax.set_xlim([0, 6.28])
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')
ax.spines['bottom'].set_position(('data', 0))
ax.set_xlabel(r'Radians ($\theta$)', labelpad=135.0)
ax.set_title('Potential V and Force F of two equal charges confined to a ring')
ax.legend()
ax.set_xticks([0, np.pi/4, 2*np.pi/4, 3*np.pi/4, np.pi, 5*np.pi/4, 6*np.pi/4, 7*np.pi/4, 2*np.pi])
ax.set_xticklabels(['0', r'$\frac{\pi}{4}$', r'$\frac{\pi}{2}$', r'$\frac{3\pi}{4}$', r'$\pi$',
                    r'$\frac{5\pi}{4}$', r'$\frac{3\pi}{2}$', r'$\frac{7\pi}{4}$', r'$2\pi$'])
plt.show()


tol = 1e-4
rtol = 4
theta12 = 2
theta13 = 4
theta23 = theta12 - theta13
Q1, Q2, Q3 = 3, 1, 7


def total_force(th12, th13, th23):
    f1 = np.round(F(th12, Q1, Q2), -rtol)
    f2 = np.round(F(th13, Q1, Q3), -rtol)
    f3 = np.round(F(th23, Q2, Q3), -rtol)
    return f1, f2, f3


def total_potential(th12, th13, th23):
    v1 = np.abs(V(th12, Q1, Q2))
    v2 = np.abs(V(th13, Q1, Q3))
    v3 = np.abs(V(th23, Q2, Q3))
    return v1, v2, v3


condition1 = (abs(F(theta13, Q1, Q3) + F(theta23, Q2, Q3)) > tol)
condition2 = (abs(F(theta12, Q1, Q2) + F(theta23, Q2, Q3)) > tol)
while condition1 or condition2:
    theta23 = theta13 - theta12
    theta13 = theta13 - (F(theta13, Q1, Q3) + F(theta23, Q2, Q3))/(der_F(theta13, Q1, Q3) + der_F(theta23, Q2, Q3))
    condition2 = (abs(F(theta12, Q1, Q2) + F(theta23, Q2, Q3)) > tol)
    while condition2:
        theta23 = theta12 - theta13
        theta12 = theta12 - (F(theta12, Q1, Q2) + F(theta23, Q2, Q3))/(der_F(theta12, Q1, Q2) + der_F(theta23, Q2, Q3))
        condition2 = (abs(F(theta12, Q1, Q2) + F(theta23, Q2, Q3)) > tol)
    theta23 = theta13 - theta12
    condition1 = (abs(F(theta13, Q1, Q3) + F(theta23, Q2, Q3)) > tol)
else:
    V1, V2, V3 = total_potential(theta12, theta13, theta23)
    F1, F2, F3 = total_force(theta12, theta13, theta23)
    print(f'angle 1, 2: {round(np.rad2deg(theta12))}')
    print(f'angle 1, 3: {round(np.rad2deg(theta13))}')
    print(f'angle 2, 3: {round(abs(np.rad2deg(theta13) - np.rad2deg(theta12)))}')
    print(V1, V2, V3)
    print(F1, F2, F3)

fig2, ax2 = plt.subplots(dpi=200)
xr = np.linspace(-R, R, 1000)
ax2.plot(xr, np.sqrt(R**2 - xr**2), color='grey')
ax2.plot(xr, -np.sqrt(R**2 - xr**2), color='grey')
ax2.set_ylim([-R-0.2, R+0.2])
ax2.set_xlim([-R-0.7, R+0.7])
ax2.spines['left'].set_color('black')
ax2.spines['bottom'].set_color('black')
ax2.spines['left'].set_position(('data', 0))
ax2.spines['bottom'].set_position(('data', 0))
ax2.plot(R, 0, 'r.', markersize=20)
ax2.plot(R * np.cos(theta12), R * np.sin(theta12), 'g.', markersize=20)
ax2.plot(R * np.cos(theta13), R * np.sin(theta13), 'b.', markersize=20)
ax2.text(R + 0.1, 0.1, f'$q_1$={Q1}C', color='red')
ax2.text(R * np.cos(theta12) + 0.1, R * np.sin(theta12) + 0.1, f'$q_2$={Q2}C', color='green')
ax2.text(R * np.cos(theta13) + 0.1, R * np.sin(theta13) + 0.1, f'$q_3$={Q3}C', color='blue')
ax2.set_title('Three charges confined to a ring')
ax2.text(-1.7, 1, fr'$\theta$ from $q_1$ to $q_2$: {round(np.rad2deg(theta12), 2)}$^\circ$')
ax2.text(-1.7, 0.8, fr'$\theta$ from $q_1$ to $q_3$: {round(np.rad2deg(theta13), 2)}$^\circ$')
plt.show()
