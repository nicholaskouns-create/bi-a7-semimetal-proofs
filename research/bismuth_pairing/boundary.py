import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigvalsh
from pathlib import Path
import json
OUT=Path(__file__).parent
sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]],complex); sz=np.diag([1,-1]).astype(complex); I=np.eye(2)
def spectrum(kind,n=48,seed=83,disorder_scale=1.,strain=0.):
 rng=np.random.default_rng(seed); H=np.zeros((4*n,4*n),complex)
 if kind==0: masses=np.full(n,.42);mus=np.zeros(n);lams=np.full(n,.34);bonds=np.full(n-1,.36);dis=np.zeros(n)
 else:
  bi=(np.arange(n)//6)%2==0
  masses=np.where(bi,.42,1.1);mus=np.where(bi,0.,.35);lams=np.where(bi,.34,.055);bonds=np.where(bi[:-1]==bi[1:],.36,.13);dis=np.zeros(n)
  if kind==2:
   masses+=rng.normal(0,.15,n)*disorder_scale;mus+=rng.normal(0,.13,n)*disorder_scale;dis=rng.normal(0,.12,n)*disorder_scale;bonds*=1+disorder_scale*(rng.uniform(.65,1.35,n-1)-1)
 bonds*=1+strain
 for i in range(n):
  H[4*i:4*i+4,4*i:4*i+4]=masses[i]*np.kron(sz,I)+lams[i]*np.kron(sx,sy)-(mus[i]+dis[i])*np.eye(4)
  if i<n-1:
   b=-bonds[i]*np.kron(sz,I)+.12j*bonds[i]*np.kron(sx,sz)
   H[4*i:4*i+4,4*i+4:4*i+8]=b;H[4*i+4:4*i+8,4*i:4*i+4]=b.conj().T
 return eigvalsh(H)
def susceptibility(w,T):
 x=np.abs(w);return float(np.mean(np.tanh(x/(2*T))/(2*np.maximum(x,1e-12))))
Ts=np.geomspace(.003,.2,90)
names=['Bulk A7 Bi proxy','Ideal Bi/Mg proxy','Disordered Bi-Pb/Mg-Zn proxy']
ws=[spectrum(i) for i in range(3)]
curves=np.array([[1/susceptibility(w,t) for t in Ts] for w in ws])
fig,ax=plt.subplots(figsize=(9,5.5))
for name,c in zip(names,curves):ax.plot(Ts,c,label=name,lw=2)
ax.set(xscale='log',xlabel='Temperature (model units)',ylabel='Critical attractive coupling $g_c$',title='Pairing-instability boundary: $g\\,\\chi(T)=1$')
ax.legend(fontsize=9);ax.grid(alpha=.25);fig.tight_layout();fig.savefig(OUT/'pairing_boundary.png',dpi=180)
rows=[{'temperature':t,'critical_couplings':{names[i]:1/susceptibility(ws[i],t) for i in range(3)}} for t in [.005,.02,.05,.1]]
slices={'strain':{},'disorder':{}}
for e in [-.1,0,.1]:slices['strain'][str(e)]=1/susceptibility(spectrum(2,strain=e),.02)
for d in [0,.5,1,1.5]:slices['disorder'][str(d)]=1/susceptibility(spectrum(2,disorder_scale=d),.02)
(OUT/'results.json').write_text(json.dumps({'model':'1D 48-site 192-state illustrative two-orbital spinful Hamiltonian; separable attraction; no physical calibration','boundary':'gcrit=1/mean(tanh(abs(eig)/(2T))/(2abs(eig)))','table':rows,'slices_at_T_0.02':slices},indent=2))
print(json.dumps({'table':rows,'slices':slices},indent=2))
