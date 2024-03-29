import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


# Define the function
# spring 'constant' of the rope, calculated as E*A/L
E = 960  # N/mm*2
A = (4./2)**2 * np.pi  # [mm*2]
L = 8000  # [mm]
kr = E*A/L
# kr = 0.8  # [N/mm]
print(f"Using rope spring constant of {round(kr, 2)} N/mm")
m = 35  # [kg]
g = 9.81  # [m/s^2]
stair_angle = 38*np.pi/180  # [rad]
mu_moving = 0.05  # friction of moving plate on stairs
F = m*g*(np.sin(stair_angle) + mu_moving * np.cos(stair_angle))  # [N]
mu_winch = 0.18
theta = 5.5 * 2*np.pi  # [rad]
exp_mu_theta = np.exp(mu_winch*theta)
alpha = 1.1

def T(ks, dxs):
    return ks/2*dxs - 4*kr/(ks+4*kr)*(-F + ks/2*dxs + 2*kr*dxs) + 2*dxs

def f(ks, dxs):
    return T(ks, dxs) - alpha * exp_mu_theta/(1-exp_mu_theta) * F

# Plot the function
ks = np.linspace(0.1, 10, 100)  # [N/mm]
dxs = np.linspace(1, 50, 100)  # [mm]
X, Y = np.meshgrid(ks, dxs)
Z = f(X, Y)

### Solution 1 ###
soln1_ks = 4*(kr-1)
soln1_dxs = 8*F*kr/(16*(kr-1)**2 + 16*(kr-1)*kr)
# KKT conditions
phi_squared1 = f(soln1_ks, soln1_dxs)
eta_squared1 = (soln1_ks/2 + 2*kr)*soln1_dxs - F
soln1_L = round(T(soln1_ks, soln1_dxs), 2)
print(f"Solution 1: ks: {soln1_ks} N/mm, delta_x_s: {np.round(soln1_dxs, 4)} with KKT conditions phi**2 = {np.round(phi_squared1, 2)} > 0 and eta**2 = {np.round(eta_squared1, 2)} > 0, Langrangian = Tension: {soln1_L}")

# ### Plot solution 1 using variable kr
# kr = np.linspace(2, 10, 100)  # [N/mm]
# soln1_ks = 4*(kr-1)
# soln1_dxs = 8*F*kr/(16*(kr-1)**2 + 16*(kr-1)*kr)
# fig = plt.figure()
# ax = fig.add_subplot()
# col_k = 'tab:red'
# ax.plot(kr, soln1_ks, color=col_k)
# ax.set_xlabel('kr', color=col_k)
# ax.tick_params(axis='y', labelcolor=col_k)
# ax2 = ax.twinx()
# col_d = 'tab:blue'
# ax2.plot(kr, soln1_dxs, color=col_d)
# ax2.set_ylabel('optimal dxs', color=col_d)
# ax2.tick_params(axis='y', labelcolor=col_d)
# fig.tight_layout()
# plt.show()

### Solution 3 ###
soln3_ks = 2*(F - 2*(kr+1))
soln3_dxs = F/(F-2)
# KKT conditions
phi_squared3 = f(soln3_ks, soln3_dxs)
eta_squared3 = (soln3_ks/2 + 2*kr)*soln3_dxs - F
nu3 = (F-4*kr)/(F-2)
soln3_L = round(T(soln3_ks, soln3_dxs) - nu3 * ((soln3_ks/2 +2*kr)*soln3_dxs - F), 2)
print(f"Solution 3: ks: {soln3_ks} N/mm, delta_x_s: {np.round(soln3_dxs, 4)} with KKT conditions phi**2 = {np.round(phi_squared3, 2)} > 0 and eta**2 = {np.round(eta_squared3, 2)} = 0, Langrangian: {soln3_L}, Tension: {T(soln3_ks, soln3_dxs)}")

# ### Plot solution 3 using variable kr
# kr = np.linspace(2, 10, 100)  # [N/mm]
# soln3_ks = 2*(F - 2*(kr+1))
# soln3_dxs = F/(F-2)
# fig = plt.figure()
# ax = fig.add_subplot()
# col_k = 'tab:red'
# ax.plot(kr, soln3_ks, color=col_k)
# ax.set_xlabel('kr', color=col_k)
# ax.tick_params(axis='y', labelcolor=col_k)
# ax2 = ax.twinx()
# col_d = 'tab:blue'
# ax2.plot(kr, [soln3_dxs,]*100, color=col_d)
# ax2.set_ylabel('optimal dxs', color=col_d)
# ax2.tick_params(axis='y', labelcolor=col_d)
# fig.tight_layout()
# plt.show()

### Solution 4 ###
soln4_ks = (4 - 4*alpha * exp_mu_theta/(1-exp_mu_theta)*kr) / (alpha * exp_mu_theta/(1-exp_mu_theta) - 1)
soln4_dxs = -(alpha * exp_mu_theta/(1-exp_mu_theta) - 1)*F / (2*(kr - 1))
print(f"Solution 4: ks: {soln4_ks} N/mm, delta_x_s: {np.round(soln4_dxs, 4)}. Invalid since ks<0")

noslip = np.where(Z>5000, 5000, Z)
noslip = np.where(noslip<0, 0, noslip)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
surf = ax.plot_surface(X, Y, T(X,Y), rstride=1, cstride=1, 
                      cmap='autumn',linewidth=0, antialiased=False)
# surf = ax.plot_surface(X, Y, T(X,Y)/100, rstride=1, cstride=1, 
#                       cmap=cm.RdBu,linewidth=0, antialiased=False)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# ax.set_zlim(-100, 10000)
ax.set_xlabel('kd [N/mm]')
ax.set_ylabel('dxs [mm]')
ax.set_zlabel('f')

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()