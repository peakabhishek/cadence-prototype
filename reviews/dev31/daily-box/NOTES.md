# DEV-31 daily time box — Design mocks

19 Nov 2026. Hi-fi mocks from the approved 7b6482d build, 1280×800 @2x, Asia/Kolkata, existing tokens only.

Abhishek decided (relayed by Jeff in Dev Team, 5:19 PM IST) that time boxes are daily. One Hit / Missed rule everywhere: a boxed goal is Hit only when that day's finished minutes reach the box; with no box, it is Hit when one session finishes that day. "Not yet" is only on today's row, never on a past day.

## Screens

- `l0d-daily-box-carry.png` — empty Wednesday morning. Carry-over row for a boxed miss: "Missed · 25m of 1h". Field label "Time box · optional" with helper "Per day".
- `l1d-daily-box-after-carry.png` — after the carry-over tap. Same label and helper; "Today so far · Wednesday" shows "0m / 1h box".
- `l8d-daily-box-week.png` — Week by day. Tuesday: "1h 15m / 1h · Hit", "25m · Hit" (no box), "25m / 1h · Missed". Today: "25m / 1h · Not yet". Hero: "2 of 4 daily goals hit".

All text colours used here pass WCAG AA against their backgrounds (--text-muted 7.49:1 on --surface, --wither-ink 7.46:1 on --surface and 6.26:1 on --wither-bg, --on-leaf 6.85:1 on --leaf).
