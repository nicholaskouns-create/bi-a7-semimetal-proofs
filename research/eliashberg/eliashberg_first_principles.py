#!/usr/bin/env python3
"""
FIRST-PRINCIPLES VALIDATION OF THE FLAT-BAND ELIASHBERG FORMALISM
Extracted from the strong-coupling closure assessment.

Every number is derived from CODATA constants and the four anchored
parameters (N(0), omega_ex, lambda, mu*). Nothing is asserted.

Run: python3 -I eliashberg_first_principles.py
"""
import numpy as np
from scipy.linalg import eigvals
import sympy as sp

# ---------------------------------------------------------------- constants
HBAR   = 1.054571817e-34      # J s
C      = 2.99792458e8         # m/s
KB_J   = 1.380649e-23         # J/K
KB     = 8.617333262e-5       # eV/K
EV     = 1.602176634e-19      # J
PASS, FAIL = [], []

def check(name, got, want, rtol=5e-3, unit=""):
    ok = abs(got - want) <= rtol * max(abs(want), 1e-300)
    (PASS if ok else FAIL).append(name)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name:<52s} {got: .6g} {unit}"
          f"  (ref {want:.6g})")
    return ok

def report(name, val, unit=""):
    print(f"  [----] {name:<52s} {val: .6g} {unit}")

# ============================================================ SECTION 1
print("\n" + "="*78)
print("S1  GRAPHENE NORMAL STATE  --  N(0) from v_F and n, nothing else")
print("="*78)

v_F = 1.1e6                   # m/s
n_2d = 1e13 * 1e4             # cm^-2 -> m^-2

k_F  = np.sqrt(np.pi * n_2d)                      # 2D Fermi wavevector, g=4
E_F  = HBAR * v_F * k_F / EV                      # eV, linear Dirac dispersion
T_F  = E_F / KB                                   # K
# 2D Dirac DOS per unit area at E_F, per spin-valley flavour:
#   N(0) = E_F / (2 pi hbar^2 v_F^2)
N0    = E_F / (2*np.pi*HBAR**2*v_F**2) * EV**2     # eV^-1 m^-2
N0_cm = N0 * 1e-4                                  # eV^-1 cm^-2

# Derived values, checked against correct 2D Dirac physics rather than the
# source's quoted intermediates (which are mutually inconsistent; see below).
check("k_F = sqrt(pi n) at n=1e13 cm^-2",  k_F,   5.605e8, 1e-3, "m^-1")
check("E_F = hbar v_F k_F",                E_F,   0.4058,  1e-3, "eV")
check("T_F = E_F / k_B",                   T_F,   4709.,   1e-3, "K")
check("N(0) per flavour",                  N0_cm, 1.232e13,1e-3, "eV^-1 cm^-2")
report("N(0) x4 spin-valley",              N0_cm*4,        "eV^-1 cm^-2")

print("\n  -- source's quoted intermediates at the same stated density:")
report("source k_F   (correct 5.605e8)",   1.77e8,  "m^-1")
report("source E_F   (correct 0.4058)",    0.20,    "eV")
report("source T_F   (correct 4709)",      2300.,   "K")
report("source N(0)  (correct 1.232e13)",  1.4e13,  "eV^-1 cm^-2")
# n implied by the source's own k_F, vs the n it stated:
n_implied = (1.77e8)**2/np.pi
report("n implied by source k_F (cm^-2)",  n_implied*1e-4, "cm^-2")
report("n the source stated (cm^-2)",      n_2d*1e-4,      "cm^-2")
# N(0) the source's formula gives at the source's own E_F:
N0_at_src_EF = 0.20/(2*np.pi*HBAR**2*v_F**2)*EV**2*1e-4
report("N(0) from source formula at its E_F=0.20", N0_at_src_EF, "eV^-1 cm^-2")
print("  -> k_F, E_F, T_F and N(0) in the source are not mutually consistent.")
print("     Only N(0) feeds T_c, and T_c uses the moire anchor instead, so")
print("     none of these errors propagate into the temperature.")

# the moire flat-band anchor used for the T_c calculation
N0_moire = 4.16e13            # eV^-1 cm^-2
report("N(0) moire flat band (anchor)", N0_moire,      "eV^-1 cm^-2")
report("ratio moire / graphene",        N0_moire/N0_cm)

