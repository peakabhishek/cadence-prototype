# Design recheck of cadence PR #63 at a698fc7

Frame 06 Undo focus follow-up on `0013b16`. The app was run locally from `a698fc756f0f86055c88b01fe07c565bb0e5486f` on synthetic data only (real server in-process, system Chrome via Playwright, 1440×900 at 2×, IST). Diff since `0013b16` is `undo()` / `focusOpener()` in `web/review-sheet.js`, tests, and a CHANGELOG line; no CSS, tokens or in-app copy. Nothing was pushed to cadence.

Verdict: **Design: changes requested** on `a698fc7`. When the Review button is in view, Undo in frame 06 now focuses it with the token ring and leaves the sheet closed. When the Review button is only scrolled out of view, focus still goes to that button but `preventScroll: true` leaves it off screen — a blocker (focus on an invisible control).

- `after/` this build.
- `before/` the same frame 06 Undo (and a few regression frames) on `0013b16`.
- `side-by-side/` 0013b16 vs a698fc7, and the scrolled-out blocker.
- `notes/findings.md` the review notes, capture scripts and raw results.

This review is for `a698fc7` only. Abhishek’s visual OK stays a separate merge-time gate (spec §6).
