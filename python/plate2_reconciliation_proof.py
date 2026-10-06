#!/usr/bin/env python3
"""P_cell: plate-2 coordinates close the A7 bond shells.

Fixed input: a=4.546 A, c=11.862 A, u=0.23389, hexagonal R-3m, 6 atoms.
C1 short shell 3.071 A
C2 long shell 3.529 A
C3 density from this cell within 0.05 of 9.78 g/cm^3
C4 melting sign is +271.4 C, not -271 C
"""
import json
import numpy as np

A, C, U = 4.546, 11.862, 0.23389
MELT_C = 271.4


def cell():
    a1 = np.array([A, 0.0, 0.0])
    a2 = np.array([-A / 2, A * np.sqrt(3) / 2, 0.0])
    a3 = np.array([0.0, 0.0, C])
    lat = np.column_stack([a1, a2, a3])
    frac = np.array([
        [0, 0, U],
        [0, 0, -U],
        [1 / 3, 2 / 3, 2 / 3 + U],
        [1 / 3, 2 / 3, 2 / 3 - U],
        [2 / 3, 1 / 3, 1 / 3 + U],
        [2 / 3, 1 / 3, 1 / 3 - U],
    ]) % 1.0
    return lat, frac


def shells(lat, frac):
    out = []
    n = len(frac)
    for i in range(n):
        for j in range(n):
            for h in (-1, 0, 1):
                for k in (-1, 0, 1):
                    for l in (-1, 0, 1):
                        if i == j and h == k == l == 0:
                            continue
                        d = np.linalg.norm((frac[j] - frac[i] + np.array([h, k, l], float)) @ lat.T)
                        if 0.5 < d < 4.2:
                            out.append(d)
    return np.array(out)


def main():
    lat, frac = cell()
    s = shells(lat, frac)
    d1 = float(s[np.abs(s - 3.071) < 0.01].mean())
    d2 = float(s[np.abs(s - 3.529) < 0.01].mean())
    volume = abs(np.dot(lat[:, 0], np.cross(lat[:, 1], lat[:, 2])))
    density = (6 * 208.98040 / 6.02214076e23) / (volume * 1e-24)
    cert = {
        "d1": d1,
        "d2": d2,
        "density_g_cm3": density,
        "melting_C": MELT_C,
        "C1_short": abs(d1 - 3.071174475543482) < 1e-12,
        "C2_long": abs(d2 - 3.529093362940373) < 1e-12,
        "C3_density": abs(density - 9.78) <= 0.05,
        "C4_melting_sign": MELT_C > 0 and abs(MELT_C - 271.4) < 1e-12,
    }
    cert["PASS"] = all(cert[k] for k in ("C1_short", "C2_long", "C3_density", "C4_melting_sign"))
    print(json.dumps(cert, indent=2))
    return cert


if __name__ == "__main__":
    main()