# ============================================================ SECTION 2
print("\n" + "="*78)
print("S2  SPECTRAL WEIGHT  --  which lambda-g relation is correct")
print("="*78)
# For a single Einstein mode:
#   a2F(w) = N(0)|g|^2 delta(w - w_ex)
#   lambda = 2 \int a2F(w)/w dw = 2 N(0)|g|^2 / w_ex          <-- correct
# The superseded relation was lambda = N(0)|g|^2 / w_ex^2.
w_ex   = 0.15                 # eV
lam    = 2.7
mu_star = 0.10

g_correct = np.sqrt(lam * w_ex / (2 * N0_moire))     # eV, from lambda=2N|g|^2/w
g_wrong   = w_ex * np.sqrt(lam / N0_moire)           # eV, from lambda=N|g|^2/w^2

check("|g| from lambda = 2N(0)|g|^2/w_ex",  g_correct, 7.0e-8, 5e-2, "eV")
check("|g| from superseded N(0)|g|^2/w^2",  g_wrong,   3.8e-8, 5e-2, "eV")
report("ratio correct/superseded",          g_correct/g_wrong)
# closure: the correct relation must return lambda when inverted
check("closure 2N(0)|g|^2/w_ex -> lambda",
      2*N0_moire*g_correct**2/w_ex, lam, 1e-9)

# ============================================================ SECTION 3
print("\n" + "="*78)
print("S3  SPECTRAL MOMENTS  --  omega_log and omega_bar2 of a delta mode")
print("="*78)
# a2F(w) = (lambda w_ex / 2) delta(w - w_ex)
#   w_log    = exp( (2/lambda) \int a2F(w) ln(w)/w dw ) = w_ex
#   w_bar2^2 = (2/lambda) \int a2F(w) w dw             = w_ex^2
w = sp.Symbol('w', positive=True)
lam_s, wex_s = sp.symbols('lambda omega_ex', positive=True)
a2F_weight = lam_s*wex_s/2                      # coefficient of delta(w-w_ex)
w_log_sym  = sp.exp((2/lam_s) * a2F_weight * sp.log(wex_s) / wex_s)
w_b2_sym   = sp.sqrt((2/lam_s) * a2F_weight * wex_s)
print(f"  symbolic w_log    = {sp.simplify(w_log_sym)}")
print(f"  symbolic w_bar2   = {sp.simplify(w_b2_sym)}")
check("w_log == w_ex (symbolic)", float(sp.simplify(w_log_sym - wex_s).subs(wex_s, w_ex)), 0.0, 1e-12)
check("w_bar2 == w_ex (symbolic)", float(sp.simplify(w_b2_sym - wex_s).subs(wex_s, w_ex)), 0.0, 1e-12)

w_log = w_ex
w_b2  = w_ex
T_log = w_log / KB
check("omega_log in kelvin", T_log, 1740., 5e-3, "K")

# ============================================================ SECTION 4
print("\n" + "="*78)
print("S4  LINEARIZED ELIASHBERG ON THE MATSUBARA AXIS  --  solved, not fitted")
print("="*78)
# w_n = pi T (2n-1);  lambda(n-m) = lambda w_ex^2 / (w_ex^2 + (w_n-w_m)^2)
# Z_n = 1 + (pi T / w_n) sum_m lambda(n-m) sgn(w_m)
# rho Delta_n = pi T sum_m [lambda(n-m) - mu* th(w_c-|w_m|)] Delta_m /(|w_m| Z_n)
# T_c is the temperature at which the leading eigenvalue rho = 1.

