"""Design recheck of cadence PR #63 at 8efafcb vs 154a9f7. Synthetic data only."""
import os, sys, json
from pathlib import Path
from datetime import datetime, timedelta, timezone

os.environ.setdefault("TREE", "/workspace/cadence-r63-8efafcb")
os.environ.setdefault("LABEL", "8efafcb")
os.environ.setdefault("OUT", "/workspace/design-review-63/build-8efafcb")

# Import harness from the previous capture (TREE already set).
sys.path.insert(0, "/workspace/design-review-63")
import capture63 as C

from playwright.sync_api import sync_playwright
import review_fixtures as fx

IST = C.IST
at = C.at
OUT = Path(os.environ["OUT"]); OUT.mkdir(parents=True, exist_ok=True)
LABEL = os.environ["LABEL"]
RESULTS = {"audit": {}, "texts": {}, "errors": {}, "metrics": {}, "tree": os.environ["TREE"], "label": LABEL}

def run_case(h, name, scn, fn, when=at(2026, 11, 27, 14, 0)):
    pg = h.start(scn, when)
    try:
        fn(pg)
        RESULTS["texts"][name] = {"sheet": C.sheet_text(pg), "note": C.note_text(pg), "toast": C.toast_text(pg)}
        RESULTS["errors"][name] = list(h.errors)
        RESULTS["metrics"].setdefault(name, {})["held_resolve_posts"] = list(h.held_posts)
    finally:
        h.stop()
    print("ok", name)

def kb_undo(pg):
    pg.wait_for_selector('#review-toast [data-act="undo"]')
    pg.focus('#review-toast [data-act="undo"]')
    pg.keyboard.press("Enter")
    pg.wait_for_selector("#review-toast", state="hidden")
    pg.wait_for_timeout(200)

