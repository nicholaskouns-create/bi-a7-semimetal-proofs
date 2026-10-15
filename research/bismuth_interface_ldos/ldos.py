import numpy as np, json
from scipy.linalg import eigh
import matplotlib.pyplot as plt
from pathlib import Path
from sys import path
path.insert(0,str(Path(__file__).resolve().parents[1]/'bismuth_heterostructure'))
from run import build
out=Path(__file__).resolve().parent
E=np.linspace(-1.5,1.5,501); eta=.065; T=.02; g=.45
names=['Bulk A7 proxy','Ideal Bi/Mg proxy','Disordered Bi-Pb/Mg-Zn proxy']
fig,ax=plt.subplots(1,3,figsize=(14,4.3),sharey=True)
report={}
for kind,name in enumerate(names):
 H=build(kind);w,v=eigh(H); weights=(np.abs(v.reshape(48,4,192))**2).sum(axis=1)
 kernel=np.exp(-.5*((E[:,None]-w[None,:])/eta)**2)/(eta*np.sqrt(2*np.pi))
 ldos=weights@kernel.T/4
 interfaces=np.array([i for i in range(48) if i%6 in (0,5)])
 bulk=np.array([i for i in range(48) if i%6 in (2,3)])
 Nint=ldos[interfaces].mean(axis=0);Ninner=ldos[bulk].mean(axis=0)
 chi=np.tanh(np.abs(w)/(2*T))/(2*np.maximum(np.abs(w),1e-12))
 projected=(weights[interfaces].sum(axis=0)/len(interfaces))
 chi_int=float(np.sum(projected*chi)/4)
 gc=1/chi_int
 report[name]={'interface_ldos_EF_per_orbital_model_energy':float(np.interp(0,E,Nint)), 'interior_ldos_EF_per_orbital_model_energy':float(np.interp(0,E,Ninner)), 'interface_projected_pair_susceptibility':chi_int,'critical_g_model_units':gc,'pairing_eigenvalue_g_0.45':g*chi_int}
 ax[kind].imshow(ldos,origin='lower',aspect='auto',extent=[E[0],E[-1],0,48],cmap='magma')
 ax[kind].axvline(0,color='cyan',lw=1,ls='--');ax[kind].set(title=name,xlabel='Energy (model units)');ax[kind].set_xlim(-1,1)
ax[0].set_ylabel('Layer / site index')
fig.suptitle('Computed layer-resolved DOS: 48-site phenomenological model')
fig.tight_layout();fig.savefig(out/'ldos.png',dpi=170)
(out/'results.json').write_text(json.dumps({'status':'computed phenomenological proxy; no measured interface LDOS dataset available','model':'48 sites, 4 states/site, 1D; not Liu-Allen sp3 or DFT; no actual specimen calibration','broadening':eta,'T_model':T,'g_model':g,'results':report,'experimental_constraints':{'ORNL':'EDS composition maps and TEM morphology, not energy-resolved interface LDOS','Bi_SOC_eV_literature':1.5}},indent=2))
print(json.dumps(report,indent=2))
