"""Design review captures for cadence PR #63 at 154a9f7 vs ac4e8d6.
Synthetic data only. 1440x900 at 2x, IST. Real server in-process.
TREE=/workspace/cadence-r63-154a9f7 python3 capture63.py
"""
import json, os, sys, tempfile, threading, shutil, time, unicodedata
from pathlib import Path
from datetime import datetime, timedelta, timezone
from unittest import mock
from playwright.sync_api import sync_playwright

TREE = Path(os.environ.get("TREE", "/workspace/cadence-r63-154a9f7")).resolve()
LABEL = os.environ.get("LABEL") or TREE.name.split("-")[-1]  # 154a9f7 or ac4e8d6
OUT = Path(os.environ.get("OUT", f"/workspace/design-review-63/build-{LABEL}"))
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(TREE / "server"))
sys.path.insert(0, str(TREE / "tests"))
import cadence_server as cs
import review_fixtures as fx

IST = timezone(timedelta(hours=5, minutes=30))
D = "2026-11-27"
FOCUS, DEEP = "Focus", "Deep work"
GYM, GYM_PHONE = "Gym", "Gym, legs day"
BANK = "Call the bank"
at = lambda *a: datetime(*a, tzinfo=IST)
METRICS = {}
RESULTS = {"audit": {}, "texts": {}, "errors": {}, "metrics": {}, "tree": str(TREE), "label": LABEL}

def goals_today():
    return [fx.goal("g1", FOCUS, 30, day=D), fx.goal("g2", "Write the weekly review", 45, day=D),
            fx.goal("g3", GYM, None, day=D), fx.goal("g4", "Read one paper", 25, day=D),
            fx.goal("g5", "Plan Friday’s demo", 25, day=D)]

def mix():
    """Frame 13b fixture used in the #61 review (same names as capture-ac4e8d6)."""
    old = "2026-11-17"
    return fx.build({old: [fx.goal("x1", FOCUS, 30, day=old), fx.goal("x2", GYM, None, day=old)], D: goals_today()},
        held=[{"seq": q, "reason": "too_old"} for q in (1, 2, 3, 4)],
        changes=[fx.change(1, "edit_goal", old + "T10:00:00+05:30", goal_id="x1", set={"title": DEEP}),
                 fx.change(2, "edit_goal", old + "T10:01:00+05:30", goal_id="x2", set={"title": GYM_PHONE}),
                 fx.change(3, "add_goal", old + "T10:02:00+05:30", goal={"id": "n1", "title": BANK, "box_minutes": 30, "box_period": "day"}),
                 fx.change(4, "add_session", old + "T11:00:00+05:30", session=fx.session("p1", "x1", 25, old))],
        sessions=[fx.session("m1", "g1", 25, D, hour=8)])

FOCUS_JS = r"""() => {
  const a = document.activeElement;
  if (!a) return {none:true};
  const cs = getComputedStyle(a);
  const leaf = getComputedStyle(document.documentElement).getPropertyValue('--leaf').trim();
  return {
    tag: a.tagName, id: a.id || null,
    act: a.getAttribute('data-act'),
    key: a.getAttribute('data-key') || a.getAttribute('data-id'),
    text: (a.textContent||'').trim().slice(0,80),
    className: String(a.className||'').slice(0,80),
    isBody: a === document.body,
    isHtml: a === document.documentElement,
    isView: a.id === 'view',
    inSheet: !!(a.closest && a.closest('#review-root .sheet')),
    inToast: !!(a.closest && a.closest('#review-toast')),
    outline: cs.outline, outlineColor: cs.outlineColor, outlineWidth: cs.outlineWidth,
    outlineOffset: cs.outlineOffset, outlineStyle: cs.outlineStyle,
    boxShadow: cs.boxShadow, leafToken: leaf,
    tabindex: a.getAttribute('tabindex')
  };
}"""

GROUPS_JS = r"""() => [...document.querySelectorAll('#review-root .grp')].map(g => ({
  key: g.getAttribute('data-g'),
  title: ((g.querySelector('.gn')||{}).textContent||'').trim(),
  acts: [...g.querySelectorAll('[data-act]')].map(b => ({
    act: b.getAttribute('data-act'),
    key: b.getAttribute('data-key') || b.getAttribute('data-id'),
    text: (b.textContent||'').trim().slice(0,40)
  }))
}))"""

