import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

sns.set_style('darkgrid')


''' Exercise 2'''


def function(x):
    """ x^2 + 4x - 12 """
    return x**2 + 4*x - 12


def derivative(x):
    """ 2x + 4 """
    return 2*x + 4


xr = np.arange(-9.0, 5.0, 0.2)

fig1, ax1 = plt.subplots(dpi=200)
ax1.plot(xr, function(xr), label='f(x) = $x^2$ + 4x - 12')
ax1.plot(xr, derivative(xr), label="f'(x) = 2x + 4")
ax1.spines['left'].set_color('black')
ax1.spines['bottom'].set_color('black')
ax1.spines['top'].set_color('None')
ax1.spines['right'].set_color('None')
ax1.spines['left'].set_position(('data', 0))
ax1.spines['bottom'].set_position(('data', 0))
ax1.set_ylim([-21, 21])
ax1.legend()
ax1.set_title("f(x), f'(x) and first root estimate")

x1 = 1
x1 = x1 - function(x1)/derivative(x1)

ax1.plot(x1, function(x1), 'r.', markersize=10)
ax1.text(2.5, 2, '$x_1$, f($x_1$)', fontsize=10, color='red')
ax1.set_xlabel('X', x=0.99, labelpad=-25)
ax1.set_ylabel('Y', y=0.97, labelpad=-30, rotation=0)
plt.show()


def newton_raphson_method(tolerance):
    X1 = 3        # to find first root
    # X1 = -4     # to find second root
    nsteps = 0
    while abs(function(X1)) > tolerance:
        nsteps += 1
        X1 = X1 - function(X1) / derivative(X1)
    else:
        print('X1:', X1)
        print('f(X1):', function(X1))
        print('nsteps:', nsteps, '\n')
        return nsteps


tol = 0.0001
newton_raphson_method(tol)

tols = [10**-x for x in range(2, 18)]
total_steps = list(map(newton_raphson_method, tols))

fig2, ax2 = plt.subplots(dpi=200)
ax2.plot(np.log10(tols), total_steps, 'b.-', markerfacecolor='red', markersize=10)
ax2.set_title('Newton-Raphson method: n_steps Vs. tolerance')
ax2.set_xlabel('log(tolerance)')
ax2.set_ylabel('n_steps')
plt.show()

