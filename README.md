# INSIDE THE SILICON
## The Science Behind Semiconductor Microchips

An Academic Language Lab & Electronics and Communication Engineering (ECE) Showcase

[![GitHub Pages Deployment](https://img.shields.io/badge/Deployment-GitHub%20Pages-brightgreen)](#github-pages-deployment)
[![MATLAB Simulation](https://img.shields.io/badge/Simulation-MATLAB%20%7C%20Octave-blue)](#matlab-simulation)
[![Academic Project](https://img.shields.io/badge/Course-B.Tech%20ECE%202026--2027-orange)](#student--academic-details)

---

## 1. Project Overview

**"INSIDE THE SILICON: The Science Behind Semiconductor Microchips"** is a cinematic, five-minute scientific web presentation and interactive laboratory application. Set within an advanced ISO 4 semiconductor cleanroom research facility at night, the project follows two research scientists—**Dr. Adrian** (Senior Semiconductor Device Scientist) and **Ethan** (Junior Electronics Researcher)—as they explore the solid-state physics, quantum mechanics, and circuit abstractions that enable microscopic silicon wafers to power modern computing.

The presentation merges:
- **Cinematic Scientific Storytelling:** A structured six-act dialogue exploring atomic lattice structures, energy bandgap physics, extrinsic doping, PN junction electrostatics, and MOSFET channel inversion.
- **Visual Consistency:** Photorealistic character representations for cinematic scenes paired with specialized SVG vector HUD portraits for interactive dialogue telemetry.
- **Interactive Scientific Visualizers:** Real-time animated HTML5 Canvas and SVG visualizers demonstrating silicon crystal tetrahedral bonding, carrier drift and diffusion, space-charge depletion widths, and MOSFET gate inversion.
- **Genuine MATLAB Simulation:** An authentic numerical simulation script (`MOSFET_Simulation.m`) modeling NMOS characteristic curves using the educational Shichman-Hodges formulation with complete SI unit derivations.
- **Interactive MATLAB Desktop Interface:** An in-browser IDE experience featuring a code editor with syntax highlighting, an interactive command window with animated `fprintf` logging, a workspace variable inspector, and interactive characteristic curve plotting with real-time parameter tweaking.
- **Dual-Voice Audio & Subtitles:** Timestamped dialogue progression with Web Speech API synthesis, fallback pre-recorded audio cues, and procedural Web Audio cleanroom laboratory soundscapes.
- **Zero-Dependency Static Deployment:** Designed to run 100% autonomously on GitHub Pages with no server-side runtime, with optional Flask/Docker packaging for server-based environments.

---

## 2. Student & Academic Details

- **Student Name:** Anuska Ghosh
- **Course:** Bachelor of Technology (B.Tech), First Year
- **Branch:** Electronics and Communication Engineering (ECE)
- **Section:** B4
- **Roll Number:** 66
- **Academic Year:** 2026–2027
- **Department:** Language Lab / Department of Electronics and Communication Engineering

---

## 3. Six-Act Screenplay Structure

1. **Act 1: The Discovery (0:00–0:35)**
   - *Setting:* Advanced ISO 4 semiconductor cleanroom at night, amber inspection lights, robotic 300mm wafer handling system.
   - *Core Theme:* Microprocessor scaling, billions of transistors per square millimeter, the central question of solid-state control.
2. **Act 2: The Silicon Foundation (0:35–1:20)**
   - *Setting:* Atomic scale visualization.
   - *Core Theme:* Group IV silicon diamond cubic lattice, covalent bonding, energy bandgap ($E_g = 1.12\text{ eV}$), intrinsic carrier concentration ($n_i$), extrinsic donor ($N_D$) and acceptor ($N_A$) doping.
3. **Act 3: The Secret of the Junction (1:20–2:05)**
   - *Setting:* Cross-sectional metallurgical boundary.
   - *Core Theme:* Carrier diffusion vs drift, uncompensated space-charge ions, condition-dependent built-in potential ($V_{bi}$), forward bias exponential diffusion, and nonzero reverse saturation leakage ($I_s$).
4. **Act 4: The Microchip Revolution (2:05–3:00)**
   - *Setting:* 3D planar NMOS transistor geometry.
   - *Core Theme:* Gate dielectric capacitance, threshold voltage ($V_{TH}$), surface inversion layer channel, linear vs saturation pinch-off ($V_{DS} \ge V_{GS} - V_{TH}$), digital logic inversion.
5. **Act 5: MATLAB Scientific Experiment (3:00–4:15)**
   - *Setting:* Cleanroom workstation running the MATLAB Desktop environment.
   - *Core Theme:* Mathematical validation of NMOS behavior using `MOSFET_Simulation.m`, parametric sweep of $V_{GS} \in [1.0, 3.0]\text{ V}$, pinch-off locus, tabular command window logging, and CSV dataset export.
6. **Act 6: The Future of Silicon (4:15–5:00)**
   - *Setting:* Macro-to-nanoscale camera pull-out.
   - *Core Theme:* FinFETs, Gate-All-Around (GAA) nanosheets, sub-2nm nodes, High-NA EUV lithography, pervasive computing in AI, robotics, space, and society.

---

## 4. Repository Structure

```
inside_the_silicon/
├── index.html                          # Root entry point for GitHub Pages
├── README.md                           # Project presentation, overview & academic metadata
├── DEPLOYMENT_GUIDE.md                 # GitHub Pages, local server & Docker instructions
├── requirements.txt                    # Python dependencies for optional backend/verification
├── app.py                              # Optional Flask server for local/cloud hosting
├── Dockerfile                          # Containerization configuration
├── Procfile                            # Cloud platform deployment process file
│
├── matlab/
│   ├── MOSFET_Simulation.m             # Authentic, fully-documented MATLAB script
│   └── README.md                       # MATLAB technical instructions, execution guide & equations
│
├── results/
│   ├── mosfet_results.json             # Structured simulation results for web visualization
│   ├── mosfet_results.csv              # Raw tabular IV simulation data for export
│   └── mosfet_characteristics.png      # High-resolution MATLAB-style generated plot
│
├── static/
│   ├── css/
│   │   ├── main.css                    # Base layout, typography, reset
│   │   ├── laboratory-theme.css        # Cleanroom dark aesthetic (midnight cyan, graphite, gold)
│   │   ├── cinematic-player.css        # Player HUD, scrub bar, subtitle card, controls
│   │   └── matlab-desktop.css          # MATLAB desktop interface styling, editor, workspace
│   │
│   ├── js/
│   │   ├── app.js                      # Application entry point & coordination
│   │   ├── presentation-engine.js      # Timeline, playback, scene state machine
│   │   ├── character_anim.js           # Two-character animation, speaker glow & camera director
│   │   ├── ambient-particles.js        # Continuous cleanroom laminar motes & laser sweep engine
│   │   ├── audio-voice-synthesizer.js  # Web Speech dual-voice + procedural Web Audio ambience
│   │   ├── matlab-simulator.js         # Interactive MATLAB IDE emulator, terminal, graph renderer
│   │   ├── visualizers/
│   │   │   ├── silicon-lattice.js      # Act 2: Crystal lattice, covalent bonds, doping
│   │   │   ├── pn-junction.js          # Act 3: Depletion region, drift/diffusion, bias
│   │   │   ├── mosfet-transistor.js    # Act 4: Gate field, inversion layer, pinch-off
│   │   │   └── ic-scale-zoom.js        # Act 6: Zoom from macro wafer to nanoscale transistor
│   │   └── data/
│   │       └── dialogue.json           # Complete timestamped script, speaker cues, subtitles
│   │
│   ├── images/
│   │   ├── characters/                 # Photorealistic feathered standees (Dr. Adrian & Ethan) & SVG icons
│   │   └── lab/                        # Cleanroom backgrounds, wafer illustrations
│   │
│   └── audio/                          # Audio assets and documentation
│
└── docs/
    ├── PROJECT_OVERVIEW.md             # Academic project background & presentation abstract
    ├── TECHNICAL_DOCUMENTATION.md      # Scientific derivations, algorithms & code architecture
    ├── SCREENSHOT_GUIDE.md             # Guide to key UI views for academic report submission
    └── TEST_REPORT.md                  # Comprehensive verification test matrix & results
```

---

## 5. Quick Start & Execution

### Option A: Static Web Execution (Recommended for GitHub Pages)
Because all animations, audio synthesis, and interactive simulations run directly in client-side HTML5/CSS3/JavaScript, simply open `index.html` in any modern web browser or serve via any static HTTP server:
```bash
# Using Python built-in HTTP server:
python -m http.server 8000
# Open http://localhost:8000 in your browser
```

### Option B: Optional Flask Server
For containerized or full-stack deployments:
```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5000 in your browser
```

### Option C: MATLAB Execution
To run the authentic numerical device simulation in MATLAB or GNU Octave:
```matlab
cd matlab/
MOSFET_Simulation
```
This executes the parameter calculations, outputs formatted console metrics, and exports CSV, JSON, and PNG graphics to `../results/`.

---

## 6. Scientific Attribution & References

1. Sze, S. M., & Ng, K. K. (2006). *Physics of Semiconductor Devices* (3rd ed.). John Wiley & Sons.
2. Streetman, B. G., & Banerjee, S. K. (2015). *Solid State Electronic Devices* (7th ed.). Pearson.
3. Sedra, A. S., & Smith, K. C. (2019). *Microelectronic Circuits* (8th ed.). Oxford University Press.
4. Pierret, R. F. (1996). *Semiconductor Device Fundamentals*. Addison-Wesley.
