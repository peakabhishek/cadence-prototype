"""Capture the #58 Review sheet at 011eb14, all 16 frame states, 1440x900 @2x, synthetic data only.
Runs the real server in-process (as tests/test_browser_smoke.py does) with the frames' own goal names."""
import json, os, sys, tempfile, threading, shutil, time
from pathlib import Path
from datetime import datetime, timedelta, timezone
from unittest import mock
from playwright.sync_api import sync_playwright

TREE = Path("/workspace/cadence-r61-011eb14")
sys.path.insert(0, str(TREE / "server")); sys.path.insert(0, str(TREE / "tests"))
import cadence_server as cs
import review_fixtures as fx

IST = timezone(timedelta(hours=5, minutes=30))
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/workspace/design-review-61/build")
OUT.mkdir(parents=True, exist_ok=True)
D = "2026-11-27"
FOCUS, DEEP = "Focus", "Deep work"
WEEKLY, WEEKLY_PHONE = "Write the weekly review", "Weekly review"
GYM, GYM_PHONE = "Gym", "Gym, legs day"
PAPER, BANK, DEMO = "Read one paper", "Call the bank", "Plan Friday’s demo"
at = lambda *a: datetime(*a, tzinfo=IST)
snaps = fx.later_snaps

def goals_today(extra=()):
    return [fx.goal("g1", FOCUS, 30, day=D), fx.goal("g2", WEEKLY, 45, day=D), fx.goal("g3", GYM, None, day=D),
            fx.goal("g4", PAPER, 25, day=D), fx.goal("g5", DEMO, 25, day=D)] + list(extra)

E = {  # the frames' entries, as the Mac would hold them
 "e1": dict(ch=fx.change(1, "add_session", "2026-11-18T11:00:00+05:30", session=fx.session("p1", "g4", 25, "2026-11-18")), held={"seq": 1, "reason": "too_old"}),
 "e2": dict(ch=fx.change(2, "edit_goal", D + "T10:00:00+05:30", goal_id="g1", set={"title": DEEP}), held={"seq": 2, "reason": "superseded", "fields": ["title"], "later": ["title"]}),
 "e3": dict(ch=fx.change(3, "edit_goal", D + "T10:01:00+05:30", goal_id="g2", set={"box_minutes": 60}), held={"seq": 3, "reason": "superseded", "fields": ["box_minutes"]}),
 "e4": dict(ch=fx.change(4, "edit_goal", D + "T10:02:00+05:30", goal_id="g2", set={"title": WEEKLY_PHONE}), held={"seq": 4, "reason": "superseded", "fields": ["title"]}),
 "e5": dict(ch=fx.change(5, "edit_goal", "2026-11-19T10:00:00+05:30", goal_id="g3", set={"title": GYM_PHONE}), held={"seq": 5, "reason": "too_old"}),
 "e6": dict(ch=fx.change(6, "add_goal", "2026-11-17T10:00:00+05:30", goal={"id": "n1", "title": BANK, "box_minutes": 30, "box_period": "day"}), held={"seq": 6, "reason": "too_old"}),
 "e7": dict(ch={"change_id": "c7", "seq": 7, "op": "future_op", "commit_at": "2026-11-24T10:00:00+05:30", "commit_day": "2026-11-24"}, held={"seq": 7, "reason": "invalid"}),
 "e9": dict(ch=fx.change(8, "edit_goal", "2026-11-26T10:00:00+05:30", goal_id="g5", set={"box_minutes": 50}), held={"seq": 8, "reason": "superseded", "fields": ["box_minutes"], "later": ["box_minutes"]}),
}
def days_base(goals):
    return {D: goals, "2026-11-18": [fx.goal("g4", PAPER, 25, day="2026-11-18"), fx.goal("g1", FOCUS, 30, day="2026-11-18")],
            "2026-11-19": [fx.goal("g3", GYM, None, day="2026-11-19")]}
