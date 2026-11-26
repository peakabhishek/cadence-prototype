"""Capture Mac Today (synthetic data only) at BEFORE (260dd8d) and AFTER (6975f9b)."""
import json, os, subprocess, sys, tempfile, time, socket, shutil
from pathlib import Path
from datetime import datetime, timedelta, timezone
from playwright.sync_api import sync_playwright
IST = timezone(timedelta(hours=5, minutes=30))
OUT = Path("/workspace/design-review-55")
TREES = {"before": Path("/workspace/cadence-r55-before"), "after": Path("/workspace/cadence-r55-after")}

def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p

def seed(tree, folder, held, v4):
    sys.path.insert(0, str(tree / "server"))
    for m in [m for m in sys.modules if m in ("cadence_server", "phone_merge")]:
        del sys.modules[m]
    import cadence_server as cs
    now = datetime.now(IST); today = now.date()
    C = today.isoformat() + "T00:05:00+05:30"
    goals = [{"id": "g%d" % i, "title": t, "box_minutes": b, "box_period": "day", "created_at": C}
             for i, (t, b) in enumerate((("Write the weekly review", 45), ("Read one paper", 25), ("Gym", None), ("Plan Friday’s demo", 25)), 1)]
    base = today.isoformat()
    sessions = [
        {"id": "s1", "goal_id": "g1", "minutes": 25, "outcome": "grown", "started_at": base + "T00:06:00+05:30", "ended_at": base + "T00:31:00+05:30"},
        {"id": "s2", "goal_id": "g2", "minutes": 25, "outcome": "grown", "started_at": base + "T00:32:00+05:30", "ended_at": base + "T00:57:00+05:30"},
    ]
    data = dict(cs.empty_data_v3(), days=[{"date": base, "goals": goals}], sessions=sessions)
    data = cs.with_days(data, today=today, disk=data)
    if held is not None and hasattr(cs,'file_form'):
        data["syncState"] = {"devices": {"phone-r3": dict({"last_applied_seq": 3}, **({"sync_held": held} if held else {}))}}
    form = cs.file_form(data, True) if (v4 and hasattr(cs,'file_form')) else data
    (folder / cs.DATA_FILENAME).write_text(json.dumps(form), "utf-8")

def run(label, tree, variant, held, v4=True, phone=False, wait_note=None):
    tmp = Path(tempfile.mkdtemp()); folder = tmp / "OneDrive - Peak Routine" / "Cadence"; folder.mkdir(parents=True)
    (tmp / "cfg").mkdir(); (tmp / "cfg" / "config.json").write_text(json.dumps({"data_dir": str(folder)}))
    seed(tree, folder, held, v4)
    port = free_port()
    env = dict(os.environ, CADENCE_CONFIG_DIR=str(tmp / "cfg"), CADENCE_SUGGESTED_DIR=str(folder), CADENCE_PORT=str(port), CADENCE_QUIET="1")
    proc = subprocess.Popen([sys.executable, str(tree / "server" / "cadence_server.py")], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=str(tree))
    try:
        for _ in range(50):
            try: socket.create_connection(("127.0.0.1", port), 0.2).close(); break
            except OSError: time.sleep(0.2)
        res = {}
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
            vp = {"width": 390, "height": 844} if phone else {"width": 1280, "height": 800}
            ctx = b.new_context(viewport=vp, device_scale_factor=2, timezone_id="Asia/Kolkata")
            pg = ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append("console:" + m.text) if m.type == "error" else None)
            if phone:
                pg.add_init_script("window.Capacitor={isNativePlatform:function(){return true;}};window.CADENCE_CONFIG={phoneStore:'mock-onedrive'};")
            else:
                d = datetime.now(IST).date()
                pg.clock.install(time=datetime(d.year, d.month, d.day, 19, 30, tzinfo=IST))  # evening, as in the frame
            pg.goto("http://127.0.0.1:%d/#today" % port)
            pg.wait_for_selector("body[data-loaded]", timeout=15000)
            pg.wait_for_timeout(1200)
            res["notes"] = pg.evaluate("[...document.querySelectorAll('.sync-note')].map(e=>e.innerText)")
            res["banner"] = pg.evaluate("[...document.querySelectorAll('#demo-banner')].map(e=>e.innerText)")
            res["errors"] = errs
            res["title"] = pg.inner_text("#today-title") if pg.query_selector("#today-title") else None
            if not phone:
                res["metrics"] = pg.evaluate("""()=>{const r=s=>{const e=document.querySelector(s);if(!e)return null;const b=e.getBoundingClientRect();return [Math.round(b.x*10)/10,Math.round(b.y*10)/10,Math.round(b.width*10)/10,Math.round(b.height*10)/10]};
                 const st=s=>{const e=document.querySelector(s);if(!e)return null;const c=getComputedStyle(e);return {fs:c.fontSize,fw:c.fontWeight,lh:c.lineHeight,color:c.color,bg:c.backgroundColor,pad:c.padding,rad:c.borderRadius,gap:c.gap,mt:c.marginTop,mb:c.marginBottom}};
                 return {panel:r('.panel.left'),h1:r('#today-title'),sub:r('.today .sub'),note:r('.sync-note'),noteIco:r('.sync-note svg'),noteSpan:r('.sync-note span'),goalsLbl:r('.goals .lbls'),firstGoal:r('.goals .goal, .goals .row, .goals li'),noteStyle:st('.sync-note'),noteSpanStyle:st('.sync-note span')}}""")
            f = OUT / label / (variant + ".png")
            pg.screenshot(path=str(f)); res["file"] = str(f)
            if not phone and pg.query_selector(".sync-note"):
                pg.locator(".panel.left").screenshot(path=str(OUT / label / (variant + "-panel.png")))
            b.close()
        return res
    finally:
        proc.terminate()
        try: proc.wait(5)
        except Exception: proc.kill()
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    results = {}
    for label in ("before", "after"):
        tree = TREES[label]
        for variant, held in (("today-normal", None), ("today-held-empty-list", [])):
            results[label + "/" + variant] = run(label, tree, variant, held)
    tree = TREES["after"]
    results["after/today-synchold-3"] = run("after", tree, "today-synchold-3", [1, 2, 3])
    results["after/today-synchold-1"] = run("after", tree, "today-synchold-1", [2])
    results["after/today-v3-file"] = run("after", tree, "today-v3-file-no-syncstate", None, v4=False)
    results["after/phone-390-demo-banner"] = run("after", tree, "phone-390-demo-banner", None, phone=True)
    results["before/phone-390-no-banner"] = run("before", TREES["before"], "phone-390-no-banner", None, phone=True)
    json.dump(results, open(OUT / "capture-results.json", "w"), indent=1, ensure_ascii=False)
    for k, v in results.items(): print(k, v["notes"], v["banner"], v["errors"], v["title"])
