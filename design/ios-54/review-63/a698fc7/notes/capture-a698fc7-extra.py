"""Extra a698fc7 cases: hidden Review fallback, IST midnight, scrolled-out Review."""
import os, sys, json
from pathlib import Path

os.environ.setdefault("TREE", "/workspace/cadence-r63-a698fc7")
os.environ.setdefault("LABEL", "a698fc7")
os.environ.setdefault("OUT", "/workspace/design-review-63/build-a698fc7")

sys.path.insert(0, "/workspace/design-review-63")
import capture63 as C
import capture8efafcb as prev
from capture8efafcb import kb_undo, run_case, RESULTS

from playwright.sync_api import sync_playwright
import review_fixtures as fx

at = C.at
OUT = Path(os.environ["OUT"]); OUT.mkdir(parents=True, exist_ok=True)
LABEL = os.environ["LABEL"]

# Seed RESULTS from the already-finished prev.main() run
existing = json.loads(Path(f"/workspace/design-review-63/results-{LABEL}.json").read_text())
RESULTS["audit"] = existing.get("audit", {})
RESULTS["texts"] = existing.get("texts", {})
RESULTS["errors"] = existing.get("errors", {})
RESULTS["metrics"] = existing.get("metrics", {})
RESULTS["tree"] = existing.get("tree", os.environ["TREE"])
RESULTS["label"] = LABEL
if Path(f"/workspace/design-review-63/metrics-{LABEL}.json").exists():
    C.METRICS.update(json.loads(Path(f"/workspace/design-review-63/metrics-{LABEL}.json").read_text()))

SCROLL_GEOM_JS = r"""() => {
  const b = document.querySelector('.today .sync-note [data-act="review"]');
  const note = document.querySelector('.today .sync-note');
  const header = document.querySelector('header.lbar, .lbar');
  const view = document.getElementById('view');
  const ae = document.activeElement;
  const r = b ? b.getBoundingClientRect() : null;
  const nr = note ? note.getBoundingClientRect() : null;
  const h = header ? header.getBoundingClientRect() : null;
  const cs = b ? getComputedStyle(b) : null;
  const vcs = view ? getComputedStyle(view) : null;
  const vh = window.innerHeight, vw = window.innerWidth;
  const fully = !!(r && r.top >= 0 && r.bottom <= vh && r.left >= 0 && r.right <= vw);
  return {
    scrollY: window.scrollY,
    scrollHeight: document.documentElement.scrollHeight,
    viewport: {w: vw, h: vh},
    focus: ae && {tag: ae.tagName, id: ae.id || null, act: ae.getAttribute('data-act'),
                  className: String(ae.className||'').slice(0,80)},
    isBody: ae === document.body,
    isView: ae === view,
    isReview: !!(ae && ae.getAttribute && ae.getAttribute('data-act') === 'review'),
    btn: r && {top: r.top, bottom: r.bottom, left: r.left, right: r.right, width: r.width, height: r.height},
    note: nr && {top: nr.top, bottom: nr.bottom, left: nr.left, right: nr.right},
    header: h && {top: h.top, bottom: h.bottom, height: h.height,
                  position: header ? getComputedStyle(header).position : null},
    btnFullyInView: fully,
    btnOffscreen: !!(r && (r.bottom <= 0 || r.top >= vh || r.right <= 0 || r.left >= vw)),
    underHeader: !!(r && h && r.top < h.bottom && r.bottom > h.top && h.bottom > 0 && h.top < vh),
    outline: cs && {outline: cs.outline, color: cs.outlineColor, width: cs.outlineWidth,
                    style: cs.outlineStyle, offset: cs.outlineOffset},
    viewOutline: vcs && {outline: vcs.outline, color: vcs.outlineColor, width: vcs.outlineWidth,
                         style: vcs.outlineStyle, outlineNone: vcs.outlineStyle === 'none' || vcs.outlineWidth === '0px'},
    headerDate: (document.getElementById('header-date')||{}).textContent || null,
    noteText: note ? note.innerText.replace(/\s+/g,' ').trim() : null,
    sheetCount: document.querySelectorAll('#review-root .sheet').length
  };
}"""

