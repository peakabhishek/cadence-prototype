# Findings for a698fc7 (PR #63 recheck)

Head checked: `a698fc756f0f86055c88b01fe07c565bb0e5486f`, still the PR head when this review was written. Previous Design: pass on `0013b16` had a pre-existing nit: Undo of the last single choice in frame 06 left the sheet closed (correct) but sent focus to `<body>`. Diff `0013b16..a698fc7` touches only `web/review-sheet.js` (`undo()` now calls `focusOpener()` when the sheet stays closed; `focusOpener()` skips a hidden Review button and falls back to `#view`), tests, and a CHANGELOG line. No CSS, tokens or in-app copy. `ios-tokens.css`, `tokens.css`, `review-sheet.css`, `app.css` and `index.html` are identical to `0013b16`. 108 computed custom properties match.

Ran the Mac app locally from `a698fc7` on synthetic data only (real server in-process, system Chrome via Playwright, 1440×900 at 2×, IST).

Verdict: **Design: changes requested.**

## Blocking

**Undo in frame 06, when the Review note is only scrolled out of view, focuses the Review button but leaves it off screen.** `focusOpener()` treats a scrolled-out Review button as on screen (it still has a box) and then calls `focus({ preventScroll: true })`, so the page does not scroll it into view. Confirmed on screen: after Use, the page was scrolled down (scrollY 1600, the note’s restored position is near y=220); after Undo, focus is the Review button (`data-act="review"`, 2 px `var(--leaf)` ring in computed style), the sheet stays closed and the note is back, but the viewport is still the empty scrolled-down wash. The focused control is only visible in a full-page crop of the top of the document, not in what the person sees. Focus on an invisible control. Never `<body>`, but not a defined visible target either.

The agreed rule: after Undo in frame 06 the sheet stays closed; focus goes to the Review button; if that button is hidden or off screen, to `#view`; never `<body>`. For this target, drop `preventScroll`, and scroll it in with `block: 'nearest'`, instant (no smooth scroll), clearing any sticky header. This review is for `a698fc7` only; the next SHA should be rechecked.

## What I checked (confirmed on screen)

1. **Frame 06 Undo, Review button in view.** After Undo of the last single Use, the sheet stays closed, the Review note comes back (“1 phone change to review”), and focus is on the Review button with a visible 2 px `var(--leaf)` ring (`#1B5E3B` / `rgb(27, 94, 59)`). On `0013b16` focus was on `<body>`. That frame differs from `0013b16` by 1,450 px (0.028%), the ring.

2. **Fallback, when the Review button is hidden.** With `display: none` on the Review button (Linus’s hidden-button test), Undo leaves the sheet closed, the note comes back, and focus is on `#view`, not `<body>`. `#view` has `outline: none` (existing in `app.css`), so there is no visible focus indicator. Nit, below.

3. **IST midnight.** Reproduced: sheet opened at 23:58 IST on Thursday 26 Nov, clock advanced to 00:04 on Friday 27 Nov (header date updates, Today behind the sheet shows the new day’s fresh list). Use then Undo: the sheet stays closed, nothing is written (no `/api/held/resolve` post), focus is on the Review button with the token ring. The Review note itself is unchanged (“1 phone change to review”).

4. **Frame 06 stays closed, Review note visually unchanged.** After the ordinary Undo, the note returns in the same place and wording as before the Use; only the focus ring is new versus `0013b16`. After Use, and after an emptying Keep all, the frames are pixel-identical to `0013b16`.

5. **Earlier paths unchanged versus `0013b16`.** Single-row Undo still focuses the restored row’s first choice (Gym’s Keep, token ring). Undo of Keep all still focuses Keep all, original order restored. Emptied-sheet Undo still reopens the sheet with focus on Keep all. Keep all that leaves nothing still focuses `#view`. All of those frames, plus 13b before/after Keep all, fallback Undo, and Linus’s mix, are pixel-identical to `0013b16`. Helper copy is unchanged: “Keeps your Mac’s version of goal edits. Everything else stays here to choose.” (U+2019, 240 px, two lines, Source Sans 3 600 13 / 17.55).

6. **No CSS, token or copy drift.** Diff `0013b16..a698fc7` is `undo()` / `focusOpener()` in `web/review-sheet.js`, tests, and a CHANGELOG line. 108 computed custom properties match.

## Nits

When focus correctly falls back to `#view` (hidden Review button, or Keep all that leaves nothing), `#view` shows no visible focus indicator. This is existing `outline: none` on `.view` in `app.css`, not introduced here. Not a merge blocker for the scrolled-out fix, but there is no on-screen cue that the page has a defined target.

## Abhishek’s visual OK

Stays a separate merge-time gate (spec §6), queued with Friday. Not part of this review.
