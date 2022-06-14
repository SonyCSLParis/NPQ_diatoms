import numpy as np
from scipy.optimize import curve_fit
import data_gen as dg

ETR_max = 250 #vb6f
Ek = 100
sII = 5
Fm = 1
LHCX = 1

ke_params = {"A": 1, "alpha": 0.5, "I1": 100}
kd_params = {"A1": 0.05, "A2": .5, "I50NPQ": 200, "n": 4}

Is =np.linspace(0,500,100)
NPQs = NPQ(Is, ke_params, kd_params, LHCX)

ETRs   = ETR(Is, ETR_max, Ek)
phiIIs = phiII(Is, ETRs, sII)
Fmps = Fmp(NPQs, Fm)
Fps = Fp(phiIIs, Fmps)


pl.subplot(221)
pl.plot(Is, ETRs)
pl.title("ETR")
pl.subplot(222)
pl.plot(Is, phiIIs)
pl.title(r"$\phi_{II}$")
pl.subplot(223)
pl.plot(Is, NPQs)
pl.title("NPQ")
pl.subplot(224)
pl.plot(Is, Fps, 'r', label="F'")
pl.plot(Is, Fmps, 'b', label='Fm')
pl.savefig("data_test.png")
