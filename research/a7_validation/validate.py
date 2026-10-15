import numpy as np,json
from scipy.linalg import eigh,expm
import matplotlib.pyplot as plt
from pathlib import Path
O=Path(__file__).resolve().parent
I=np.eye(2);sx=np.array([[0,1],[1,0]]);sy=np.array([[0,-1j],[1j,0]]);sz=np.diag([1,-1])
Lx=np.array([[0,0,0],[0,0,-1j],[0,1j,0]])
Ly=np.array([[0,0,1j],[0,0,0],[-1j,0,0]])
Lz=np.array([[0,-1j,0],[1j,0,0],[0,0,0]])
SOC=.75*(np.kron(Lx,sx)+np.kron(Ly,sy)+np.kron(Lz,sz))
n=24;a=4.546;c=11.862;u=.23398;d=c/6
ons=np.diag([.10,.10,-.20]);T=np.diag([-.32,-.32,-.22])
def calc(case,seed=17):
 rng=np.random.default_rng(seed);dim=6*n;H=np.zeros((dim,dim),complex)
 isbi=np.ones(n,dtype=bool) if case=='A7 Bi reference' else (np.arange(n)%8<4)
 for j in range(n):
  block=np.kron(ons,I)+SOC
  if not isbi[j]:block=np.kron(np.diag([.55,.55,.8]),I)+.08*SOC
  if case=='BiPb MgZn geometry-constrained proxy':block=block+rng.normal(0,.15)*np.eye(6)
  H[6*j:6*j+6,6*j:6*j+6]=block
  if j<n-1:
   t=T.copy() if isbi[j]==isbi[j+1] else .35*T
   if case=='BiPb MgZn geometry-constrained proxy':t=t*rng.uniform(.7,1.3)
   hop=np.kron(t,I)
   H[6*j:6*j+6,6*(j+1):6*(j+2)]=hop
   H[6*(j+1):6*(j+2),6*j:6*j+6]=hop.conj().T
 w,v=eigh(H);weights=np.abs(v.reshape(n,6,dim))**2;local=weights.sum(axis=1)
 interface=np.array([j for j in range(n) if (j>0 and isbi[j]!=isbi[j-1]) or (j<n-1 and isbi[j]!=isbi[j+1])])
 if len(interface)==0:interface=np.arange(n)
 E=np.linspace(-2.5,2.5,450);eta=.08
 ldos=np.exp(-.5*((E[None,:,None]-w[None,None,:])/eta)**2)*local[:,None,:]
 ldos=ldos.sum(axis=2)/(eta*np.sqrt(2*np.pi)*6)
 temp=.02;kernel=np.tanh(np.abs(w)/(2*temp))/(2*np.maximum(np.abs(w),1e-12))
 p=local[interface].sum(axis=0)/(6*len(interface));chi=float(np.dot(p,kernel))
 return {'w':w,'v':v,'ldos':ldos,'interface':interface,'chi':chi,'critical_g':1/chi,'E':E,'H':H,'isbi':isbi}
R={k:calc(k) for k in ['A7 Bi reference','Ideal Bi Mg layered','BiPb MgZn geometry-constrained proxy']}
fig,axs=plt.subplots(1,3,figsize=(13,4),sharex=True,sharey=True)
for ax,(name,r) in zip(axs,R.items()):
 ax.imshow(r['ldos'],origin='lower',aspect='auto',extent=[-2.5,2.5,0,n*d],cmap='magma')
 ax.axvline(0,color='cyan',lw=.7);ax.set_title(name,fontsize=9)
 ax.set_xlabel('Energy (eV, reference zero)')
axs[0].set_ylabel('Depth (Å)');fig.tight_layout();fig.savefig(O/'layer_ldos.png',dpi=180)
r=R['Ideal Bi Mg layered'];H=r['H'];w=r['w'];v=r['v']
psi=np.zeros(H.shape[0],complex);psi[0]=1
U=expm(-1j*H*.7)
unitarity=np.linalg.norm(U.conj().T@U-np.eye(len(U)),ord=np.inf)
norm=float(np.linalg.norm(U@psi))
BdG=np.block([[H,np.zeros_like(H)],[np.zeros_like(H),-H.conj()]])
X=np.block([[np.zeros_like(H),np.eye(len(H))],[np.eye(len(H)),np.zeros_like(H)]])
ph=np.linalg.norm(X@BdG.conj()@X+BdG,ord=np.inf)
socvals=np.linalg.eigvalsh(SOC)
ut=np.kron(np.eye(3),1j*sy)
tr=np.linalg.norm(ut@SOC.conj()@ut.conj().T-SOC)
report={'experimental_constraints':{'a_hex_A':a,'c_hex_A':c,'u':u,'lambda_Bi_eV':1.5,'layer_spacing_proxy_A':d,'specimen_band_width_A':'not publicly quantified here','measured_interface_LDOS':'not available'},'assumptions':{'p_only':True,'third_neighbor_Liu_Allen_full_parameterization':False,'hoppings_eV':T.diagonal().tolist(),'interface_hopping_factor':.35,'mu_reference_eV':0,'LDOS_gaussian_width_eV':.08,'pairing_T_eV':.02,'pairing_interaction':'separable toy model'},'results':{k:{'interface_ldos_mu':float(np.interp(0,r['E'],r['ldos'][r['interface']].mean(axis=0))),'pairing_chi_eV_inverse':r['chi'],'critical_g_eV':r['critical_g'],'interfaces':r['interface'].tolist()} for k,r in R.items()},'checks':{'Hermitian':bool(all(np.allclose(r['H'],r['H'].conj().T) for r in R.values())),'SOC_spectrum_eV':socvals.round(8).tolist(),'SOC_expected_eV':[-1.5,-1.5,.75,.75,.75,.75],'SOC_time_reversal_residual':float(tr),'unitary_propagation_residual':float(unitarity),'wavefunction_norm':norm,'BdG_particle_hole_residual':float(ph)}}
assert report['checks']['Hermitian'] and np.allclose(socvals,[-1.5,-1.5,.75,.75,.75,.75]) and tr<1e-10 and unitarity<1e-10 and ph<1e-10
(O/'results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
