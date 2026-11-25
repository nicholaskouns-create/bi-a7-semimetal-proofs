> ⚛️ **[E₄₇ Φ₄ LIVE QUANTUM CIRCUIT](https://nicholaskouns-create.github.io/qsvt-phi4/)** · [250D QSP / 500D LCU full interactive diagram](https://nicholaskouns-create.github.io/E47-Kartekeya/interfaces/qsvt-phi4-circuit/) · [First-principles formalism and 14-check NumPy certificate](https://github.com/nicholaskouns-create/E47-Kartekeya/tree/main/research/e47/qsp_phi4). Cross-repository research link; not an independent validation in this repository.

# bi-a7-semimetal-proofs

> **Current license:** [All Rights Reserved](LICENSE) for owned original material. No new reuse permission. Earlier licenses and third-party/public-domain rights remain unaffected.


> **Current licensing:** [All Rights Reserved](LICENSE) for original material owned by Nicholas Shane Kouns. No new reuse permission is granted. Previously granted licenses and third-party/public-domain rights remain unaffected.


Python certificates for the bismuth A7 cell and the semiconductor/semimetal edge sign.

- `python/plate2_reconciliation_proof.py` — C1–C4: cell shells, density, melting sign.
- `python/bi_topology_proof.py` — P1 cell shells, P2 T–L overlap block, P3 Berry sign flip.
- `python/semimetal_semiconductor_proof.py` — S1–S6 on the sign of E_g.
- `PROOFS.md` — the statements, with the 15 October 2026 erratum at the top.
- `records/` — run output from the current scripts. The PySCF record is a 2x2x2 ECP mesh, not an L-point SOC band.
- `research/` — executable A7 spin-orbit, layered-interface, LDOS, pairing-boundary, and bulk-calibration simulations added 15 October 2026.

```bash
python python/plate2_reconciliation_proof.py
python python/bi_topology_proof.py
python python/semimetal_semiconductor_proof.py

python research/bismuth_heterostructure/run.py
python research/bismuth_pairing/boundary.py
python research/bismuth_material_calibration/calibrate.py
python research/bismuth_interface_ldos/ldos.py
python research/a7_validation/validate.py
```

Each proof script prints its certificate as JSON and exits nonzero if any statement fails. CI runs the original proof suite on every push and pull request. See `research/README.md` for the evidence boundary and reproduction notes for the newer simulations.

[The E₄₇ spectral kernel · formalism and verification](app/e47-spectral-kernel/README.md)


<!-- FUN-WITH-EINSTEIN-2026 -->
### 🪐 Fun With Einstein · Interactive spectral & quantum lab

[Launch Fun With Einstein](https://nicholaskouns-create.github.io/fun-with-einstein/) · [Source & Python/Lean/Coq proof modules](https://github.com/nicholaskouns-create/E47-Kartekeya/tree/main/docs/fun-with-einstein) · [CI compiler status](https://github.com/nicholaskouns-create/E47-Kartekeya/actions/workflows/fun-with-einstein.yml).

Fivefold C₅ eigenvalue ratio = φ⁻²; 125D Casimir E₄₇ projector; 250D quantum-ancilla probability α=47/(125φ²); stationary Einstein-equation recovery. Spectral simulation and gravitational statements have different evidence classes.
<!-- /FUN-WITH-EINSTEIN-2026 -->


---

### Interactive E₄₇ spectral geometry (computed)

[**Open the standalone E₄₇ 3D visualizer**](./e47-geometry/index.html) · [**Open on GitHub Pages**](https://nicholaskouns-create.github.io/bi-a7-semimetal-proofs/e47-geometry/)

An additive, mobile-friendly research instrument showing the 125-site product-spin lattice, the exact 47-dimensional projector-density field (125 rational samples with denominator 315), five orthogonal axial slices, the seven SU(2) spectral sectors, optimal contraction Γ* = I − K²/99144 and the five-stage exact polynomial projector. The volumetric embedding is a coordinate visualization, not a claim that E₄₇ is a physical three-dimensional solid. No existing instruments are replaced.