def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        h = C.H(p, b)

        # (5) regression + (1) 13b Keep all then Undo
        def f13b(pg):
            h.open_sheet()
            C.snapshot(pg, "13b_before", RESULTS["metrics"])
            RESULTS["metrics"]["13b_tokens"] = pg.evaluate(C.TOKENS_JS)
            h.shot("13b-before-keep-all")
            pg.focus('#review-root [data-act="keepall"]')
            pg.keyboard.press("Enter")
            pg.wait_for_selector("#review-toast:not([hidden])")
            pg.wait_for_timeout(150)
            C.snapshot(pg, "13b_after_keepall", RESULTS["metrics"])
            h.shot("13b-after-keep-all-focus")
            kb_undo(pg)
            C.snapshot(pg, "13b_after_undo", RESULTS["metrics"])
            h.shot("13b-after-undo-focus")
        run_case(h, "13b-keep-all-and-undo", C.mix(), f13b)

        # Steve: Undo of a SINGLE row while Keep all is still on screen.
        # Design: focus should return to that row's first choice (Gym's Keep), not Keep all.
        def fsingle(pg):
            h.open_sheet()
            C.snapshot(pg, "single_before", RESULTS["metrics"])
            h.shot("single-row-before")
            btn = pg.query_selector('#review-root .grp[data-g="x2"] [data-act="keep"]')
            RESULTS["metrics"]["single_acted_row"] = pg.evaluate("""() => {
              const b = document.querySelector('#review-root .grp[data-g="x2"] [data-act="keep"]');
              const g = document.querySelector('#review-root .grp[data-g="x2"]');
              return {exists:!!b, keepAll:!!document.querySelector('#review-root [data-act="keepall"]'),
                      groupTitle: (g && g.querySelector('.gn')||{}).textContent};
            }""")
            btn.focus(); pg.keyboard.press("Enter")
            pg.wait_for_selector("#review-toast:not([hidden])")
            C.snapshot(pg, "single_after_keep", RESULTS["metrics"])
            h.shot("single-row-after-keep")
            kb_undo(pg)
            C.snapshot(pg, "single_after_undo", RESULTS["metrics"])
            h.shot("single-row-after-undo-focus")
        run_case(h, "single-row-undo-with-keepall-visible", C.mix(), fsingle)

        # (2) Keep all empties the sheet; Undo reopens it, focus Keep all
        def fnoleftover(pg):
            h.open_sheet()
            C.snapshot(pg, "noleftover_before", RESULTS["metrics"])
            RESULTS["metrics"]["noleftover_before_sheet_text"] = C.sheet_text(pg)
            h.shot("noleftover-before")
            pg.focus('#review-root [data-act="keepall"]')
            pg.keyboard.press("Enter")
            pg.wait_for_selector("#review-root .sheet", state="detached")
            pg.wait_for_timeout(200)
            C.snapshot(pg, "noleftover_after_close", RESULTS["metrics"])
            h.shot("noleftover-after-close")
            kb_undo(pg)
            C.snapshot(pg, "noleftover_after_undo", RESULTS["metrics"])
            RESULTS["metrics"]["noleftover_after_undo_sheet_text"] = C.sheet_text(pg)
            h.shot("noleftover-after-undo-focus")
        run_case(h, "noleftover-undo-reopens", fx.three_edits(), fnoleftover, when=at(2026, 11, 26, 14, 0))

        # (3) Fallback: mixed() has no Keep all; Undo of Keep focuses first choice (Add this session)
        def ffallback(pg):
            h.open_sheet()
            C.snapshot(pg, "fallback_before", RESULTS["metrics"])
            h.shot("fallback-before")
            # keyboard Keep on the edit
            keep = pg.query_selector('#review-root .grp[data-g="g1"] [data-act="keep"]')
            keep.focus(); pg.keyboard.press("Enter")
            pg.wait_for_selector("#review-toast:not([hidden])")
            C.snapshot(pg, "fallback_after_keep", RESULTS["metrics"])
            h.shot("fallback-after-keep")
            kb_undo(pg)
            C.snapshot(pg, "fallback_after_undo", RESULTS["metrics"])
            h.shot("fallback-after-undo-focus")
        run_case(h, "fallback-no-keepall", fx.mixed(), ffallback, when=at(2026, 11, 26, 14, 0))

        # (4) Frame 06: last single choice closes sheet; Undo leaves it closed; where is focus?
        def f06(pg):
            h.open_sheet()
            C.snapshot(pg, "frame06_before", RESULTS["metrics"])
            h.shot("frame06-before")
            use = pg.query_selector('#review-root [data-act="use"]')
            use.focus(); pg.keyboard.press("Enter")
            pg.wait_for_selector("#review-root .sheet", state="detached")
            pg.wait_for_timeout(200)
            C.snapshot(pg, "frame06_after_use", RESULTS["metrics"])
            h.shot("frame06-after-use")
            kb_undo(pg)
            C.snapshot(pg, "frame06_after_undo", RESULTS["metrics"])
            RESULTS["metrics"]["frame06_after_undo"]["sheetCount"] = len(pg.query_selector_all("#review-root .sheet"))
            RESULTS["metrics"]["frame06_after_undo"]["reviewBtn"] = bool(pg.query_selector('.today .sync-note [data-act="review"]'))
            h.shot("frame06-after-undo")
        run_case(h, "frame06-last-choice-undo", fx.one_entry(), f06, when=at(2026, 11, 26, 14, 0))

        # Linus keep_all_mix (Synthetic names) — regression vs his shots / 154a9f7
        def flinus(pg):
            h.open_sheet()
            C.snapshot(pg, "linus_before", RESULTS["metrics"])
            h.shot("linus-13b-before")
            pg.focus('#review-root [data-act="keepall"]')
            pg.keyboard.press("Enter")
            pg.wait_for_selector("#review-toast:not([hidden])")
            C.snapshot(pg, "linus_after_keepall", RESULTS["metrics"])
            h.shot("linus-after-keep-all-focus")
            kb_undo(pg)
            C.snapshot(pg, "linus_after_undo", RESULTS["metrics"])
            h.shot("linus-after-undo-focus")
        run_case(h, "linus-keep-all-mix", fx.keep_all_mix(), flinus, when=at(2026, 11, 26, 14, 0))

        b.close()

    json.dump(C.METRICS, open(f"/workspace/design-review-63/metrics-{LABEL}.json", "w"), indent=1)
    json.dump(RESULTS, open(f"/workspace/design-review-63/results-{LABEL}.json", "w"), indent=1, ensure_ascii=False)
    print("DONE", LABEL, "shots", len(list(OUT.glob('*.png'))))

if __name__ == "__main__":
    main()