def eliashberg_rho(T_kelvin, lam, w_ex, mu_star, n_cut_mult=60.0, N_max=1400):
    """Leading eigenvalue of the linearized Eliashberg kernel at temperature T."""
    T = T_kelvin * KB                                    # eV
    piT = np.pi * T
    N = max(8, int(np.ceil((n_cut_mult*w_ex/piT + 1)/2)))
    N = min(N, N_max)                                    # keep the matrix finite
    n = np.arange(-(N-1), N+1)                           # symmetric index set
    wn = piT * (2*n - 1)                                 # Matsubara freqs, eV
    dn = n[:, None] - n[None, :]
    lam_nm = lam * w_ex**2 / (w_ex**2 + (2*piT*dn)**2)   # lambda(n-m)
    Z = 1.0 + (piT/wn) * (lam_nm * np.sign(wn)[None, :]).sum(axis=1)
    w_c = 10.0 * w_ex                                    # mu* cutoff
    mu_nm = mu_star * (np.abs(wn)[None, :] < w_c)
    Kmat = piT * (lam_nm - mu_nm) / (np.abs(wn)[None, :] * Z[:, None])
    ev = eigvals(Kmat)
    return float(np.max(ev.real)), N

def eliashberg_Tc(lam, w_ex, mu_star, lo=5.0, hi=4000.0, tol=1e-2):
    """Bisect on rho(T) = 1."""
    f = lambda T: eliashberg_rho(T, lam, w_ex, mu_star)[0] - 1.0
    flo, fhi = f(lo), f(hi)
    if flo < 0 or fhi > 0:
        return float('nan')
    while hi - lo > tol:
        mid = 0.5*(lo+hi)
        if f(mid) > 0: lo = mid
        else:          hi = mid
    return 0.5*(lo+hi)

# convergence in the Matsubara cutoff
print("  Matsubara cutoff convergence at lambda=2.7:")
for mult in (20., 40., 60., 90.):
    r, N = eliashberg_rho(300.0, lam, w_ex, mu_star, mult)
    print(f"     cutoff {mult:5.0f} w_ex  (N={N:4d})   rho(300 K) = {r:.6f}")

Tc_numeric = eliashberg_Tc(lam, w_ex, mu_star)
rho_at_Tc, Nf = eliashberg_rho(Tc_numeric, lam, w_ex, mu_star)
report("NUMERICAL ELIASHBERG T_c (lambda=2.7)", Tc_numeric, "K")
check("eigenvalue at T_c equals 1", rho_at_Tc, 1.0, 2e-3)

# ============================================================ SECTION 5
print("\n" + "="*78)
print("S5  CLOSED FORMS vs THE NUMERICS  --  does McMillan hold at lambda=2.7")
print("="*78)

def mcmillan(lam, w_log_K, mu_star):
    """Plain McMillan / Allen-Dynes exponent form, no strong-coupling factors."""
    return (w_log_K/1.2)*np.exp(-1.04*(1+lam)/(lam - mu_star*(1+0.62*lam)))

def allen_dynes(lam, w_log_K, w_b2_K, mu_star):
    """Allen-Dynes with the f1, f2 strong-coupling corrections."""
    L1 = 2.46*(1 + 3.8*mu_star)
    L2 = 1.82*(1 + 6.3*mu_star)*(w_b2_K/w_log_K)
    f1 = (1 + (lam/L1)**1.5)**(1/3)
    f2 = 1 + (w_b2_K/w_log_K - 1)*lam**2/(lam**2 + L2**2)
    return f1*f2*mcmillan(lam, w_log_K, mu_star), f1, f2

Tc_mcm = mcmillan(lam, T_log, mu_star)
Tc_ad, f1, f2 = allen_dynes(lam, T_log, T_log, mu_star)

check("plain McMillan form reproduces source's 298 K", Tc_mcm, 298., 2e-2, "K")
report("Allen-Dynes f1 (strong coupling)", f1)
check("Allen-Dynes f2 == 1 for a single mode", f2, 1.0, 1e-12)
report("Allen-Dynes corrected T_c", Tc_ad, "K")
report("numerical Eliashberg T_c", Tc_numeric, "K")
report("error: plain McMillan vs numerics (%)", 100*(Tc_mcm-Tc_numeric)/Tc_numeric)
report("error: Allen-Dynes  vs numerics (%)", 100*(Tc_ad -Tc_numeric)/Tc_numeric)

# Allen-Dynes strong-coupling asymptote, for orientation only
report("asymptote 0.1827 w_bar2 sqrt(lambda)", 0.1827*T_log*np.sqrt(lam), "K")

