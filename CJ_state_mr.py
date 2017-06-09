import cantera as ct
import matplotlib as mpl
mpl.use("pgf")
pgf_with_rc_fonts = {
    "font.family": "serif",
    "font.serif": [],                   # use latex default serif font
    "font.sans-serif": ["DejaVu Sans"], # use a specific sans-serif font
}
mpl.rcParams.update(pgf_with_rc_fonts)
import matplotlib.pylab as plt
from SDToolbox import *

#Keybord input
Tmin = 273
Tmax = 550
Pmin = 0.5*ct.one_atm
Pmax = 10*ct.one_atm
fimin = 0.1
fimax = 4.0

#Number of iterations
npoints = 48

#Creating lists with initial parameters
Pi = np.linspace(Pmin, Pmax, npoints)
Ti = np.linspace(Tmin, Tmax, npoints)
fi = np.linspace(fimin, fimax, npoints)


#Lists for plots
cj_speed_Pressure = np.zeros((npoints, 3))
cj_speed_Temp = np.zeros((npoints, 3))
cj_speed_Phi = np.zeros((npoints, 3))


#Methane-Oxygen
#T=const and phi=const
for p, i in zip(Pi, np.linspace(0, npoints+1, npoints+1, endpoint=False, dtype=int)):
    T1 = 300
    q = 'CH4:0.5 O2:1'
    mech = 'gri30_highT.cti' #mechanism used for the process

    [cj_speed, R2] = CJspeed(p, T1, q, mech, 0)
    gas = PostShock_eq(cj_speed, p, T1, q, mech)
    Ps = gas.P/one_atm

    print ' '
    print 'CJ State'
    gas()

    print ' '
    print 'For ' + q + ' with P1 = %.2f atm & T1 = %.2f K using ' % (p/ct.one_atm, T1) + mech
    print 'CJ Speed is %.2f m/s' % cj_speed

    print 'The CJ State is %.2f atm & %.2f K' % (Ps, gas.T)

    cj_speed_Pressure[i, 0] = cj_speed
    cj_speed_Pressure[i, 1] = gas.T
    cj_speed_Pressure[i, 2] = Ps

for t, i in zip(Ti, np.linspace(0, npoints+1, npoints+1, endpoint=False, dtype=int)):
    P1 = ct.one_atm
    q = 'CH4:0.5 O2:1'
    mech = 'gri30_highT.cti' #mechanism used for the process

    [cj_speed, R2] = CJspeed(P1, t, q, mech, 0)
    gas = PostShock_eq(cj_speed, P1, t, q, mech)
    Ps = gas.P/one_atm

    print ' '
    print 'CJ State'
    gas()

    print ' '
    print 'For ' + q + ' with P1 = %.2f atm & T1 = %.2f K using ' % (P1, t) + mech
    print 'CJ Speed is %.2f m/s' % cj_speed

    print 'The CJ State is %.2f atm & %.2f K' % (Ps, gas.T)

    cj_speed_Temp[i, 0] = cj_speed
    cj_speed_Temp[i, 1] = gas.T
    cj_speed_Temp[i, 2] = Ps

print cj_speed_Temp

#T=const and T=const
for f, i in zip(fi, np.linspace(0, npoints+1, npoints+1, endpoint=False, dtype=int)):
    P1 = ct.one_atm
    T1 = 300
    no = float(1/f)
    q = 'CH4:0.5 O2:' + str(no)
    mech = 'gri30_highT.cti' #mechanism used for the process

    [cj_speed, R2] = CJspeed(P1, T1, q, mech, 0)

    gas = PostShock_eq(cj_speed, P1, T1, q, mech)
    Ps = gas.P/one_atm

    print ' '
    print 'CJ State'
    gas()

    print ' '
    print 'For ' + q + ' with P1 = %.2f atm & T1 = %.2f K using ' % (P1, T1) + mech
    print 'CJ Speed is %.2f m/s' % cj_speed

    print 'The CJ State is %.2f atm & %.2f K' % (Ps, gas.T)
    
    [ae, af] = equilSoundSpeeds(gas)

    print 'The sound speeds are: af = %.2f m/s & ae = %.2f m/s' % (af, ae)
    print ' '

    cj_speed_Phi[i, 0] = cj_speed
    cj_speed_Phi[i, 1] = gas.T
    cj_speed_Phi[i, 2] = Ps

