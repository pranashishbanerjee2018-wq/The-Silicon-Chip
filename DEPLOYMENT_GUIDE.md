# Deployment Guide
## INSIDE THE SILICON: The Science Behind Semiconductor Microchips

This guide provides step-by-step instructions for deploying the project to **GitHub Pages**, running it locally on **Windows 11 / macOS / Linux**, hosting it via the included **Flask backend**, and running it inside a **Docker container**.

---

## 1. GitHub Pages Deployment (Zero-Backend Mode)

The project is natively architected for **GitHub Pages**. All interactive visualizers, dual-voice speech synthesis, laboratory soundscapes, and MATLAB desktop emulation execute 100% client-side in standard ECMAScript 2020 JavaScript.

### Step-by-Step Instructions:
1. **Initialize Git Repository (if not already done):**
   ```bash
   cd inside_the_silicon
   git init
   git add .
   git commit -m "Initial release: Inside the Silicon scientific presentation"
   ```

2. **Push to GitHub:**
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-username>/inside-the-silicon.git
   git push -u origin main
   ```

3. **Enable GitHub Pages:**
   - Go to your repository settings on GitHub (`Settings` -> `Pages`).
   - Under **Build and deployment** > **Source**, select **Deploy from a branch**.
   - Under **Branch**, select `main` and root folder `/(root)`.
   - Click **Save**.

4. **Verify Deployment:**
   - Within 1–2 minutes, your website will be live at:
     `https://<your-username>.github.io/inside-the-silicon/`
   - All asset links use strict relative paths (`static/css/...`, `static/js/...`, `results/...`), guaranteeing flawless operation on GitHub Pages sub-paths.

---

## 2. Local Static Server Deployment

Because modern browsers enforce strict Cross-Origin Resource Sharing (CORS) policies when loading local JSON files via the `file://` protocol (`fetch('static/data/dialogue.json')`), running a lightweight local server is recommended during development:

### Option A: Python Built-In HTTP Server (Zero Dependencies)
```bash
cd inside_the_silicon
python -m http.server 8000
```
Open your browser to: `http://localhost:8000`

### Option B: Node.js `npx serve`
```bash
cd inside_the_silicon
npx serve .
```

### Option C: VS Code Live Server Extension
- Right-click `index.html` inside VS Code and select **Open with Live Server**.

---

## 3. Python Flask Backend Deployment

An optional Flask application (`app.py`) is provided for platforms requiring server-side Python hosting (such as Render, Railway, Heroku, or PythonAnywhere):

### Installation & Run:
```bash
cd inside_the_silicon
pip install -r requirements.txt
python app.py
```
Open your browser to: `http://127.0.0.1:5000`

---

## 4. Docker Containerization

To run the project in an isolated, production-grade container environment:

### Build Container:
```bash
docker build -t inside-the-silicon:latest .
```

### Run Container:
```bash
docker run -d -p 8080:80 --name inside_silicon_app inside-the-silicon:latest
```
Access the application at: `http://localhost:8080`

---

## 5. Deployment Verification Checklist

Before publishing, verify:
- [x] `index.html` is at the repository root.
- [x] All asset paths use relative forward slashes (`static/css/`, `static/js/`, etc.).
- [x] Pre-generated MATLAB results (`results/mosfet_results.json`, `results/mosfet_results.csv`, `results/mosfet_characteristics.png`) are committed.
- [x] Audio unlock gateway functions cleanly on first click.
- [x] Responsive layout verified across mobile (375px), tablet (768px), and desktop (1920px).
