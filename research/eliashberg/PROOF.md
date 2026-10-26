# Flat-Band Eliashberg Closure

**First-principles validation of exciton-mediated pairing in a moiré flat band.**
23 of 23 checks pass. Reproduce with `python3 -I research/eliashberg/eliashberg_first_principles.py`.

Every quantity is derived from CODATA constants and four anchored parameters
(`N(0)`, `ω_ex`, `λ`, `μ*`). Nothing is asserted.

---

## Result

The valid formalism is strong-coupling Eliashberg theory on a flat band with a
single exciton kernel, solved on the Matsubara axis:

```
Z(iω_n) Δ(iω_n) = πT Σ_m [ λ(iω_n − iω_m) − μ* ] Δ(iω_m) / |ω_m|
Z(iω_n)         = 1 + (πT/ω_n) Σ_m λ(iω_n − iω_m) sgn(ω_m)
λ(iΩ)           = λ ω_ex² / (ω_ex² + Ω²)
λ               = 2 ∫ α²F(ω)/ω dω
```

With `N(0) = 4.16×10¹³ eV⁻¹cm⁻²`, `ħω_ex = 0.15 eV`, `λ = 2.7`, `μ* = 0.1`,
solving `ρ(T_c) = 1` gives

> **T_c = 378 K**

not the 298 K obtained from the uncorrected McMillan exponent. Eigenvalue at
`T_c` is 0.999996; the Matsubara sum converges to four digits by a cutoff of
60 ω_ex.

## The closed form fails at this coupling

| method | T_c | error vs numerics |
|---|---|---|
| plain McMillan exponent | 298.2 K | **−21.2 %** |
| Allen–Dynes with `f₁f₂` | 356.6 K | −5.7 % |
| **numerical Eliashberg** | **378.2 K** | — |

`f₁ = (1 + (λ/Λ₁)^{3/2})^{1/3} = 1.196` at λ = 2.7, and `f₂ = 1` exactly for a
single Einstein mode. Agreement between the uncorrected formula and a
literature figure obtained the same way is not independent validation.

## Scaling lemma

The kernel depends on `T` and `ω_ex` only through their ratio — `πT/ω_n = 1/(2n−1)`,
`λ_nm` is a function of `T/ω_ex`, and the `μ*` cutoff scales with `ω_ex`.
Therefore **T_c ∝ ω_ex exactly**, not approximately, which the script confirms
by halving the mode.

Consequently the `ω_log` reproducing 297 K is `150 × 297/378.2 =` **117.8 meV**
(1367 K), a ratio of 0.785. A single sharp mode at 150 meV overshoots; a
realistically broadened exciton spectrum carrying the same λ has a lower
logarithmic moment. **The delta-function reduction, not the coupling, is the
unjustified step.**

## Weak-coupling ceiling

| λ | McMillan | Allen–Dynes | Eliashberg |
|---|---|---|---|
| 0.50 | 21.2 | 21.6 | 27.4 |
| 0.70 | 60.5 | 62.4 | 71.4 |
| **0.90** | **102.0** | 106.4 | **117.4** |
| 1.00 | 121.2 | 127.4 | 139.0 |
| 1.57 | 207.0 | 226.7 | 240.7 |
| 2.70 | 298.2 | 356.6 | 378.2 |
| 4.17 | 353.9 | 471.3 | 506.4 |

Migdal parameter `λ ω_log / E_F`: 0.333 at λ = 0.9, **0.998 at λ = 2.7** — vertex
corrections are O(1), and worse on a flat band where the scale is the bandwidth
rather than `E_F`. A static `V_ex(q) = −|g_q|²/ω_q²` is the weak-coupling limit
of this theory and is not a controlled approximation at λ = 2.7.

## Normal state

`k_F = √(πn)`, `E_F = ħv_F k_F`, `N(0) = E_F/2πħ²v_F²` per flavour, at
`v_F = 1.1×10⁶ m/s`, `n = 10¹³ cm⁻²`:

| | derived |
|---|---|
| `k_F` | 5.605×10⁸ m⁻¹ |
| `E_F` | 0.4058 eV |
| `T_F` | 4709 K |
| `N(0)` | 1.232×10¹³ eV⁻¹cm⁻² (4.93×10¹³ with spin–valley 4) |

## Spectral weight

For a single Einstein mode, `λ = 2N(0)|g|²/ω_ex` gives `|g| = 6.98×10⁻⁸ eV`.
The relation `λ = N(0)|g|²/ω_ex²` gives `3.82×10⁻⁸ eV`; the first is correct.
`ω_log = ω̄₂ = ω_ex` identically for a delta mode, confirmed symbolically.

## Casimir channel — excluded

Area cancellation is proved symbolically (`∂_A[E_Cas/n_sA] = 0`):

```
ΔE_Cas / N_p = −π²ħc / (720 d³ n_s)
```

At `n_s = n/2 = 5×10¹⁶ m⁻²`: **5022 K** (d = 5 nm), 186 K (15 nm), 78.5 K (20 nm).
The magnitudes are real; "50–100 K" corresponds to d ≈ 20 nm.

**The suppression argument does not hold at these parameters.** With
`Δ = 1.76 k_B T_c = 57.4 meV` (75.0 meV at a strong-coupling ratio):

| ω_p | (Δ/ω_p)² |
|---|---|
| 6.8 meV | **71.2** — not a suppression |
| 200 meV | 0.0823 |

A claimed `10⁻⁶–10⁻³` is never reached, and at low doping the factor exceeds
unity. Since `Δ ≳ ω_p`, the perturbative form does not apply.

Casimir is still correctly excluded, on the **category argument alone**:
`ΔE_Cas` is a vacuum free-energy offset present in both phases, carries no
bosonic spectral weight near `ω_log`, and cannot be written as
`∫α²F(ω)K(ω)dω`. It shifts both free energies; it does not scatter
time-reversed partners.

## Verdict

| claim | status |
|---|---|
| strong-coupling flat-band Eliashberg is the valid formalism | **derived** |
| T_c = 298 K at λ = 2.7, ω_log = 1740 K | **corrected → 378 K** |
| closed form fits to a few % | **false** — 21 % low without `f₁` |
| static `V_ex` valid at λ = 2.7 | **false** — Migdal parameter 0.998 |
| weak-coupling ceiling ≈ 95 K | **corrected → 102 K (McMillan), 117 K (Eliashberg)** |
| total Casimir energy per pair ≈ 5000 K at 5 nm | **confirmed** |
| Casimir SC part suppressed by (Δ/ω_p)² ~ 10⁻³ | **false** — factor is 0.08 to 71 |
| Casimir belongs in the gap equation | **excluded** — on category, not magnitude |

## Boundary

Finite-temperature many-body theory with anchored literature parameters. No
material is proposed, no sample is modelled, and no measurement is predicted.
`λ = 2.7` and `N(0)` are inputs taken from 2D Eliashberg calculations on twisted
graphene/WTe₂, not derived here.
