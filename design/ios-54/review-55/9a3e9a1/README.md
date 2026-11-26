# Design re-review of cadence PR #55 at 9a3e9a1

Compared with the formal review at `6975f9b` (`design/ios-54/review-55/6975f9b/`). Mac app run locally from `/workspace/cadence-r55-9a3e9a1` on synthetic data only, Chromium via Playwright, 1280x800 at 2x, same goals and clock (19:30 IST) as the earlier review.

States:
- `today-normal.png`
- `today-synchold-3.png`, `today-synchold-1.png` (existing sync_held)
- `today-too-old-8day.png` — seeded `held: [{seq:1, reason:"too_old"}]`, the file shape after the Mac holds an 8-day-old entry
- `today-unreadable.png` — seeded `held: [{seq:1, reason:"invalid"}]`
- `today-newer-schema.png` — seeded `schema_held: 2`

`notes/capture-9a3e9a1.py` regenerates the after shots.
