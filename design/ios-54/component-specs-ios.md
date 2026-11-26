# Cadence for iPhone — component specs, Option B “Windowsill, native iOS” (cadence#54)

> **PROVISIONAL until Abhishek approves the iPhone visual direction.** Written so the Capacitor build can start now (Abhishek, 26 Nov: "Mock any dependencies on me. Move forward."). Tokens: `ios-tokens.css`, which loads after `tokens.css` (handoff, unchanged). Fake data only in every mock and test.

Frames for every component: `frames/B/*.png` (390×844 @2x). Board: `boards/B-windowsill-native.png`.

**Spec assumptions (Steve, 26 Nov; not decided by Design):** the phone shares the Mac’s goals (same IST day, same 6-goal limit). Adding and ticking goals works offline and syncs later. A goal can be edited on both devices. No notifications, widgets or Live Activities in v1. v1 is today’s goals plus focus sessions, for Abhishek only. Merge rule over 6 goals: pinned at [#54 comment 7196971740](https://github.com/peakabhishek/cadence/issues/54#issuecomment-7196971740).

---

## 0. Demo-mode banner
- **When:** only while the mock storage adapter is active, controlled by the same config flag. Never in a real-storage build.
- **Anatomy:** a thin full-width strip directly below the status bar, inside the top safe area (`top: var(--ios-safe-top)`), height `--banner-demo-h` (24px). Background `--banner-demo-bg` #F6D9A8, text `--banner-demo-text` #5A3A12 (7.52:1, AA), `--ios-footnote` 600, centred. Content below moves down by 24px (it never overlaps the nav bar).
- **Copy, exactly:** “Demo data, not synced”
- **Behaviour:** on every screen, including sheets, focus and errors. No close button, no swipe-away. VoiceOver reads it once per screen as static text.

## 1. Tab bar and nav bar
- **Tab bar:** two tabs, **Today** (list icon) and **Focus** (timer icon). Height `--ios-tabbar-h` + `--ios-safe-bottom`. Background `--ios-tabbar-bg` with `backdrop-filter: blur(var(--ios-tabbar-blur))`, top hairline `--ios-separator`. Selected: `--ios-tint`, filled icon. Idle: `--ios-label-2`, outline icon. Labels `--ios-caption2`. No Week tab in v1.
- **Nav bar:** 44px. Large title (“Today”, `--ios-large-title`, tracking `--ios-tracking-tight`) under it, left-aligned, 16px margin. Under the title: the date and the sync status (§7) on one line, `--ios-subhead` `--ios-label-2`. Right: a 32px `--ios-tint-wash` circle with a plus (Add goal). The large title collapses to a 17px centred title on scroll.
- The tab bar hides during a running focus session and on full-screen errors.

## 2. Today’s goal list
- Inset grouped section, 16px side margins, `--ios-r-cell-group`, `--ios-cell` fill.
- Section header: “GOALS” left and “4 of 6” right, `--ios-footnote` uppercase `--ios-label-2`.
- Above the goals: the **plant card** (120px, `--ios-plant-card`, radius 12px) with today’s money plant (shipped `web/plants/*.svg`, stage from finished minutes) and the tally “2 plants · 1h 10m” (`--ios-title2`) plus “Focused today”.
- The last row in the section is **Add goal** (plus icon + label in `--ios-tint`). At 6 goals it is replaced by the line “Six goals — plenty for one day.” in `--ios-label-2`.
- Primary button “Start focusing” sits above the tab bar: full width minus 32px, `--ios-button-h`, `--ios-r-button`, `--ios-tint` / `--ios-on-tint`.

## 3. Goal row
- Min height `--ios-cell-min-h`. Left: tick (`--ios-tick`, 1.8px ring `--ios-label-2`; ticked = filled `--ios-tint` with `--ios-on-tint` check). Title `--ios-body`, one line, ellipsis. Right: detail `--ios-subhead` `--ios-label-2`: “30 / 45 min”, “Not yet” (no time box), or “Add time box” in `--ios-tint`.
- Separator inset `--ios-separator-inset`.
- Swipe left: **Remove** (in `--ios-warn-ink` on `--ios-warn-bg`, not system red). Removing shows the shipped inline line “Removed <goal>. Undo”.
- **Not synced yet** marker: a 14px cloud-slash icon after the title, `--ios-label-2`, when the row has changes queued offline.
- Tick vs the “hit” rule (finished minutes reach the box): open question for the spec. Mocks show a ticked row = hit.

## 4. Add-goal sheet
- System-style sheet from the bottom, `--ios-r-sheet` top corners, grabber 36×5 `--ios-grabber`, background `--ios-sheet-bg`. Nav row: “Cancel” (left, `--ios-tint`), “New goal” (`--ios-headline`), “Add” (right, `--ios-headline` `--ios-tint`; greyed `--ios-label-2` until there is a title).
- Fields: title (placeholder “What matters today?”), then “Time box” row with “None” / minutes value and a chevron.
- Keyboard up on open; the sheet sits on the keyboard (fixed to its top edge). Return key label “add”.
- **At 6 goals:** the Add button stays enabled; tapping it keeps the text and shows, under the field, exactly: “Today already has 6 goals. Remove one to add this.” in `--ios-warn-ink`. Nothing is added.

## 5. Parked group and Move in
Rule: [#54 comment 7196971740](https://github.com/peakabhishek/cadence/issues/54#issuecomment-7196971740) (final).
- **Note** (info banner at the top of Today, `--ios-tint-wash` / `--ios-tint-strong`), exactly: “1 goal didn’t fit today’s 6. It’s in Parked.” / plural: “2 goals didn’t fit today’s 6. They’re in Parked.”
- **Parked section:** its own inset grouped section under the goals, header “PARKED”. Rows show the title, a muted “From your phone · 9:12 PM” style source line, and a **Move in** button (small tinted capsule).
- **Move in disabled** while the day has 6 goals: capsule in `--ios-fill` with `--ios-label-2` text (still 4.5:1+), `aria-disabled="true"`, and a hint under the section: “Remove one of today’s goals first.” (`--ios-footnote`, `--ios-label-2`).
- **Move in enabled** as soon as the day has fewer than 6: capsule `--ios-tint` / `--ios-on-tint`; the hint disappears.
- After **Move in** the goal joins the list at the end; the Parked section disappears when empty. Parked goals never move in on their own.
- **Past days:** Parked rows are read-only, no Move in.
- **Displaced goal** (frame labelled *only if Steve keeps first-6-by-save-time*): when a phone goal with an earlier save time syncs in and pushes a visible goal out, the note reads exactly “A goal synced from your phone took this spot. Yours is in Parked.”
- Parked goals don’t count toward the day, the week or Friday’s `weeks` data; the “4 of 6” counter ignores them.

## 6. Focus session timer
- Full screen, tab bar hidden. Eyebrow “FOCUSING ON” (`--ios-footnote` 600 `--ios-label-2`), goal title `--ios-title2`.
- Plant on the sill (shipped SVG, growing stage), glow `--ios-glow` behind it.
- Timer `--ios-timer` in `--ios-tint-strong`, `font-variant-numeric: tabular-nums`. Under it: “remaining of 50:00 · ends 10:30 PM”, `--ios-subhead`.
- Progress bar 6px, `--ios-fill` track, `--ios-tint` fill.
- **Give up**: outline capsule, label `--ios-warn-ink`. Only Give up withers a plant.
- What happens on screen lock / app switch is a spec question (the Mac’s 10-minute sleep rule); the mock note “Your session keeps counting if you switch apps.” is placeholder copy.

## 7. Sync status (depends on sync decision)
- One line under the large title: synced = check icon + “Last synced 9:40 PM”; syncing = rotating sync icon + “Syncing…”; offline = cloud-slash + “Offline”; failed = alert icon + “Not synced” in `--ios-warn-ink`.
- Tapping the line opens a small **Sync sheet**: device rows (“This iPhone”, “MacBook”), “Last synced 9:40 PM”, queued changes (“2 changes waiting”), and “Sync now”.
- **Offline banner** (info): “You’re offline. Changes stay on this phone and sync when you’re back.”
- **Sync failed banner** (warn): title “Couldn’t sync.” body “Your changes are safe on this phone.” action “Try again”.
- **Edited on both devices** (conflict) sheet: title “Edited on both devices”, body “Nothing is lost. Choose which version to keep.” Two cards, **On your Mac** (time) and **On this iPhone** (time, “made offline”), each with its title and time box; buttons “Keep Mac version” / “Keep iPhone version”, and “Decide later” text button. Until chosen the row shows the iPhone version with a small “2 versions” chip in `--ios-warn-ink`.

## 8. First-run sign-in — **MOCKED**
- **MOCKED:** the real Microsoft sign-in comes later. In the mock adapter the button goes straight to Today with demo data, and the demo banner shows.
- Plant (empty pot) on the sill, title “Grow a plant for every focus session.” (`--ios-title1`), body “Sign in with the Microsoft account that holds your Cadence folder, so this iPhone shares today’s goals with your Mac.” Button “Sign in with Microsoft” (primary), text button “Try with demo data”. Footnote: “Cadence reads and writes one file in your OneDrive folder. Nothing else.”

## 9. Sign-in expired
- Warn banner at the top of Today, not a blocking screen: title “Sign in again to sync.” body “Your Microsoft sign-in expired. Your changes are safe on this phone.” action “Sign in”. Sync status line shows “Not synced”. Work continues offline-style.

## 10. Empty, loading and error states
- **Empty (signed in, no goals today):** plant card with the empty pot and “No plants yet today”, goals section with only **Add goal**, and the hint “Up to 6 goals a day. Focus on one and a money plant grows. Only Give up withers it.”
- **Loading:** large title and date render at once; plant card and 4 rows are skeletons (`--ios-fill`, 8px radius, gentle shimmer, no spinner). “Start focusing” disabled.
- **Error (nothing cached, can’t load):** centred in the content area: cloud-slash icon in a 56px `--ios-tint-wash` circle, title “We couldn’t load today.” (`--ios-title3`), body “Cadence couldn’t reach your goals. Nothing has been lost.”, primary “Try again”. Tab bar stays.
- **Day boundary:** a session that started before midnight IST and ends after it counts for the day it started. End screen: “Grew.” (`--ios-end-title`), meta “Started 11:50 PM Thursday · ended 12:30 AM”, info note “It’s Friday now. Today starts with a fresh list.”, buttons “See Thursday’s grove” (primary) and “Go to today” (outline). An app left open overnight rolls to the new day silently once no session is running; drafts keep their text.

## 11. Capacitor wrapper vs native Swift — where they differ
Both are installable (local Xcode build for v1; TestFlight blocked while the Apple Developer account is on hold). The design works for both; these are the build differences:

| Area | Capacitor wrapper | Native Swift |
|---|---|---|
| Keyboard | WKWebView resizes or pans; use `@capacitor/keyboard` (`resize: native`) and pin the sheet to `keyboardWillShow` height. Hide the form accessory bar (`Keyboard.setAccessoryBarVisible(false)`). | Sheet follows the keyboard via `safeAreaInset`/keyboard layout guide; no accessory bar. |
| Status bar and safe areas | `viewport-fit=cover` + `env(safe-area-inset-*)`; status bar style set by `@capacitor/status-bar` (dark text on light). | Safe areas are automatic; `preferredStatusBarStyle`. |
| Haptics | Optional via `@capacitor/haptics` (light tap on tick and Move in, success on Grew). Design never relies on them. | `UIImpactFeedbackGenerator` / `.sensoryFeedback`. Same moments. |
| System sheets | Sheets are drawn in HTML to match iOS (grabber, 12px corners, swipe down to close). Detents are emulated. | Real `.sheet` with `.presentationDetents`. |
| Type | `-apple-system` gives SF Pro; Dynamic Type via `font: -apple-system-body` keywords or a native plugin reading the content size. | `UIFont.preferredFont` / `.font(.body)`; Fraunces registered as a custom font with `UIFontMetrics` scaling. |
| Blur tab bar | `backdrop-filter` (supported in WKWebView). | `UITabBar` standard appearance. |
| Swipe to remove | Custom gesture in the web layer. | `swipeActions`. |
