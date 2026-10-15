# Proofs

## Erratum · 15 October 2026

E1. The 40 meV scale in P2 and S3 is bismuth's indirect band overlap between the T-point hole band and the L-point electron band. The direct gap at L is 10–15 meV. Earlier text called the P2 block an L-point overlap. Sources: [arXiv:1002.4206](https://arxiv.org/abs/1002.4206), Table I (40 meV overlap, 15 meV L gap); [arXiv:2102.02018](https://arxiv.org/abs/2102.02018) (10–15 meV L gap, with the experimental references).

E2. S4–S6 passed E_g in as the mass, so they restated S1. A negative indirect overlap is not a Dirac-mass inversion: the two are independent (Bi₂Se₃ has inverted bands and a full gap). S4–S6 now name what they check, the sign of E_g. The mass-sign Berry flip is P3.

## P_cell. Plate-2 coordinates close the A7 shells

Given Lambda = (a, c, u) = (4.546, 11.862, 0.23389), hexagonal R-3m, 6 atoms.

C1. Short shell is 3.071 A.
C2. Long shell is 3.529 A.
C3. Density from this cell is within 0.05 of 9.78 g/cm^3.
C4. Melting sign is +271.4 C. The printed -271 C beside 544 K is a sign error.

Run: python python/plate2_reconciliation_proof.py
Record: records/p_cell_pass.json. PASS true.

The ~3.4 A interlayer label is not this closure. The c-projection of the long bond is 2.359 A. The long bond itself is 3.529 A.

## P_Bi. A7 semimetal quantum topology

P1. Neighbor multiset under 4.2 A is two shells, d1 < d2, d2/d1 > 1.
P2. spec(delta tau_z / 2) = {-delta/2, +delta/2}, delta = 40 meV, the T–L overlap scale.
P3. gamma(-m) = -gamma(m), and |gamma| -> pi as m -> 0.

Run: python python/bi_topology_proof.py
Record: records/p_bi_pass.json. PASS true.
d1 = 3.071174475543482 A, d2 = 3.529093362940372 A, ratio = 1.1491022053756343.
Overlap spectrum = {-0.02, +0.02} eV.
gamma(+0.02) = -2.82899 = -gamma(-0.02). |gamma(1e-4)| = 3.14002, matching pi(1 - m/E) on the loop.

P2 certifies the overlap block that was written down. It does not derive 40 meV from (a, c, u).

## P_edge. Semiconductor versus semimetal

E_g = E_c^min - E_v^max.

S1. E_g(semiconductor) > 0 and E_g(semimetal) < 0.
S2. n_e(0) = n_h(0) = 0 if E_g > 0; both positive if E_g < 0.
S3. delta = -E_g(semimetal) = 40 meV.
S4. sgn(E_g(semiconductor)) = -sgn(E_g(semimetal)). Restates S1 (E2).
S5. The semiconductor gap sign is +1; the semimetal gap sign is -1. Restates S1 (E2).
S6. A negative gap holds for the semimetal and is refused for the semiconductor. Restates S1 (E2).

Run: python python/semimetal_semiconductor_proof.py
Record: records/p_edge_pass.json. PASS true.
