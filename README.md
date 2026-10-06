# bi-a7-semimetal-proofs

Python certificates for the bismuth A7 cell and the semiconductor/semimetal edge sign.

- `python/bi_topology_proof.py` — P1 cell shells, P2 overlap block, P3 Berry sign flip.
- `python/semimetal_semiconductor_proof.py` — S1–S6, including negative mass.
- `PROOFS.md` — the statements.
- `records/` — local run output. The PySCF record is a 2x2x2 ECP mesh, not an L-point SOC band.

```bash
python python/bi_topology_proof.py
python python/semimetal_semiconductor_proof.py
```
