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
