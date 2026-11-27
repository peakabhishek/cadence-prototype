# Findings for 154a9f7 (PR #63)

Head checked: `154a9f70e2c9920e017f97d1144472d1c32a9a70`, still the PR head when this review was written. Stacked on #61 at `ac4e8d6bd496f1d8e93b1cefa89a40653de15727`. This review applies only to `154a9f7`; a later SHA with the Undo-focus fix will be rechecked separately.

Ran the Mac app locally from both SHAs on synthetic data only (real server in-process, system Chrome via Playwright, 1440×900 at 2×, IST). No real names or personal data.

Verdict: **Design: changes requested.**

## Blocking

1. **After Undo of Keep all, focus must return to the Keep all button.** If Keep all is not visible, it falls back to the first leftover choice button. On `154a9f7`, in the 13b case, Undo restores the original rows and order (Focus, Gym, Call the bank) and Keep all is visible again, but `document.activeElement` is the sheet container (`.sheet`, tabindex -1, outline none). Confirmed on screen; no focus ring on Keep all. The after-Undo frame is pixel-identical to the sheet before Keep all. Same behaviour Quinn reported.

2. **When Keep all leaves nothing, Undo does not reopen the sheet.** After Keep all on three goal edits, the sheet closes and focus correctly goes to `#view` (not `<body>`), with the Undo toast visible. After Undo, the Review note returns (“3 phone changes to review”) and nothing was written, but the sheet stays closed and focus falls to `<body>`. There is then no Keep all or choice button to land on. Confirmed on screen. Pre-existing on `ac4e8d6`. The next SHA should cover this as well as (1).

## The two #62 nits (both pass on 154a9f7)

- **Focus after Keep all.** In 13b, keyboard Keep all lands on **Add this session** (`data-act="add"`, `data-id="phone-r3:4"`). The ring is `2px solid var(--leaf)` (`#1B5E3B` / `rgb(27, 94, 59)`), outline-offset 2px. On `ac4e8d6` it landed on the sheet.
- **Group order in 13b.** After Keep all, groups stay `[x1 Focus (Add this session), n1 Call the bank]`. The Focus session stays above the add. On `ac4e8d6` the add jumped above Focus (`[n1, x1]`).

## Unchanged

- Helper copy, exactly: “Keeps your Mac’s version of goal edits. Everything else stays here to choose.” Apostrophe is U+2019. 240 px wide, two lines (35.1 px, Source Sans 3 600 13 / 17.55). Hidden after Keep all, when Keep all itself is gone.
- No token drift. `ios-tokens.css`, `tokens.css` and `review-sheet.css` are identical to `ac4e8d6`. 108 computed custom properties match. The only `web/` change on the PR is `review-sheet.js`.
- Before Keep all, the 13b sheet is pixel-identical on both SHAs.

## Quinn’s other #62 cases checked on screen

- **Keep all leaves nothing:** the sheet closes; focus goes to `#view` (`<main id="view" tabindex="-1">`), not `<body>`. The Review note is gone, so there is no empty-state heading or close/done control. `#view` is the defined target for that post-resolve state. The ring is hidden (`#view` has `outline: none`), which is existing Today behaviour, not a new issue.
- **Reload while Undo is pending:** no `POST /api/held/resolve` before or after the reload. The Today note still says “4 phone changes to review”. Reopening the sheet shows all four rows in the original order (Focus, Gym, Call the bank). Pass.

## Linus’s `docs/screens/issue-62/` shots

- `after-keep-all-focus-first-leftover.png` is pixel-identical to this run’s keyboard Keep-all shot (Synthetic names).
- `13b-keep-for-all-leaves-the-add-and-session-held.png` matches this run after the toast ends except 4,876 pixels (0.09%) on the Add this session button: this run still shows the `:focus-visible` ring; his shot is after the toast ends without that ring. Group order matches. The retake in `docs/screens/issue-58-review-sheet/` is pixel-identical to the issue-62 13b shot.

## Abhishek’s visual OK

Stays a separate merge-time gate (spec §6), queued with Friday. Not part of this review.
