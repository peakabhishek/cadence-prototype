# Cadence for iPhone: Option B prototype (clickable, fake data)

Live: https://peakabhishek.github.io/cadence-prototype/prototype/ios-b/

Open in Safari on the iPhone, then Share > Add to Home Screen to run it full screen.
Every screen shows "Demo data, not synced". Nothing is saved anywhere except this browser (localStorage).

## Try it
- **Today**: tick a goal, "+" or "Add goal" opens the sheet (type, pick a time box, Add). Swipe a goal left to Remove, Undo appears.
  At 6 goals the Add goal row is dimmed and the sheet shows "Today already has 6 goals. Remove one to add this."
- **Focus** tab: pick a goal and a length (25, 50, or 1 min for demo), Start focusing. The countdown is computed from the start time, so it stays right after you lock the phone or switch apps. Let it finish for "Grew." or tap Give up for the withered plant.
- **Tap the sync line** under the title for the Sync sheet (Sync now).
- **"..." (top left)** opens Demo states: Parked sequence (guided, 4 steps), 6 goals, session past midnight IST, new day,
  first run (mocked sign-in), empty, loading, error with Try again, offline, syncing, 2 changes waiting to upload, waiting for your Mac,
  Mac needs update, syncHeld, sync failed (Try again), edited on both devices (conflict sheet), sign-in expired, phone clock is off,
  Days follow India time (also shows by itself if the phone is not on India time). "Reset demo" clears saved state.

## Files
- `index.html` self-contained (tokens, CSS, JS, plant art inlined). `manifest.webmanifest`, `icon-*.png` for Add to Home Screen.
- `src/` source: `app.src.html`, `app.js`, `build.py` (rebuilds index.html from `design/ios-54/ios-tokens.css` + handoff `tokens.css`), `shots.py` (Playwright walk, 390x844 @3x), `icons.py`.
- `screens/` screenshots of every flow and state from the headless run.

## Known gaps vs the real app
- No haptics, no system sheets or native keyboard behaviour beyond what Safari gives; Dynamic Type follows Safari's text size only.
- Add sheet uses time-box chips instead of the push-in Time box picker in the frame.
- "Demo guide" strip, Focus idle (pick a goal), Give up confirm and Gave up screens are not in the B frames.
- Font: system font (SF Pro on iPhone). Screenshots here use Inter as a stand-in, as the frames do.
- `?frame=1` or a desktop window draws a simulated status bar and Dynamic Island; on the phone it uses the real safe areas.
