import asyncio, pathlib
from palettes import OPTIONS, check
from frames import SCREENS
from render import render_all, OUT

META = {
 "A": dict(mood="Warm, familiar, calm: the Mac app in your pocket.",
           who="Abhishek moving between Mac and iPhone who wants nothing to relearn.",
           type="Fraunces (display: titles 32, timer 84) + Source Sans 3 (UI 17). Dynamic Type: title → .largeTitle, goal 17 → .body, row detail 14 → .subheadline, captions 13 → .footnote, tabs 15 → .subheadline.",
           space="Base 8 from tokens.css; 22pt side margin; 56pt goal cards; 52pt buttons.",
           radius="Cards 14–16, sheets 24, buttons and segmented nav pill (999).",
           icons="Shipped 1.75px outline line icons; numbers in circles on goals.",
           plant="Shipped money plant on a windowsill card with morning light; focus puts it big on the sill.",
           nav="Web-style pill segmented control (Today / Focus) under the wordmark."),
 "B": dict(mood="Quiet, native, trustworthy: an Apple-style app wearing Cadence’s colours.",
           who="Quick one-handed check-ins on iPhone through the day; best for accessibility (Dynamic Type).",
           type="System font (SF Pro; Inter stands in on these mocks) on iOS text styles: Large Title 34, Title2 22, Body 17, Subhead 15, Footnote 13, Caption2 11. Fraunces only for the timer (76) and “Grew.”",
           space="iOS 16pt margins, 50pt inset grouped rows, 52pt inset separators, 24pt section gaps.",
           radius="Groups 12, buttons 14, sheets 12 with grabber, chips pill.",
           icons="SF-Symbols-style 1.9px strokes; outline idle, filled when selected; ticks are circles.",
           plant="Plant card at the top of Today; large plant card on Focus.",
           nav="Large title + bottom tab bar (Today / Focus), system-style sheets."),
 "C": dict(mood="Calm night garden: low light, moonglow, made for evening focus.",
           who="Late-evening and night sessions, OLED screens, the day-boundary moments.",
           type="Fraunces SOFT 100 (greeting 30) + Inter UI 17; timer Inter Light 72 tabular. Dynamic Type mapping as B.",
           space="16pt margins; 58pt goal pills; 56pt primary + floating add button.",
           radius="Goal cards 20, sheets 24–26, buttons pill.",
           icons="Rounded 2.1px strokes; progress rings instead of ticks.",
           plant="Hero plant under a moon glow and stars; in Focus a progress ring circles the plant.",
           nav="No tab bar: one Today screen; Focus is full screen; add via floating +."),
}
SW = [("primary","Primary"),("primary_deep","Primary deep"),("on_primary","On primary"),("accent","Accent (pots only)"),("sun","Glow (decor)"),
      ("bg","Background"),("surface","Surface"),("text","Text"),("muted","Muted text"),("line","Line"),
      ("success","Success"),("info_bg","Info bg"),("info_ink","Info ink"),("warn_bg","Warn bg"),("warn_ink","Warn ink")]

BASECSS = """*{box-sizing:border-box;margin:0;padding:0} body{font-family:'Inter',sans-serif;background:#EFE8DD;color:#2A2118;padding:48px 56px}
h1{font-family:'Fraunces';font-size:46px;font-weight:600} .lead{display:inline-block;background:#1B5E3B;color:#F7F0E6;font:700 15px Inter;padding:6px 12px;border-radius:999px;vertical-align:middle;margin-left:14px}
.meta{display:grid;grid-template-columns:1.1fr 1fr 1fr;gap:28px;margin-top:22px}
.card{background:#FFFBF6;border-radius:18px;padding:20px 22px;font-size:15px;line-height:1.45}
.card h3{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#5C5146;margin:10px 0 4px} .card h3:first-child{margin-top:0}
.sw{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}.sw div{font-size:11.5px;line-height:1.3}.sw i{display:block;height:38px;border-radius:8px;border:1px solid rgba(0,0,0,.12);margin-bottom:4px}
table{border-collapse:collapse;width:100%;font-size:12.5px} td{padding:3px 4px;border-bottom:1px solid #EFE4D5} td.r{text-align:right;font-variant-numeric:tabular-nums}
.ok{color:#1B5E3B;font-weight:700}.no{color:#9B2C1F;font-weight:700}
.grid{display:grid;grid-template-columns:repeat(6,300px);gap:30px 26px;margin-top:34px}
.f{text-align:left}.f img{width:300px;border-radius:40px;box-shadow:0 0 0 8px #1D1A17,0 18px 40px -16px rgba(0,0,0,.45);display:block;margin:8px 8px 0}
.f p{font-size:14px;font-weight:600;margin-top:18px}.f .n{color:#5C5146;font-weight:700}
.tag{display:inline-block;font-size:11.5px;font-weight:700;padding:3px 8px;border-radius:999px;background:#F6D9A8;color:#5A3A12;margin-top:4px}
.foot{margin-top:36px;font-size:14px;color:#5C5146}
"""

