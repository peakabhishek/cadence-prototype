"""Mac (web app, shipped Windowsill look) frames. 1280x800 @2x. Fake data."""
import asyncio
from frames import ic, PL, SIX
from render import render_all, OUT

css = open("/workspace/focus-tracker/handoff/tokens.css").read()
BASE = f"""<!doctype html><html><head><meta charset=utf-8><style>{css}
*{{box-sizing:border-box;margin:0;padding:0}} body{{width:1280px;height:800px;background:var(--bg);font-family:var(--font-ui);color:var(--text);overflow:hidden}}
.chrome{{height:46px;background:var(--chrome);border-bottom:1px solid var(--chrome-line);display:flex;align-items:center;padding:0 16px;gap:8px}}
.dot{{width:12px;height:12px;border-radius:50%}} .url{{margin:0 auto;width:360px;height:28px;border-radius:8px;background:var(--url-bg);font-size:13px;color:var(--text-muted);display:flex;align-items:center;justify-content:center}}
.wrap{{display:grid;grid-template-columns:1fr 520px;height:754px;background:radial-gradient(60% 70% at 20% 60%,#F6D9A8 0%,rgba(246,217,168,.2) 45%,transparent 75%)}}
.left{{position:relative}} .wm{{position:absolute;top:28px;left:56px;font-family:var(--font-display);font-weight:600;font-size:27px;color:var(--leaf-deep)}}
.sill{{position:absolute;left:0;right:0;bottom:60px;height:26px;background:linear-gradient(var(--sill-top),var(--sill-bot));border-top:1px solid var(--sill-edge)}}
.panel{{background:var(--surface);margin:24px 32px 24px 0;border-radius:24px;padding:32px 36px;box-shadow:var(--shadow-sheet);display:flex;flex-direction:column}}
h1{{font-family:var(--font-display);font-size:36px;font-weight:600}} .sub{{color:var(--text-muted);font-size:17px;margin:4px 0 16px}}
.lbl{{font-size:13px;font-weight:700;color:var(--text-muted);margin:12px 0 8px;display:flex;justify-content:space-between}}
.g{{display:flex;align-items:center;gap:12px;border:1.5px solid var(--line);border-radius:14px;height:46px;padding:0 14px;margin-bottom:7px;font-size:16px;background:var(--surface)}}
.n{{width:24px;height:24px;border-radius:50%;background:var(--track);display:flex;align-items:center;justify-content:center;font-family:var(--font-display);font-size:14px;color:var(--text-muted)}}
.tt{{flex:1}} .bx{{font-size:14px;color:var(--text-muted);font-weight:600}}
.note{{display:flex;gap:8px;align-items:flex-start;background:var(--leaf-wash);color:var(--leaf-deep);border-radius:12px;padding:10px 12px;font-size:15px;font-weight:600;margin-bottom:8px;line-height:1.35}}
.pg{{border:1.5px dashed var(--line);border-radius:14px;padding:10px 14px;display:flex;align-items:center;gap:12px}}
.pk{{height:32px;padding:0 14px;border-radius:999px;background:var(--track);color:var(--text-muted);font-weight:600;font-size:14px;display:flex;align-items:center}}
.hint{{font-size:13px;color:var(--text-muted);margin-top:6px}}
.foot{{margin-top:auto;padding-top:16px;font-size:13.5px;font-weight:600;color:var(--text-muted);display:flex;gap:6px;align-items:center}}
</style></head><body>
<div class=chrome><span class=dot style="background:#E8A89A"></span><span class=dot style="background:#E9CF8F"></span><span class=dot style="background:#A9C9A0"></span><div class=url>Cadence · Today</div></div>
<div class=wrap><div class=left><div class=wm>Cadence</div>
<img src="{{plant}}" style="position:absolute;left:220px;bottom:78px;width:230px"><div class=sill></div></div>
<div class=panel>{{panel}}</div></div></body></html>"""

def rows(goals):
    return "".join(f'<div class="g"><span class="n">{i}</span><span class="tt">{t}</span><span class="bx">{d}</span></div>'
                   for i, (t, b, d, h) in enumerate(goals, 1))

parked_goals = [SIX[0], SIX[1], SIX[2], SIX[3], ("Morning pages", "15 min", "0 / 15 min", False), SIX[5]]
parked = BASE.replace("{plant}", PL("mid")).replace("{panel}", f"""
<h1>Good evening.</h1><p class=sub>Thursday 26 Nov · What matters today?</p>
<div class=lbl><span>Goals</span><span>6 of 6</span></div>{rows(parked_goals)}
<div class=lbl style="margin-top:16px"><span>Parked</span><span>not counted</span></div>
<div class=note>{ic("list",16,1.75)}1 goal synced from your phone didn’t fit today’s 6. It’s in Parked.</div>
<div class=pg><span class=tt>Call the bank</span><span class=pk aria-disabled=true>Move in</span></div>
<p class=hint>Remove one of today’s goals first.</p>""")

# Today is unchanged (Mac already has the newer edits). The held phone changes stay on the phone.
held_goals = [("Write the weekly review", "45 min", "30 / 45 min", False),
              ("Read one paper", "30 min", "30 / 30 min", True),
              ("Gym", "", "Not yet", False),
              ("Plan Friday’s demo", "25 min", "0 / 25 min", False)]
held = BASE.replace("{plant}", PL("mid")).replace("{panel}", f"""
<h1>Good evening.</h1><p class=sub>Thursday 26 Nov · What matters today?</p>
<div class=note>{ic("cloud",16,1.75)}3 changes from your phone weren’t applied, to avoid overwriting newer edits.</div>
<div class=lbl><span>Goals</span><span>4 of 6</span></div>{rows(held_goals)}
<div class=foot>{ic("check",14,1.75)}Saved · OneDrive folder</div>""")

jobs = [
    (OUT / "frames" / "mac" / "mac-parked-note.png", parked, 1280, 800),
    (OUT / "frames" / "mac" / "mac-sync-held.png", held, 1280, 800),
]
asyncio.run(render_all(jobs))
print("ok", len(jobs))
