#!/usr/bin/env python3
"""P_edge: semiconductor versus semimetal on the band edges.

E_g = E_c_min - E_v_max
semiconductor: E_g > 0, Fermi level in the gap, n(T=0) = 0
semimetal:     E_g < 0, overlap delta = -E_g, both pockets occupied at T=0

S4-S6 track the sign of E_g, so they restate S1. The sign of E_g is not a
Dirac mass: an indirect overlap and a band inversion are independent
(Bi2Se3 is inverted with a full gap). The mass-sign Berry flip is P3 in
bi_topology_proof.py. See the erratum in PROOFS.md.
"""
import json
import numpy as np

K_B = 8.617333262145e-5  # eV/K


def edges(ec_min, ev_max):
    eg = ec_min - ev_max
    kind = "semiconductor" if eg > 0 else "semimetal"
    return eg, kind


def fermi_for_intrinsic(ec_min, ev_max):
    return 0.5 * (ec_min + ev_max)


def carriers_at_zero(ec_min, ev_max, ef, dos_c=1.0, dos_v=1.0):
    n_e = dos_c * max(ef - ec_min, 0.0)
    n_h = dos_v * max(ev_max - ef, 0.0)
    return n_e, n_h


def thermal_n(eg, T, n0=1.0):
    if eg > 0:
        return float(n0 * np.exp(-eg / (2 * K_B * T)))
    return n0


def gap_sign(eg):
    if eg == 0:
        raise ValueError("gap sign is undefined at E_g = 0")
    return -1.0 if eg < 0 else 1.0


def main():
    rows = {}
    for name, (ec, ev) in (("semiconductor", (0.55, -0.55)), ("semimetal", (-0.020, 0.020))):
        eg, kind = edges(ec, ev)
        ef = fermi_for_intrinsic(ec, ev)
        ne, nh = carriers_at_zero(ec, ev, ef)
        rows[name] = {
            "Ec_min_eV": ec,
            "Ev_max_eV": ev,
            "Eg_eV": eg,
            "kind": kind,
            "EF_eV": ef,
            "n_e_T0": ne,
            "n_h_T0": nh,
            "n_300K_relative": thermal_n(eg, 300.0),
            "gap_sign": gap_sign(eg),
        }
    sc, sm = rows["semiconductor"], rows["semimetal"]
    cert = {
        "title": "P_edge",
        "S1_sign": sc["Eg_eV"] > 0 and sm["Eg_eV"] < 0,
        "S2_carriers": sc["n_e_T0"] == 0 and sm["n_e_T0"] > 0 and sm["n_h_T0"] > 0,
        "S3_overlap": abs(sm["Eg_eV"] + 0.040) < 1e-12,
        "S4_gap_sign_flip": sc["gap_sign"] == -sm["gap_sign"],
        "S5_gap_sign": sc["gap_sign"] == 1.0 and sm["gap_sign"] == -1.0,
        "S6_negative_gap": sm["gap_sign"] < 0 and not sc["gap_sign"] < 0,
        "cases": rows,
    }
    cert["PASS"] = all(cert[k] for k in (
        "S1_sign", "S2_carriers", "S3_overlap",
        "S4_gap_sign_flip", "S5_gap_sign", "S6_negative_gap",
    ))
    print(json.dumps(cert, indent=2))
    return cert


if __name__ == "__main__":
    raise SystemExit(0 if main()["PASS"] else 1)
