import numpy as np
from scipy.linalg import eigh
import json
from pathlib import Path
O=Path(__file__).resolve().parent
sx=np.array([[0,1],[1,0]],complex)
sy=np.array([[0,-1j],[1j,0]],complex)
sz=np.diag([1,-1]).astype(complex)
I=np.eye(2)
def onsite(m,mu,lam): return m*np.kron(sz,I)+lam*np.kron(sx,sy)-mu*np.eye(4)
def hop(t): return -t*np.kron(sz,I)+.12j*t*np.kron(sx,sz)
def build(kind,n=48,seed=83):
 rng=np.random.default_rng(seed); H=np.zeros((4*n,4*n),complex)
 if kind==0:
  masses=np.full(n,.42); mus=np.zeros(n); lams=np.full(n,.34); bonds=np.full(n-1,.36); disorder=np.zeros(n)
 else:
  bi=(np.arange(n)//6)%2==0
  masses=np.where(bi,.42,1.1).astype(float); mus=np.where(bi,0.,.35); lams=np.where(bi,.34,.055)
  bonds=np.where(bi[:-1]==bi[1:],.36,.13); disorder=np.zeros(n)
  if kind==2:
   masses+=rng.normal(0,.15,n);mus+=rng.normal(0,.13,n);disorder=rng.normal(0,.12,n);bonds*=rng.uniform(.65,1.35,n-1)
 for i in range(n):
  H[4*i:4*i+4,4*i:4*i+4]=onsite(masses[i],mus[i]+disorder[i],lams[i])
  if i<n-1:
   b=hop(bonds[i]);H[4*i:4*i+4,4*(i+1):4*(i+2)]=b;H[4*(i+1):4*(i+2),4*i:4*i+4]=b.conj().T
 return H
names=['Bulk A7 Bi proxy','Ideal Bi/Mg superlattice proxy','Disordered Bi-Pb / Mg-Zn proxy']; results={}
for kind,name in enumerate(names):
 H=build(kind); assert np.allclose(H,H.conj().T)
 w,v=eigh(H); below=w[w<=0];above=w[w>0]
 x=np.linspace(-2.3,2.3,650);sigma=.065
 dos=np.exp(-.5*((x[:,None]-w[None,:])/sigma)**2).sum(axis=1)/(len(w)*sigma*np.sqrt(2*np.pi))
 siteweights=(abs(v.reshape(48,4,-1))**2).sum(axis=1);iprs=(siteweights**2).sum(axis=0);near=np.argsort(abs(w))[:12]
 boundary=np.array([i for i in range(48) if i%6 in (0,5)])
 T=.02;g=.45;chi=np.tanh(abs(w)/(2*T))/(2*np.maximum(abs(w),1e-12));pair=float(g*np.mean(chi))
 results[name]={'finite_size_level_gap':float(above.min()-below.max()),'dos_at_fermi':float(np.interp(0,x,dos)),'mean_near_fermi_ipr':float(iprs[near].mean()),'mean_interface_weight':float(siteweights[boundary,:][:,near].sum(axis=0).mean()),'pairing_eigenvalue':pair,'pairing_threshold_reached':pair>=1}
(O/'results.json').write_text(json.dumps({'model':'illustrative 1D 48-site 4-state/site model, not calibrated to measured bismuth or specimen','parameters':{'temperature':.02,'pairing_g':.45,'broadening':.065,'seed':83},'results':results},indent=2))
print(json.dumps(results,indent=2))