VIEW_FOCUS_JS = r"""() => {
  const a = document.activeElement;
  const view = document.getElementById('view');
  const cs = a ? getComputedStyle(a) : null;
  return {
    tag: a && a.tagName, id: a && a.id,
    isView: a === view, isBody: a === document.body,
    outline: cs && cs.outline, outlineStyle: cs && cs.outlineStyle,
    outlineWidth: cs && cs.outlineWidth, outlineColor: cs && cs.outlineColor,
    boxShadow: cs && cs.boxShadow,
    viewCssOutline: view ? getComputedStyle(view).outline : null
  };
}"""


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        h = C.H(p, b)

        def fhidden(pg):
            h.open_sheet()
            C.snapshot(pg, "frame06_hidden_before", RESULTS["metrics"])
            use = pg.query_selector('#review-root [data-act="use"]')
            use.focus(); pg.keyboard.press("Enter")
            pg.wait_for_selector("#review-root .sheet", state="detached")
            pg.wait_for_timeout(200)
            pg.evaluate("""() => {
              const s = document.createElement('style');
              s.id = 'iris-hide-review';
              s.textContent = '.today .sync-note [data-act="review"] { display: none !important; }';
              document.head.appendChild(s);
            }""")
            kb_undo(pg)
            pg.wait_for_selector(".today .sync-note")
            C.snapshot(pg, "frame06_hidden_after_undo", RESULTS["metrics"])
            RESULTS["metrics"]["frame06_hidden_geom"] = pg.evaluate(SCROLL_GEOM_JS)
            RESULTS["metrics"]["frame06_hidden_view_focus"] = pg.evaluate(VIEW_FOCUS_JS)
            RESULTS["metrics"]["frame06_hidden_after_undo"]["reviewDisplay"] = pg.evaluate("""() => {
              const b = document.querySelector('.today .sync-note [data-act="review"]');
              return b ? getComputedStyle(b).display : null;
            }""")
            h.shot("frame06-hidden-review-after-undo")
        run_case(h, "frame06-hidden-review-fallback", fx.one_entry(), fhidden, when=at(2026, 11, 26, 14, 0))

        def fmid(pg):
            h.open_sheet()
            C.snapshot(pg, "frame06_midnight_before", RESULTS["metrics"])
            RESULTS["metrics"]["frame06_midnight_before"]["headerDate"] = pg.inner_text("#header-date")
            h.shot("frame06-midnight-before")
            pg.clock.run_for(6 * 60 * 1000)
            h.srv_clock(at(2026, 11, 27, 0, 4))
            pg.wait_for_function("() => document.getElementById('header-date').innerText.indexOf('27') >= 0")
            pg.wait_for_timeout(200)
            RESULTS["metrics"]["frame06_midnight_after_tick"] = {
                "headerDate": pg.inner_text("#header-date"),
                "sheetPresent": bool(pg.query_selector("#review-root .sheet")),
            }
            h.shot("frame06-midnight-after-tick")
            use = pg.query_selector('#review-root [data-act="use"]')
            use.focus(); pg.keyboard.press("Enter")
            pg.wait_for_selector("#review-root .sheet", state="detached")
            pg.wait_for_timeout(200)
            C.snapshot(pg, "frame06_midnight_after_use", RESULTS["metrics"])
            kb_undo(pg)
            pg.wait_for_selector('.today .sync-note [data-act="review"]')
            C.snapshot(pg, "frame06_midnight_after_undo", RESULTS["metrics"])
            RESULTS["metrics"]["frame06_midnight_geom"] = pg.evaluate(SCROLL_GEOM_JS)
            RESULTS["metrics"]["frame06_midnight_after_undo"]["headerDate"] = pg.inner_text("#header-date")
            h.shot("frame06-midnight-after-undo")
        run_case(h, "frame06-ist-midnight-undo", fx.one_entry(), fmid, when=at(2026, 11, 26, 23, 58))

        def fscroll(pg):
            h.open_sheet()
            C.snapshot(pg, "frame06_scroll_before", RESULTS["metrics"])
            RESULTS["metrics"]["frame06_scroll_note_before"] = pg.evaluate(SCROLL_GEOM_JS)
            use = pg.query_selector('#review-root [data-act="use"]')
            use.focus(); pg.keyboard.press("Enter")
            pg.wait_for_selector("#review-root .sheet", state="detached")
            pg.wait_for_timeout(200)
            pg.evaluate("""() => {
              const d = document.createElement('div');
              d.id = 'iris-scroll-spacer';
              d.style.height = '2400px';
              d.setAttribute('aria-hidden', 'true');
              document.body.appendChild(d);
            }""")
            pg.evaluate("window.scrollTo(0, 1600)")
            pg.wait_for_timeout(150)
            RESULTS["metrics"]["frame06_scroll_before_undo"] = pg.evaluate(SCROLL_GEOM_JS)
            h.shot("frame06-scrolled-before-undo")
            kb_undo(pg)
            pg.wait_for_selector('.today .sync-note [data-act="review"]')
            pg.wait_for_timeout(200)
            RESULTS["metrics"]["frame06_scroll_after_undo"] = pg.evaluate(SCROLL_GEOM_JS)
            C.snapshot(pg, "frame06_scroll_after_undo", RESULTS["metrics"])
            h.shot("frame06-scrolled-after-undo")
            pg.screenshot(path=str(OUT / "frame06-scrolled-after-undo-full.png"), full_page=True)
        run_case(h, "frame06-scrolled-out-review-undo", fx.one_entry(), fscroll, when=at(2026, 11, 26, 14, 0))

        b.close()

    json.dump(C.METRICS, open(f"/workspace/design-review-63/metrics-{LABEL}.json", "w"), indent=1)
    json.dump(RESULTS, open(f"/workspace/design-review-63/results-{LABEL}.json", "w"), indent=1, ensure_ascii=False)
    print("DONE extra", LABEL, "shots", len(list(OUT.glob('*.png'))))


if __name__ == "__main__":
    main()
