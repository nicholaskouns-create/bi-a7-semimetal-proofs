# bi-a7-semimetal-proofs

Python certificates for the bismuth A7 cell and the semiconductor/semimetal edge sign.

- `python/plate2_reconciliation_proof.py` — C1–C4: cell shells, density, melting sign.
- `python/bi_topology_proof.py` — P1 cell shells, P2 T–L overlap block, P3 Berry sign flip.
- `python/semimetal_semiconductor_proof.py` — S1–S6 on the sign of E_g.
- `PROOFS.md` — the statements, with the 15 October 2026 erratum at the top.
- `records/` — run output from the current scripts. The PySCF record is a 2x2x2 ECP mesh, not an L-point SOC band.

```bash
python python/plate2_reconciliation_proof.py
python python/bi_topology_proof.py
python python/semimetal_semiconductor_proof.py
```

Each script prints its certificate as JSON and exits nonzero if any statement fails. CI runs all three on every push and pull request.
