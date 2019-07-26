from honest import honest
from bobForge import bobForge
import math
import numpy

config=numpy.loadtxt("config.txt")
trials=int(config[0])
QBER=float(config[1])
transmission=float(config[2])
epsilon=float(config[3])

print("---------    NUMERICAL COMPUTATION   ---------")
p_h=honest(trials, QBER, transmission)
print("p_h ~ {}".format(p_h))
C_min=bobForge(trials, QBER, transmission)
print("C_min ~ {}".format(C_min))

g=C_min-p_h

s_a=p_h+g/4
s_v=p_h+3*g/4
print("s_a ~ {}".format(s_a))
print("s_v ~ {}".format(s_v))

L_h=-math.log(epsilon/2)/pow(s_a-p_h,2)
L_F=-math.log(epsilon)/pow(C_min-s_v,2)
L_R=-math.log(epsilon/2)/pow(s_v-s_a,2)
print("L_h ~ {}".format(L_h))
print("L_F ~ {}".format(L_F))
print("L_R ~ {}".format(L_R))

print("---------    ANALYTICAL VALUES   ---------")
Ap_h=transmission*QBER/2
AC_min=pow(transmission,2)*(QBER + 1./2)/4+transmission*(1-transmission)/4
print("p_h ~ {}".format(Ap_h))
print("C_min ~ {}".format(AC_min))

Ag=AC_min-Ap_h

As_a=Ap_h+Ag/4
As_v=Ap_h+3*Ag/4
print("s_a ~ {}".format(As_a))
print("s_v ~ {}".format(As_v))

AL_h=-math.log(epsilon/2)/pow(As_a-Ap_h,2)
AL_F=-math.log(epsilon)/pow(AC_min-As_v,2)
AL_R=-math.log(epsilon/2)/pow(As_v-As_a,2)
print("L_h ~ {}".format(AL_h))
print("L_F ~ {}".format(AL_F))
print("L_R ~ {}".format(AL_R))
