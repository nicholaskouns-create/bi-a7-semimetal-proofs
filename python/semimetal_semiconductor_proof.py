#!/usr/bin/env python3
"""P_edge: semiconductor versus semimetal on one edge Hamiltonian.

E_g = E_c_min - E_v_max
semiconductor: E_g > 0, Fermi level in the gap, n(T=0) = 0
semimetal:     E_g < 0, overlap delta = -E_g, both pockets occupied at T=0
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
        return n0 * np.exp(-eg / (2 * K_B * T))
    return n0


def berry_sign(m):
    if m == 0:
        raise ValueError("mass sign is undefined at m = 0")
    return -1.0 if m < 0 else 1.0


def check_mass_sign(m, expected):
    got = berry_sign(m)
    return got == expected, got


def check_negative_mass(m):
    got = berry_sign(m)
    return got < 0, got


def main():
    rows = {}
    for name, (ec, ev) in (("semiconductor", (0.55, -0.55)), ("semimetal", (-0.020, 0.020))):
        eg, kind = edges(ec, ev)
        ef = fermi_for_intrinsic(ec, ev)
        ne, nh = carriers_at_zero(ec, ev, ef)
        sign_ok, mass = check_mass_sign(eg, +1.0 if name == "semiconductor" else -1.0)
        negative_ok, _ = check_negative_mass(eg) if name == "semimetal" else (None, None)
        rows[name] = {
            "Ec_min_eV": ec,
            "Ev_max_eV": ev,
            "Eg_eV": eg,
            "kind": kind,
            "EF_eV": ef,
            "n_e_T0": ne,
            "n_h_T0": nh,
            "n_300K_relative": thermal_n(eg, 300.0),
            "mass_sign": mass,
            "mass_sign_ok": sign_ok,
            "negative_mass": negative_ok,
        }
    cert = {
        "title": "P_edge",
        "S1_sign": rows["semiconductor"]["Eg_eV"] > 0 and rows["semimetal"]["Eg_eV"] < 0,
        "S2_carriers": rows["semiconductor"]["n_e_T0"] == 0 and rows["semimetal"]["n_e_T0"] > 0 and rows["semimetal"]["n_h_T0"] > 0,
        "S3_overlap": abs(rows["semimetal"]["Eg_eV"] + 0.040) < 1e-12,
        "S4_mass_flip": rows["semiconductor"]["mass_sign"] == -rows["semimetal"]["mass_sign"],
        "S5_mass_sign": rows["semiconductor"]["mass_sign_ok"] and rows["semimetal"]["mass_sign_ok"],
        "S6_negative_mass": rows["semimetal"]["negative_mass"] is True and rows["semiconductor"]["negative_mass"] is not True,
        "cases": rows,
    }
    cert["PASS"] = all(cert[k] for k in ("S1_sign", "S2_carriers", "S3_overlap", "S4_mass_flip", "S5_mass_sign", "S6_negative_mass"))
    print(json.dumps(cert, indent=2))
    return cert


if __name__ == "__main__":
    main()
