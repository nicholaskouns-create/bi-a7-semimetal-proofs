# Bismuth research simulations

This directory contains the reproducible simulation pass added on 15 October 2026.

## Modules

- `bismuth_heterostructure/run.py` — 48-site spinful two-orbital bulk/layered/disordered comparison.
- `bismuth_pairing/boundary.py` — temperature-, strain-, and disorder-dependent pairing boundary.
- `bismuth_material_calibration/calibrate.py` — phenomenological bulk calibration to measured bismuth carrier density and Tc.
- `bismuth_interface_ldos/ldos.py` — layer/interface-resolved LDOS and interface-projected pairing susceptibility.
- `a7_validation/validate.py` — p-orbital A7 spin-orbit model, time-reversal check, unitary evolution, and BdG particle-hole check.

Each subdirectory contains generated JSON results and run logs. Plot PNGs are committed where supported by this pass.

## Reproduce

```bash
python research/bismuth_heterostructure/run.py
python research/bismuth_pairing/boundary.py
python research/bismuth_material_calibration/calibrate.py
python research/bismuth_interface_ldos/ldos.py
python research/a7_validation/validate.py
```

## Evidence boundary

These simulations are model studies. The A7 SOC implementation and algebraic symmetry/unitarity checks are executable validations of the stated Hamiltonians. The Bi/Mg and Bi-Pb/Mg-Zn interface hopping, disorder, and pairing parameters are phenomenological unless explicitly marked as experimentally anchored. No measured interface-resolved LDOS dataset is included, so the simulations do not establish superconductivity in the analyzed specimen.
