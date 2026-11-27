# Findings for 700445c (PR #63 recheck)

Head checked: `700445c03fffcbb0df6ab2182fa29de7b11c2848`, still the PR head when this review was written. Previous Design: changes requested on `a698fc7` blocked on probe g: Undo in frame 06 with the Review note only scrolled out of view focused the Review button but `preventScroll` left it off screen. Diff `a698fc7..700445c` touches only `web/review-sheet.js` (`focusOpener()`: `scrollIntoView({block:'nearest', behavior:'instant'})`, then a 4px sticky-header clearance, then `focus()` without `preventScroll`; `#view` fallback only when the button is missing or hidden), tests, and a CHANGELOG line. No CSS, tokens or in-app copy. `ios-tokens.css`, `tokens.css`, `review-sheet.css`, `app.css` and `index.html` are identical to `a698fc7` and to `0013b16`. 108 computed custom properties match `0013b16`.

Ran the Mac app locally from `700445c` on synthetic data only (real server in-process, system Chrome via Playwright, 1440×900 at 2×, IST). The scrolled-out case follows Linus’s probe g setup: `.today` is tall, `.lbar` is sticky, the page is scrolled to the bottom before Undo.

Verdict: **Design: pass.**

## Blocking
None.

## What I checked (all confirmed on screen)

1. **Undo in frame 06, Review note scrolled out of view.** Before Undo, scrollY was 3184 and the Review note was not in the viewport. After Undo, `scrollIntoView` was called once on the Review button with `block: 'nearest'` and `behavior: 'instant'` (one scroll event, span 0 ms, scrollY 3184 → 144). The viewport screenshot (not a full-page crop) shows the Review button fully in view, with a visible 2 px `var(--leaf)` ring (`#1B5E3B` / `rgb(27, 94, 59)`, offset 2 px). The whole box is in the viewport (top 87.9, bottom 111.9, viewport 900). The sticky header sits at 0–84 px; the button is not under it. `elementFromPoint` at the button’s centre returns the Review button itself. The sheet stays closed; nothing is written.

2. **In-view frame 06 Undo.** The sheet stays closed, the Review note comes back (“1 phone change to review”), and focus is on the Review button with the same token ring. Pixel-identical to `a698fc7`. Versus `0013b16` (focus on `<body>`), the only difference is the ring (1,450 px / 0.028%).

3. **Hidden-button fallback.** With `display: none` on the Review button, Undo leaves the sheet closed, the note comes back, and focus is on `#view`, not `<body>`. `#view` still has `outline: none` (existing nit, below). Pixel-identical to `a698fc7`.

4. **IST midnight.** Reproduced: sheet opened at 23:58 IST on Thursday 26 Nov, clock advanced to 00:04 on Friday 27 Nov. Use then Undo: the sheet stays closed, nothing is written, focus is on the Review button with the token ring. The Review note itself is unchanged. Pixel-identical to `a698fc7`.

5. **Earlier paths unchanged versus `0013b16`.** Single-row Undo still focuses the restored row’s first choice (Gym’s Keep, token ring). Undo of Keep all still focuses Keep all, original order restored. Emptied-sheet Undo still reopens the sheet with focus on Keep all. Keep all that leaves nothing still focuses `#view`. All of those frames, plus 13b before/after Keep all, fallback Undo, and Linus’s mix, are pixel-identical to `0013b16`. Helper copy is unchanged: “Keeps your Mac’s version of goal edits. Everything else stays here to choose.” (U+2019, 240 px, two lines, Source Sans 3 600 13 / 17.55).

6. **No CSS, token or copy drift, and no writes.** Diff `a698fc7..700445c` is `focusOpener()` in `web/review-sheet.js`, tests, and a CHANGELOG line. 108 computed custom properties match `0013b16`. No `/api/held/resolve` posts on any of these paths.

## Nits
When focus correctly falls back to `#view` (hidden Review button, or Keep all that leaves nothing), `#view` shows no visible focus indicator. This is existing `outline: none` on `.view` in `app.css`, carried over from the `a698fc7` review. Not a merge blocker for this SHA.

## Abhishek’s visual OK

Stays a separate merge-time gate (spec §6), queued with Friday. Not part of this review.