def option_board(k):
    o = OPTIONS[k]; m = META[k]; c = o["c"]
    sw = "".join(f'<div><i style="background:{c[n]}"></i><b>{lab}</b><br>{c[n]}</div>' for n, lab in SW)
    rows = "".join(f'<tr><td>{use}</td><td>{fh} on {bh}</td><td class=r>{r:.2f}:1</td><td class="{"ok" if ok else ("" if ok is None else "no")}">{"decor" if ok is None else ("AA ✓" if ok else "FAIL")}</td></tr>' for f,b,fh,bh,use,mn,r,ok in check(k))
    grid = "".join(f'<div class=f><img src="{(OUT/"frames"/k/(slug+".png")).as_uri()}"><p><span class=n>{slug[:2]}</span> {title}</p>' + (f'<span class=tag>{tag}</span>' if tag else "") + '</div>' for slug, title, fn, tag in SCREENS)
    lead = '<span class=lead>Recommended lead</span>' if k == "B" else '<span class=lead style="background:#5C5146">Alternative</span>'
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{BASECSS}</style></head><body>
<p style="font-weight:700;color:#5C5146;letter-spacing:.08em">CADENCE FOR IPHONE · #54 · OPTION {k} · iPhone 390×844 @2x · fake data · {'provisional until Abhishek approves' }</p>
<h1>{k}. {o['name']}{lead}</h1>
<div class=meta><div class=card><h3>Mood</h3>{m['mood']}<h3>Who it’s for</h3>{m['who']}<h3>Navigation</h3>{m['nav']}<h3>Type</h3>{m['type']}</div>
<div class=card><h3>Palette</h3><div class=sw>{sw}</div><h3>Spacing</h3>{m['space']}<h3>Radius</h3>{m['radius']}<h3>Icons</h3>{m['icons']}<h3>Plant imagery</h3>{m['plant']}</div>
<div class=card><h3>WCAG contrast (checked)</h3><table>{rows}</table></div></div>
<div class=grid>{grid}</div>
<p class=foot>Frames labelled “depends on sync decision” show one way sync could look; the sync approach is undecided. Parked rule: Steve’s spec §4.3. Mac frame for the parked note: frames/mac/mac-parked-note.png. Source: design/ios-54/src (HTML/CSS rendered with headless Chromium).</p>
</body></html>"""

def overview():
    pick = ["01-today", "02-focus", "03-add-goal", "15-parked-c-move-in-disabled", "09-day-boundary"]
    cols = ""
    for k, o in OPTIONS.items():
        m = META[k]
        imgs = "".join(f'<img src="{(OUT/"frames"/k/(p+".png")).as_uri()}">' for p in pick)
        badge = '<span class=lead>Recommended lead</span>' if k == "B" else ""
        cols += f'<div class=col><h2>{k}. {o["name"]}{badge}</h2><p class=m>{m["mood"]} <b>For:</b> {m["who"]}</p><div class=row>{imgs}</div></div>'
    css = BASECSS + """.col{background:#FFFBF6;border-radius:24px;padding:24px 26px;margin-top:26px}.col h2{font-family:Fraunces;font-size:30px;font-weight:600}
.m{font-size:16px;color:#5C5146;margin:6px 0 16px}.row{display:flex;gap:26px}.row img{width:250px;border-radius:34px;box-shadow:0 0 0 7px #1D1A17;margin:7px}
.why{background:#E6EEE3;border-radius:18px;padding:18px 22px;margin-top:22px;font-size:16px;line-height:1.5;color:#0F3D27}"""
    why = ("<b>Why B leads:</b> Cadence iOS ships as an installable app, a Capacitor wrapper or native Swift (not picked yet). "
           "B uses only patterns both can draw the same way: the system font stack, large title, tab bar, inset grouped lists and sheets. "
           "It keeps the approved Windowsill colours and plant, so the Mac and the iPhone read as one product, and Dynamic Type comes almost free. "
           "A is the safest port but feels like a web page on iPhone; C is a strong mood but adds a new dark palette nobody has approved yet.")
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{css}</style></head><body>
<p style="font-weight:700;color:#5C5146;letter-spacing:.08em">CADENCE FOR IPHONE · #54 · VISUAL DIRECTION OPTIONS · Iris (Design), 26 Nov 2026 · fake data · provisional until Abhishek approves</p>
<h1>Three iPhone directions from the shipped Windowsill look</h1>
<p class=m style="font-size:17px">Each column: Today · Focus · Add goal (keyboard) · Parked with Move in disabled · Session past midnight IST. All 23 frames per option are on the option boards.</p>
<div class=why>{why}</div>{cols}</body></html>"""

jobs = [(OUT / "boards" / f"{o['slug']}.png", option_board(k), 2000, 2600) for k, o in OPTIONS.items()]
jobs.append((OUT / "boards" / "00-overview.png", overview(), 1720, 1200))
async def run():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await (await b.new_context(viewport={"width": 2000, "height": 1000}, device_scale_factor=1)).new_page()
        for path, html, w, h in jobs:
            await pg.set_viewport_size({"width": w, "height": h})
            f = pathlib.Path("/workspace/ios54-tmp") / (path.stem + ".html"); f.write_text(html)
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(400)
            path.parent.mkdir(exist_ok=True)
            await pg.screenshot(path=str(path), full_page=True)
        await b.close()
asyncio.run(run()); print("boards ok")
