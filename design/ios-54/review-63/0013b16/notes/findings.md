# Findings for 0013b16 (PR #63 recheck)

Head checked: `0013b163f583d4ac011fc06232088aed684a4025`, still the PR head when this review was written. Previous Design: pass on `8efafcb` had a non-blocking nit: Undo of a single row focused Keep all. Diff `8efafcb..0013b16` touches only `web/review-sheet.js` (`undo()`), tests, and a CHANGELOG line. No CSS, tokens or in-app copy. `ios-tokens.css`, `tokens.css`, `review-sheet.css` and `app.css` are identical to `8efafcb`. 108 computed custom properties match.

Ran the Mac app locally from `0013b16` on synthetic data only (real server in-process, system Chrome via Playwright, 1440×900 at 2×, IST).

Verdict: **Design: pass.**

## Blocking
None.

## What I checked (all confirmed on screen)

1. **Single-row Undo, Keep all still on the sheet.** Keep on Gym, then Undo. Focus is on Gym’s Keep (`data-act="keep"`, `data-key="x2"`), with a visible 2 px `var(--leaf)` ring (`#1B5E3B` / `rgb(27, 94, 59)`). Keep all is visible but not focused. On `8efafcb` focus was on Keep all.

2. **Undo of Keep all in 13b.** Focus is still on the Keep all button, same token ring. Groups return to the original order: Focus, Gym, Call the bank. Pixel-identical to `8efafcb`.

3. **Undo after Keep all emptied and closed the sheet.** The sheet reopens exactly as it was (same sheet text, groups Synthetic Focus / weekly review / Gym). Focus is on Keep all, not `<body>`. Pixel-identical to `8efafcb`.

4. **Fallback, when Keep all is not on the sheet.** `mixed()` (one session + one edit). After Undo of Keep on the edit, focus goes to that restored row’s first choice, **Keep Mac’s version** (`data-key="g1"`), with the token ring. On `8efafcb` it landed on Add this session (first choice in the group, not the restored row).

5. **Frame 06 is unchanged:** Undo of the last single choice leaves the sheet closed and brings the Review note back. After Undo, focus still falls to `<body>`. Pixel-identical to `8efafcb`. Pre-existing nit only; not a merge blocker for this SHA.

6. **No regression from `8efafcb`.** After Keep all, focus still lands on **Add this session**; Focus session stays above the add. Those frames, the Keep-all Undo frames, and the emptying-Keep-all Undo frames are pixel-identical. Helper copy is unchanged: “Keeps your Mac’s version of goal edits. Everything else stays here to choose.” (U+2019, 240 px, two lines, Source Sans 3 600 13 / 17.55).

## Nits
None new. The frame 06 `<body>` focus after Undo of the last single choice is the same pre-existing nit noted on `8efafcb`.

## Abhishek’s visual OK

Stays a separate merge-time gate (spec §6), queued with Friday. Not part of this review.