def scenario(keys, schema=False, late_counts=None, mac_session=True, extra_goals=()):
    ents = [E[k] for k in keys]
    fs = {}
    if "e2" in keys: fs["g1"] = {"title": 1}
    if "e9" in keys: fs["g5"] = {"box_minutes": 2}
    sn = snaps(*[E[k]["held"]["seq"] for k in keys if E[k]["held"].get("later")])
    # a "Can't tell which is newer" row: the restart path leaves a snapshot with since = the counter floor (no Mac edit proven later)
    for k in keys:
        h_ = E[k]["held"]
        if h_["reason"] == "superseded" and not h_.get("later"):
            sn[str(h_["seq"])] = {"hold_seq": 1, "since": 1}
    if any(E[k]["held"]["reason"] == "superseded" and not E[k]["held"].get("later") for k in keys) and "g1" not in fs:
        fs["g1"] = {"title": 1}
    sess = [fx.session("m1", "g4", 25, "2026-11-18", hour=8)] if mac_session else []
    data, doc = fx.build(days_base(goals_today(extra_goals)), held=[e["held"] for e in ents], changes=[e["ch"] for e in ents],
                         sessions=sess, schema_held=2 if schema else None, field_seq=fs or None, snaps=sn or None, late_counts=late_counts)
    if schema: doc["schemaVersion"] = 2
    return data, doc
def many(): return scenario(["e1","e2","e3","e4","e5","e6","e7","e9"], schema=True)
def three(lc=None): return scenario(["e1","e2","e3"], late_counts=lc)
def one(): return scenario(["e2"], mac_session=False)
def upgrade():
    d, doc = fx.build(days_base(goals_today()), held=[{"seq": 1, "reason": "superseded", "fields": ["title"], "later": ["title"]},
        {"seq": 2, "reason": "superseded", "fields": ["box_minutes"], "later": ["box_minutes"]}, {"seq": 3, "reason": "superseded", "fields": ["box_minutes"], "later": ["box_minutes"]}],
        changes=[fx.change(1, "edit_goal", D + "T10:00:00+05:30", goal_id="g1", set={"title": DEEP}),
                 fx.change(2, "edit_goal", D + "T10:01:00+05:30", goal_id="g2", set={"box_minutes": 60}),
                 fx.change(3, "edit_goal", D + "T10:02:00+05:30", goal_id="g5", set={"box_minutes": 50})],
        field_seq={"g1": {"title": 1}, "g2": {"box_minutes": 2}, "g5": {"box_minutes": 3}}, snaps=snaps(1, 2, 3), late_counts={"applied": 8, "review": 3})
    return d, doc
def mixed():
    return fx.build({D: [fx.goal("g1", FOCUS, 30, day=D)], "2026-11-18": [fx.goal("g1", FOCUS, 30, day="2026-11-18")]},
        held=[E["e2"]["held"]], sync_held=[1], field_seq={"g1": {"title": 1}}, snaps=snaps(2),
        changes=[fx.change(1, "add_session", "2026-11-18T11:00:00+05:30", session=fx.session("p1", "g1", 25, "2026-11-18")), dict(E["e2"]["ch"], seq=2, change_id="c2")])
def remove_restore():
    live = [fx.goal("a%d" % i, n, 30, day=D) for i, n in enumerate(["Write the weekly review", "Read one paper", "Gym", "Plan Friday’s demo"], 1)]
    return fx.build({D: live + [fx.goal("k", DEEP, 30, day=D), fx.goal("m", "Inbox zero", 30, day=D), fx.goal("r", DEEP, 30, removed=True, day=D)]}, sync_held=[1, 2],
        changes=[fx.change(1, "remove_goal", D + "T10:00:00+05:30", goal_id="k"), fx.change(2, "restore_goal", D + "T10:01:00+05:30", goal_id="r")])
def applied_only():
    return fx.build({D: goals_today()}, changes=[], late_counts={"applied": 8, "review": 0})