#PLOTS
number = [0, 1, 2]
#in fucntion of pressure
fig, ax = plt.subplots()
axes = [ax, ax.twinx(), ax.twinx()]
fig.subplots_adjust(right=0.75)
axes[-1].spines['right'].set_position(('axes', 1.2))
axes[-1].set_frame_on(True)
axes[-1].patch.set_visible(False)
colors = ('darkcyan', 'red', 'navy')
paramaters = ('Detonation velocity  [m/s]', 'Temperature [K]', 'Pressure [atm]')
for ax, color, i, par in zip(axes, colors, number, paramaters):
    ax.set_ylabel('%s' % par, color=color)
    ax.tick_params(axis='y', colors=color)
    ax.plot(Pi/ct.one_atm, cj_speed_Pressure[:, i], linestyle='-', linewidth=0.7, color=color)
axes[0].set_xlabel('Initial pressure [atm]')
axes[0].xaxis.set_ticks(np.arange(0, Pmax/ct.one_atm + 1, 1))
axes[0].set_yticks(np.linspace(axes[0].get_yticks()[0], axes[0].get_yticks()[-1], len(axes[0].get_yticks())))
axes[1].set_yticks(np.linspace(axes[1].get_yticks()[0], axes[1].get_yticks()[-1], len(axes[0].get_yticks())))
plt.tight_layout()
plt.savefig('pres_plot.pdf')

number = [0, 1, 2]
#in fucntion of pressure
fig, ax = plt.subplots()
axes = [ax, ax.twinx(), ax.twinx()]
fig.subplots_adjust(right=0.75)
axes[-1].spines['right'].set_position(('axes', 1.2))
axes[-1].set_frame_on(True)
axes[-1].patch.set_visible(False)
colors = ('darkcyan', 'Red', 'navy')
paramaters = ('Detonation velocity  [m/s]', 'Temperature [K]', 'Pressure [atm]')
for ax, color, i, par in zip(axes, colors, number, paramaters):
    ax.set_ylabel('%s' % par, color=color)
    ax.tick_params(axis='y', colors=color)
    ax.plot(Ti, cj_speed_Temp[:, i], linestyle='-', linewidth=0.7, color=color)
axes[0].set_xlabel('Initial temperature [K]')
axes[0].xaxis.set_ticks(np.arange(260, Tmax, 20))
axes[0].set_yticks(np.linspace(axes[0].get_yticks()[0], axes[0].get_yticks()[-1], len(axes[0].get_yticks())))
axes[1].set_yticks(np.linspace(axes[1].get_yticks()[0], axes[1].get_yticks()[-1], len(axes[0].get_yticks())))
plt.tight_layout()
plt.savefig('temp_plot.pdf')


#in fucntion of pressure
fig, ax = plt.subplots()
axes = [ax, ax.twinx(), ax.twinx()]
fig.subplots_adjust(right=0.75)
axes[-1].spines['right'].set_position(('axes', 1.2))
axes[-1].set_frame_on(True)
axes[-1].patch.set_visible(False)
colors = ('darkcyan', 'Red', 'navy')
paramaters = ('Detonation velocity  [m/s]', 'Temperature [K]', 'Pressure [atm]')
for ax, color, i, par in zip(axes, colors, number, paramaters):
    ax.set_ylabel('%s' % par, color=color)
    ax.tick_params(axis='y', colors=color)
    ax.plot(fi, cj_speed_Phi[:, :], linestyle='-', linewidth=0.7, color=color)
axes[0].set_xlabel('$\Phi$ [-]')
axes[0].xaxis.set_ticks(np.arange(fimin-0.2, fimax+1, 1))
axes[0].set_yticks(np.linspace(axes[0].get_yticks()[0], axes[0].get_yticks()[-1], len(axes[0].get_yticks())))
axes[1].set_yticks(np.linspace(axes[1].get_yticks()[0], axes[1].get_yticks()[-1], len(axes[0].get_yticks())))
plt.tight_layout()
plt.savefig('phi_plo.pdf')


plt.plot(fi, cj_speed_Phi[:, 1]/300, linestyle='-', color='black')
plt.yticks(np.arange(0, 17, 1))
plt.ylabel('$T_2/T_1$')
plt.xlabel('$\Phi$')
plt.tight_layout()
plt.savefig('porownanie_temp.pdf')

plt.plot(fi, cj_speed_Phi[:, 2], linestyle='-', color='black')
plt.ylabel('$P_2/P_1$')
plt.xlabel('$\Phi$')
plt.yticks(np.arange(0, 70, 10))
plt.tight_layout()
plt.savefig('porownanie_pres.pdf')
