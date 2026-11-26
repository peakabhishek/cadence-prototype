import asyncio, sys
from palettes import OPTIONS
from frames import SCREENS
from render import render_all, OUT
only = sys.argv[1:]  # e.g. B 01-today
jobs = []
for k, o in OPTIONS.items():
    if only and only[0] != k and only[0] != "all": continue
    o = dict(o, key=k)
    for slug, title, fn, tag in SCREENS:
        if len(only) > 1 and not any(slug.startswith(x) for x in only[1:]): continue
        jobs.append((OUT / "frames" / k / f"{slug}.png", fn(o)))
asyncio.run(render_all(jobs))
print(len(jobs), "frames")
