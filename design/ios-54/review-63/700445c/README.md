# Design recheck of cadence PR #63 at 700445c

Probe g / scrolled-out Review focus follow-up on `a698fc7`. The app was run locally from `700445c03fffcbb0df6ab2182fa29de7b11c2848` on synthetic data only (real server in-process, system Chrome via Playwright, 1440×900 at 2×, IST). Diff since `a698fc7` is `focusOpener()` in `web/review-sheet.js`, tests, and a CHANGELOG line; no CSS, tokens or in-app copy. Nothing was pushed to cadence.

Verdict: **Design: pass** on `700445c`. After Undo in frame 06 with the Review note scrolled out of view, the button jumps into the viewport instantly (`block: 'nearest'`), sits clear of the sticky header, and shows the token ring. `elementFromPoint` at its centre is the button. `#view` remains the fallback only when the button is hidden or missing.

- `after/` this build, including the viewport shot after the scrolled-out Undo.
- `before/` the same scrolled-out Undo on `a698fc7`, plus a few frames from `0013b16`.
- `side-by-side/` a698fc7 vs 700445c, and before/after on this SHA.
- `notes/findings.md` the review notes, capture script and raw results.

This review is for `700445c` only. Abhishek’s visual OK stays a separate merge-time gate (spec §6).