HELPER_JS = r"""() => {
  const el = document.querySelector('#review-root .foot-help');
  if (!el) return null;
  const r = el.getBoundingClientRect(), cs = getComputedStyle(el), lh = parseFloat(cs.lineHeight);
  const t = el.textContent;
  const cps = [...t].filter(c => c.charCodeAt(0) > 127).map(c => 'U+'+c.charCodeAt(0).toString(16).toUpperCase().padStart(4,'0'));
  return {text:t, width:+r.width.toFixed(1), height:+r.height.toFixed(1),
          lines: Math.round(r.height/lh), font:cs.font, color:cs.color, maxWidth:cs.maxWidth,
          nonAscii: cps};
}"""

TOKENS_JS = r"""() => {
  const cs = getComputedStyle(document.documentElement);
  const out = {};
  for (const k of cs) { if (k.startsWith('--')) out[k] = cs.getPropertyValue(k).trim(); }
  return out;
}"""

class H:
    def __init__(self, pw, browser):
        self.pw, self.browser = pw, browser
    def start(self, scn, when):
        self.tmp = Path(tempfile.mkdtemp())
        self.folder = self.tmp / "OneDrive - Peak Routine" / "Cadence"
        self.folder.mkdir(parents=True)
        (self.tmp / "cfg").mkdir()
        (self.tmp / "cfg" / "config.json").write_text(json.dumps({"data_dir": str(self.folder)}))
        os.environ["CADENCE_CONFIG_DIR"] = str(self.tmp / "cfg")
        os.environ["CADENCE_SUGGESTED_DIR"] = str(self.folder)
        os.environ["CADENCE_QUIET"] = "1"
        data, doc = scn
        fx.write(self.folder, data, doc, state_dir=self.tmp / "cfg")
        self.srv = cs.make_server(0)
        self.base = "http://127.0.0.1:%d" % self.srv.server_address[1]
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.srv_clock(when)
        self.errors, self.posts, self.held_posts = [], [], []
        self.ctx = self.browser.new_context(viewport={"width": 1440, "height": 900},
                                            device_scale_factor=2, timezone_id="Asia/Kolkata")
        self.pg = self.ctx.new_page(); self.pg.set_default_timeout(15000)
        self.pg.on("pageerror", lambda e: self.errors.append(str(e)))
        self.pg.on("console", lambda m: self.errors.append("console:" + m.text) if m.type == "error" else None)
        def on_req(r):
            if r.method == "POST" and "/api/held" in r.url:
                self.posts.append((r.method, r.url, r.post_data))
                if "/resolve" in r.url:
                    self.held_posts.append({"url": r.url, "body": r.post_data})
        self.pg.on("request", on_req)
        self.pg.clock.install(time=when)
        self.pg.goto(self.base + "/#today")
        self.pg.wait_for_selector("body[data-loaded='true']")
        self.pg.evaluate("document.fonts.ready"); self.pg.wait_for_timeout(300)
        return self.pg
    def srv_clock(self, instant):
        if getattr(self, "_p", None): self._p.stop()
        base_real = time.time()
        self._p = mock.patch.object(cs, "_utc_now",
            lambda: instant.astimezone(timezone.utc) + timedelta(seconds=time.time() - base_real))
        self._p.start()
    def open_sheet(self):
        pg = self.pg
        pg.click('.today .sync-note [data-act="review"]')
        pg.wait_for_selector("#review-root .sheet")
        pg.wait_for_function("""() => { const s = document.querySelector('#review-root .sheet');
          return !!s && !s.querySelector('[aria-busy=\"true\"]') && s.getAttribute('aria-busy') !== 'true'; }""")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
    def finish_undo(self):
        self.pg.clock.run_for(5100)
        self.pg.wait_for_selector("#review-toast", state="hidden")
    def shot(self, name):
        self.pg.evaluate("document.fonts.ready"); self.pg.wait_for_timeout(200)
        self.pg.screenshot(path=str(OUT / (name + ".png")))
        try:
            m = self.pg.evaluate(open("/workspace/design-review-63/metrics.js").read())
            if m: METRICS[name] = m
        except Exception as e:
            METRICS[name] = {"error": str(e)}
    def stop(self):
        try: self.ctx.close()
        except Exception: pass
        try: self.srv.shutdown(); self.srv.server_close()
        except Exception: pass
        if getattr(self, "_p", None):
            try: self._p.stop()
            except Exception: pass
        shutil.rmtree(self.tmp, ignore_errors=True)

