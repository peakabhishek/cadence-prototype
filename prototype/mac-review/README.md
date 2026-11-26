# Cadence Mac: Review held changes (cadence#58), clickable prototype

Live: https://peakabhishek.github.io/cadence-prototype/prototype/mac-review/

Synthetic data only. Nothing is saved; reloading resets it.

## Try it
- **Review** on the green note opens the sheet. It shows a short loading state, then one row per held change.
- **Keep Mac’s version** or **Use phone’s version** removes the row and shows a 5-second Undo toast. The choice is treated as saved when the toast ends.
- **Keep Mac’s version for all** applies to every row that has buttons. Rows that say "Update Cadence on this Mac to apply this." stay.
- **Close**, the × button, Esc, or a click outside the sheet closes it and keeps every change held.
- When the last held change is resolved, the sheet closes and the note disappears. Undo brings the note back.
- Demo bar (bottom right): jump to each of the 10 frame states, or "Make the next save fail" to see the error and Try again.

## Files
- `index.html`, `review.css`, `review.js`: the prototype.
- `tokens.css`: byte copy of cadence `web/tokens.css`, loaded before `design/ios-54/ios-tokens.css` (5436723).
- `shots.py`: renders `design/ios-54/frames/mac/review-sheet/*.png` (1440×900 @2x) from this page with `?state=…&frame=1`.

Spec and copy: `design/ios-54/notes/review-sheet-58.md`.
