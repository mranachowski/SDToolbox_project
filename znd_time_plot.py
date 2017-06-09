import matplotlib as mpl
mpl.use("pgf")
pgf_with_rc_fonts = {
    "font.family": "serif",
    "font.serif": [],                   # use latex default serif font
}
mpl.rcParams.update(pgf_with_rc_fonts)
import matplotlib.pylab as plt
import numpy as np

time = np.genfromtxt('znd_time.csv', delimiter=';')

plt.plot(time[:, 0], time[:, 1], linestyle='-', color='black')
plt.xlabel('$\Phi$')
plt.ylabel('$t_{ind}\ [s]$')
plt.tight_layout()
plt.savefig('zdn_time.pdf')
