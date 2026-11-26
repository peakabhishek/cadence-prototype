# Mac “Review held changes” sheet (cadence#58)

Iris (Design), 27 Nov 2026. Frames: `design/ios-54/frames/mac/review-sheet/` (1440×900 CSS px, rendered @2x = 2880×1800). Clickable: [`prototype/mac-review/`](https://peakabhishek.github.io/cadence-prototype/prototype/mac-review/). The frames are screenshots of that prototype (`prototype/mac-review/shots.py`), so the frames and the prototype can’t drift apart. All data is synthetic.

**Behaviour source.** Steve accepted Iris’s proposal (Abhishek can still overrule it). Steve and Tony then agreed two more rules: “Use phone’s version” overwrites only the fields that the held entry changed, and the kept-Mac log holds only the entry id, device, date and reason. **The storage and sync assumptions below are Steve’s (product) and Linus’s (build) to confirm. This file only draws them.**

## Frames
| # | File | State |
|---|---|---|
| 1 | `01-today-note-review.png` | Today with the syncHeld note (today’s copy) and the “Review” text-link button. The count is 3. |
| 2 | `02-sheet-one-entry.png` | The sheet with one too-old entry. |
| 3 | `03-sheet-many-scrolling.png` | 7 entries, scrolled 150 px into the list: too old, lost the compare, unreadable and newer schema mixed. The footer stays fixed. |
| 4 | `04-undo-keep-mac.png` | After “Keep Mac’s version”: the row is gone, the count is 2, and the Undo toast shows. |
| 5 | `05-undo-use-phone.png` | After “Use phone’s version”: the same layout with the Use toast. |
| 6 | `06-last-resolved-note-gone.png` | The last entry is resolved: the sheet has closed, the note is gone, and the Undo toast stays on Today. |
| 7 | `07-loading.png` | The sheet while the held list is being read: skeleton rows and “Reading held changes…”, no choice buttons. |
| 8 | `08-error-still-held.png` | The choice couldn’t be saved. The row is back in its place, still held, with retry copy. |
| 9 | `09-day-boundary-midnight-ist.png` | The sheet left open across midnight IST: Today behind it moved to Sat 28 Nov, and the rows and dates are unchanged. Has an annotation. |
| 10 | `10-closed-without-action.png` | Closed without choosing: the note shows the same count. Has an annotation. |

Annotations (frames 9 and 10, dashed box at top left) are not product UI.

## Copy (exact, curly apostrophes, never “discard”)
| Where | Copy |
|---|---|
| Today note, several (unchanged from #55) | “3 changes from your phone weren’t applied, to avoid overwriting newer edits.” |
| Today note, one (unchanged from #55) | “1 change from your phone wasn’t applied, to avoid overwriting newer edits.” |
| Note button (text link) | “Review” |
| Sheet title | “Held changes from your phone” |
| Sheet subtitle, several | “Your Mac didn’t apply these N changes, to avoid overwriting newer edits. Nothing changes until you choose.” |
| Sheet subtitle, one | “Your Mac didn’t apply this change, to avoid overwriting newer edits. Nothing changes until you choose.” |
| Subtitle while loading | “Your Mac didn’t apply some changes from your phone, to avoid overwriting newer edits.” |
| Loading line | “Reading held changes…” |
| Choice row, line 1 | Goal name, as the Mac has it now. Example: “Read one paper” |
| Choice row, line 2 (the ONE field the phone would set, then the Mac’s current value) | “Focus on 18 Nov: 30 min logged (Mac has 20 min)” · “Time box: 60 min (Mac has 45 min)” · “Name: “Gym, legs day” (Mac has “Gym”)” · “Added to 17 Nov (Mac doesn’t have it)” |
| Choice row, line 3 | “From your phone on 18 Nov · More than 7 days old”, or “From your phone on 25 Nov · Your Mac changed this later” (lost the field-by-field compare) |
| Choice buttons | “Keep Mac’s version” (default, filled) · “Use phone’s version” (outline) |
| Unreadable row | Title: “A change from your phone”. Meta: “From your phone on 24 Nov · This Mac can’t read it yet”. Line: “Update Cadence on this Mac to apply this.” No buttons. |
| Newer-schema row | Title: “Changes from a newer Cadence on your phone”. Meta: “From your phone · Made by a newer version of Cadence”. Line: “Update Cadence on this Mac to apply this.” No buttons. |
| Footer hint | “Closing keeps every change held.” |
| Footer buttons | “Keep Mac’s version for all” (shown only with 2 or more choice rows) · “Close” |
| Toast after Keep | “Kept your Mac’s version for Read one paper.” + “Undo” |
| Toast after Use | “Used your phone’s version for Read one paper.” + “Undo” |
| Toast after Keep for all | “Kept your Mac’s version for 5 changes.” + “Undo” |
| Error in the row | “Couldn’t save your choice, so this change is still held. Check that your OneDrive folder is available.” + “Try again” |

Dates are always absolute (“on 18 Nov”, IST day of the phone’s stamp), never “yesterday” or “8 days ago”, so nothing in a row changes at midnight.

## VoiceOver labels
| Control | Label (pattern, then example) |
|---|---|
| Review | “Review N held changes” / “Review 1 held change” |
| Keep Mac’s version | “Keep Mac’s version for {goal}: keeps {Mac value} and drops the phone’s {phone value}”. Example: “Keep Mac’s version for Read one paper: keeps 20 min on 18 Nov and drops the phone’s 30 min” |
| Use phone’s version | “Use phone’s version for {goal}: sets {field} to {phone value}, replacing the Mac’s {Mac value}”. Example: “Use phone’s version for Read one paper: sets 30 min logged on 18 Nov, replacing the Mac’s 20 min” |
| Keep Mac’s version for all | “Keep Mac’s version for all N changes you can choose. The phone changes are dropped.” |
| Close and × | “Close. Every change stays held.” |
| Try again | “Try again: ” + the label of the button that failed |
| Undo | “Undo” inside a polite live-region toast that reads the toast sentence first |

Sheet: `role="dialog"`, `aria-modal="true"`, labelled by the title, described by the subtitle. The list is a list (“Held changes”). Loading sets `aria-busy`. The error is `role="alert"`. Esc closes. On close, focus goes back to Review.

## Interaction rules
1. The note keeps today’s copy and count (`heldCount` from #55) and adds one text-link button. It is not a second card. The note disappears when nothing is held.
2. Review opens the sheet. Each held entry is one row. Too-old rows and rows that lost the field-by-field compare get the two buttons. Unreadable and newer-schema rows get no buttons and clear by themselves once the Mac is updated.
3. **Each choice row names exactly the field the phone value would set, with the Mac’s current value next to it.** “Use phone’s version” is Abhishek’s explicit choice: it overwrites only the fields that the held entry changed, even where the Mac has a newer stamp. One row is one held entry. If an entry changed two fields, both go on line 2 of the same row (see the open questions).
4. “Keep Mac’s version” is the default (filled button, first in tab order) and drops the phone change. It is the **only** way a phone change gets dropped. The log stores only the entry id, device, date and reason, with no goal names or values. There is **no history UI**.
5. No confirm dialog. Each choice removes the row at once and shows a 5-second Undo toast at the bottom centre (the existing Mac `.toast`). A new choice ends the previous toast. Undo puts the row back in its place and the count back.
6. **The prototype assumes the choice is written when the 5-second Undo ends.** Until then the entry is still held on disk, so quitting the app within the 5 seconds leaves it held. Linus to confirm, or to replace this with an immediate write plus a reverse write on Undo.
7. If the write fails, the row comes back in place, still held, with the error and Try again (frame 8). Nothing is dropped.
8. Closing the sheet (Close, ×, Esc, or a click outside) without a choice keeps every entry held, and the note count stays the same (frame 10).
9. When the last entry is resolved, the sheet closes and the note disappears. The toast stays on Today, and Undo brings the note back but doesn’t reopen the sheet (frame 6). If only unreadable or newer-schema rows remain, the sheet stays open with them, and “Keep Mac’s version for all” is hidden.
10. Day boundary: a sheet left open across midnight IST keeps its rows, dates and count. Nothing auto-resolves. Today behind it moves to the new day as usual, and the note stays on the new day (frame 9).

## Tokens used (colours only from `tokens.css` = cadence `web/tokens.css`, then `ios-tokens.css` at 5436723)
- Note: `--leaf-wash` background, `--leaf-deep` text. Review link: `--leaf`.
- Sheet: `--surface`, `--r-sheet`, `--shadow-dialog`, `--scrim` behind it, `--line` separators. Title in `--font-display` and `--text`. Body in `--font-ui` and `--text`, with `--text-muted` for the Mac value, meta, hint and icons.
- Buttons: filled `--leaf` with `--on-leaf` and `--shadow-primary`. Outline `--leaf` on `--surface`. Text buttons `--leaf`. Height `--tap-min`, radius `--r-pill`.
- Error: `--wither-bg` and `--wither-ink`. Skeleton: `--track`. Toast: `--surface`, `--line` ring, `--shadow-card`, check in `--success`.
- Window frame: `--chrome`, `--chrome-line`, `--url-bg`, `--window-light-1/2/3` (traffic lights), `--sun` glow (decorative), `--sill-*`.
- A grep of `prototype/mac-review/review.css` and `review.js` for hex, rgb(a) and hsl(a) literals finds none. Sizes use tokens where one exists.

## Contrast (WCAG 2.x, computed)
| Pair | Foreground | Background | Ratio | Needs | Result |
|---|---|---|---|---|---|
| Note text | `--leaf-deep` #0F3D27 | `--leaf-wash` #E6EEE3 | 10.31:1 | 4.5 | PASS |
| Review link | `--leaf` #1B5E3B | `--leaf-wash` #E6EEE3 | 6.53:1 | 4.5 | PASS |
| Sheet title, goal name, change line, toast text | `--text` #2A2118 | `--surface` #FFFBF6 | 15.33:1 | 4.5 | PASS |
| Mac value, meta line, hint, close icon, update line | `--text-muted` #5C5146 | `--surface` #FFFBF6 | 7.49:1 | 4.5 | PASS |
| Keep Mac’s version (filled) | `--on-leaf` #F7F0E6 | `--leaf` #1B5E3B | 6.85:1 | 4.5 | PASS |
| Use phone’s version / Keep … for all / Close / Undo text | `--leaf` #1B5E3B | `--surface` #FFFBF6 | 7.52:1 | 4.5 | PASS |
| Outline button border, focus ring (UI) | `--leaf` #1B5E3B | `--surface` #FFFBF6 | 7.52:1 | 3.0 | PASS |
| Error line and Try again | `--wither-ink` #74492B | `--wither-bg` #F3E6D6 | 6.26:1 | 4.5 | PASS |
| Annotation (frames only, not UI) | `--text` #2A2118 | `--track` #EFE4D5 | 12.59:1 | 4.5 | PASS |
| Skeleton bar vs sheet (decorative) | `--track` #EFE4D5 | `--surface` #FFFBF6 | 1.22:1 | – | decorative |
| Separator (decorative) | `--line` #E6D7C4 | `--surface` #FFFBF6 | 1.37:1 | – | decorative |

## Assumptions to confirm (Steve: product, Linus: storage and sync)
- The Mac can show the goal name, the one field and the Mac’s current value for too-old and lost-compare entries.
- For an unreadable entry it can still read the phone’s stamp day. If it can’t, the row drops “on 24 Nov”.
- A newer-schema file is one row with no date, matching `heldCount` counting `schema_held` as 1.
- “Lost the field-by-field compare” is a held reason that the Mac stores, alongside `too_old` and `invalid`.
