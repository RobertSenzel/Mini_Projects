import numpy as np
import matplotlib.pylab as plt
from seaborn import set_style
set_style('darkgrid')


def simpsons(a, b, nsteps, func):
    """ computes the integral of func from a to b. Divides the interval by nsteps """
    h = (b - a) / nsteps
    X = [a + j * h for j in range(1, nsteps)]
    even_terms = sum([func(x) for j, x in enumerate(X) if (j % 2 == 0)])
    odd_terms = sum([func(x) for j, x in enumerate(X) if (j % 2 != 0)])
    return (h/3) * (func(a) + func(b) + 2 * odd_terms + 4 * even_terms)


difference = abs(simpsons(0, 1, 8, np.exp) - np.e + 1)
print("Simpson's approximation:", simpsons(0, 1, 8, np.exp))
print("Analytic solution:", np.e - 1)
print('Difference:', difference)
print('%Error:', (difference * 100)/simpsons(0, 1, 8, np.exp))


def a0_coeff(func, nsteps):
    """ a0 coefficient for Fourier series """
    T = (2 * np.pi) / w
    integral = simpsons(0, T, nsteps, func)
    return (1 / T) * integral


def ak_bk_coeff(func, nsteps, k):
    """ ak and bk coefficient for Fourier series at harmonic k"""
    T = (2 * np.pi) / w

    def ak_func(t): return func(t) * np.cos(k * w * t)
    def bk_func(t): return func(t) * np.sin(k * w * t)

    ak_integral = simpsons(0, T, nsteps, ak_func)
    bk_integral = simpsons(0, T, nsteps, bk_func)
    return (2 / T) * ak_integral, (2 / T) * bk_integral


def fourier(func, K, t, nsteps):
    """ calculates the fourier series at point t with K terms"""
    sum_term = []
    a0 = a0_coeff(func, nsteps)
    print(f'a0 = {a0}') if t == 0 else None
    for k in range(1, K+1):
        ak, bk = ak_bk_coeff(func, nsteps, k)
        if t == 0:
            print(f'a{k} = {ak}') if k <= 8 else None
            print(f'b{k} = {bk}') if k <= 8 else None
        term1 = ak * np.cos(k * w * t)
        term2 = bk * np.sin(k * w * t)
        sum_term.append(term1 + term2)
    return a0 + sum(sum_term)


def functions(t):
    """ functions to be analysed """
    alpha = 3
    func_list = [np.sin(w * t),                                                     # trial 1
                 np.cos(w * t) + 3 * np.cos(2 * w * t) - 4 * np.cos(3 * w * t),     # trial 2
                 np.sin(w * t) + 3 * np.sin(3 * w * t) + 5 * np.sin(5 * w * t),     # trial 3
                 np.sin(w * t) + 2 * np.cos(3 * w * t) + 3 * np.sin(5 * w * t),     # trial 4
                 1 if 0 <= (w * t) <= np.pi else -1,                                # square wave
                 1 if 0 <= (w * t) <= (2*np.pi)/alpha else -1]                      # rectangular wave
    return func_list[4]


# plots
trange = np.arange(0, 2*np.pi, 0.01)
fig, ax = plt.subplots(nrows=2, dpi=200)
ax1, ax2 = ax
N_steps, K_terms, w = 100, 30, 1
fig.suptitle(f'rectangle wave, k = {K_terms}')
function_points, fourier_points = [], []
for tr in trange:
    print('t =', tr) if tr % 1 == 0 else None
    fourier_points.append(fourier(func=functions, K=K_terms, t=tr, nsteps=N_steps))
    function_points.append(functions(t=tr))

ax1.plot(trange, function_points, 'b-', label='function')
ax1.plot(trange, fourier_points, 'r--', label='fourier series')
ax1.legend(loc=1)

for n in range(1, K_terms+1):
    aK, bK = ak_bk_coeff(func=functions, nsteps=N_steps, k=n)
    ak_terms = [aK * np.cos(n * tr) for tr in trange]
    bk_terms = [bK * np.sin(n * tr) for tr in trange]
    ax2.plot(trange, ak_terms, color='green')
    ax2.plot(trange, bk_terms, color='orange')

for ax in [ax1, ax2]:
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['bottom'].set_position(('data', 0))
    ax.set_xlim([0, 2 * np.pi])
    ax.set_xticks([0, np.pi / 4, 2 * np.pi / 4, 3 * np.pi / 4, np.pi,
                   5 * np.pi / 4, 6 * np.pi / 4, 7 * np.pi / 4, 2 * np.pi])
    ax.set_xticklabels(['0', r'$\frac{\pi}{4}$', r'$\frac{\pi}{2}$', r'$\frac{3\pi}{4}$', r'$\pi$',
                        r'$\frac{5\pi}{4}$', r'$\frac{3\pi}{2}$', r'$\frac{7\pi}{4}$', r'$2\pi$'])
    ax.tick_params(axis='x', which='major', pad=66)
    ax.set_ylabel('Y', rotation=0)
ax2.set_xlabel(r'$\omega$t  [rad]')
ax2.legend(['$a_k$', '$b_k$'], loc=1)
plt.show()
