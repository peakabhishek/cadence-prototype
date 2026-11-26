# Tick as a derived Hit mark (Q6)

Steve, 27 Nov 2026. v1 has no manual tick. The tick only shows the derived `hit` status: finished focus minutes compared with the time box, which is the Mac’s rule. Tapping the tick does nothing. Tapping the goal opens Focus. Nothing about the tick syncs, and the tick never carries a not-synced marker.

## Status mark, not a control

- **Hit:** a filled `--ios-tint` (`#1B5E3B`, the tick token in `ios-tokens.css`) circle with a `--ios-on-tint` check.
- **Not hit:** an empty `--ios-label-2` (`#5C5146`) ring, 1.8px, 24px (`--ios-tick`).
- No hover, pressed or focus style on the mark itself, and no button chrome (no shadow, no fill well).
- Palette `--accent` (`#C45C2A`, terracotta) is decorative and is not used for the tick.

## Contrast (WCAG 2.x non-text, 3:1)

Checked with `design/ios-54/src/palettes.py` (`ratio()`), option B:

| Part | Foreground | Background | Ratio | Need | Result |
|---|---|---|---|---|---|
| Empty ring on cell | `#5C5146` (`--ios-label-2`) | `#FFFBF6` (`--ios-cell`) | 7.49:1 | 3:1 | PASS |
| Empty ring on page | `#5C5146` | `#F7F0E6` (`--ios-bg`) | 6.82:1 | 3:1 | PASS |
| Filled tick on cell | `#1B5E3B` (`--ios-tint`) | `#FFFBF6` | 7.52:1 | 3:1 | PASS |
| Check on filled tick | `#F7F0E6` (`--ios-on-tint`) | `#1B5E3B` | 6.85:1 | 3:1 | PASS |

## Sync markers stay in the row’s trailing slot

The tick itself never shows a sync icon. A row whose sessions or edits have not been merged by the Mac keeps a marker in the trailing slot, after the time detail:

- **Queued on the phone** (not yet uploaded), including offline, queued, sync failed, and syncHeld: the held / not-synced cloud-slash icon. `aria-label`: “Changes not synced, saved on this phone”.
- **Uploaded, but the Mac’s `lastAppliedSeq` does not cover it yet:** the waiting laptop icon, the same mark as frame 20’s “Waiting for your Mac” status line.

The waiting marker clears by itself once the Mac applies the change, even when that happens the next day.

Frame 21’s Hit row (“Read one paper”) shows the waiting laptop, so a Hit + waiting example sits in the 07 / 19 / 21 set. Frame 20 uses the same trailing waiting mark on that Hit row. Frames 07 and 19 keep the held / not-synced icon on the queued Hit row and on “Call the bank”.

## Accessibility

The tick is not a button and is not in the tab or swipe order as a control. VoiceOver reads it as part of the row label, not as a separate checkbox.

- Hit, with a time box: “Read one paper, 30 of 30 minutes, hit”
- Not hit, with a time box: “Write the weekly review, 30 of 45 minutes”
- Short forms of the same pattern, as agreed: “Read, 30 of 30 minutes, hit” and “Read, 10 of 30 minutes”
- No time box: “Gym, Not yet”

If the row also has a trailing sync marker, that phrase is appended: “Changes not synced, saved on this phone” or “Waiting for your Mac”.

## Frames updated

Every B frame that shows a tick was checked. These change visually (trailing-slot move, or a waiting mark added):

- 07-offline, 11-sync-failed, 13-parked-a-before-sync, 19-sync-queued, 20-waiting-for-mac, 21-mac-needs-update, 24-sync-held

These show ticks but already had no row sync mark on the tick, so the mark stays a status ring with no hover or press style: 01-today, 03-add-goal, 04-six-goal-limit, 06-loading (skeleton rings), 10-sync-status, 12-conflict, 14-parked-b-moving, 15-parked-c-move-in-disabled, 16-parked-d-move-in-enabled, 17-parked-e-moved-in, 18-sign-in-expired, 22-not-ist-hint, 23-phone-clock-off.

No ticks: 02-focus, 05-empty-first-run, 08-error, 09-day-boundary.
