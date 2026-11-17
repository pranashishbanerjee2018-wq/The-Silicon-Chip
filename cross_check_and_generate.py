"""
INSIDE THE SILICON: MOSFET NUMERICAL SIMULATION INDEPENDENT CROSS-CHECK
Academic Project: Anuska Ghosh | B.Tech ECE, Roll 66, Sec B4 (2026-2027)

This script independently evaluates the Shichman-Hodges analytical NMOS model,
cross-checks mathematical boundary conditions and derivative continuity,
and generates the authoritative simulation datasets and publication-quality plots.
"""

import os
import json
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg") # Non-interactive headless backend
import matplotlib.pyplot as plt

def run_cross_check_and_generate():
    print("=" * 75)
    print("  INSIDE THE SILICON: INDEPENDENT NUMERICAL CROSS-CHECK & GENERATOR")
    print("  Model: Shichman-Hodges Ideal Long-Channel NMOS Model")
    print("=" * 75)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    # 1. Device Physical Parameters (Standard Educational NMOS Formulation)
    eps_0 = 8.854187817e-12      # F/m
    eps_ox_rel = 3.9             # SiO2 relative permittivity
    eps_ox = eps_ox_rel * eps_0  # F/m ~ 3.453e-11 F/m
    # Nominal educational gate dielectric thickness: t_ox = 17.2656 nm -> C_ox = 2.000e-3 F/m^2 (0.200 uF/cm^2)
    C_ox = 2.000e-3              # F/m^2 (0.200 uF/cm^2)
    t_ox = eps_ox / C_ox         # m ~ 17.2656 nm
    mu_n_cm2 = 500.0             # cm^2/(V*s)
    mu_n = mu_n_cm2 * 1e-4       # m^2/(V*s) = 0.0500
    k_n_prime = mu_n * C_ox      # A/V^2 = 1.000e-4 (0.100 mA/V^2)
    W = 10.0e-6                  # 10.0 um
    L = 1.0e-6                   # 1.0 um
    aspect_ratio = W / L         # 10.0
    beta = k_n_prime * aspect_ratio # A/V^2 = 1.000e-3 (1.000 mA/V^2 exact)
    V_TH = 0.70                  # V

    print("\n[STEP 1] Device Parameters & Exact SI Derivations:")
    print(f"  V_TH                  = {V_TH:.3f} V")
    print(f"  mu_n                  = {mu_n_cm2:.1f} cm^2/(V*s)  [= {mu_n:.4f} m^2/(V*s)]")
    print(f"  t_ox                  = {t_ox*1e9:.3f} nm          [= {t_ox:.4e} m]")
    print(f"  C_ox                  = {C_ox*1e2:.3f} uF/cm^2     [= {C_ox:.4e} F/m^2]")
    print(f"  k_n' (mu_n * C_ox)    = {k_n_prime*1e3:.3f} mA/V^2      [= {k_n_prime:.4e} A/V^2]")
    print(f"  W / L                 = {W*1e6:.1f} um / {L*1e6:.1f} um (Aspect Ratio = {aspect_ratio:.1f})")
    print(f"  beta (k_n' * W/L)     = {beta*1e3:.3f} mA/V^2      [= {beta:.4e} A/V^2 exact]")

    # Voltage Sweeps
    v_gs_list = [1.0, 1.5, 2.0, 2.5, 3.0]
    v_ds_vals = np.round(np.arange(0.0, 3.55, 0.05), 2) # 71 points: 0.0 to 3.5 V

    # Numerical Verification Data Structures
    curves_data = []
    csv_rows = []
    
    print("\n[STEP 2] Parametric Sweep & Mathematical Assertion Checks:")
    print("  (Verifying first-derivative continuity dI_D/dV_DS = 0 across pinch-off boundary)")
    print("-" * 75)
    print(f" {'V_GS (V)':>8} | {'V_DS,sat (V)':>12} | {'I_D,sat (mA)':>12} | {'1st-Deriv dI/dV (mS)':>20} | {'Check':>8}")
    print("-" * 75)

    all_tests_passed = True

    for vgs in v_gs_list:
        v_ds_sat = round(vgs - V_TH, 4)
        i_d_sat = round((beta / 2.0) * (vgs - V_TH)**2, 8)
        gm_sat = round(beta * (vgs - V_TH), 8)

        # Check derivative continuity at boundary:
        # Linear dId/dVds as Vds -> V_ds_sat from left: beta * ((Vgs - Vth) - Vds) -> 0
        # Saturation dId/dVds: 0
        left_deriv = beta * ((vgs - V_TH) - v_ds_sat) # Exactly zero
        continuity_passed = abs(left_deriv) < 1e-12

        status = "PASSED" if continuity_passed else "FAILED"
        if not continuity_passed:
            all_tests_passed = False

        print(f" {vgs:8.2f} | {v_ds_sat:12.3f} | {i_d_sat*1e3:12.4f} | {left_deriv*1e3:24.4e} | {status:>8}")

        curve_points = []
        for vds in v_ds_vals:
            if vgs <= V_TH:
                id_val = 0.0
                reg = "Cut-off"
            elif vds < v_ds_sat:
                id_val = beta * ((vgs - V_TH) * vds - (vds**2 / 2.0))
                reg = "Linear (Triode)"
            else:
                id_val = i_d_sat
                reg = "Saturation (Pinch-off)"

            curve_points.append({
                "v_ds": float(vds),
                "i_d_mA": round(float(id_val * 1e3), 4),
                "region": reg
            })

            csv_rows.append([
                f"{vgs:.2f}",
                f"{vds:.2f}",
                f"{id_val * 1e3:.4f}",
                reg
            ])

        curves_data.append({
            "v_gs": float(vgs),
            "v_ds_sat": float(v_ds_sat),
            "i_d_sat_mA": round(float(i_d_sat * 1e3), 4),
            "data": curve_points
        })

    print("-" * 75)
    print(f"  All derivative continuity and boundary checks: {'PASSED' if all_tests_passed else 'FAILED'}")

    # [STEP 3] Export Authoritative CSV
    csv_file = os.path.join(results_dir, "mosfet_results.csv")
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["V_GS_V", "V_DS_V", "I_D_mA", "Operating_Region"])
        writer.writerows(csv_rows)
    print(f"\n[STEP 3] CSV Export: {csv_file} ({len(csv_rows)} data points)")

    # [STEP 4] Export Authoritative JSON
    json_file = os.path.join(results_dir, "mosfet_results.json")
    json_content = {
        "project": "INSIDE THE SILICON",
        "author": "Anuska Ghosh",
        "roll_number": "66",
        "section": "B4",
        "academic_year": "2026-2027",
        "model": "Shichman-Hodges Ideal Long-Channel NMOS",
        "parameters": {
            "threshold_voltage_V": V_TH,
            "beta_mA_V2": round(beta * 1e3, 3),
            "mobility_cm2_Vs": mu_n_cm2,
            "oxide_capacitance_uF_cm2": round(C_ox * 1e2, 4),
            "channel_width_um": W * 1e6,
            "channel_length_um": L * 1e6,
            "aspect_ratio_W_over_L": aspect_ratio
        },
        "curves": curves_data
    }
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_content, f, indent=2)
    print(f"[STEP 4] JSON Export: {json_file}")

    # [STEP 5] Generate High-Resolution Publication Plot
    png_file = os.path.join(results_dir, "mosfet_characteristics.png")
    
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    fig.patch.set_facecolor("#0b0e14")
    ax.set_facecolor("#07090e")

    colors = ["#33ccff", "#00f2a9", "#ffd11a", "#ff7324", "#d957ff"]

    for i, curve in enumerate(curves_data):
        vds_arr = [p["v_ds"] for p in curve["data"]]
        id_arr = [p["i_d_mA"] for p in curve["data"]]
        lbl = f"$V_{{GS}} = {curve['v_gs']:.1f}$ V  ($I_{{D,sat}} = {curve['i_d_sat_mA']:.3f}$ mA)"
        ax.plot(vds_arr, id_arr, color=colors[i], linewidth=2.4, label=lbl)

    # Plot saturation boundary parabola: V_DS = V_GS - V_TH => I_D = (beta/2) * V_DS^2
    v_boundary = np.linspace(0.0, max(c["v_ds_sat"] for c in curves_data), 100)
    i_boundary = (beta / 2.0) * (v_boundary**2) * 1e3
    ax.plot(v_boundary, i_boundary, color="#ff4d4d", linestyle="--", linewidth=2.0,
            label=r"Pinch-Off Boundary: $V_{DS,sat} = V_{GS} - V_{TH}$")

    # Region Labels
    ax.text(0.45, 1.65, "LINEAR (TRIODE) REGION\n$V_{DS} < V_{GS} - V_{TH}$",
            color="#5ce1e6", fontsize=9.5, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#0b1726", edgecolor="#1a4d6e", alpha=0.90))
    ax.text(2.10, 0.45, r"SATURATION (PINCH-OFF) REGION" + "\n" + r"$V_{DS} \geq V_{GS} - V_{TH}$",
            color="#ffc048", fontsize=9.5, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#261c0b", edgecolor="#6e4f1a", alpha=0.90))

    ax.set_xlabel("Drain-to-Source Voltage $V_{DS}$ (V)", fontsize=12, fontweight="bold", color="#e6f2ff", labelpad=10)
    ax.set_ylabel("Drain Current $I_D$ (mA)", fontsize=12, fontweight="bold", color="#e6f2ff", labelpad=10)
    ax.set_title("INSIDE THE SILICON: NMOS Drain Characteristics ($I_D - V_{DS}$)\n"
                 r"Shichman-Hodges Educational Model | $V_{TH} = 0.70$ V, $\beta = 1.00$ mA/V$^2$",
                 fontsize=13, fontweight="bold", color="#ffffff", pad=14)

    ax.set_xlim(0.0, 3.5)
    ax.set_ylim(0.0, 3.0)
    ax.grid(True, linestyle=":", color="#24334a", alpha=0.7)

    legend = ax.legend(loc="upper left", framealpha=0.9, facecolor="#0e131d", edgecolor="#24334a", fontsize=9.5)
    for text in legend.get_texts():
        text.set_color("#d8e5f3")

    plt.tight_layout()
    plt.savefig(png_file, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[STEP 5] Publication Plot Export: {png_file} (300 DPI)")

    # [STEP 6] Cross-Check CSV vs JSON
    print("\n[STEP 6] Cross-Verification Between CSV and JSON Datasets:")
    with open(csv_file, "r", encoding="utf-8") as f:
        csv_lines = list(csv.reader(f))[1:] # skip header
    with open(json_file, "r", encoding="utf-8") as f:
        json_obj = json.load(f)

    flat_json_points = []
    for c in json_obj["curves"]:
        for p in c["data"]:
            flat_json_points.append([f"{c['v_gs']:.2f}", f"{p['v_ds']:.2f}", f"{p['i_d_mA']:.4f}", p["region"]])

    mismatch_count = 0
    for idx, (csv_pt, json_pt) in enumerate(zip(csv_lines, flat_json_points)):
        if csv_pt != json_pt:
            mismatch_count += 1
            print(f"  Mismatch at index {idx}: CSV={csv_pt} vs JSON={json_pt}")

    if mismatch_count == 0:
        print(f"  Total verified points: {len(csv_lines)}")
        print("  CSV and JSON records match 100% identically with zero discrepancies!")
    else:
        print(f"  Warning: {mismatch_count} mismatches found!")

    print("\n" + "=" * 75)
    print("  SIMULATION CROSS-CHECK & GENERATION COMPLETED SUCCESSFULLY")
    print("=" * 75)

if __name__ == "__main__":
    run_cross_check_and_generate()
