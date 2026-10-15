# bi-a7-semimetal-proofs

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
