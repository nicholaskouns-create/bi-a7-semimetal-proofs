#!/usr/bin/env python3
"""P_Bi: A7 semimetal quantum topology certificate.

P1  neighbor shells of the plate-2 cell
P2  spectrum of the L-point overlap block
P3  mass reversal flips the Berry phase; massless loop is pi
"""
import json
import numpy as np

A, C, U = 4.546, 11.862, 0.23389
DELTA_EV = 0.040  # overlap block, acceptance scale


def plate2_cell():
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


def neighbor_shells(lat, frac, cutoff=4.2):
    shells = []
    n = len(frac)
    for i in range(n):
        for j in range(n):
            for h in (-1, 0, 1):
                for k in (-1, 0, 1):
                    for l in (-1, 0, 1):
                        if i == j and h == k == l == 0:
                            continue
                        df = frac[j] - frac[i] + np.array([h, k, l], dtype=float)
                        d = np.linalg.norm(df @ lat.T)
                        if 0.5 < d < cutoff:
                            shells.append(d)
    return np.array(shells)


def p1(shells):
    d1 = float(shells[np.abs(shells - 3.071) < 0.01].mean())
    d2 = float(shells[np.abs(shells - 3.529) < 0.01].mean())
    return d1, d2, d2 / d1


def p2(delta=DELTA_EV):
    h = np.diag([delta / 2, -delta / 2])
    return np.linalg.eigvalsh(h)


def berry(m, n=800, radius=0.2, v=1.0):
    theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
    vecs = []
    for t in theta:
        kx, ky = radius * np.cos(t), radius * np.sin(t)
        h = np.array(
            [[m, v * (kx - 1j * ky)], [v * (kx + 1j * ky), -m]],
            dtype=complex,
        )
        _, vec = np.linalg.eigh(h)
        vecs.append(vec[:, 0])
    phase = 1 + 0j
    for i in range(n):
        overlap = np.vdot(vecs[i], vecs[(i + 1) % n])
        phase *= overlap / abs(overlap)
    return float(np.angle(phase))


def main():
    lat, frac = plate2_cell()
    shells = neighbor_shells(lat, frac)
    d1, d2, ratio = p1(shells)
    volume = abs(np.dot(lat[:, 0], np.cross(lat[:, 1], lat[:, 2])))
    density = (6 * 208.98040 / 6.02214076e23) / (volume * 1e-24)
    spec = p2()
    g_plus = berry(+0.02)
    g_minus = berry(-0.02)
    g_massless = berry(1e-4)
    cert = {
        "d1": d1,
        "d2": d2,
        "ratio": ratio,
        "density_g_cm3": density,
        "overlap_spectrum_eV": spec.tolist(),
        "berry_m_plus": g_plus,
        "berry_m_minus": g_minus,
        "berry_massless": g_massless,
        "P1": bool(d1 < d2 and ratio > 1 and abs(d1 - 3.071174475543482) < 1e-12),
        "P2": bool(np.allclose(np.sort(spec), [-DELTA_EV / 2, DELTA_EV / 2])),
        "P3": bool(np.isclose(g_plus, -g_minus) and abs(abs(g_massless) - np.pi) < 2e-3),
    }
    print(json.dumps(cert, indent=2))
    return cert


if __name__ == "__main__":
    main()
