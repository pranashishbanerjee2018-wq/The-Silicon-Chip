import os
import sys
import time
import threading
import subprocess
from http.server import SimpleHTTPRequestHandler, HTTPServer
from PIL import Image

PORT = 8089
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

print(f"Using browser binary: {CHROME_PATH}")

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # suppress server logs for cleaner output

def start_server():
    server = HTTPServer(('127.0.0.1', PORT), QuietHandler)
    server.serve_forever()

t = threading.Thread(target=start_server, daemon=True)
t.start()
print(f"Local test HTTP server started on http://127.0.0.1:{PORT}")
time.sleep(1)

os.makedirs('docs/screenshots', exist_ok=True)

scenes = [
    ("01_hero_gateway.png", f"http://127.0.0.1:{PORT}/index.html", "Hero Gateway Screen"),
    ("02_cleanroom_two_characters.png", f"http://127.0.0.1:{PORT}/index.html?act=1", "Act 1: Two-Character Cleanroom Lab Scene"),
    ("03_silicon_lattice.png", f"http://127.0.0.1:{PORT}/index.html?act=2", "Act 2: Silicon Crystal Lattice & Bandgap"),
    ("04_pn_junction.png", f"http://127.0.0.1:{PORT}/index.html?act=3", "Act 3: PN Junction Depletion Zone"),
    ("05_mosfet_transistor.png", f"http://127.0.0.1:{PORT}/index.html?act=4", "Act 4: 3D MOSFET Channel Pinch-Off"),
    ("06_matlab_workbench.png", f"http://127.0.0.1:{PORT}/index.html?act=5", "Act 5: Desktop MATLAB Educational Simulator"),
    ("07_ic_scale_zoom.png", f"http://127.0.0.1:{PORT}/index.html?act=6", "Act 6: Integrated Circuit Multi-Scale Zoom"),
    ("08_viva_exam_modal.png", f"http://127.0.0.1:{PORT}/index.html?modal=tech", "Technical Specifications & Viva Questions Modal")
]

all_passed = True
for filename, url, description in scenes:
    out_path = os.path.join('docs', 'screenshots', filename)
    print(f"\nCapturing: {description} -> {out_path}")
    
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--virtual-time-budget=2000", # allow scripts to render visualizers
        "--window-size=1440,900",
        f"--screenshot={out_path}",
        url
    ]
    
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=20)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
            im = Image.open(out_path)
            print(f"  [SUCCESS] {out_path} ({im.size[0]}x{im.size[1]}, {os.path.getsize(out_path)} bytes)")
        else:
            print(f"  [FAIL] Screenshot missing or too small! Size: {os.path.getsize(out_path) if os.path.exists(out_path) else 0}")
            all_passed = False
    except Exception as e:
        print(f"  [ERROR] Execution failed: {e}")
        all_passed = False

if all_passed:
    print("\nALL 8 SCENE SCREENSHOTS CAPTURED AND VERIFIED SUCCESSFULLY!")
else:
    print("\nSOME SCREENSHOTS FAILED. Inspect outputs.")
