import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


# Define the function
kr = 107000  # [N/mm]
m = 25  # [kg]
g = 9.81*10*3  # [mm/s^2]
stair_angle = 38*np.pi/180  # [rad]
mu_moving = 0.01  # friction of moving plate on stairs
F = m*g*(np.sin(stair_angle) + mu_moving * np.cos(stair_angle))  # [N]
mu_winch = 0.18
theta = 6 * 2*np.pi  # [rad]

def f(ks, dxs):
    return ks/2*dxs + 4*kr/(ks-4*kr)*(-F + ks/2*dxs-2*kr*dxs) - 2*dxs - np.exp(mu_winch*theta) * F

# Plot the function
ks = np.linspace(0, 200000, 1000)  # [N/mm]
dxs = np.linspace(1, 20, 100)  # [mm]
X, Y = np.meshgrid(ks, dxs)
Z = f(X, Y)

noslip = np.where(Z<0, Z, 0)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
surf = ax.plot_surface(X, Y, noslip, rstride=1, cstride=1, 
                      cmap=cm.RdBu,linewidth=1, antialiased=False)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# ax.legend()
# ax.set_zlim(-100, 1)
ax.set_xlabel('kd [N/mm]')
ax.set_ylabel('dxs [mm]')
ax.set_zlabel('f')

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()