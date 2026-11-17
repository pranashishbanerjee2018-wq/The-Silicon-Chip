import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('=== 1. CHECK SCRIPTS IN INDEX.HTML ===')
scripts = re.findall(r'<script\s+src=["\']([^"\']+)["\']', html)
for s in scripts:
    norm = os.path.normpath(s)
    exists = os.path.exists(norm)
    status = "OK" if exists else "MISSING!"
    print(f'[{status}] {s}')

print('\n=== 2. CHECK STYLESHEETS IN INDEX.HTML ===')
css_files = re.findall(r'<link\s+rel=["\']stylesheet["\']\s+href=["\']([^"\']+)["\']', html)
for c in css_files:
    norm = os.path.normpath(c)
    exists = os.path.exists(norm)
    status = "OK" if exists else "MISSING!"
    print(f'[{status}] {c}')

print('\n=== 3. CHECK IMAGES IN INDEX.HTML ===')
img_tags = re.findall(r'<img\s+[^>]*src=["\']([^"\']+)["\']', html)
for img in img_tags:
    norm = os.path.normpath(img)
    exists = os.path.exists(norm)
    status = "OK" if exists else "MISSING!"
    print(f'[{status}] {img}')

print('\n=== 4. CHECK CRITICAL DOM IDS ===')
critical_ids = [
    'hero-gateway',
    'presentation-section',
    'presentation-stage',
    'cinematic-bg-layer',
    'ambient-particles-canvas',
    'scientific-visualization-layer',
    'view-cleanroom_lab',
    'view-silicon_lattice',
    'view-pn_junction',
    'view-mosfet_transistor',
    'view-matlab_simulation',
    'view-ic_scale_zoom',
    'char-adrian-anchor',
    'char-ethan-anchor',
    'cinematic-telemetry-overlay',
    'dialogue-hud',
    'subtitle-speaker-badge',
    'subtitle-text',
    'timeline-progress',
    'dialogue-progress-fill',
    'timeline-scrub',
    'time-display',
    'act-display',
    'play-pause-btn',
    'skip-back-btn',
    'skip-forward-btn',
    'restart-btn',
    'speed-select',
    'volume-btn',
    'fullscreen-btn',
    'tech-modal',
    'outro-modal'
]

missing_ids = []
for cid in critical_ids:
    if f'id="{cid}"' not in html and f"id='{cid}'" not in html:
        missing_ids.append(cid)

if missing_ids:
    print(f"FAILED: Missing IDs: {missing_ids}")
else:
    print(f"ALL {len(critical_ids)} critical DOM IDs present in index.html.")

print('\n=== 5. CHECK AUTHENTIC MATLAB OUTPUTS ===')
results = [
    'matlab/MOSFET_Simulation.m',
    'results/mosfet_results.csv',
    'results/mosfet_results.json',
    'results/mosfet_characteristics.png'
]
for r in results:
    exists = os.path.exists(r)
    size = os.path.getsize(r) if exists else 0
    print(f'{"[OK]" if exists else "[MISSING]"} {r} ({size} bytes)')
