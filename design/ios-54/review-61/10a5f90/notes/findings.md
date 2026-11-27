# Findings for 10a5f90 (do not post the GitHub review yet)

Head checked at the end of this recheck: `10a5f90e0b9f2a5b5ce1b970bffb77b11fff9ba7`, still the PR head, draft=false.

## The six nits (all fixed on the screen)
1. `.foot-help` is `calc(var(--s-8) * 5)` = 240 px. “Sessions stay here until you add them.” is one line (213 px). No orphaned “them.”
2. Button side padding is 18 px (`calc(var(--s-4) + 2px)`). Keep / Use widths are within ~1 px of the prototype (162.6 vs 161.3).
3. “Try again” is 32 px tall (`height: var(--s-6)`). Error line padding matches the prototype (10 px 12 px).
4. Group heights are within 1 px of the prototype (e.g. 158.8 vs 158.2). The earlier ~10 px gap is gone. The 32 px title still makes the header 4 px taller, as accepted on 011eb14.
5. Linus’s shots in `docs/screens/issue-58-review-sheet/` are 2× (2880×1800). Frame 10 is the closed Today (`10-closed-without-action.png`). The old misnamed open shot is gone; the open-before-close shot is `10a-sheet-open-before-closing.png`.
6. After Keep from the keyboard, focus moves to the next row’s Keep button (Write the weekly review). See `after/focus-after-keep.png`.

## Frame 13 and 13b
Keep for all resolves goal edits only (server: `op == "edit_goal"`). Held adds, sessions, removes, restores and unreadable rows stay, with their own buttons.

- Frame 13 vs the approved frame: the leftover add (“Call the bank”) now stays, with Keep and Use, in its original place in the list. The session, unreadable and newer-schema rows stay. The heading and note update to 4. The bulk button goes. The toast is “Kept your Mac’s version for 5 goal edits.” (Linus’s fixture has 4; data only). This is the intended change from the approved frame, where the add was included in for all (count 3, toast “6 goal edits”).
- 13b (edits + add + session, then Keep for all): the add keeps Keep and Use, the session keeps Add this session, the heading and note go from 4 to 2, the bulk button goes, the toast is “Kept your Mac’s version for 2 goal edits.” Linus’s 13b matches (Synthetic names; his shot is after the toast ends).
- After Keep for all, focus lands on the sheet itself, not the first leftover button. Predictable, one Tab reaches the close control then the leftover rows. Nit, not a blocker.
- In 13b the Focus session group was first (grouped with its edit) and drops below the add once the edit is gone, because group order follows the first remaining row in the list. Frame 13 does not jump (the session is already first in the list). Nit: leave groups in place.

Held removes can appear (frame 15, own Keep goal / Remove goal buttons). Keep for all does not resolve them. The settled helper, “Everything else stays here…”, covers adds, sessions, removes and restores without listing them.

## Helper copy (waiting on Linus’s copy-only commit)
Still on this SHA: “Sessions stay here until you add them.” That sentence is now wrong.

Measured in the real sheet (Source Sans 3, 600, 13 px / 17.55 px, max-width 240 px):
- “Keeps your Mac’s version of goal edits. Everything else stays here to choose one by one.” → 3 lines (52.6 px).
- “Keeps your Mac’s version of goal edits. Everything else stays here to choose.” → 2 lines (35.1 px).

Use the shorter line. (Curly apostrophe in “Mac’s”.)

Same-commit follow-ups, if he can:
- The helper only renders when a session is still in the sheet (`hasSession`). With the new copy, show it whenever Keep for all is visible and something would be left (add, session, remove, restore, or unreadable).
- The button’s aria-label still ends “Sessions stay held until you add them.”
- The bulk save-error banner still ends “Sessions were not changed.”

## 07b
Matches look B: “Couldn’t read the held changes. Check that your OneDrive folder is available.”, “Nothing has changed.”, Try again, `--wither-bg` / `--wither-ink`. Linus’s 07b matches (Synthetic names only).

## Contrast and tokens
No contrast below AA (lowest 6.26:1). `review-sheet.css` still tokens-only for colour. Spacing literals are the prototype’s 14 / 6 / 2 / 6 / 10 px, written as a scale step + 2 px.

## Suggested GitHub review (post only on the copy-only SHA, once it lands)
If the helper, and ideally the aria-label and bulk-error line, use the two-line copy above, start: “Design: pass on &lt;sha&gt;”. Blocking: none. Nits: helper visibility when there is no session; group order after Keep for all in 13b; focus after Keep for all lands on the sheet. Link screenshots from this folder and any new frame-13 shot he adds.
If the helper is still the sessions-only sentence, start: “Design: changes requested on &lt;sha&gt;”. Blocking: the helper sentence is still wrong; use “Keeps your Mac’s version of goal edits. Everything else stays here to choose.”
