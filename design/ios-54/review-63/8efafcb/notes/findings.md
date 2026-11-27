# Findings for 8efafcb (PR #63 recheck)

Head checked: `8efafcb3a8746749c396e5b5f6c69c41fb849d92`, still the PR head when this review was written. Previous Design: changes requested was on `154a9f7`. Diff `154a9f7..8efafcb` touches only `web/review-sheet.js` (`undo()`, three added lines), plus tests, fixtures and a CHANGELOG line. No CSS, tokens or in-app copy. `ios-tokens.css`, `tokens.css`, `review-sheet.css` and `app.css` are identical to `154a9f7`. 108 computed custom properties match.

Ran the Mac app locally from `8efafcb` on synthetic data only (real server in-process, system Chrome via Playwright, 1440×900 at 2×, IST).

Verdict: **Design: pass.**

## Blocking
None.

## What I checked (all confirmed on screen)

1. **Undo of Keep all in 13b.** Focus is on the Keep all button, with a visible 2 px `var(--leaf)` ring (`#1B5E3B` / `rgb(27, 94, 59)`). Groups return to the original order: Focus, Gym, Call the bank. Helper and Keep all are back. On `154a9f7` focus was on the sheet.

2. **Undo after Keep all emptied and closed the sheet.** The sheet reopens exactly as it was (same sheet text, groups Synthetic Focus / weekly review / Gym). Focus is on Keep all, with the same token ring, not on `<body>`. On `154a9f7` the sheet stayed closed and focus fell to `<body>`.

3. **Fallback, when Keep all is not on the sheet.** `mixed()` (one session + one edit, no Keep all). After Undo of Keep on the edit, focus goes to the first choice, **Add this session**, with the token ring. Not the sheet or `<body>`.

4. **Frame 06 is unchanged:** Undo of the last single choice (Use on the only row) leaves the sheet closed. The Review note returns (“1 phone change to review”). After the Use, while the toast is up, focus is on `#view`. After Undo, focus falls to `<body>` even though the Review button is back. See nits.

5. **No regression from `154a9f7`.** After Keep all in 13b, focus still lands on **Add this session** with the token ring; Focus session stays above the add. The 13b-before and 13b-after-Keep-all frames are pixel-identical to `154a9f7`. Helper copy is unchanged: “Keeps your Mac’s version of goal edits. Everything else stays here to choose.” (U+2019, 240 px, two lines, Source Sans 3 600 13 / 17.55).

## Nits

1. **Undo of a single row, while Keep all is on the sheet, also focuses Keep all.** Confirmed on screen: Keep on Gym, then Undo. The Gym row and original order come back, but `document.activeElement` is Keep all, with the token ring, not Gym’s Keep (the restored row’s first choice). Focus is on a sensible, visible control, not `<body>` or off-screen, so this is not a blocker. Keep all focus should be only for Undo of Keep all. `undo()` always sets `focusNext` to Keep all first whenever the sheet is open.

2. **Frame 06 after Undo of the last single choice:** the sheet correctly stays closed and the Review note returns, but focus falls to `<body>` instead of the Review button or `#view`. Pre-existing (the new `undo()` only moves focus when the sheet is open, and only reopens after a bulk Keep all). Not a merge blocker for this SHA.

## Abhishek’s visual OK

Stays a separate merge-time gate (spec §6), queued with Friday. Not part of this review.
