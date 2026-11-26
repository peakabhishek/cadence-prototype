# Cadence Mac: Review held changes (cadence#58), clickable prototype

Live: https://peakabhishek.github.io/cadence-prototype/prototype/mac-review/

Synthetic data only. Nothing is saved; reloading resets it.

## Try it
- **Review** on the green note opens the sheet. It shows a short loading state, then the held changes grouped by goal (frame 3 is the main frame).
- **Keep Mac’s version**, **Use phone’s version** or **Add this session** applies to the whole goal group, removes it and shows a 5-second Undo toast. The choice is treated as saved when the toast ends.
- **Keep Mac’s version for all** is the only bulk action, one write. Changes that say "Update Cadence on this Mac to apply this." stay.
- **Close**, the × button, Esc, or a click outside the sheet closes it and keeps every change held.
- When the last held change is resolved, the sheet closes and the note disappears. Undo brings the note back.
- Demo bar (bottom right): jump to each of the 13 frame states (11 is the once-only "8 phone changes applied, 3 to review" note, 12 the empty state, 13 Undo after "for all"), or "Make the next save fail" to see the error and Try again (single group or "for all").

## Files
- `index.html`, `review.css`, `review.js`: the prototype.
- `tokens.css`: byte copy of cadence `web/tokens.css`, loaded before `design/ios-54/ios-tokens.css` (5436723).
- `shots.py`: renders `design/ios-54/frames/mac/review-sheet/*.png` (1440×900 @2x) from this page with `?state=…&frame=1`.

Spec and copy: `design/ios-54/notes/review-sheet-58.md`.
