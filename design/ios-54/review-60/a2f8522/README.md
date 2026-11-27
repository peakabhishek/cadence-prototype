# Design review of cadence PR #60 at a2f8522

#58 data layer only (the Review sheet UI is not in this PR). Compared with the formal #55 review at `3b1f92f` (`design/ios-54/review-55/3b1f92f/`). Mac app run locally from `/workspace/cadence-r60-a2f8522` on synthetic data only, Chromium via Playwright, 1280×800 at 2×, same goals and clock (19:30 IST) as the #55 reviews.

States:
- `today-normal.png`
- `today-synchold-3.png`, `today-synchold-1.png` (existing sync_held)
- `today-superseded.png` — seeded `held: [{seq:1, reason:"superseded", fields:["title","box_minutes"]}]`
- `today-superseded-later.png` — seeded `held: [{seq:1, reason:"superseded", fields:["title"], later:["title"]}]` (#58 shape)
- `today-late-counts-only.png` — seeded `syncState.late_counts: {applied:2, review:1}` and no held entries
- `today-synchold-1-late-counts.png` — syncHeld 1 plus those late_counts

`notes/capture-a2f8522.py` regenerates the after shots. Every comparable view is pixel-identical (and SHA-256 identical) to the `3b1f92f` after shots. late_counts do not appear on Today.
