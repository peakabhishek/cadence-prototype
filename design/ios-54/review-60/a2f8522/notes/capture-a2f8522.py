"""Capture Mac Today at a2f8522, same synthetic goals and method as the 3b1f92f #55 review."""
import json, os, subprocess, sys, tempfile, time, socket, shutil
from pathlib import Path
from datetime import datetime, timedelta, timezone
from playwright.sync_api import sync_playwright

sys.path.insert(0, "/workspace/design-review-55")
import capture as C

OUT = Path("/workspace/design-review-60/a2f8522")
TREE = Path("/workspace/cadence-r60-a2f8522")
IST = C.IST

def seed(folder, *, sync_held=None, held_entries=None, schema_held=None, late_counts=None, v4=True):
    sys.path.insert(0, str(TREE / "server"))
    for m in [m for m in sys.modules if m in ("cadence_server", "phone_merge")]:
        del sys.modules[m]
    import cadence_server as cs
    now = datetime.now(IST); today = now.date()
    Cstamp = today.isoformat() + "T00:05:00+05:30"
    goals = [{"id": "g%d" % i, "title": t, "box_minutes": b, "box_period": "day", "created_at": Cstamp}
             for i, (t, b) in enumerate((("Write the weekly review", 45), ("Read one paper", 25), ("Gym", None), ("Plan Friday’s demo", 25)), 1)]
    base = today.isoformat()
    sessions = [
        {"id": "s1", "goal_id": "g1", "minutes": 25, "outcome": "grown", "started_at": base + "T00:06:00+05:30", "ended_at": base + "T00:31:00+05:30"},
        {"id": "s2", "goal_id": "g2", "minutes": 25, "outcome": "grown", "started_at": base + "T00:32:00+05:30", "ended_at": base + "T00:57:00+05:30"},
    ]
    data = dict(cs.empty_data_v3(), days=[{"date": base, "goals": goals}], sessions=sessions)
    data = cs.with_days(data, today=today, disk=data)
    if sync_held is not None or held_entries is not None or schema_held is not None or late_counts is not None:
        rec = {"last_applied_seq": 3}
        if sync_held:
            rec["sync_held"] = sync_held
        if held_entries:
            rec["held"] = held_entries
        if schema_held is not None:
            rec["schema_held"] = schema_held
        state = {"devices": {"phone-r3": rec}}
        if late_counts is not None:
            state["late_counts"] = late_counts
        data["syncState"] = state
    form = cs.file_form(data, True) if v4 else data
    (folder / cs.DATA_FILENAME).write_text(json.dumps(form), "utf-8")

def run(variant, **seed_kw):
    tmp = Path(tempfile.mkdtemp()); folder = tmp / "OneDrive - Peak Routine" / "Cadence"; folder.mkdir(parents=True)
    (tmp / "cfg").mkdir(); (tmp / "cfg" / "config.json").write_text(json.dumps({"data_dir": str(folder)}))
    seed(folder, **seed_kw)
    port = C.free_port()
    env = dict(os.environ, CADENCE_CONFIG_DIR=str(tmp / "cfg"), CADENCE_SUGGESTED_DIR=str(folder), CADENCE_PORT=str(port), CADENCE_QUIET="1")
    proc = subprocess.Popen([sys.executable, str(TREE / "server" / "cadence_server.py")], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=str(TREE))
    try:
        for _ in range(50):
            try: socket.create_connection(("127.0.0.1", port), 0.2).close(); break
            except OSError: time.sleep(0.2)
        else:
            out = proc.stdout.read(4000).decode("utf-8", "replace") if proc.stdout else ""
            raise RuntimeError("server did not start: " + out)
        res = {}
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
            ctx = b.new_context(viewport={"width": 1280, "height": 800}, device_scale_factor=2, timezone_id="Asia/Kolkata")
            pg = ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append("console:" + m.text) if m.type == "error" else None)
            d = datetime.now(IST).date()
            pg.clock.install(time=datetime(d.year, d.month, d.day, 19, 30, tzinfo=IST))
            pg.goto("http://127.0.0.1:%d/#today" % port)
            pg.wait_for_selector("body[data-loaded]", timeout=15000)
            pg.wait_for_timeout(1200)
            res["notes"] = pg.evaluate("[...document.querySelectorAll('.sync-note')].map(e=>e.innerText)")
            res["bodyHasReviewCopy"] = pg.evaluate(r"""(() => {
              const t = document.body.innerText;
              return /too.?old|unreadable|schema|superseded|discard|Can.t tell which is newer|You also changed|Mac has Focus/i.test(t);
            })()""")
            res["bodySnippetHasLate"] = pg.evaluate("/late_counts|Got it|Review sheet|Add this session/i.test(document.body.innerText)")
            res["errors"] = errs
            res["title"] = pg.inner_text("#today-title") if pg.query_selector("#today-title") else None
            res["fullText"] = pg.evaluate("document.body.innerText")
            res["metrics"] = pg.evaluate("""()=>{const r=s=>{const e=document.querySelector(s);if(!e)return null;const b=e.getBoundingClientRect();return [Math.round(b.x*10)/10,Math.round(b.y*10)/10,Math.round(b.width*10)/10,Math.round(b.height*10)/10]};
                 const st=s=>{const e=document.querySelector(s);if(!e)return null;const c=getComputedStyle(e);return {fs:c.fontSize,fw:c.fontWeight,lh:c.lineHeight,color:c.color,bg:c.backgroundColor,pad:c.padding,rad:c.borderRadius,gap:c.gap,mt:c.marginTop,mb:c.marginBottom}};
                 return {note:r('.sync-note'),noteIco:r('.sync-note svg'),noteSpan:r('.sync-note span'),noteStyle:st('.sync-note'),noteText: document.querySelector('.sync-note span') && document.querySelector('.sync-note span').textContent}}""")
            f = OUT / (variant + ".png")
            pg.screenshot(path=str(f)); res["file"] = str(f)
            if pg.query_selector(".sync-note"):
                pg.locator(".panel.left").screenshot(path=str(OUT / (variant + "-panel.png")))
                pg.locator(".sync-note").screenshot(path=str(OUT / (variant + "-note.png")))
            b.close()
        return res
    finally:
        proc.terminate()
        try: proc.wait(5)
        except Exception: proc.kill()
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [
        ("today-normal", {}),
        ("today-synchold-3", {"sync_held": [1, 2, 3]}),
        ("today-synchold-1", {"sync_held": [2]}),
        ("today-superseded", {"held_entries": [{"seq": 1, "reason": "superseded", "fields": ["title", "box_minutes"]}]}),
        ("today-superseded-later", {"held_entries": [{"seq": 1, "reason": "superseded", "fields": ["title"], "later": ["title"]}]}),
        ("today-late-counts-only", {"late_counts": {"applied": 2, "review": 1}}),
        ("today-synchold-1-late-counts", {"sync_held": [2], "late_counts": {"applied": 2, "review": 1}}),
    ]
    results = {}
    for name, kw in jobs:
        r = run(name, **kw)
        results[name] = {k: v for k, v in r.items() if k != "fullText"}
        results[name]["_hasDiscard"] = "discard" in (r.get("fullText") or "").lower()
        results[name]["_hasSupersededWord"] = "superseded" in (r.get("fullText") or "").lower()
        print(name, r["notes"], "reviewCopy=", r["bodyHasReviewCopy"], "lateUI=", r["bodySnippetHasLate"],
              "title=", r["title"], "errs=", r["errors"])
    json.dump(results, open("/workspace/design-review-60/capture-a2f8522-results.json", "w"), indent=1, ensure_ascii=False)