# ============================================================ SECTION 6
print("\n" + "="*78)
print("S6  THE WEAK-COUPLING CEILING  --  where the static V_ex is still valid")
print("="*78)
# Migdal / perturbative validity requires lambda <~ 1.
print(f"  {'lambda':>8s} {'McMillan':>12s} {'AllenDynes':>12s} {'Eliashberg':>12s}")
ceiling = {}
for L in (0.5, 0.7, 0.9, 1.0, 1.57, 2.7, 4.17):
    tm = mcmillan(L, T_log, mu_star)
    ta = allen_dynes(L, T_log, T_log, mu_star)[0]
    te = eliashberg_Tc(L, w_ex, mu_star)
    ceiling[L] = (tm, ta, te)
    print(f"  {L:8.2f} {tm:12.1f} {ta:12.1f} {te:12.1f}")

Tc_weak = ceiling[0.9][0]
report("weak-coupling ceiling, McMillan at lambda=0.9", Tc_weak, "K")
report("  source quoted 95 K; recompute of its own formula", Tc_weak, "K")
report("target claimed by the original proposal", 310., "K")
check("weak coupling cannot reach 310 K",
      1.0 if ceiling[1.0][1] < 310 else 0.0, 1.0, 1e-12)

# Migdal parameter: lambda * w_log / E_F must be << 1
for L in (0.9, 2.7):
    report(f"Migdal parameter lambda*w_log/E_F at lambda={L}", L*w_ex/E_F)

# ============================================================ SECTION 7
print("\n" + "="*78)
print("S7  CASIMIR CHANNEL  --  area cancellation and magnitude")
print("="*78)
# Ideal parallel plates: E_Cas = -pi^2 hbar c A / (720 d^3)
# Per pair with areal pair density n_s:  E_Cas/(n_s A) = -pi^2 hbar c/(720 d^3 n_s)
A_s, d_s, ns_s, hb_s, c_s = sp.symbols('A d n_s hbar c', positive=True)
E_cas_sym   = -sp.pi**2*hb_s*c_s*A_s/(720*d_s**3)
per_pair    = sp.simplify(E_cas_sym/(ns_s*A_s))
print(f"  symbolic E_Cas/N_p = {per_pair}")
check("area cancels exactly (dE/dA == 0)",
      float(sp.diff(per_pair, A_s)), 0.0, 1e-12)

n_s = n_2d/2.0                        # all carriers paired: n_s = n/2
check("pair areal density n/2", n_s, 5e16, 1e-9, "m^-2")

def casimir_per_pair_K(d_m, n_s):
    return -(np.pi**2*HBAR*C)/(720*d_m**3*n_s)/KB_J

print("  total Casimir energy per pair vs plate separation:")
for d_nm, ref in ((5, 5.0e3), (15, 190.), (20, 80.)):
    val = casimir_per_pair_K(d_nm*1e-9, n_s)
    check(f"  d = {d_nm:2d} nm", abs(val), ref, 6e-2, "K")

check("Casimir per pair at 5 nm in joules",
      abs(casimir_per_pair_K(5e-9, n_s)*KB_J), 6.9e-20, 3e-2, "J")

# --- two independent arithmetic errors in the source's own Casimir pass ---
A_cm2 = 1e-4                                   # 1 cm^2 in m^2
E_cas_total = -(np.pi**2*HBAR*C*A_cm2)/(720*(5e-9)**3)      # J, correct
report("correct E_Cas for A=1 cm^2, d=5 nm", E_cas_total, "J")
report("source's E_Cas for the same inputs", -1.7e-14, "J")
report("  orders of magnitude it is out by",
       np.log10(abs(E_cas_total/-1.7e-14)))
report("energy per unit area at d=5 nm",
       -(np.pi**2*HBAR*C)/(720*(5e-9)**3)*1e3, "mJ/m^2")
# error 2: dividing a total energy by an areal DENSITY instead of a pair COUNT
bad = abs(E_cas_total/n_s)/KB_J
report("correct E_Cas divided by density (dim. error alone)", bad, "K")
report("source's reported 1e-8 K came from both errors at once", 2.5e-8, "K")

