"""
INSIDE THE SILICON: The Science Behind Semiconductor Microchips
Flask Backend Service (Optional deployment runtime for containerized hosting)

Academic Showcase:
Student Name: Anuska Ghosh
Course: B.Tech First Year (ECE), Section B4, Roll Number: 66
Academic Year: 2026-2027
Department: Language Lab / Electronics and Communication Engineering
"""

import os
import json
from flask import Flask, send_from_directory, jsonify, request

app = Flask(__name__, static_folder="static", template_folder=".")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    """Serves the primary presentation website."""
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    """Serves root-level and directory static files."""
    if os.path.exists(os.path.join(BASE_DIR, path)):
        return send_from_directory(BASE_DIR, path)
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/api/results", methods=["GET"])
def get_simulation_results():
    """Returns pre-generated authoritative MATLAB simulation results."""
    results_path = os.path.join(BASE_DIR, "results", "mosfet_results.json")
    if os.path.exists(results_path):
        with open(results_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({"error": "Results not found. Run simulation first."}), 404

@app.route("/api/simulate", methods=["POST"])
def dynamic_simulation():
    """
    Optional API endpoint to compute Shichman-Hodges NMOS parameters dynamically
    for external API consumers.
    """
    req_data = request.get_json() or {}
    v_th = float(req_data.get("v_th", 0.70))
    beta = float(req_data.get("beta", 1.0e-3)) # A/V^2
    v_gs_list = req_data.get("v_gs", [1.0, 1.5, 2.0, 2.5, 3.0])
    v_ds_max = float(req_data.get("v_ds_max", 3.5))
    step = float(req_data.get("v_ds_step", 0.05))

    v_ds_vals = [round(i * step, 3) for i in range(int(v_ds_max / step) + 1)]
    curves = []

    for vgs in v_gs_list:
        vgs = float(vgs)
        v_ds_sat = max(0.0, vgs - v_th)
        i_d_sat = (beta / 2.0) * (vgs - v_th)**2 if vgs > v_th else 0.0

        curve_points = []
        for vds in v_ds_vals:
            if vgs <= v_th:
                id_val = 0.0
                region = "Cut-off"
            elif vds < v_ds_sat:
                id_val = beta * ((vgs - v_th) * vds - (vds**2 / 2.0))
                region = "Linear (Triode)"
            else:
                id_val = i_d_sat
                region = "Saturation (Pinch-off)"
            
            curve_points.append({
                "v_ds": vds,
                "i_d_mA": round(id_val * 1e3, 4),
                "region": region
            })
        
        curves.append({
            "v_gs": vgs,
            "v_ds_sat": round(v_ds_sat, 3),
            "i_d_sat_mA": round(i_d_sat * 1e3, 4),
            "points": curve_points
        })

    return jsonify({
        "status": "success",
        "model": "Shichman-Hodges Educational Long-Channel NMOS",
        "parameters": {
            "v_th_V": v_th,
            "beta_mA_V2": beta * 1e3
        },
        "curves": curves
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
