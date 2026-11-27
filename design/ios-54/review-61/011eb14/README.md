# Design review of cadence PR #61 at 011eb14

The #58 "Review held changes" sheet (Mac), judged against frames 01–16 at cadence-prototype `d60c889` (`design/ios-54/frames/mac/review-sheet/`) and `design/ios-54/notes/review-sheet-58.md`. The app was run locally from the PR head `011eb14846f1bea8f3e5c89bb2f4cbf565ca953c` on synthetic data only (the real server in-process, system Chrome via Playwright, 1440×900 at 2×, IST, page and server clocks pinned). Nothing was pushed to cadence.

- `after/` the build, one PNG per frame state (2880×1800, same as the frames). Extra states: `03b` (list scrolled to the end), `07b` (load error with Try again), `15b` (Restore → Parked toast), `focus-ring.png` (keyboard focus).
- `side-by-side/` frame (left) vs build (right), half size. The frames are screenshots of the prototype with a faux window bar and the phone-width Today card, so the page behind the sheet differs by design; compare the sheet.
- `notes/` the scripts and raw results: `capture61.py` (all states, copy, contrast audit), `metrics.js` + `proto-metrics.json` + `build-metrics.json` (geometry and computed style, prototype vs build), `a11y61.py` (Tab order, focus trap, Esc, scrim, focus return), `once61.py` (once-only note across reload and midnight).

Data-only differences (not design): session minutes 25 vs 30 and the Mac total 25 vs 20 min (the app only accepts 25/50/90 sessions); Today behind the sheet is the real Mac layout with five goals; greeting follows the clock.