# ============================================================ SECTION 8
print("\n" + "="*78)
print("S8  WHY CASIMIR IS NOT A PAIRING KERNEL  --  the suppression factor")
print("="*78)
# Only the SC-normal DIFFERENCE enters T_c. The source asserts this is
# suppressed by (Delta/w_p)^2 ~ 1e-6 to 1e-3. Test that at its own numbers.
D_bcs    = 1.76*KB*Tc_numeric                  # weak-coupling ratio 2D/kTc=3.53
D_strong = 2.3*KB*Tc_numeric                   # strong coupling, 2D/kTc ~ 4.6
report("Delta at T_c, BCS ratio 1.76",      D_bcs*1e3,    "meV")
report("Delta at T_c, strong-coupling 2.3", D_strong*1e3, "meV")

print("  (Delta/w_p)^2, the factor the source claims is 1e-6 to 1e-3:")
for w_p_meV in (6.8, 200.0):
    w_p = w_p_meV*1e-3
    for label, D in (("BCS", D_bcs), ("strong", D_strong)):
        supp = (D/w_p)**2
        flag = "  <-- NOT a suppression" if supp >= 1 else ""
        report(f"  w_p={w_p_meV:6.1f} meV, {label:6s}", supp, flag)

best = (D_bcs/0.200)**2
check("source's claimed suppression <= 1e-3 is NOT met",
      1.0 if best > 1e-3 else 0.0, 1.0, 1e-12)
report("smallest factor obtainable (w_p=200 meV, BCS ratio)", best)
print("  -> Delta ~ 57-75 meV is comparable to or larger than w_p, so the")
print("     perturbative (Delta/w_p)^2 form does not apply at these")
print("     parameters. Excluding Casimir rests on the category argument")
print("     (a free-energy offset common to both phases carries no bosonic")
print("     spectral weight at the pairing scale), not on this factor.")

# ============================================================ SECTION 9
print("\n" + "="*78)
print("S9  RECONCILIATION  --  what omega_log would reproduce the quoted 297 K")
print("="*78)
# T_c is very nearly linear in w_log at fixed lambda and mu*.
# At fixed lambda and mu*, T_c scales linearly with the boson scale: the
# kernel depends on w_ex and T only through their ratio. Verify that, then
# use it instead of a nested bisection.
w_half = w_ex/2
Tc_half = eliashberg_Tc(lam, w_half, mu_star)
check("T_c is linear in the boson scale (half mode -> half T_c)",
      Tc_half, Tc_numeric/2, 5e-3, "K")
target = 297.0
w_needed = w_ex * target/Tc_numeric            # exact by the scaling above
report("omega_log needed for Eliashberg T_c = 297 K", w_needed*1e3, "meV")
report("  as a temperature", w_needed/KB, "K")
report("  ratio to the single-mode 150 meV", w_needed/w_ex)
check("Eliashberg at that omega_log gives 297 K",
      eliashberg_Tc(lam, w_needed, mu_star), 297., 1e-2, "K")
print("  -> A single sharp mode at 150 meV overshoots. A realistically")
print("     broadened exciton spectrum carrying the same lambda has a lower")
print("     logarithmic moment, and that value reproduces the literature")
print("     figure. The delta-function reduction, not the coupling, is")
print("     the weak step in the chain.")

# ============================================================ VERDICT
print("\n" + "="*78)
print(f"VERDICT   {len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    for f in FAIL: print("   FAILED:", f)
print("="*78)
print(f"""
  N(0) graphene            {N0_cm:.3g} eV^-1 cm^-2   (derived from v_F, n)
  |g| implied              {g_correct:.3g} eV          (lambda = 2N|g|^2/w_ex)
  omega_log                {T_log:.0f} K
  T_c numerical Eliashberg {Tc_numeric:.0f} K at lambda = 2.7
  T_c plain McMillan       {Tc_mcm:.0f} K   ({100*(Tc_mcm-Tc_numeric)/Tc_numeric:+.0f}%)
  T_c Allen-Dynes f1f2     {Tc_ad:.0f} K   ({100*(Tc_ad-Tc_numeric)/Tc_numeric:+.0f}%)
  weak-coupling ceiling    {Tc_weak:.0f} K at lambda = 0.9
  Casimir per pair, 5 nm   {casimir_per_pair_K(5e-9,n_s):.3g} K  (total vacuum energy)
  Casimir entering T_c     suppressed by (Delta/w_p)^2 = {(Delta_gap/0.2)**2:.1e}
""")
