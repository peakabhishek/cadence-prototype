# Design review of cadence PR #61 at ac4e8d6

Copy-only follow-up on `10a5f90` (bbd39ed: helper, when it shows, aria-label, error “Nothing else was changed.”; ac4e8d6: “Sample User” in the ios-tokens.css header comment and three fixtures, token values unchanged). Judged against the settled two-line helper and the 10a5f90 recheck at `design/ios-54/review-61/10a5f90/`. The app was run locally from `ac4e8d6bd496f1d8e93b1cefa89a40653de15727` on synthetic data only (real server in-process, system Chrome via Playwright, 1440×900 at 2×, IST). Nothing was pushed to cadence.

- `after/` the build, including `13-keep-for-all-helper.png`, `15-sheet-remove-restore.png` (with two goal edits so Keep all and the helper show), `helper-hidden-edits-only.png`, and `bulk-error-nothing-else-changed.png`.
- `side-by-side/` frame vs build, plus `helper-hidden-vs-visible.png`.
- `notes/` the capture script, raw results, and Linus’s 13 helper / 15 shots next to this build.

The helper reads exactly “Keeps your Mac’s version of goal edits. Everything else stays here to choose.” (U+2019), two lines at 240 px. It shows when a leftover row would stay (frame 13: adds and sessions; frame 15: a held remove) and hides when the sheet has only goal edits. The aria-label and the bulk error (“Nothing else was changed.”) match. The two later nits from the 10a5f90 recheck are in cadence#62.
