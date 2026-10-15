import numpy as np, json
from pathlib import Path
import matplotlib.pyplot as plt
p=Path(__file__).parent
kB=8.617333262145e-5
Tc=0.00053
n_cm=3e17
hbar=1.054571817e-34
me=9.1093837139e-31
q=1.602176634e-19
kF=(3*np.pi**2*n_cm*1e6)**(1/3)
masses=[0.01,0.05,0.1,1.0]
fermi=[hbar**2*kF**2/(2*(m*me))/q for m in masses]
cutoffs_mev=[0.1,1,10]
rows=[]
for cutoff in cutoffs_mev:
 lam=1/np.log(1.13*(cutoff/1000)/(kB*Tc))
 rows.append({'cutoff_meV':cutoff,'effective_dimensionless_lambda_to_reproduce_Tc':lam})
fig,ax=plt.subplots(figsize=(8,5))
lambdas=np.linspace(.04,.18,250)
for c in cutoffs_mev:
 temperatures=1.13*(c/1000)/kB*np.exp(-1/lambdas)
 ax.semilogy(lambdas,temperatures*1000,label=f'Cutoff {c:g} meV')
ax.axhline(Tc*1000,linestyle='--',color='black',label='Observed bulk Bi 0.53 mK')
ax.set(xlabel='Effective dimensionless pairing coupling λ',ylabel='Predicted Tc (mK)',title='Bulk Bi: conditional weak-coupling calibration')
ax.set_ylim(1e-5,1e3);ax.grid(alpha=.25);ax.legend();fig.tight_layout()
fig.savefig(p/'calibration.png',dpi=180)
result={'status':'bulk experimentally anchored; interface not calibrated','experimental':{'bulk_Tc_K':Tc,'bulk_carrier_density_cm3':n_cm},'derived':{'kF_single_spherical_pocket_m_inverse':kF,'effective_mass_sensitivity':[{'mstar_over_me':m,'EF_meV':f*1000} for m,f in zip(masses,fermi)],'cutoff_sensitivity':rows},'caveats':['Tc and density are measured bulk values, not specimen values','effective masses and cutoff values are sensitivity assumptions, not measurements of this specimen','single spherical pocket approximation is not the multivalley Bi band structure','weak-coupling formula is a phenomenological inversion; bismuth is nonadiabatic','no measured interface hopping, strain, alloy disorder, or Eliashberg spectral function supplied','cannot predict heterostructure Tc without independent interface data']}
(p/'results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
