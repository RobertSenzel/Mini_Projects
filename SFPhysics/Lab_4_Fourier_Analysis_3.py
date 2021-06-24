import numpy as np
import matplotlib.pylab as plt
from seaborn import set_style
set_style('darkgrid')

N = 100     # Number of samples
h = 0.1     # Sampling time


def signal(t):
    """ Signal that is sampled """
    '''w = 1
    ng = []
    for tt in t:
        ng.append(1 if 0 <= (w * tt) <= 1 else -1)
    return np.array(ng)'''
    #return np.sin(np.pi * t) + 2 * np.cos(3 * np.pi * t) + 3 * np.sin(5 * np.pi * t)
    return np.sin(3 * np.pi * t)


def Transform():
    """ Fourier transform """
    X = np.array([])
    domain = np.arange(-N/2, N/2)
    kdomain = np.arange(-N / 2, N / 2, h)
    for k in kdomain:
        term = signal(domain * h) * np.exp((-2j * np.pi * k * domain) / N)
        X = np.append(X, sum(term))
    return X


def reconstruction():
    """ back-transform """
    f = np.array([])
    domain = np.arange(-N / 2, N / 2, h)
    kdomain = np.arange(-N / 2, N / 2, h)
    for n in domain:
        term = Transform() * np.exp((2j * np.pi * n * kdomain) / N)
        f = np.append(f, (1/N) * sum(term))
    return f


# plots
domains = np.arange(-N/2, N/2)
kdomains = np.arange(-N/2, N/2, h)
fig1, ax = plt.subplots(nrows=3, figsize=(8, 8))
ax1, ax2, ax3 = ax

# signal reconstruction
ax1.plot(kdomains*h, np.real(reconstruction())*h, 'r-', label='reconstruction')
ax1.plot(domains*h, signal(domains*h), 'b.', label='signal sample points')
ax1.legend()
ax1.set_xlim([0, 1.2])
ax1.set_xlabel('time [s]')
ax1.set_title('Signal reconstruction')

# power spectrum
transform = Transform()
ax2.plot(kdomains*h, 2 * abs(transform))
ax2.set_xlabel('frequency [Hz]')
ax2.set_ylabel('power [W]')
ax2.set_title('Power spectrum')
ax2.set_xlim([0, 3.5])

# Fourier components
ax3.plot(kdomains, np.real(transform), label='real')
ax3.plot(kdomains, np.imag(transform), label='imag')
ax3.set_xlabel('n')
ax3.set_title('Fourier transform components')
ax3.legend()
plt.show()
