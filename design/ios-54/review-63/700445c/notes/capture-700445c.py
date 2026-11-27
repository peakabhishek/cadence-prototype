"""Design recheck of cadence PR #63 at 700445c vs a698fc7 / 0013b16. Synthetic data only."""
import os, sys, json
from pathlib import Path

os.environ.setdefault("TREE", "/workspace/cadence-r63-700445c")
os.environ.setdefault("LABEL", "700445c")
os.environ.setdefault("OUT", "/workspace/design-review-63/build-700445c")

sys.path.insert(0, "/workspace/design-review-63")
import capture63 as C
import capture8efafcb as prev
from capture8efafcb import kb_undo, run_case, RESULTS

from playwright.sync_api import sync_playwright
import review_fixtures as fx

at = C.at
OUT = Path(os.environ["OUT"]); OUT.mkdir(parents=True, exist_ok=True)
LABEL = os.environ["LABEL"]

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
  const hs = header ? getComputedStyle(header) : null;
  const vh = window.innerHeight, vw = window.innerWidth;
  const RING = 4;
  let stickyBottom = 0;
  document.querySelectorAll('header, .lbar, body *').forEach(el => {
    const s = getComputedStyle(el);
    if ((s.position !== 'sticky' && s.position !== 'fixed') || s.display === 'none' ||
        s.visibility === 'hidden' || s.pointerEvents === 'none') return;
    const br = el.getBoundingClientRect();
    if (br.height <= 0 || br.bottom <= 0 || br.top > 120) return;
    if (br.top <= (parseFloat(s.top) || 0) + 1) stickyBottom = Math.max(stickyBottom, br.bottom);
  });
  const cover = stickyBottom + RING;
  const fully = !!(r && r.top >= 0 && r.bottom <= vh && r.left >= 0 && r.right <= vw);
  const clearOfHeaderAndRing = !!(r && r.top >= cover && r.bottom <= vh - RING && r.left >= RING && r.right <= vw - RING);
  const cx = r ? r.left + r.width / 2 : null;
  const cy = r ? r.top + r.height / 2 : null;
  const hit = (cx != null) ? document.elementFromPoint(cx, cy) : null;
  const hitOk = !!(hit && b && (hit === b || b.contains(hit)));
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
    header: h && {top: h.top, bottom: h.bottom, height: h.height, position: hs && hs.position, zIndex: hs && hs.zIndex},
    stickyBottom: stickyBottom,
    cover: cover,
    btnFullyInView: fully,
    clearOfHeaderAndRing: clearOfHeaderAndRing,
    underHeader: !!(r && h && r.top < h.bottom && r.bottom > h.top && h.bottom > 0 && h.top < vh),
    elementFromPoint: {cx, cy, hitOk,
      hit: hit && {tag: hit.tagName, act: hit.getAttribute('data-act'), id: hit.id || null,
                   className: String(hit.className||'').slice(0,80)}},
    outline: cs && {outline: cs.outline, color: cs.outlineColor, width: cs.outlineWidth,
                    style: cs.outlineStyle, offset: cs.outlineOffset},
    viewOutline: vcs && {outline: vcs.outline, style: vcs.outlineStyle, width: vcs.outlineWidth,
                         outlineNone: vcs.outlineStyle === 'none' || vcs.outlineWidth === '0px'},
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

INSTALL_SCROLL_HOOKS = r"""() => {
  window.__irisScroll = { intoView: [], events: [], start: performance.now() };
  if (!Element.prototype.__irisOrigSIV) {
    Element.prototype.__irisOrigSIV = Element.prototype.scrollIntoView;
  }
  Element.prototype.scrollIntoView = function(opts) {
    window.__irisScroll.intoView.push({
      t: performance.now(),
      opts: opts && {block: opts.block, behavior: String(opts.behavior), inline: opts.inline},
      act: this.getAttribute && this.getAttribute('data-act'),
      tag: this.tagName,
      yBefore: window.scrollY
    });
    return Element.prototype.__irisOrigSIV.apply(this, arguments);
  };
  window.addEventListener('scroll', () => {
    window.__irisScroll.events.push({t: performance.now(), y: window.scrollY});
  }, true);
}"""

