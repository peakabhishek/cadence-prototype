# Design recheck of cadence PR #61 at 10a5f90

Recheck of Iris’s six Design: nits on 011eb14 (review 6084350423), plus frame 13, Linus’s new 13b and 07b, against frames 01–16 at cadence-prototype `d60c889` and `design/ios-54/notes/review-sheet-58.md`. The app was run locally from `10a5f90e0b9f2a5b5ce1b970bffb77b11fff9ba7` on synthetic data only (real server in-process, system Chrome via Playwright, 1440×900 at 2×, IST, page and server clocks pinned). Nothing was pushed to cadence.

This folder is the on-screen evidence for 10a5f90. The helper under “Keep Mac’s version for all” still reads “Sessions stay here until you add them.” A settled copy-only follow-up (not in this SHA) should use: “Keeps your Mac’s version of goal edits. Everything else stays here to choose.” The longer room draft, with “one by one”, wraps to three lines at 240 px; dropping “one by one” fits in two.

- `after/` the build, one PNG per frame state (2880×1800). Extra states: `03b`, `07b`, `13b`, `15b`, `focus-after-keep.png`.
- `side-by-side/` frame (left) vs build (right), half size. 07b and 13b have no approved frame, so they are paired with frames 07 and 13. The frames are prototype shots with a faux window bar, so compare the sheet.
- `notes/` the capture script and raw results, geometry vs the prototype, and Linus’s 13 / 13b / 07b next to this build.

Data-only differences (not design): session minutes 25 vs 30; Today behind the sheet is the real Mac layout; greeting follows the clock; Linus’s shots use “Synthetic …” names.
