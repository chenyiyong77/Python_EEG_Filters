# First the required libraries are imported:
# * `Axes3D` allows adding 3d objects to a 2d matplotlib plot.
# * The `cm` routine contains many [colour
# maps](http://wiki.scipy.org/Cookbook/Matplotlib/Show_colormaps)
# * The `LinearLocator` and `FormatStrFormatter` methods to customize the tick
# marks on the axes.
# * The `pyplot` submodule from the **matplotlib** library, a python 2D
# plotting library which produces publication quality figures.  
# * The `numpy` library for efficient numeric-array manipulation

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

# The next code computes the points to plot a *hyperbolic paraboloid*. Two
# [sequential
# arrays](https://www.getdatajoy.com/learn/How_to_Create_Numpy_Arrays#Sequential_Arrays)
# are created with `arange()`.
x = np.arange(-5, 5, 0.25)              # points in the x axis
y = np.arange(-5, 5, 0.25)              # points in the y axis
X, Y = np.meshgrid(x, y)                # create the "base grid"
Z = X**2 - Y**2                         # points in the z axis

# Now we set up the plot. The function `plot_surface()` is the main command
# here. The parameters `rstride` and `cstride` control how much detail in the
# wireframe you get.
fig = plt.figure()
ax = fig.gca(projection='3d')               # 3d axes instance
surf = ax.plot_surface(X, Y, Z,             # data values (2D Arryas)
                       rstride=2,           # row step size
                       cstride=2,           # column step size
                       cmap=cm.RdPu,        # colour map
                       linewidth=1,         # wireframe line width
                       antialiased=True)

print("X",X)
print(np.shape(X))
print("Y",Y)
print(np.shape(Y))
print("Z",Z)
print(np.shape(Z))
# Fine-tuning the plot. Set 6 evenly spaced tick marks on the z-axis, the
# format for the tick labels and a colour bar on the right of the plot. The
# last two lines control the position of the *camera*.
ax.zaxis.set_major_locator(LinearLocator(6))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.set_title('Hyperbolic Paraboloid')        # title
fig.colorbar(surf, shrink=0.5, aspect=5)     # colour bar

ax.view_init(elev=30,azim=70)                # elevation & angle
ax.dist=8                                    # distance from the plot
plt.show()