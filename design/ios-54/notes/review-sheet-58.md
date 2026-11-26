# Mac “Review held changes” sheet (cadence#58)

Iris (Design), 27 Nov 2026, updated for the #58 scope in Steve’s comment 7204074363, Quinn’s plan 7204084211 and the spec V3 “Held end state”. Frames: `design/ios-54/frames/mac/review-sheet/` (1440×900 CSS px, rendered @2x = 2880×1800). Clickable: [`prototype/mac-review/`](https://peakabhishek.github.io/cadence-prototype/prototype/mac-review/). The frames are screenshots of that prototype (`prototype/mac-review/shots.py`), so the frames and the prototype can’t drift apart. All data is synthetic. Option B tokens and style are unchanged.

**Credits.** Scope: Steve. Snapshot approach (fields untouched since the hold apply from the phone, only Mac-edited fields go to Review): Linus. “Can’t tell which is newer” wording for fields with no stamp: Tony. **Storage and sync assumptions below are Steve’s (product) and Linus’s (build) to confirm. This file only draws them.**

## What changed in this update
1. **Session rows** read “Add 30-min session from your phone (18 Nov)” with the button “Add this session”. The Mac’s day total sits beside it as muted context (“Mac’s total for 18 Nov: 20 min”). The row never says “set focus to X”: adding a session replaces no total.
2. **Goal-edit rows use set wording**: “Name: Deep work (Mac has Focus)”, “Time box: 60 min (Mac has 45 min)”.
3. **Two reasons for a field the Mac also has.** With a snapshot (the Mac that held it had #58): “You changed the name on this Mac after this was held”. With no snapshot or no stamp (the holding Mac ran #55 only): “Can’t tell which is newer. Mac has Focus”. The second never claims the Mac edit came later.
4. **Frame 03 is the main frame**: rows grouped by goal, with per-goal “Keep Mac’s version” and “Use phone’s version” (“Add this session” for a goal whose only held change is a session). “Keep Mac’s version for all” is the only bulk action.
5. **Today note is routine housekeeping**: same leaf-wash note, no error colour, “3 phone changes to review” + “Review”.
6. **New frame 11**: the once-only note after the upgrade, “8 phone changes applied, 3 to review”.
7. New frames 12 (empty) and 13 (Undo after “Keep Mac’s version for all”). Notes below cover save timing, failure, Esc, no confirm dialog and the day boundary.

## Frames
| # | File | State |
|---|---|---|
| 1 | `01-today-note-review.png` | Today with the housekeeping note “3 phone changes to review” and the “Review” text link. |
| 2 | `02-sheet-one-entry.png` | The sheet with one held change (goal Focus, snapshot reason). |
| 3 | `03-sheet-many-scrolling.png` | **Main frame.** 9 held changes grouped by goal (session, snapshot and no-stamp reasons, a goal with 2 changes, too-old, unreadable and newer-schema group last). The list scrolls, the footer stays fixed. |
| 4 | `04-undo-keep-mac.png` | After “Keep Mac’s version” on Focus: the group is gone, the count is 2, the Undo toast shows. |
| 5 | `05-undo-use-phone.png` | After “Add this session” on Read one paper: the same layout with the session toast. |
| 6 | `06-last-resolved-note-gone.png` | The last group is resolved with “Use phone’s version”: the sheet has closed, the note is gone, and the Undo toast stays on Today. |
| 7 | `07-loading.png` | The sheet while the held list is being read: skeleton groups and “Reading held changes…”, no choice buttons. |
| 8 | `08-error-still-held.png` | A choice couldn’t be saved. The group is back in its place, still held, with retry copy. |
| 9 | `09-day-boundary-midnight-ist.png` | Sheet left open across midnight IST: Today behind it moved to Sat 28 Nov, the groups, rows, dates and count are unchanged. Has an annotation. |
| 10 | `10-closed-without-action.png` | Closed without choosing: the note shows the same count. Has an annotation. |
| 11 | `11-today-applied-note-once.png` | **New.** Today right after the Mac upgrade: “8 phone changes applied, 3 to review” with “Review” and “Got it”. Has an annotation. |
| 12 | `12-sheet-empty.png` | **New.** Empty state: the sheet is open and the Mac finds nothing held (for example the upgrade applied it meanwhile). “No held changes. Nothing needs your choice right now.” and Close only. |
| 13 | `13-undo-keep-for-all.png` | **New.** After “Keep Mac’s version for all”: one toast for all 7 changes, the unreadable and newer-schema rows stay, the count is 2. |

Annotations (frames 9, 10 and 11, dashed box at top left) are not product UI.

## Copy (exact, curly apostrophes, never “discard”)
| Where | Copy |
|---|---|
| Today note, several | “3 phone changes to review” |
| Today note, one | “1 phone change to review” |
| Note button (text link) | “Review” |
| Once-only note after the upgrade | “8 phone changes applied, 3 to review” + “Review” + “Got it”. With nothing to review: “8 phone changes applied” + “Got it”. |
| Sheet title | “Held changes from your phone” |
| Sheet subtitle, several | “Your Mac didn’t apply these N changes, to avoid overwriting newer edits. Nothing changes until you choose.” |
| Sheet subtitle, one | “Your Mac didn’t apply this change, to avoid overwriting newer edits. Nothing changes until you choose.” |
| Subtitle while loading | “Your Mac didn’t apply some changes from your phone, to avoid overwriting newer edits.” |
| Subtitle when empty | “Nothing from your phone is held right now.” |
| Loading line | “Reading held changes…” |
| Empty state | “No held changes” / “Nothing needs your choice right now.” |
| Group header | Goal name as the Mac has it now (“Focus”), plus “2 changes” when the group has more than one row. |
| Session row | “Add 30-min session from your phone (18 Nov)” · muted “Mac’s total for 18 Nov: 20 min”. Meta: “More than 7 days old”. |
| Goal-edit row (snapshot) | “Name: Deep work (Mac has Focus)”. Meta: “You changed the name on this Mac after this was held”. Time box: “You changed the time box on this Mac after this was held”. |
| Goal-edit row (no snapshot or no stamp) | “Time box: 60 min”. Meta: “Can’t tell which is newer. Mac has 45 min”. Name: “Can’t tell which is newer. Mac has Focus”. The Mac value sits in the meta line here, so it isn’t said twice. |
| Goal-edit and add row (too old) | “Name: Gym, legs day (Mac has Gym)” / “Added to 17 Nov (Mac doesn’t have it)”. Meta: “From your phone on 19 Nov · More than 7 days old”. |
| Group buttons | “Keep Mac’s version” (default, filled) · “Use phone’s version” (outline). A group whose only change is a session: “Add this session” (“Add these sessions” for several). |
| Unreadable group | Header “Can’t be applied on this Mac yet”. Rows: “A change from your phone” / “From your phone on 24 Nov · This Mac can’t read it yet” and “Changes from a newer Cadence on your phone” / “From your phone · Made by a newer version of Cadence”. Line: “Update Cadence on this Mac to apply this.” No buttons. |
| Footer hint | “Closing keeps every change held.” |
| Footer buttons | “Keep Mac’s version for all” (shown only with 2 or more changes you can choose) · “Close” |
| Toast after Keep | “Kept your Mac’s version for Focus.” + “Undo” |
| Toast after Use | “Used your phone’s version for Focus.” + “Undo” |
| Toast after Add this session | “Added the 30-min session to Read one paper.” + “Undo” |
| Toast after Keep for all | “Kept your Mac’s version for 7 changes.” + “Undo” |
| Error in a group | “Couldn’t save your choice, so this change is still held. Check that your OneDrive folder is available.” (“these changes are still held” for a group of 2 or more) + “Try again” |
| Error after “for all” | “Couldn’t save your choice, so all 7 changes are still held. Check that your OneDrive folder is available.” + “Try again” (banner above the list; prototype only, via the demo bar) |

Dates are always absolute (“18 Nov”, IST day of the phone’s stamp), never “yesterday” or “8 days ago”, so nothing in a row changes at midnight.

## VoiceOver labels
| Control | Label (pattern, then example) |
|---|---|
| Review | “Review N held changes” / “Review 1 held change” |
| Keep Mac’s version (group) | “Keep Mac’s version for {goal}: {what it keeps and drops}”. Example: “Keep Mac’s version for Focus: keeps the name Focus and drops the phone’s name Deep work” |
| Use phone’s version (group) | “Use phone’s version for {goal}: {what it sets, replacing the Mac’s value}”. Example: “Use phone’s version for Focus: renames it to Deep work, replacing the Mac’s Focus” |
| Add this session | “Add this session to {goal}: adds a 30-min session on 18 Nov. The Mac’s own sessions stay as they are” |
| Keep Mac’s version for all | “Keep Mac’s version for all N changes you can choose. The phone changes are dropped.” |
| Close and × | “Close. Every change stays held.” |
| Try again | “Try again: ” + the label of the button that failed |
| Got it | “Got it. Hide this note” |
| Undo | “Undo” inside a polite live-region toast that reads the toast sentence first |

Sheet: `role="dialog"`, `aria-modal="true"`, labelled by the title, described by the subtitle. The list is a list (“Held changes, grouped by goal”), each group a list item with its rows as a nested list. Loading sets `aria-busy`. Errors are `role="alert"`. Esc closes. On close, focus goes back to Review.

## Interaction rules
1. The note is housekeeping: leaf-wash, no error colour, one text-link “Review”. It is not a second card. The count is the number of held changes (`heldCount`), the same number as in the sheet subtitle. The note disappears when nothing is held.
2. Review opens the sheet. Held changes are **grouped by goal**; each group has one pair of buttons that applies to every change in that group. Unreadable and newer-schema changes sit in a last group with no buttons and clear by themselves once the Mac is updated.
3. **Set wording only for goal fields.** “Use phone’s version” is Abhishek’s explicit choice: it overwrites only the fields that the held entry changed. A session is never “set”: “Add this session” adds that one session (deduped by id) and replaces no Mac total. The Mac’s day total is shown as context only.
4. “Keep Mac’s version” is the default (filled button, first in tab order) and drops the phone change. The log stores only the entry id, device, date and reason, with no goal names or values (DPDP Act). There is **no history UI**.
5. **No confirm dialog.** A choice removes its group at once and shows a 5-second Undo toast at the bottom centre. A new choice ends the previous toast. Undo puts the group back in its place and the count back.
6. **A choice is saved when the 5-second Undo ends**, not at once. Until then the entry is still held on disk, so quitting the app inside the 5 seconds leaves it held (spec V3).
7. **“Keep Mac’s version for all” is one write**, saved after its Undo ends. It is the only bulk action. It leaves the unreadable and newer-schema changes alone.
8. **A failed save puts the entry back as held**, in its place, with the error and Try again (frame 8). Nothing is dropped and nothing half-applies. For “for all”, every change comes back and one banner above the list says so.
9. **Closing (Close, ×, Esc or a click outside) keeps everything held**, and the note count stays the same (frame 10).
10. When the last change is resolved, the sheet closes and the note disappears. The toast stays on Today, and Undo brings the note back but doesn’t reopen the sheet (frame 6). If only unreadable or newer-schema changes remain, the sheet stays open with them and “Keep Mac’s version for all” is hidden.
11. **Once-only applied note (frame 11).** After the upgrade applies untouched phone edits, the first Today view shows “N phone changes applied, M to review”. The counts are what the upgrade did and never change afterwards (not at midnight, not while the sheet is open). “Review” opens the sheet with exactly M changes. “Review” or “Got it” ends it, and Today then shows the housekeeping note for what is still held. With M = 0 there is no “Review”. With N = 0 this note isn’t shown at all, only the normal note. The counts have to match what actually happened (spec V3 done-when).
12. **Empty state (frame 12).** The sheet is only reachable from the note, but the list can be empty when it opens or while it is open (for example the upgrade applied the change meanwhile). It then says so and offers Close only.

## Day boundary (frame 9, every time-based screen)
A sheet left open across midnight IST keeps its groups, rows, dates and count. Nothing auto-resolves and the 5-second Undo is unaffected. Today behind it moves to the new day as usual and the note stays. Row dates are absolute, so they stay correct. The once-only applied note (frame 11) is not recomputed at midnight. A session row’s “Mac’s total for 18 Nov” is a total for that named day, so it never changes meaning at midnight.

## Tokens used (colours only from `tokens.css` = cadence `web/tokens.css`, then `ios-tokens.css` at 5436723)
- Note (both the routine note and the once-only applied note): `--leaf-wash` background, `--leaf-deep` text. Review and Got it links: `--leaf`. No error colour.
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

- New in this update: goal group header and count (`--text`, `--text-muted`), the thin rule left of each held-change line (`--line`, decorative), the empty-state check (`--text-muted`). No new colour pairs, so the contrast table below still covers everything.

## Assumptions to confirm (Steve: product, Linus: storage and sync)
- The Mac can show the goal name as it has it now, the one field, and the Mac’s current value (or “Mac doesn’t have it”) for each held change.
- The Mac knows, per held field, whether the entry was held with a snapshot (frame “You changed the name on this Mac after this was held”) or without one (“Can’t tell which is newer”). This is a stored reason per field.
- For a held session the Mac can read the Mac’s total for the session’s day.
- For an unreadable entry it can still read the phone’s stamp day. If it can’t, the row drops “on 24 Nov”.
- A newer-schema file is one row with no date, matching `heldCount` counting `schema_held` as 1.
- The applied and to-review counts for the once-only note are recorded by the upgrade itself and survive a crash or reload until the note has been seen.

## Open questions (for Steve’s spec; questions, not decisions)
1. Is the Today note copy “N phone changes to review” the new `syncHeld` note copy? #55’s copy (“N changes from your phone weren’t applied, to avoid overwriting newer edits.”) is already built and tested. The sheet subtitle keeps the longer sentence.
2. Is one choice per goal enough when a goal has several held fields (each group applies to all its rows), or is a choice per field ever needed?
3. Mixed groups: a goal with a held session and a held goal edit. Frames show groups with only one kind. Does “Keep Mac’s version” drop the session too, and what does “Use phone’s version” do with the session?
4. Held removes and restores (Quinn’s case 5) aren’t drawn. What should they say?
5. When does the once-only applied note count as shown: when Today renders it, or when “Review” or “Got it” is used? What if the Mac quits before it is seen?
6. If every phone edit applied and nothing is left to review, is “8 phone changes applied” still wanted as a one-time note?
7. Where can the Mac read the Mac’s total for a past day that the session row shows (“Mac’s total for 18 Nov: 20 min”)?
8. What does “Use phone’s version” do on a day that already has 6 goals (the parked rule, §4.3)?