class H:
    def __init__(self, pw, browser):
        self.pw, self.browser = pw, browser
    def start(self, scn, when):
        self.tmp = Path(tempfile.mkdtemp()); self.folder = self.tmp / "OneDrive - Peak Routine" / "Cadence"; self.folder.mkdir(parents=True)
        (self.tmp / "cfg").mkdir(); (self.tmp / "cfg" / "config.json").write_text(json.dumps({"data_dir": str(self.folder)}))
        os.environ["CADENCE_CONFIG_DIR"] = str(self.tmp / "cfg"); os.environ["CADENCE_SUGGESTED_DIR"] = str(self.folder); os.environ["CADENCE_QUIET"] = "1"
        data, doc = scn; fx.write(self.folder, data, doc, state_dir=self.tmp / "cfg")
        self.srv = cs.make_server(0); self.base = "http://127.0.0.1:%d" % self.srv.server_address[1]
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.srv_clock(when)
        self.errors = []; self.posts = []
        self.ctx = self.browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2, timezone_id="Asia/Kolkata")
        self.pg = self.ctx.new_page(); self.pg.set_default_timeout(15000)
        self.pg.on("pageerror", lambda e: self.errors.append(str(e)))
        self.pg.on("console", lambda m: self.errors.append("console:" + m.text) if m.type == "error" else None)
        self.pg.on("request", lambda r: self.posts.append((r.method, r.url, r.post_data)) if r.method == "POST" and "/api/held" in r.url else None)
        self.pg.clock.install(time=when)
        self.pg.goto(self.base + "/#today"); self.pg.wait_for_selector("body[data-loaded='true']")
        self.pg.evaluate("document.fonts.ready"); self.pg.wait_for_timeout(300)
        return self.pg
    def srv_clock(self, instant):
        if getattr(self, "_p", None): self._p.stop()
        base_real = time.time()
        self._p = mock.patch.object(cs, "_utc_now", lambda: instant.astimezone(timezone.utc) + timedelta(seconds=time.time() - base_real)); self._p.start()
    def open_sheet(self):
        pg = self.pg
        pg.click('.today .sync-note [data-act="review"]'); pg.wait_for_selector("#review-root .sheet")
        pg.wait_for_function("() => { const s = document.querySelector('#review-root .sheet'); return !!s && !s.querySelector('[aria-busy=\"true\"]') && s.getAttribute('aria-busy') !== 'true'; }")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
    def finish_undo(self):
        self.pg.clock.run_for(5100); self.pg.wait_for_selector("#review-toast", state="hidden")
    def shot(self, name):
        self.pg.evaluate("document.fonts.ready"); self.pg.wait_for_timeout(200)
        self.pg.screenshot(path=str(OUT / (name + ".png")))
        try:
            m = self.pg.evaluate(open("/workspace/design-review-61/metrics.js").read())
            if m: METRICS[name] = m
        except Exception as e: METRICS[name] = {"error": str(e)}
    def stop(self):
        try: self.ctx.close()
        except Exception: pass
        self.srv.shutdown(); self.srv.server_close(); self._p.stop(); shutil.rmtree(self.tmp, ignore_errors=True)

METRICS = {}
JS_AUDIT = r"""() => {
  const lum = c => { const a=[c[0],c[1],c[2]].map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*a[0]+.7152*a[1]+.0722*a[2]};
  const parse = s => { const m=s.match(/rgba?\(([^)]+)\)/); if(!m) return null; const p=m[1].split(',').map(x=>parseFloat(x)); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1}; };
  const blend=(f,b)=>({r:f.r*f.a+b.r*(1-f.a),g:f.g*f.a+b.g*(1-f.a),b:f.b*f.a+b.b*(1-f.a),a:1});
  const bgOf = el => { let stack=[]; for(let e=el;e;e=e.parentElement){const c=parse(getComputedStyle(e).backgroundColor); if(c&&c.a>0){stack.push(c); if(c.a>=1)break;}} let base={r:255,g:255,b:255,a:1}; for(let i=stack.length-1;i>=0;i--) base=blend(stack[i],base); return base; };
  const out=[]; const roots=[...document.querySelectorAll('#review-root, #review-toast, .today .sync-note')];
  const seen=new Set();
  roots.forEach(root=>{ const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT); let n; while(n=w.nextNode()){ const t=n.textContent.trim(); if(!t) continue; const el=n.parentElement; if(seen.has(el)) continue; seen.add(el);
    const cs=getComputedStyle(el); let fg=parse(cs.color); if(!fg) continue; const bg=bgOf(el); fg=blend(fg,bg);
    const L1=lum([fg.r,fg.g,fg.b]),L2=lum([bg.r,bg.g,bg.b]); const ratio=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05);
    const fs=parseFloat(cs.fontSize), fw=parseInt(cs.fontWeight); const large = fs>=24 || (fs>=18.66 && fw>=700);
    out.push({text:t.slice(0,48), sel:(el.className&&el.className.baseVal===undefined?'.'+String(el.className).split(' ').join('.'):el.tagName), ratio:Math.round(ratio*100)/100, need:large?3:4.5, fs, fw, color:cs.color}); } });
  return out; }"""
