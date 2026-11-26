# Renders the cadence#58 frames from the prototype. Serve the repo root first: python3 -m http.server 8799 --bind 127.0.0.1
import json, sys
from playwright.sync_api import sync_playwright
OUT = sys.argv[1] if len(sys.argv) > 1 else "design/ios-54/frames/mac/review-sheet"
import os; os.makedirs(OUT, exist_ok=True)
STATES = [("01-today-note-review", "today"), ("02-sheet-one-entry", "one"), ("03-sheet-many-scrolling", "many"),
          ("04-undo-keep-mac", "undo-keep"), ("05-undo-use-phone", "undo-use"), ("06-last-resolved-note-gone", "resolved"),
          ("07-loading", "loading"), ("08-error-still-held", "error"), ("09-day-boundary-midnight-ist", "midnight"),
          ("10-closed-without-action", "closed"),
          ("11-today-applied-note-once", "upgrade"), ("12-sheet-empty", "empty"), ("13-undo-keep-for-all", "undo-all"),
          ("14-sheet-mixed-session-and-edit", "mixed"), ("15-sheet-remove-restore", "remove-restore"), ("16-today-applied-only", "applied-only")]
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2, timezone_id="Asia/Kolkata")
    pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("requestfailed", lambda r: errs.append("failed " + r.url))
    pg.on("response", lambda r: errs.append("%d %s" % (r.status, r.url)) if r.status >= 400 else None)
    for name, st in STATES:
        pg.goto("http://127.0.0.1:8799/prototype/mac-review/?state=%s&frame=1" % st)
        pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        if st == "many": pg.evaluate("document.querySelector('.list').scrollTop=0"); pg.wait_for_timeout(100)
        info = pg.evaluate("""()=>({text:document.body.innerText, note:(document.querySelector('.note .txt')||{}).textContent||null,
          sheet:!!document.querySelector('.sheet'), rows:document.querySelectorAll('.row[data-id]').length,
          listScroll: (()=>{const l=document.querySelector('.list');return l?[l.scrollTop,l.scrollHeight,l.clientHeight]:null})(),
          fonts:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family)})""")
        pg.screenshot(path="%s/%s.png" % (OUT, name))
        res[name] = {k: v for k, v in info.items() if k != "text"}
        res[name]["discard"] = "discard" in info["text"].lower()
        res[name]["straight_apos"] = [w for w in info["text"].split() if "'" in w]
    b.close()
res["errors"] = errs
json.dump(res, open("/tmp/review-sheet-shots.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(res, indent=1, ensure_ascii=False))
