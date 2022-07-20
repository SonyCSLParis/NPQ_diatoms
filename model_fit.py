import numpy as np
from scipy.optimize import curve_fit
import data_gen as dg

def func_full(I, ke_A, ke_alpha, kd_A1, Ek, n):
   kd_A2 = .5
   I1 = 0.1
   I2 = Ek
   I50NPQ = 2*Ek
   #n = 4
   ke = ke_A*(1-ke_alpha*np.exp(-Is/I1))*np.exp(-Is/I2)
   kd = kd_A1 + kd_A2*I**n/(I50NPQ**n+I**n)
   DES =kd/(kd+ke)
   return DES

def func_simple(I, ke_A, kd_A1, Ek, n):
   kd_A2 = 1
   I2 = Ek
   I50NPQ = 2*Ek
   #n = 4
   ke = ke_A*np.exp(-Is/I2)
   kd = kd_A1 + kd_A2*I**n/(I50NPQ**n+I**n)
   DES =kd/(kd+ke)
   return DES

def func_simple_no_Ek(I, ke_A, kd_A1, n):
   kd_A2 = 1
   I2 = 100
   I50NPQ = 200
   #n = 4
   ke = ke_A*np.exp(-Is/I2)
   kd = kd_A1 + kd_A2*I**n/(I50NPQ**n+I**n)
   DES =kd/(kd+ke)
   return DES

def func_simple2(I, ke_A, kd_A1, I50NPQ, I2, n):
   kd_A2 = 0.5
   #I2 = 100
   #I50NPQ = 2*Ek
   #n = 4
   ke = ke_A*np.exp(-Is/I2)
   kd = kd_A1 + kd_A2*I**n/(I50NPQ**n+I**n)
   DES =kd/(kd+ke)
   return DES


def gen_data(N=100, mode="simple"):
    ETR_max = 250 #vb6f
    Ek = 100
    sII = 5
    Fm = 1
    LHCX = 1

    ke_params = {"A": 1, "alpha": 0.5, "I1": 100}
    ke_params_full = {"A": 1, "alpha": 0.5, "I1": .1, "I2": Ek}
    kd_params = {"A1": 0.05, "A2": .5, "I50NPQ": 200, "n": 4}

    Is =np.linspace(0.1,500,N)
    if mode=="simple": NPQs = dg.NPQ_simple(Is, ke_params, kd_params, LHCX)
    else: NPQs = dg.NPQ_full(Is, ke_params_full, kd_params, LHCX)

    ETRs   = dg.ETR(Is, ETR_max, Ek)
    phiIIs = dg.phiII(Is, ETRs, sII)
    Fmps = dg.Fmp(NPQs, Fm)
    Fps = dg.Fp(phiIIs, Fmps)
    return Is, Fmps, Fps, NPQs

#ke_A, kd_A1, Ek, n
# ke_A, ke_alpha, kd_A1, Ek, n
for i in range(10):
   N=2+i*20
   Is, Fmps, Fps, NPQs = gen_data(N, "full")
   #NPQs+=np.random.normal(0, 0.02, len(NPQs))#*NPQs
   try:
      popt_1, pcov_1 = curve_fit(func_full, Is, NPQs, method= "dogbox", bounds=([0.5, 0, 0, 10, 1], [10, 1, .5, 500, 10]))
      #popt_1, pcov_1 = curve_fit(func_full, Is, NPQs, method= "trf")
      print("N: ", N, np.diag(pcov_1).sum(), "-", popt_1)
      #ke_fit_1 ={"A": popt_1[0], "I1": .1, "I2": popt_1[3]}  
      #kd_fit_1 = {"A1": popt_1[1], "A2": 1, "I50NPQ": popt_1[3]*2, "n": popt_1[3]}
   except:
      pass

#Is, Fmps, Fps, NPQs = gen_data(1000, "full")
#popt_2, pcov_2 = curve_fit(func_full, Is, NPQs, method= "dogbox")