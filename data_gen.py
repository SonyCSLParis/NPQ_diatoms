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
   return LHCX*DESs

def NPQ_good(I, ke_params, kd_params, LHCX):
   kes = ke_params["A"]*(1-ke_params["alpha"]*np.exp(-20*I/ke_params["I1"]))*np.exp(-I/ke_params["I1"])
   kds = kd_params["A1"] + kd_params["A2"]*I**kd_params["n"]/(kd_params["I50NPQ"]**kd_params["n"]+I**kd_params["n"])
   DESs = kds/(kds+kes)
   return LHCX*DESs
#test