def sheet_text(pg):
    if not pg.query_selector("#review-root .sheet"): return None
    return " ".join(pg.inner_text("#review-root .sheet").split())
def note_text(pg):
    if not pg.query_selector(".today .sync-note"): return None
    return " ".join(pg.inner_text(".today .sync-note").split())
def toast_text(pg):
    if not pg.query_selector("#review-toast:not([hidden])"): return None
    return " ".join(pg.inner_text("#review-toast").split())

def snapshot(pg, key, store):
    store[key] = {
        "focus": pg.evaluate(FOCUS_JS),
        "groups": pg.evaluate(GROUPS_JS) if pg.query_selector("#review-root .sheet") else None,
        "helper": pg.evaluate(HELPER_JS) if pg.query_selector("#review-root .sheet") else None,
        "sheet": sheet_text(pg),
        "note": note_text(pg),
        "toast": toast_text(pg),
        "sheetPresent": bool(pg.query_selector("#review-root .sheet")),
        "keepAll": bool(pg.query_selector('#review-root [data-act="keepall"]')),
        "heading": pg.inner_text("#sh-sub") if pg.query_selector("#sh-sub") else None,
    }

def run_case(h, name, scn, fn, when=at(2026, 11, 27, 14, 0)):
    pg = h.start(scn, when)
    try:
        fn(pg)
        RESULTS["texts"][name] = {"sheet": sheet_text(pg), "note": note_text(pg), "toast": toast_text(pg)}
        RESULTS["errors"][name] = list(h.errors)
        RESULTS["metrics"].setdefault(name, {})["held_resolve_posts"] = list(h.held_posts)
    finally:
        h.stop()
    print("ok", name)

