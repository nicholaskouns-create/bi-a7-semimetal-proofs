# Bismuth A7 formal verification lane

The Lean and Coq files encode exact integer-scaled **band-edge sign and pocket** results corresponding to the example inputs of `python/semimetal_semiconductor_proof.py`. Energies are scaled by 100 relative to the Python examples: (0.55,-0.55) -> (55,-55); (-0.020,0.020) -> (-2,2).

Scope: arithmetic band-edge identities, positivity/negativity, and nonnegative pocket counts in a simplified constant-DOS model. No assertion that the indirect gap sign is a Dirac mass sign or a Berry phase invariant. The 15 October erratum in PROOFS.md remains authoritative.

CI compiles each language independently. Compiler acceptance must be read from the GitHub Actions jobs; merely committing these files does not certify them. This is **not** end-to-end formal verification of A7 crystal geometry, spin–orbit Hamiltonian, pairing boundary, LDOS, or material calibration.

To run locally: `lean formal/lean/BismuthBandEdge.lean` and `coqc formal/coq/BismuthBandEdge.v`.