def audit(pg, label, store):
    rows = pg.evaluate(JS_AUDIT)
    store[label] = rows
    return [r for r in rows if r["ratio"] < r["need"]]

if __name__ == "__main__":
    res = {"audit": {}, "texts": {}, "errors": {}, "metrics": {}}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        h = H(p, b)
        import functools
        def sheet_text(): return " ".join(h.pg.inner_text("#review-root .sheet").split())
        def note_text(): return " ".join(h.pg.inner_text(".today .sync-note").split()) if h.pg.query_selector(".today .sync-note") else None
        def run(name, scn, fn, when=at(2026, 11, 27, 14, 0)):
            pg = h.start(scn, when)
            try:
                fn(pg)
                res["texts"][name] = {"sheet": sheet_text() if pg.query_selector("#review-root .sheet") else None, "note": note_text(),
                                      "toast": " ".join(pg.inner_text("#review-toast").split()) if pg.query_selector("#review-toast:not([hidden])") else None}
                res["errors"][name] = list(h.errors)
                low = audit(pg, name, res["audit"])
                if low: print("LOW CONTRAST", name, low)
            finally:
                h.stop()
            print("ok", name)
        # 01
        run("01-today-note-review", three(), lambda pg: h.shot("01-today-note-review"))
        # 02
        def f02(pg): h.open_sheet(); h.shot("02-sheet-one-entry")
        run("02-sheet-one-entry", one(), f02)
        # 03
        def f03(pg):
            h.open_sheet(); pg.evaluate("document.querySelector('#review-root .list').scrollTop=0"); h.shot("03-sheet-many-scrolling")
            pg.evaluate("(()=>{const l=document.querySelector('#review-root .list');l.scrollTop=l.scrollHeight})()"); pg.wait_for_timeout(150); h.shot("03b-sheet-many-scrolled-end")
            pg.evaluate("document.querySelector('#review-root .list').scrollTop=0")
        run("03-sheet-many-scrolling", many(), f03)
        # 04
        def f04(pg):
            h.open_sheet(); pg.click('#review-root .grp[data-g="g1"] [data-act="keep"]'); pg.wait_for_selector("#review-toast:not([hidden])"); h.shot("04-undo-keep-mac")
        run("04-undo-keep-mac", three(), f04)
        # 05
        def f05(pg):
            h.open_sheet(); pg.click('#review-root .ln[data-id="phone-r3:1"] [data-act="add"]'); pg.wait_for_selector("#review-toast:not([hidden])"); h.shot("05-undo-use-phone")
        run("05-undo-use-phone", three(), f05)
        # 06
        def f06(pg):
            h.open_sheet(); pg.click('#review-root [data-act="use"]'); pg.wait_for_selector("#review-root .sheet", state="detached"); pg.wait_for_selector("#review-toast:not([hidden])"); h.shot("06-last-resolved-note-gone")
        run("06-last-resolved-note-gone", one(), f06)
        # 07 loading
        def f07(pg):
            held = []; pg.route("**/api/held?*", lambda route: held.append(route))
            pg.click('.today .sync-note [data-act="review"]'); pg.wait_for_selector("#review-root .sheet"); pg.wait_for_timeout(300); h.shot("07-loading")
            for _ in range(100):
                if held: break
                pg.wait_for_timeout(20)
            res["metrics"]["loading_text"] = " ".join(pg.inner_text("#review-root .sheet").split())
            res["metrics"]["loading_aria_busy"] = pg.get_attribute("#review-root .list", "aria-busy")
            held[0].continue_(); pg.wait_for_timeout(500)
        run("07-loading", three(), f07)
        # 07b load-error (departure 2): fail GET /api/held
        def f07b(pg):
            pg.route("**/api/held?*", lambda route: route.fulfill(status=500, content_type="application/json", body='{"error":"read_failed"}'))
            pg.click('.today .sync-note [data-act="review"]'); pg.wait_for_selector("#review-root .sheet"); pg.wait_for_timeout(600)
            pg.evaluate("document.fonts.ready"); h.shot("07b-load-error-try-again")
            res["metrics"]["load_error_html"] = pg.inner_html("#review-root .sheet")
            res["metrics"]["load_error_has_retry"] = bool(pg.query_selector('#review-root [data-act="retry"], #review-root [data-act="reload"], #review-root button:has-text("Try again")'))
        run("07b-load-error-try-again", three(), f07b)
        # 08 error
        def f08(pg):
            h.open_sheet(); pg.route("**/api/held/resolve*", lambda route: route.fulfill(status=500, content_type="application/json", body='{"error":"save_failed"}'))
            pg.click('#review-root .grp[data-g="g1"] [data-act="use"]'); h.finish_undo(); pg.wait_for_selector('#review-root .grp[data-g="g1"] [role="alert"]'); h.shot("08-error-still-held")
        run("08-error-still-held", three(), f08)
        # 09 midnight
        def f09(pg):
            h.open_sheet(); before = sheet_text(); pg.clock.run_for(5 * 60 * 1000); h.srv_clock(at(2026, 11, 28, 0, 3))
            pg.wait_for_function("() => document.getElementById('header-date').innerText.indexOf('28') >= 0"); pg.wait_for_timeout(300)
            res["metrics"]["midnight_sheet_unchanged"] = sheet_text() == before; h.shot("09-day-boundary-midnight-ist")
        run("09-day-boundary-midnight-ist", three(), f09, when=at(2026, 11, 27, 23, 58))
        # 10 closed
        def f10(pg):
            h.open_sheet(); pg.keyboard.press("Escape"); pg.wait_for_selector("#review-root .sheet", state="detached"); h.shot("10-closed-without-action")
            res["metrics"]["focus_returns_to_review"] = pg.evaluate("document.activeElement && document.activeElement.getAttribute('data-act')")
        run("10-closed-without-action", three(), f10)
        # 11
        run("11-today-applied-note-once", upgrade(), lambda pg: h.shot("11-today-applied-note-once"))
        # 12 empty
        def f12(pg):
            raw = json.loads((h.folder / cs.DATA_FILENAME).read_text("utf-8")); raw["syncState"]["devices"][fx.DEV]["held"] = []
            (h.folder / cs.DATA_FILENAME).write_text(json.dumps(raw)); h.open_sheet(); h.shot("12-sheet-empty")
        run("12-sheet-empty", one(), f12)
        # 13
        def f13(pg):
            h.open_sheet(); pg.click('#review-root [data-act="keepall"]'); pg.wait_for_selector("#review-toast:not([hidden])"); pg.evaluate("document.querySelector('#review-root .list').scrollTop=0"); h.shot("13-undo-keep-for-all")
        run("13-undo-keep-for-all", many(), f13)
        # 14
        def f14(pg): h.open_sheet(); h.shot("14-sheet-mixed-session-and-edit")
        run("14-sheet-mixed-session-and-edit", mixed(), f14)
        # 15
        def f15(pg): h.open_sheet(); h.shot("15-sheet-remove-restore")
        run("15-sheet-remove-restore", remove_restore(), f15)
        # 15b: use restore -> parked toast
        def f15b(pg):
            h.open_sheet(); pg.click('#review-root .grp[data-g^="restore"] [data-act="use"], #review-root [data-act="use"]:below(:text("Restored on phone"))')
            pg.wait_for_selector("#review-toast:not([hidden])"); h.shot("15b-restore-parked-toast")
        try: run("15b-restore-parked-toast", remove_restore(), f15b)
        except Exception as ex: print("15b skipped", repr(ex)[:200])
        # 16
        run("16-today-applied-only", applied_only(), lambda pg: h.shot("16-today-applied-only"))
        b.close()
    json.dump(METRICS, open("/workspace/design-review-61/build-metrics.json","w"), indent=1)
    json.dump(res, open(OUT.parent / "capture61-results.json", "w"), indent=1, ensure_ascii=False)
    print("DONE")
