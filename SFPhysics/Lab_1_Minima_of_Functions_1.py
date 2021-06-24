import sys
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

sns.set_style('darkgrid')


''' Exercise 1'''


def parabola(x):
    """ x^2 + 4x - 12 """
    return x**2 + 4*x - 12


xr = np.arange(-9.0, 5.0, 0.2)

fig1, ax1 = plt.subplots(dpi=200)
ax1.plot(xr, parabola(xr))
ax1.spines['left'].set_color('black')
ax1.spines['bottom'].set_color('black')
ax1.spines['top'].set_color('None')
ax1.spines['right'].set_color('None')
ax1.spines['left'].set_position(('data', 0))
ax1.spines['bottom'].set_position(('data', 0))
ax1.set_ylim([-21, 21])
ax1.set_title('F(x) and midpoint')


x1, x3 = -2, 8       # to find first root
# x3, x1 = -10, -4    # to find second root
if not (parabola(x1) < 0) or not (parabola(x3) > 0):
    print('x1, x3 initialised incorrectly')
    sys.exit()
else:
    x2 = 0.5 * (x1 + x3)
    f_x2 = parabola(x2)
    print(x2, f_x2)

if parabola(x2) > 0:
    x3 = x2
else:
    x1 = x2
print('x1:', x1)
print('x3:', x3)

ax1.plot(x2, parabola(x2), 'r.', markersize=10)
ax1.text(1, -10, 'f(x) = $x^2$ + 4x - 12', fontsize=13, color='blue')
ax1.text(0.1, 11, 'midpoint: ($x_2$, f($x_2$))', fontsize=10, color='red')
ax1.set_xlabel('X', x=0.99, labelpad=-25)
ax1.set_ylabel('Y', y=0.97, labelpad=-30, rotation=0)
plt.show()


def bisection_method(tolerance):
    nsteps = 0
    X1, X3 = -2, 8        # to find first root
    # X1, X3 = -4, -10    # to find second root
    X2 = 0.5 * (X1 + X3)
    while abs(parabola(X2)) > tolerance:
        nsteps += 1
        X2 = 0.5 * (X1 + X3)
        if parabola(X2) > 0:
            X3 = X2
        else:
            X1 = X2
    else:
        print('x2:', X2)
        print('f(x2):', parabola(X2))
        print('nsteps:', nsteps, '\n')
        return nsteps


tol = 0.0001
bisection_method(tol)

tols = [10**-x for x in range(3, 18)]
total_steps = list(map(bisection_method, tols))

fig2, ax2 = plt.subplots(dpi=200)
ax2.plot(np.log10(tols), total_steps, 'b.-', markerfacecolor='red', markersize=10)
ax2.set_title('Bisection Method: n_steps Vs. tolerance')
ax2.set_xlabel('log(tolerance)')
ax2.set_ylabel('n_steps')
plt.show()
