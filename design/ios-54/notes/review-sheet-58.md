# Mac “Review held changes” sheet (cadence#58)

Iris (Design), 27 Nov 2026, updated for Steve’s three room calls and his [Product answers](https://github.com/peakabhishek/cadence/issues/58#issuecomment-7204338388) to the nine open questions (spec V3 Held end state). Frames: `design/ios-54/frames/mac/review-sheet/` (1440×900 CSS px, rendered @2x = 2880×1800). Clickable: [`prototype/mac-review/`](https://peakabhishek.github.io/cadence-prototype/prototype/mac-review/). The frames are screenshots of that prototype (`prototype/mac-review/shots.py`), so the frames and the prototype can’t drift apart. All data is synthetic. Option B tokens and style are unchanged.

**Credits.** Scope: Steve. Snapshot approach (fields untouched since the hold apply from the phone, only Mac-edited fields go to Review): Linus. “Can’t tell which is newer” wording for fields with no stamp: Tony. **Where the snapshot and the once-only counts live is Linus’s to build, within the limits below. This file only draws the outcomes.** Questions 2, 5, 6 and 9 are assumed defaults, which Abhishek may overrule.

## What changed in this update

**Reason copy (27 Nov, later).** The snapshot reason is no longer “You changed the name on this Mac after this was held”. Linus’s PR #60 at `1233e17` sends a field to Review when the Mac edited it after the phone last saw the Mac’s file, which can be before the hold, so that line can be false. It now reads “You also changed the name on this Mac” (and “You also changed the target on this Mac”). The no-stamp / old-phone / save-nonce fallback is unchanged: “Can’t tell which is newer. Mac has Focus”.

1. **Today note.** Once #58 ships, “N phone changes to review” replaces #55’s longer “N changes from your phone weren’t applied…”. #55 keeps its copy until then. Frame 01 already shows the new copy. The sheet subtitle keeps the longer sentence (Iris’s call, which Steve left open).
2. **One Keep/Use per goal** moves every held name and target edit on that goal together. “Keep Mac’s version” keeps them all as they are on the Mac. “Use phone’s version” applies every held phone edit field on that goal. A choice per field is not needed in this slice (Steve’s default, Abhishek may overrule). Frame 03 shows this on “Write the weekly review” (time box and name, one pair of buttons, labelled “2 changes”).
3. **Sessions are separate.** Each held session keeps its own “Add this session” button and is never added or dropped by a per-goal Keep/Use or by “Keep Mac’s version for all”. After “for all”, session rows stay in the sheet (frame 13). A quiet helper under the bulk button reads “Sessions stay here until you add them.”
4. **Mixed group, frame 14:** one goal with a held session and a held name edit. Keep/Use apply only to the name edit; the session keeps “Add this session”. This session’s day has no Mac sessions, so the row shows no day total and does not invent “0 min”. (When that day does have Mac sessions, the total sits beside the line as muted context, as in frame 03: “Mac’s total for 18 Nov: 20 min”.)
5. **Remove and restore, frame 15** (copy finalised from Steve’s example): “Remove from phone: Deep work (still on this Mac)” with “Keep goal” / “Remove goal”, plus the quiet line “Past days stay in your history.” “Restored on phone: Deep work (removed on this Mac)” with “Keep removed” / “Restore goal”. Today behind the sheet is full (6 of 6), so the restore row adds “Today has 6 goals, so this goes to Parked.” After Restore, the toast is “1 goal didn’t fit today’s 6. It’s in Parked.” A held add on a day that already shows 6 goals uses the same Parked rule; this does not apply to goal-edit fields or sessions.
6. **Once-only applied note.** Counts are fixed at what the upgrade did. The note counts as shown only after Review or Got it is tapped; a quit or reload before that shows the same note with the same counts. Store only those figures and the acknowledgment, never goal names or values (where they live is Linus’s call). Frame 11 is “8 phone changes applied, 3 to review”. **Frame 16** is the applied-only variant: “8 phone changes applied” with only Got it, no Review.
7. **Logs** hold only ids, times and flags, never goal names or values. That covers the kept-Mac log and the once-only note’s counts and acknowledgment.

## Frames
| # | File | State |
|---|---|---|
| 1 | `01-today-note-review.png` | Today with the housekeeping note “3 phone changes to review” and the “Review” text link. This is the ordinary Today note once #58 ships. |
| 2 | `02-sheet-one-entry.png` | The sheet with one held change (goal Focus, reason: “You also changed the name on this Mac”). |
| 3 | `03-sheet-many-scrolling.png` | **Main frame.** Held changes grouped by goal: a session-only goal (Add this session only, with a Mac day total), snapshot and no-stamp reasons, a goal with two edit fields and one Keep/Use pair, too-old, unreadable and newer-schema last. The footer has “Keep Mac’s version for all” and the helper “Sessions stay here until you add them.” |
| 4 | `04-undo-keep-mac.png` | After “Keep Mac’s version” on Focus: the edit is gone, the session-only group stays, the Undo toast shows. |
| 5 | `05-undo-use-phone.png` | After “Add this session” on Read one paper: the session is gone, the Undo toast shows. |
| 6 | `06-last-resolved-note-gone.png` | The last change is resolved with “Use phone’s version”: the sheet has closed, the note is gone, and the Undo toast stays on Today. |
| 7 | `07-loading.png` | The sheet while the held list is being read: skeleton groups and “Reading held changes…”, no choice buttons. |
| 8 | `08-error-still-held.png` | A choice couldn’t be saved. The group is back in its place, still held, with retry copy. Sessions still have only “Add this session”. |
| 9 | `09-day-boundary-midnight-ist.png` | Sheet left open across midnight IST: Today behind it moved to Sat 28 Nov, the groups, rows, dates and count are unchanged. Has an annotation. |
| 10 | `10-closed-without-action.png` | Closed without choosing: the note shows the same count. Has an annotation. |
| 11 | `11-today-applied-note-once.png` | Today right after the Mac upgrade: “8 phone changes applied, 3 to review” with “Review” and “Got it”. Has an annotation (counts stay fixed until Review or Got it, and survive a quit or reload). |
| 12 | `12-sheet-empty.png` | Empty state: the sheet is open and the Mac finds nothing held. “No held changes. Nothing needs your choice right now.” and Close only. |
| 13 | `13-undo-keep-for-all.png` | After “Keep Mac’s version for all”: one toast for the 6 goal edits, the session row stays with “Add this session”, unreadable and newer-schema rows stay. The count is 3. |
| 14 | `14-sheet-mixed-session-and-edit.png` | **New.** One goal, Focus, with a held session and a held name edit. “Add this session” is on the session row; Keep/Use apply only to the name. No Mac day total (that day has no Mac sessions). |
| 15 | `15-sheet-remove-restore.png` | **New.** A remove row and a restore row. The restore has the Parked quiet line, and Today behind the sheet shows 6 of 6. |
| 16 | `16-today-applied-only.png` | **New.** Applied-only once-only note: “8 phone changes applied” with only Got it, no Review. Has an annotation. |

Annotations (frames 9, 10, 11 and 16, dashed box at top left) are not product UI.

## Copy (exact, curly apostrophes, never “discard”)
| Where | Copy |
|---|---|
| Today note, several (once #58 ships; #55 keeps its longer copy until then) | “3 phone changes to review” |
| Today note, one | “1 phone change to review” |
| Note button (text link) | “Review” |
| Once-only note after the upgrade | “8 phone changes applied, 3 to review” + “Review” + “Got it”. |
| Once-only note, nothing left to review (frame 16) | “8 phone changes applied” + “Got it”. |
| Sheet title | “Held changes from your phone” |
| Sheet subtitle, several | “Your Mac didn’t apply these N changes, to avoid overwriting newer edits. Nothing changes until you choose.” |
| Sheet subtitle, one | “Your Mac didn’t apply this change, to avoid overwriting newer edits. Nothing changes until you choose.” |
| Subtitle while loading | “Your Mac didn’t apply some changes from your phone, to avoid overwriting newer edits.” |
| Subtitle when empty | “Nothing from your phone is held right now.” |
| Loading line | “Reading held changes…” |
| Empty state | “No held changes” / “Nothing needs your choice right now.” |
| Group header | Goal name as the Mac has it now (“Focus”), plus “2 changes” when the group has more than one row. |
| Session row, day has Mac sessions | “Add 30-min session from your phone (18 Nov)” · muted “Mac’s total for 18 Nov: 20 min”. Meta as needed, e.g. “More than 7 days old”. |
| Session row, day has no Mac sessions | “Add 30-min session from your phone (18 Nov)” only. No total, and never “0 min”. |
| Goal-edit row (snapshot) | “Name: Deep work (Mac has Focus)”. Meta: “You also changed the name on this Mac”. Target: “You also changed the target on this Mac”. (The Mac edited the field after the phone last saw the Mac’s file, which can be before the hold; PR #60 at 1233e17.) |
| Goal-edit row (no snapshot or no stamp) | “Time box: 60 min”. Meta: “Can’t tell which is newer. Mac has 45 min”. The Mac value sits in the meta line here, so it isn’t said twice. |
| Goal-edit and add row (too old) | “Name: Gym, legs day (Mac has Gym)” / “Added to 17 Nov (Mac doesn’t have it)”. Meta: “From your phone on 19 Nov · More than 7 days old”. |
| Per-goal buttons | “Keep Mac’s version” (default, filled) · “Use phone’s version” (outline). These cover that goal’s held name and target edits only, all of them together. |
| Session button | “Add this session”, on the session row, never part of Keep/Use or “for all”. |
| Remove row | “Remove from phone: Deep work (still on this Mac)”. Quiet line: “Past days stay in your history.” Buttons: “Keep goal” (default, filled) · “Remove goal” (outline). |
| Restore row | “Restored on phone: Deep work (removed on this Mac)”. When today already shows 6 goals, quiet line: “Today has 6 goals, so this goes to Parked.” Buttons: “Keep removed” (default, filled) · “Restore goal” (outline). |
| Unreadable group | Header “Can’t be applied on this Mac yet”. Rows: “A change from your phone” / “From your phone on 24 Nov · This Mac can’t read it yet” and “Changes from a newer Cadence on your phone” / “From your phone · Made by a newer version of Cadence”. Line: “Update Cadence on this Mac to apply this.” No buttons. |
| Footer hint | “Closing keeps every change held.” |
| Footer buttons | “Keep Mac’s version for all” (shown only with 2 or more goal edits you can choose) · “Close” |
| Helper under the bulk button | “Sessions stay here until you add them.” (only when a session is still in the sheet) |
| Toast after Keep | “Kept your Mac’s version for Focus.” + “Undo” |
| Toast after Use | “Used your phone’s version for Focus.” + “Undo” |
| Toast after Add this session | “Added the 30-min session to Read one paper.” + “Undo” |
| Toast after Keep for all | “Kept your Mac’s version for 6 goal edits.” + “Undo” |
| Toast after Keep goal | “Kept Deep work on this Mac.” + “Undo” |
| Toast after Remove goal | “Removed Deep work from this Mac.” + “Undo” |
| Toast after Keep removed | “Kept Deep work removed.” + “Undo” |
| Toast after Restore, day is full | “1 goal didn’t fit today’s 6. It’s in Parked.” + “Undo” |
| Toast after Restore, day has room | “Restored Deep work on this Mac.” + “Undo” |
| Error in a group | “Couldn’t save your choice, so this change is still held. Check that your OneDrive folder is available.” (“these changes are still held” for a group of 2 or more) + “Try again” |
| Error after “for all” | “Couldn’t save your choice, so all 6 goal edits are still held. Check that your OneDrive folder is available. Sessions were not changed.” + “Try again” |

Dates are always absolute (“18 Nov”, IST day of the phone’s stamp), never “yesterday” or “8 days ago”, so nothing in a row changes at midnight.

## VoiceOver labels
| Control | Label (pattern, then example) |
|---|---|
| Review | “Review N held changes” / “Review 1 held change” |
| Keep Mac’s version (group) | “Keep Mac’s version for {goal}: {what it keeps on every held name and target field}”. Example: “Keep Mac’s version for Write the weekly review: keeps the 45 min time box and drops the phone’s 60 min; keeps the name Write the weekly review and drops the phone’s name Weekly review” |
| Use phone’s version (group) | “Use phone’s version for {goal}: {what it sets on every held name and target field}”. |
| Add this session | “Add this session to {goal}: adds a 30-min session on 18 Nov. The Mac’s own sessions stay as they are” |
| Keep goal | “Keep goal for Deep work: Deep work stays on this Mac and the phone’s remove isn’t applied” |
| Remove goal | “Remove goal for Deep work: removes Deep work from this Mac. Past days stay in your history” |
| Keep removed | “Keep removed for Deep work: Deep work stays removed on this Mac” |
| Restore goal (day full) | “Restore goal for Deep work: restores Deep work to today’s Parked list, because today already has 6 goals showing” |
| Keep Mac’s version for all | “Keep Mac’s version for all N goal edits you can choose. Sessions stay held until you add them.” |
| Close and × | “Close. Every change stays held.” |
| Try again | “Try again: ” + the label of the button that failed |
| Got it | “Got it. Hide this note” |
| Undo | “Undo” inside a polite live-region toast that reads the toast sentence first |

Sheet: `role="dialog"`, `aria-modal="true"`, labelled by the title, described by the subtitle. The list is a list (“Held changes, grouped by goal”), each group a list item with its rows as a nested list. Loading sets `aria-busy`. Errors are `role="alert"`. Esc closes. On close, focus goes back to Review.

## Interaction rules
1. The ordinary Today note, once #58 ships, is housekeeping: leaf-wash, no error colour, “N phone changes to review” and one text-link “Review”. It replaces #55’s longer copy. #55 keeps that copy until then. The count is the number of held changes (`heldCount`), the same number as in the sheet subtitle. The note disappears when nothing is held.
2. Review opens the sheet. Held changes are **grouped by goal**. Unreadable and newer-schema changes sit in a last group with no buttons and clear by themselves once the Mac is updated.
3. **One Keep/Use per goal covers that goal’s held name and target edits only, all of them together.** It never applies to sessions. A session always has its own “Add this session” button (adds that one session, deduped by id, and replaces no Mac total).
4. The Mac’s day total is shown as muted context on a session row only when that day already has sessions on the Mac. If it has none, the row shows no total and never “0 min”.
5. “Keep Mac’s version” (or “Keep goal” / “Keep removed”) is the default (filled button, first in tab order). The kept-Mac log stores only ids, times and flags, never goal names or values. There is **no history UI**.
6. **No confirm dialog.** A choice removes the rows it covers at once and shows a 5-second Undo toast at the bottom centre. A new choice ends the previous toast. Undo puts the rows back in place and the count back.
7. **A choice is saved when the 5-second Undo ends**, not at once. Until then the entry is still held on disk, so quitting the app inside the 5 seconds leaves it held (spec V3).
8. **“Keep Mac’s version for all” is one write**, saved after its Undo ends. It is the only bulk action. It covers goal edits only. It never adds or drops sessions, and in this slice it also leaves removes, restores, unreadable and newer-schema rows alone.
9. **A failed save puts the entry back as held**, in its place, with the error and Try again (frame 8). Nothing is dropped and nothing half-applies. For “for all”, every goal edit comes back and one banner above the list says so. Sessions were not changed.
10. **Closing (Close, ×, Esc or a click outside) keeps everything held**, and the note count stays the same (frame 10).
11. When the last change is resolved, the sheet closes and the note disappears. The toast stays on Today, and Undo brings the note back but doesn’t reopen the sheet (frame 6). If only sessions, unreadable or newer-schema changes remain, the sheet stays open with them and “Keep Mac’s version for all” is hidden.
12. **Once-only applied note (frames 11 and 16).** After the upgrade, the first Today view shows “N phone changes applied, M to review” or, if nothing is left to review, “N phone changes applied”. The counts are what the upgrade did and never change afterwards (not at midnight, not while the sheet is open). The note counts as shown only after Review or Got it is tapped. If the Mac quits or reloads before that, the same note shows again with the same fixed counts. Store only those figures and the acknowledgment, never goal names or values; where they live is Linus’s call. “Review” opens the sheet with exactly M changes and ends the once-only note. “Got it” ends it too. Today then shows the housekeeping note for what is still held, or no note if nothing is held. The counts have to match what actually happened (spec V3 done-when).
13. **Empty state (frame 12).** The sheet is only reachable from the note, but the list can be empty when it opens or while it is open. It then says so and offers Close only.
14. **Parked on a full day.** A held add or restore for an IST day that already shows 6 goals goes to that day’s Parked list. Already-showing goals stay. The restore row (frame 15) has the quiet line “Today has 6 goals, so this goes to Parked.” After Restore (or a held add on a full day), both apps show “1 goal didn’t fit today’s 6. It’s in Parked.” and the held entry is resolved. This does not apply to goal-edit fields or sessions.

## Day boundary (frame 9, every time-based screen)
A sheet left open across midnight IST keeps its groups, rows, dates and count. Nothing auto-resolves and the 5-second Undo is unaffected. Today behind it moves to the new day as usual and the note stays. Row dates are absolute, so they stay correct. The once-only applied note (frames 11 and 16) is not recomputed at midnight and is not acknowledged by the day changing. A session row’s “Mac’s total for 18 Nov” is a total for that named day, so it never changes meaning at midnight.

## Tokens used (colours only from `tokens.css` = cadence `web/tokens.css`, then `ios-tokens.css` at 5436723)
- Note (both the routine note and the once-only applied note): `--leaf-wash` background, `--leaf-deep` text. Review and Got it links: `--leaf`. No error colour.
- Sheet: `--surface`, `--r-sheet`, `--shadow-dialog`, `--scrim` behind it, `--line` separators. Title in `--font-display` and `--text`. Body in `--font-ui` and `--text`, with `--text-muted` for the Mac value, meta, hint, quiet lines, helper under the bulk button, and icons.
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
| Mac value, meta line, hint, quiet line, helper, close icon, update line | `--text-muted` #5C5146 | `--surface` #FFFBF6 | 7.49:1 | 4.5 | PASS |
| Keep Mac’s version (filled) | `--on-leaf` #F7F0E6 | `--leaf` #1B5E3B | 6.85:1 | 4.5 | PASS |
| Use phone’s version / Keep … for all / Close / Undo text | `--leaf` #1B5E3B | `--surface` #FFFBF6 | 7.52:1 | 4.5 | PASS |
| Outline button border, focus ring (UI) | `--leaf` #1B5E3B | `--surface` #FFFBF6 | 7.52:1 | 3.0 | PASS |
| Error line and Try again | `--wither-ink` #74492B | `--wither-bg` #F3E6D6 | 6.26:1 | 4.5 | PASS |
| Annotation (frames only, not UI) | `--text` #2A2118 | `--track` #EFE4D5 | 12.59:1 | 4.5 | PASS |
| Skeleton bar vs sheet (decorative) | `--track` #EFE4D5 | `--surface` #FFFBF6 | 1.22:1 | – | decorative |
| Separator (decorative) | `--line` #E6D7C4 | `--surface` #FFFBF6 | 1.37:1 | – | decorative |

No new colour pairs in this update, so the table still covers the quiet lines, the bulk helper and the muted parentheticals.

## Build limits (for Linus; not product decisions)
- Review must show the matching reason for the two cases. When the Mac can tell it also edited the field (after the phone last saw the Mac’s file, which can be before the hold; Linus’s PR #60 at 1233e17), the reason is “You also changed the name on this Mac” or “You also changed the target on this Mac”. When it can’t tell (no stamp, old phone, or save-nonce fallback), the reason stays “Can’t tell which is newer. Mac has Focus”. How those cases are stored is Linus’s call. Any new record stays to ids, timestamps or flags, never goal names or values.
- After a downgrade to #55 and back, the once-only applied counts are lost and every held entry returns as the no-stamp row (“Can’t tell which is newer…”). No applied note is shown in that case. **Open question for Steve:** the frames and prototype draw it this way; confirm it matches the spec, or say otherwise.
- The two once-only counts and the acknowledgment state must survive a reload. Where they live is Linus’s call, with the same limit.
- The Mac already has that day’s sessions in the main file. How the session-row total is read is Linus’s call. If that day has no sessions on the Mac, show no total and do not invent a number.
