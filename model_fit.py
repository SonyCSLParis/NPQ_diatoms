import numpy as np
from scipy.optimize import curve_fit
import data_gen as dg

def func(I, ke_A, ke_I1, kd_A1, Ek, LHCX, n):
   kd_A2 = 1
   I1 = 0.1
   I2 = Ek
   I50NPQ = 2*Ek
   #n = 4
   ke = ke_A1*(1-ke_alpha*np.exp(-Is/I1))*np.exp(-Is/I2)
   kd = kd_A1 + kd_A2*I**n/(I50NPQ**n+I**n)
   DES =kd/(kd+ke)
   return LHCX*DES

def gen_data():
    ETR_max = 250 #vb6f
    Ek = 100
    sII = 5
    Fm = 1
    LHCX = 1

    ke_params = {"A": 1, "alpha": 0.5, "I1": 100}
    kd_params = {"A1": 0.05, "A2": .5, "I50NPQ": 200, "n": 4}

    Is =np.linspace(0,500,100)
    NPQs = dg.NPQ_simple(Is, ke_params, kd_params, LHCX)

    ETRs   = dg.ETR(Is, ETR_max, Ek)
    phiIIs = dg.phiII(Is, ETRs, sII)
    Fmps = dg.Fmp(NPQs, Fm)
    Fps = dg.Fp(phiIIs, Fmps)
    return Fmps, Fps

Fmps, Fps = gen_data()

#func should be modified to fit fluo data
#popt_1, pcov_1 = curve_fit(func, Is, DESs, method= "dogbox")
