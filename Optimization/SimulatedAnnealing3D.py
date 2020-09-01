'''
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation



def Gen_RandLine(length, dims=2):
    """
    Create a line using a random walk algorithm

    length is the number of points for the line.
    dims is the number of dimensions the line has.
    """
    lineData = np.empty((dims, length))
    lineData[:, 0] = np.random.rand(dims)
    for index in range(1, length):
        # scaling the random numbers by 0.1 so
        # movement is small compared to position.
        # subtraction by 0.5 is to change the range to [-0.5, 0.5]
        # to allow a line to move backwards.
        step = ((np.random.rand(dims) - 0.5) * 0.1)
        lineData[:, index] = lineData[:, index - 1] + step

    return lineData


def update_lines(num, dataLines, lines):
    for line, data in zip(lines, dataLines):
        # NOTE: there is no .set_data() for 3 dim data...
        line.set_data(data[0:2, :num])
        line.set_3d_properties(data[2, :num])
    return lines

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Fifty lines of random 3-D lines
data = [Gen_RandLine(1000, 3) for index in range(1)]

# Creating fifty line objects.
# NOTE: Can't pass empty arrays into 3d version of plot()
lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]

# Setting the axes properties
ax.set_xlim3d([0.0, 1.0])
ax.set_xlabel('X')

ax.set_ylim3d([0.0, 1.0])
ax.set_ylabel('Y')

ax.set_zlim3d([0.0, 1.0])
ax.set_zlabel('Z')

ax.set_title('3D Test')

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_lines, 25, fargs=(data, lines),
                                   interval=50, blit=False)

plt.show()



from mpl_toolkits import mplot3d
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm



def function(x,y):
    return 3*(1-x)**2*np.exp(-(x**2)-(y+1)**2)-10*(x/5-x**3-y**5)*np.exp(-x**2-y**2)-1/3*np.exp(-(x+1)**2-y**2)

x = np.linspace(-6, 6, 30)
y = np.linspace(-6, 6, 30)

X, Y = np.meshgrid(x, y)
Z = function(X, Y)

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                       linewidth=0, antialiased=False)

#ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       #linewidth=0, antialiased=False)
ax.scatter(1, 2, function(1,2)+1, marker='o',color='red')
ax.set_title('surface')

plt.show()
'''

import matplotlib.pyplot as plt
from itertools import count
import random
import pandas as pd
from matplotlib.animation import FuncAnimation
import numpy as np
import math


def function(x,y):
    return 3*(1-x)**2*np.exp(-(x**2)-(y+1)**2)-10*(x/5-x**3-y**5)*np.exp(-x**2-y**2)-1/3*np.exp(-(x+1)**2-y**2)


def SimulatedAnnealing(low,high,func,T):
    start=np.random.choice(np.linspace(low,high,num=10000))
    x=start*1
    y=start*1
    cur=func(x,y)
    
    for i in range(500):
        prop_x=-1000
        prop_y=-1000
        while((prop_x<low or prop_x>high) and (prop_y<low or prop_y>high)): 
            prop_x=x+np.random.normal()
            prop_y=y+np.random.normal()
           
        if func(prop_x,prop_y)>cur:
            x=prop_x
            y=prop_y
            #print("accept")
        else:
            if np.random.binomial(1, np.exp((func(prop_x,prop_y)-cur)/T), 1)==1:    
                x=prop_x
                y=prop_y              
        cur=func(x,y) 
        #print(cur)
        
        T = 0.98*T    
        
    return x,y


x1,y1= SimulatedAnnealing(-6,6,function,T=0.5)

print(x1)
print(y1)
print(function(x1,y1))