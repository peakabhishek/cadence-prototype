# Design review of cadence PR #55 at 6975f9b

Before = main `260dd8d` (the PR's merge-base). After = `6975f9b`. Mac app run locally from each commit with synthetic data only
(goals "Write the weekly review", "Read one paper", "Gym", "Plan Friday’s demo"), Chromium via Playwright, 1280x800 at 2x unless the name says otherwise.
The banner shots use a simulated Capacitor shell (`window.Capacitor.isNativePlatform() = true`), as the PR's own tests do; `-inset47/-inset54` override `--ios-safe-top` to emulate the iPhone safe area.
`notes/capture.py` and `notes/extra2.py` regenerate everything. Reference frames: `design/ios-54/frames/mac/mac-sync-held.png`, `frames/B/01-today.png`.
