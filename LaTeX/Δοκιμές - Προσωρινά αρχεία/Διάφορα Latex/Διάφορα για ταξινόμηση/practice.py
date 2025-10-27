from sympy import *
from numpy import *
import sympy as sp
import numpy as np
import random

x,y=sp.symbols("x,y")

def syst():
    row1=np.random.randint(10, size=3)
    row2=np.random.randint(10, size=3)
    equation1 = Eq(row1[0]*x-row1[1]*y,int(row1[2]))
    equation2 = Eq(row2[0]*x-row2[1]*y,int(row2[2]))
    system = Matrix((row1,row2))
    solution = solve_linear_system(system,x,y)
    var1=solution[x]
    var2=solution[y]

for i in range(5):
	syst()