def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        h = H(p, b)

        # --- 13b: before, after Keep all (keyboard, visible focus), after toast ends ---
        def f13b(pg):
            h.open_sheet()
            snapshot(pg, "13b_before", RESULTS["metrics"])
            RESULTS["metrics"]["13b_tokens"] = pg.evaluate(TOKENS_JS)
            h.shot("13b-before-keep-all")
            # keyboard path so :focus-visible shows
            pg.focus('#review-root [data-act="keepall"]')
            pg.keyboard.press("Enter")
            pg.wait_for_selector("#review-toast:not([hidden])")
            pg.wait_for_timeout(150)
            snapshot(pg, "13b_after_keepall", RESULTS["metrics"])
            h.shot("13b-after-keep-all-focus")
            # let toast end, then shot group order (Linus's 13b shot timing)
            h.finish_undo()
            snapshot(pg, "13b_after_toast_ends", RESULTS["metrics"])
            h.shot("13b-after-toast-ends")
        run_case(h, "13b-keep-all-focus-and-order", mix(), f13b)

        # --- 13b Undo: focus + group order after Undo within 5s ---
        def fundo(pg):
            h.open_sheet()
            snapshot(pg, "undo_before", RESULTS["metrics"])
            pg.focus('#review-root [data-act="keepall"]')
            pg.keyboard.press("Enter")
            pg.wait_for_selector("#review-toast:not([hidden])")
            snapshot(pg, "undo_after_keepall", RESULTS["metrics"])
            # Undo from keyboard if possible, else click
            if pg.query_selector('#review-toast [data-act="undo"]'):
                pg.focus('#review-toast [data-act="undo"]')
                pg.keyboard.press("Enter")
            pg.wait_for_function("() => !document.querySelector('#review-toast:not([hidden])') || document.querySelector('#review-root [data-act=keepall]')")
            pg.wait_for_timeout(200)
            snapshot(pg, "undo_after_undo", RESULTS["metrics"])
            h.shot("13b-after-undo-focus")
        run_case(h, "13b-undo-focus-and-order", mix(), fundo)

        # --- Reload while Undo is pending ---
        def freload(pg):
            h.open_sheet()
            snapshot(pg, "reload_before", RESULTS["metrics"])
            pg.focus('#review-root [data-act="keepall"]')
            pg.keyboard.press("Enter")
            pg.wait_for_selector("#review-toast:not([hidden])")
            snapshot(pg, "reload_after_keepall", RESULTS["metrics"])
            posts_before_reload = list(h.held_posts)
            # page reload while toast still showing (pending, nothing written)
            pg.reload()
            pg.wait_for_selector("body[data-loaded='true']")
            pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            snapshot(pg, "reload_after_page_reload", RESULTS["metrics"])
            RESULTS["metrics"]["reload_after_page_reload"]["held_posts_before_reload"] = posts_before_reload
            RESULTS["metrics"]["reload_after_page_reload"]["held_posts_after_reload"] = list(h.held_posts)
            h.shot("13b-after-reload-today")
            # reopen sheet: all original held rows should be back, original order
            if pg.query_selector('.today .sync-note [data-act="review"]'):
                h.open_sheet()
                snapshot(pg, "reload_sheet_reopened", RESULTS["metrics"])
                h.shot("13b-after-reload-sheet")
            else:
                RESULTS["metrics"]["reload_sheet_reopened"] = {"no_review_note": True, "note": note_text(pg)}
                h.shot("13b-after-reload-no-note")
        run_case(h, "13b-reload-while-undo-pending", mix(), freload)

        # --- Keep all leaves nothing (three goal edits) ---
        def fnoleftover(pg):
            h.open_sheet()
            snapshot(pg, "noleftover_before", RESULTS["metrics"])
            h.shot("noleftover-before")
            pg.focus('#review-root [data-act="keepall"]')
            pg.keyboard.press("Enter")
            # sheet may close
            try:
                pg.wait_for_selector("#review-root .sheet", state="detached", timeout=4000)
            except Exception:
                pass
            pg.wait_for_timeout(250)
            snapshot(pg, "noleftover_after", RESULTS["metrics"])
            # extra DOM facts for the focus target
            RESULTS["metrics"]["noleftover_after"]["viewExists"] = bool(pg.query_selector("#view"))
            RESULTS["metrics"]["noleftover_after"]["reviewBtn"] = bool(pg.query_selector('.today .sync-note [data-act="review"]'))
            RESULTS["metrics"]["noleftover_after"]["todayHeading"] = pg.evaluate("""() => {
              const h = document.querySelector('#header-date, h1, .today h2, #view h2');
              return h ? {tag:h.tagName, id:h.id, text:(h.textContent||'').trim().slice(0,80)} : null;
            }""")
            h.shot("noleftover-after-focus")
            # Undo after close
            if pg.query_selector('#review-toast [data-act="undo"]'):
                pg.focus('#review-toast [data-act="undo"]')
                pg.keyboard.press("Enter")
                pg.wait_for_timeout(300)
                snapshot(pg, "noleftover_after_undo", RESULTS["metrics"])
                h.shot("noleftover-after-undo")
        # three_edits is tied to fx.DAY = 2026-11-26
        run_case(h, "noleftover-three-edits", fx.three_edits(), fnoleftover, when=at(2026, 11, 26, 14, 0))

        # --- Linus's keep_all_mix (Synthetic names) for shot comparison ---
        def flinus(pg):
            h.open_sheet()
            snapshot(pg, "linus_before", RESULTS["metrics"])
            h.shot("linus-13b-before")
            pg.focus('#review-root [data-act="keepall"]')
            pg.keyboard.press("Enter")
            pg.wait_for_selector("#review-toast:not([hidden])")
            snapshot(pg, "linus_after_keepall", RESULTS["metrics"])
            h.shot("linus-after-keep-all-focus")
            h.finish_undo()
            snapshot(pg, "linus_after_toast_ends", RESULTS["metrics"])
            h.shot("linus-13b-after-toast-ends")
        run_case(h, "linus-keep-all-mix", fx.keep_all_mix(), flinus, when=at(2026, 11, 26, 14, 0))

        b.close()

    json.dump(METRICS, open(f"/workspace/design-review-63/metrics-{LABEL}.json", "w"), indent=1)
    json.dump(RESULTS, open(f"/workspace/design-review-63/results-{LABEL}.json", "w"), indent=1, ensure_ascii=False)
    print("DONE", LABEL, "shots", len(list(OUT.glob('*.png'))))

if __name__ == "__main__":
    main()
