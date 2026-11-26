# Design re-review of cadence PR #55 at 3b1f92f

Compared with the formal review at `9a3e9a1` (`design/ios-54/review-55/9a3e9a1/`). Mac app run locally from `/workspace/cadence-r55-3b1f92f` on synthetic data only, Chromium via Playwright, 1280×800 at 2×, same goals and clock (19:30 IST) as the earlier reviews.

States:
- `today-normal.png`
- `today-synchold-3.png`, `today-synchold-1.png` (existing sync_held)
- `today-too-old-8day.png` — seeded `held: [{seq:1, reason:"too_old"}]`
- `today-unreadable.png` — seeded `held: [{seq:1, reason:"invalid"}]`
- `today-newer-schema.png` — seeded `schema_held: 2`
- `today-superseded.png` — seeded `held: [{seq:1, reason:"superseded", fields:["title","box_minutes"]}]`, the file shape after a held entry loses a field (including a field with no stamp)

`notes/capture-3b1f92f.py` regenerates the after shots. All comparable views, and the new superseded view against syncHeld 1, are pixel-identical (and SHA-256 identical) to the `9a3e9a1` after shots.
