import matplotlib.pyplot as plt
from itertools import count
import random
import pandas as pd
from matplotlib.animation import FuncAnimation
import numpy as np
import math

plt.style.use('fivethirtyeight')

def function(x):
    return (5*(math.sin(math.pow(x,2)/2)/math.log(x+4, 2)))


def SimulatedAnnealing(low,high,func,T):
    start=np.random.choice(np.linspace(low,high,num=10000))
    x=start*1
    cur=func(x)
    history=[x]
    for i in range(500):
        prop=-1
        while(prop<0 or prop>10): 
            prop=x+np.random.normal()
           
        if func(prop)>cur:
            x=prop
            #print("accept")
        else:
            if np.random.binomial(1, np.exp((func(prop)-cur)/T), 1)==1:    
                x=prop
              
        cur=func(x) 
        #print(cur)
        history.append(x)
        T = 0.98*T    
        
    return x,history


x=np.arange(0,10,0.0001)
y=np.array([function(t) for t in x])

x1,x_history= SimulatedAnnealing(0,10,function,T=0.5)
y_history=np.array([function(t) for t in x_history])


def animate(i):
    x_value=(x_history[i])
    y_value=(y_history[i])
    print(i)

    plt.cla()
    plt.plot(x,y)
    plt.plot(x_value,y_value,'r*')

ani = FuncAnimation(plt.gcf(),animate,frames=np.arange(500),interval=1,repeat=False)

#plt.tight_layout()
plt.show()

