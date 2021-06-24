import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

sns.set_style('darkgrid')


''' Exercise 3'''


def V(x):
    """ interaction potential between two ions """
    c = 1.44    # eV nm
    A = 1090    # eV
    p = 0.033   # nm
    return A * np.exp(-x/p) - c/x


xr = np.arange(0.01, 1.0, 0.01)

fig1, ax1 = plt.subplots(dpi=200)
ax1.plot(xr, V(xr), label='V(x) (eV)')
ax1.spines['left'].set_color('black')
ax1.spines['bottom'].set_color('black')
ax1.spines['top'].set_color('None')
ax1.spines['right'].set_color('None')
ax1.spines['bottom'].set_position(('data', 0))
ax1.set_title('V(x) and F(x)')
ax1.set_xlim([0, 1])
ax1.set_ylim([-25, 25])
ax1.set_xlabel('x (nm)', labelpad=130)


def F(x):
    """ -V'(x) """
    c = 1.44    # eV nm
    A = 1090    # eV
    p = 0.033   # nm
    return (A/p) * np.exp(-x/p) - c/(x**2)


ax1.plot(xr, F(xr), label=r'F(x) ($\frac{eV}{nm}$)')
ax1.legend()
plt.show()


def der_F(x):
    """ -V"(x) """
    c = 1.44    # eV nm
    A = 1090    # eV
    p = 0.033   # nm
    return -(A/(p**2)) * np.exp(-x/p) + (2*c)/(x**3)


tol = 0.0001
x1 = 0.1
while abs(F(x1)) > tol:
    x1 = x1 - F(x1) / der_F(x1)
else:
    print('x1:', round(x1, 6))
    print('V(x1):', round(V(x1), 6))
    print('F(x1):', round(F(x1), 5))

''' 
    x1:     0.236054
    V(x1):  -5.247489
    F(x1):  -0.0
    
'''
