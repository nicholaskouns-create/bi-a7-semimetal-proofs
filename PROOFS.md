# Proofs

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
P2. spec(delta tau_z / 2) = {-delta/2, +delta/2}, delta = 40 meV.
P3. gamma(-m) = -gamma(m), and |gamma| -> pi as m -> 0.

Run: python python/bi_topology_proof.py
Last local result: P1 true, P2 true, P3 true.
d1 = 3.071174475543482 A, d2 = 3.529093362940372 A, ratio = 1.1491022053756343.
Overlap spectrum = {-0.02, +0.02} eV.
gamma(+0.02) = -2.82899 = -gamma(-0.02). |gamma(1e-4)| = 3.14002.

P2 certifies the overlap block that was written down. It does not derive 40 meV from (a, c, u).

## P_edge. Semiconductor versus semimetal

E_g = E_c^min - E_v^max.

S1. E_g(semiconductor) > 0 and E_g(semimetal) < 0.
S2. n_e(0) = n_h(0) = 0 if E_g > 0; both positive if E_g < 0.
S3. delta = -E_g(semimetal) = 40 meV.
S4. sgn(m_sc) = -sgn(m_sm).
S5. semiconductor mass sign is +1; semimetal mass sign is -1.
S6. negative mass holds for the semimetal and is refused for the semiconductor.

Run: python python/semimetal_semiconductor_proof.py
Last local result: PASS true. S1 through S6 true.
