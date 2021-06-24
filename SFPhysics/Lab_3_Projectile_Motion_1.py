import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

sns.set_style('darkgrid')


def air_resistance(V, D):
    """ return linear and quadratic terms """
    B = 1.6e-4  # Ns/m^2
    C = 0.25    # Ns^2/m^4
    term1 = B * D * V
    term2 = C * (D**2) * (V**2)
    return term1, term2


product_range = 10000
vel = [0.0001*x for x in range(product_range)]
dia = [0.0001*x for x in range(product_range)]
product = np.array(vel) * np.array(dia)

term1_list = []
term2_list = []
for i in range(product_range):
    term_1, term_2 = air_resistance(vel[i], dia[i])
    term1_list.append(term_1)
    term2_list.append(term_2)

fig, ax = plt.subplots(dpi=200)

ax.plot(product, term1_list, label='linear term')
ax.plot(product, term2_list, label='quadratic term')
ax.plot(product, np.array(term1_list) + np.array(term2_list), label='both terms')

ax.set_xlabel(r'Speed * Diameter [m$^2$/s]')
ax.set_title('magnitude of air resistance')
ax.set_ylabel('force [N]')
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xlim([2e-5, 1.2e-2])
ax.set_ylim([1e-9, 1e-4])
yrange = np.array([1e-9 * x for x in range(10**6)])
ax.legend(loc=9)
low_limit = 5e-5
upp_limit = 9e-3
ax.plot(np.ones(len(yrange)) * low_limit, yrange, linestyle='-', linewidth=0.5, color='black')
ax.plot(np.ones(len(yrange)) * upp_limit, yrange, linestyle='-', linewidth=0.5, color='black')

plt.show()

baseball = 5 * 0.07     # quadratic only
oil = 5e-5 * 1.5e-6     # linear only
rain = 1 * 0.001        # both terms
