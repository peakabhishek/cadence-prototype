# DEV-31 daily-goals mocks (Iris, 19 Nov 2026)

Example data is the reported bug: Tuesday 17 Nov (Write the chapter 1h box, 1h 15m, hit; Gym, no box, 50m, hit; Read one paper 2h box, 0m, missed) and Wednesday 18 Nov morning.

## Screens

1. [l0d-new-day-carry.png](l0d-new-day-carry.png) — New day, empty goals screen, with a one-tap carry-over offer for yesterday’s unmet goal. Tuesday is not shown as today’s list. A quiet “Start fresh instead” is available.
2. [l1d-after-carry.png](l1d-after-carry.png) — After the tap: “Read one paper” is a new goal for today, at 0m, with its box copied. Copy notes that Tuesday is unchanged.
3. [l8d-week-by-day.png](l8d-week-by-day.png) — Week view with each day’s own goals. Tuesday’s miss stays visible at 0m / 2h. Wednesday is empty. Past days do not change.

HTML sources (to re-shoot at 1440×900, 2×) are in `html/`. Same PNGs are also in `design/dev-31/`.

## Sign-off withheld

These mocks cover the empty morning screen, the carry-over tap, and the daily Week view, and I am happy with that UX for **daily goal lists**. I have not written a Design sign-off in the spec or on DEV-31, because a spec rule conflicts with already-approved UX:

- The Daily goals section (Steve’s 18 Nov defaults, rules 5 and 6) makes a time box apply to **that day**, and scores the week as “daily goals hit out of daily goals set”.
- The same v1 spec still records Abhishek’s 16 Nov approval of **weekly** time boxes, and L1 still requires an optional weekly time box and week-so-far progress. Approved screens and `GOAL-HIT.md` label the box “Weekly time box” and measure it Monday–Sunday.

Abhishek’s decision was “it should be daily goals,” after a bug in which Wednesday still showed Tuesday’s list and edits rewrote history. That decision clearly covers a fresh daily list, carry-over, and frozen past days. It does not clearly change the box period. Treating the existing 1h / 2h boxes as daily targets — and carrying a 2h “Read one paper” box into Wednesday as a 2h daily box — would be a much heavier product than the weekly boxes he already approved.

The mocks therefore label the field **“Time box · optional”**, not “Weekly” or “Today’s”, so the period is not quietly changed. The week hero uses “2 of 3 daily goals hit” only to illustrate Tuesday’s result under Steve’s written rule; that is not an approval of the scoring change.

**Needed before sign-off:** Steve (and Abhishek if the box period is to change) to confirm whether time boxes and hit math stay weekly, or become daily. Until then, Linus should not build the UI from a chosen period.