READ_SCROLL_HOOKS = r"""() => {
  const s = window.__irisScroll || {intoView: [], events: [], start: performance.now()};
  const ev = s.events || [];
  const span = ev.length ? (ev[ev.length-1].t - ev[0].t) : 0;
  return {
    intoView: s.intoView,
    eventCount: ev.length,
    firstY: ev.length ? ev[0].y : window.scrollY,
    lastY: ev.length ? ev[ev.length-1].y : window.scrollY,
    spanMs: span,
    now: performance.now(),
    scrollY: window.scrollY
  };
}"""

SETUP_PROBE_G = r"""() => {
  const today = document.querySelector('.today');
  if (today) today.style.minHeight = '4000px';
  const lbar = document.querySelector('.lbar');
  if (lbar) {
    lbar.style.position = 'sticky';
    lbar.style.top = '0';
    lbar.style.zIndex = '50';
    lbar.style.background = 'rgb(255, 251, 246)';
  }
  const se = document.scrollingElement || document.documentElement;
  window.scrollTo(0, se.scrollHeight);
  return { y: se.scrollTop, h: se.scrollHeight, lbarPosition: lbar ? getComputedStyle(lbar).position : null };
}"""


def main():
    prev.main()

    existing = json.loads(Path(f"/workspace/design-review-63/results-{LABEL}.json").read_text())
    RESULTS["audit"] = existing.get("audit", {})
    RESULTS["texts"] = existing.get("texts", {})
    RESULTS["errors"] = existing.get("errors", {})
    RESULTS["metrics"] = existing.get("metrics", {})
    RESULTS["tree"] = existing.get("tree", os.environ["TREE"])
    RESULTS["label"] = LABEL
    if Path(f"/workspace/design-review-63/metrics-{LABEL}.json").exists():
        C.METRICS.update(json.loads(Path(f"/workspace/design-review-63/metrics-{LABEL}.json").read_text()))

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
            setup = pg.evaluate(SETUP_PROBE_G)
            RESULTS["metrics"]["frame06_scroll_setup"] = setup
            pg.wait_for_timeout(100)
            RESULTS["metrics"]["frame06_scroll_before_undo"] = pg.evaluate(SCROLL_GEOM_JS)
            h.shot("frame06-scrolled-before-undo")
            pg.evaluate(INSTALL_SCROLL_HOOKS)
            # Keyboard Undo; do not wait so long that a smooth scroll could finish unnoticed.
            pg.wait_for_selector('#review-toast [data-act="undo"]')
            pg.focus('#review-toast [data-act="undo"]')
            pg.keyboard.press("Enter")
            pg.wait_for_selector("#review-toast", state="hidden")
            pg.wait_for_selector('.today .sync-note [data-act="review"]')
            # Immediate geom + hooks, then a viewport shot (not a full-page crop).
            RESULTS["metrics"]["frame06_scroll_hooks"] = pg.evaluate(READ_SCROLL_HOOKS)
            RESULTS["metrics"]["frame06_scroll_after_undo_geom"] = pg.evaluate(SCROLL_GEOM_JS)
            C.snapshot(pg, "frame06_scroll_after_undo", RESULTS["metrics"])
            h.shot("frame06-scrolled-after-undo")
        run_case(h, "frame06-scrolled-out-review-undo", fx.one_entry(), fscroll, when=at(2026, 11, 26, 14, 0))

        b.close()

    json.dump(C.METRICS, open(f"/workspace/design-review-63/metrics-{LABEL}.json", "w"), indent=1)
    json.dump(RESULTS, open(f"/workspace/design-review-63/results-{LABEL}.json", "w"), indent=1, ensure_ascii=False)
    print("DONE", LABEL, "shots", len(list(OUT.glob('*.png'))))


if __name__ == "__main__":
    main()
