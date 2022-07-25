import numpy as np
import matplotlib.pyplot as pl
from scipy.optimize import curve_fit

def ETR(I, ETR_max, Ek):
 return ETR_max*(1- np.exp(-I/Ek))

def phiII(I, ETR, sII):
   return ETR/(sII*I) 

def Fmp(NPQ, Fm):
   return Fm/(NPQ+1)

def Fp(phiII, Fmp):
   return (1-phiII)*Fmp

def NPQ_simple(I, ke_params, kd_params, LHCX):
   kes = ke_params["A"]*np.exp(-I/ke_params["I1"])
   kds = kd_params["A1"] + kd_params["A2"]*I**kd_params["n"]/(kd_params["I50NPQ"]**kd_params["n"]+I**kd_params["n"])
   DESs = kds/(kds+kes)
   print(kes+kds)
   print(DESs)
   return LHCX*DESs

def NPQ_good(I, ke_params, kd_params, LHCX):
   kes = ke_params["A"]*(1-ke_params["alpha"]*np.exp(-10*I/ke_params["I1"]))*np.exp(-I/ke_params["I1"])
   kds = kd_params["A1"] + kd_params["A2"]*I**kd_params["n"]/(kd_params["I50NPQ"]**kd_params["n"]+I**kd_params["n"])
   DESs = kds/(kds+kes)
   print(kes+kds)
   print(DESs)
   return LHCX*DESs
   
ke_params = {"A": 1, "alpha": 0.8, "I1": 100}
kd_params = {"A1": 0.05, "A2": .5, "I50NPQ": 200, "n": 4}
LHCX=1
sII=5
Fm=1
NPQ500 = NPQ_good(500, ke_params, kd_params, LHCX)

Is =np.linspace(1,500,100)
NPQs = NPQ_good(Is, ke_params, kd_params, LHCX)
ETRs = ETR(Is, 250, 100)
phiIIs = phiII(Is, ETRs, sII)
Fmps = Fmp(NPQs, Fm)
Fps = Fp(phiIIs, Fmps)
#pl.plot(Is,NPQs)
#pl.plot(Is,Fmps)
#pl.plot(Is,Fps)

Af = np.zeros([100,100])
Afm = np.zeros([100,100])


def NPQ_relax(I, t, ke_params, kd_params, LHCX):
   NPQ2 = NPQ_good(I, ke_params, kd_params, LHCX)
   kes = ke_params["A"]*(1-ke_params["alpha"]*np.exp(-10*I/ke_params["I1"]))*np.exp(-I/ke_params["I1"])
   kds = kd_params["A1"] + kd_params["A2"]*I**kd_params["n"]/(kd_params["I50NPQ"]**kd_params["n"]+I**kd_params["n"])
   return NPQ2 + (NPQ500-NPQ2)*np.exp(-(kes+kds)*t) 
   
def Fmp_relax(I, t, ke_params, kd_params, LHCX, Fm):
    return Fm/(NPQ_relax(I, t, ke_params, kd_params, LHCX) +1)

ts =np.linspace(0,15,100)

for i in range(100):
    pl.plot(50*ts, Fmp_relax(Is[i], ts,  ke_params, kd_params, LHCX, Fm))
    Afm[i] = Fmp_relax(Is[i], ts, ke_params, kd_params, LHCX, Fm)
    Af[0:i] = Fps
print(Af)
print(Afm)


