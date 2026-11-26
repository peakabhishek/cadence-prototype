"""Builds ../index.html (self-contained) from app.src.html + app.js + the approved tokens + plant SVGs."""
import base64, re, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent
REPO = OUT.parent.parent
tok = pathlib.Path("/workspace/focus-tracker/handoff/tokens.css").read_text()
ios = (REPO / "design/ios-54/ios-tokens.css").read_text()
plants = {}
for n in ["empty", "sprout", "early", "mid", "full", "withered"]:
    svg = (REPO / "design/ios-54/src/plants" / f"{n}.svg").read_bytes()
    plants[n] = "data:image/svg+xml;base64," + base64.b64encode(svg).decode()
import json
bg = re.search(r"--bg:\s*(#[0-9A-Fa-f]{6})", tok).group(1)
html = (HERE / "app.src.html").read_text()
js = (HERE / "app.js").read_text()
ios = ios.replace("<style>", "&lt;style&gt;").replace("</style>", "&lt;/style&gt;")
tok = tok.replace("<style>", "&lt;style&gt;").replace("</style>", "&lt;/style&gt;")
html = html.replace("__TOKENS__", tok).replace("__IOSTOKENS__", ios).replace("__BG__", bg)
html = html.replace("__PLANTS__", json.dumps(plants)).replace("__JS__", js)
html = re.sub(r"\{\{(\d+(?:\.\d+)?)\}\}", lambda m: f"{float(m.group(1))/17:.4f}rem", html)
(OUT / "index.html").write_text(html)
import json as _j
(OUT / "manifest.webmanifest").write_text(_j.dumps({
    "name": "Cadence for iPhone (Option B demo)", "short_name": "Cadence", "description": "Clickable prototype, fake data.",
    "start_url": "./", "scope": "./", "display": "standalone", "orientation": "portrait",
    "background_color": bg, "theme_color": bg,
    "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"}]}, indent=2))
print("index.html", (OUT / "index.html").stat().st_size, "bytes; bg", bg)
