"""Build HTML for each iPhone frame (390x844 CSS px, rendered @2x). Fake data only."""
import pathlib
from palettes import OPTIONS

ROOT = pathlib.Path(__file__).resolve().parent
PL = lambda n: (ROOT / "plants" / f"{n}.svg").as_uri()

# ---------- icons (24px viewBox, stroke) ----------
P = {
 "sprout": '<path d="M12 21v-8"/><path d="M12 13c0-4-3-6-7-6 0 4 3 6 7 6z"/><path d="M12 11c0-3.5 2.5-5.5 6.5-5.5 0 3.5-2.5 5.5-6.5 5.5z"/>',
 "timer": '<circle cx="12" cy="13.5" r="7.5"/><path d="M12 13.5V9.5"/><path d="M9.5 2.5h5"/>',
 "plus": '<path d="M12 5v14M5 12h14"/>',
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "cloud": '<path d="M7 18h10a4 4 0 0 0 .6-7.95A6 6 0 0 0 6.1 11 3.5 3.5 0 0 0 7 18z"/>',
 "cloudoff": '<path d="M7 18h10a4 4 0 0 0 .6-7.95A6 6 0 0 0 6.1 11 3.5 3.5 0 0 0 7 18z"/><path d="M3 3l18 18"/>',
 "sync": '<path d="M20 11a8 8 0 0 0-14.5-4.5L4 8"/><path d="M4 4v4h4"/><path d="M4 13a8 8 0 0 0 14.5 4.5L20 16"/><path d="M20 20v-4h-4"/>',
 "alert": '<path d="M12 3l9.5 17h-19z"/><path d="M12 10v4.5M12 17.5v.01"/>',
 "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
 "phone": '<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.5h2"/>',
 "moon": '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
 "chev": '<path d="M9 5l7 7-7 7"/>',
 "x": '<path d="M6 6l12 12M18 6L6 18"/>',
 "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
 "more": '<circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/>',
 "list": '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r=".6"/><circle cx="4.5" cy="12" r=".6"/><circle cx="4.5" cy="18" r=".6"/>',
}
def ic(name, size=18, sw=None, cls=""):
    return (f'<svg class="ic {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="{sw or "var(--icon-sw)"}" stroke-linecap="round" stroke-linejoin="round">{P[name]}</svg>')

GOALS = [("Write the weekly review", "45 min", "30 / 45 min", False),
         ("Read one paper", "30 min", "30 / 30 min", True),
         ("Gym", "", "Not yet", False),
         ("Plan Friday’s demo", "25 min", "0 / 25 min", False)]
SIX = GOALS + [("Morning pages", "15 min", "15 / 15 min", True), ("Deep work on the stack", "60 min", "20 / 60 min", False)]

def base_css(o):
    c = o["c"]; dark = o["dark"]; k = o["key"]
    v = "".join(f"--{n.replace('_','-')}:{h};" for n, h in c.items())
    ui = '"Source Sans 3"' if k == "A" else '"Inter"'
    disp = '"Fraunces"'
    return f"""
:root{{{v} --ui:{ui},system-ui,sans-serif; --disp:{disp},Georgia,serif; --icon-sw:{ {'A':'1.75','B':'1.9','C':'2.1'}[k]};
 --r-card:{ {'A':'16px','B':'12px','C':'22px'}[k]}; --r-btn:{ {'A':'999px','B':'14px','C':'999px'}[k]};}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:390px;height:844px;overflow:hidden}}
body{{font-family:var(--ui);color:var(--text);background:var(--bg);-webkit-font-smoothing:antialiased;position:relative;
 font-feature-settings:"tnum" 0; letter-spacing:{'-0.01em' if k!='A' else '0'}}}
.disp{{font-family:var(--disp);font-variation-settings:"SOFT" 60,"opsz" 72;letter-spacing:-0.01em}}
.ic{{flex:none;vertical-align:middle}}
/* device chrome */
.sb{{position:absolute;top:0;left:0;right:0;height:54px;display:flex;align-items:center;justify-content:space-between;padding:6px 30px 0 46px;z-index:50;
 font:600 17px/1 "Inter",system-ui;color:{'#F2EBDD' if dark else '#1F1A14'};letter-spacing:-0.02em}}
.sb.light{{color:#fff}}
.island{{position:absolute;top:11px;left:50%;margin-left:-63px;width:126px;height:37px;border-radius:20px;background:#000;z-index:60}}
.hi{{position:absolute;bottom:8px;left:50%;margin-left:-67px;width:134px;height:5px;border-radius:3px;background:{'#F2EBDD' if dark else '#1F1A14'};z-index:60}}
.sbr{{display:flex;gap:6px;align-items:center}}
.scr{{position:absolute;inset:0;padding-top:54px;padding-bottom:34px;display:flex;flex-direction:column}}
.btn{{display:flex;align-items:center;justify-content:center;gap:8px;height:52px;border-radius:var(--r-btn);font:600 17px/1 var(--ui);border:0}}
.btn.pri{{background:var(--primary);color:var(--on-primary)}}
.btn.out{{background:var(--surface);color:var(--primary-deep);border:1.5px solid var(--line)}}
.btn.txt{{background:none;color:var(--primary);height:44px}}
.muted{{color:var(--muted)}}
.cap{{font-size:13px;color:var(--muted);line-height:1.35}}
.banner{{display:flex;gap:10px;align-items:flex-start;padding:12px 14px;border-radius:14px;font-size:15px;line-height:1.35}}
.banner.info{{background:var(--info-bg);color:var(--info-ink)}}
.banner.warn{{background:var(--warn-bg);color:var(--warn-ink)}}
.banner b{{display:block;font-weight:700;margin-bottom:2px}}
.banner .act{{margin-left:auto;font-weight:700;white-space:nowrap;align-self:center;padding-left:6px;text-decoration:underline;text-underline-offset:3px}}
.bar{{height:6px;border-radius:3px;background:var(--track);overflow:hidden}} .bar i{{display:block;height:100%;background:var(--primary);border-radius:3px}}
.chip{{display:inline-flex;align-items:center;gap:5px;font-size:13px;font-weight:600;padding:4px 9px;border-radius:999px;background:var(--track);color:var(--muted)}}
.chip.ok{{background:var(--wash);color:var(--primary-deep)}}
.chip.warn{{background:var(--warn-bg);color:var(--warn-ink)}}
.skel{{background:var(--track);border-radius:8px}}
.shimmer{{background:linear-gradient(90deg,var(--track),{'#2E4337' if dark else '#F6EEE3'},var(--track))}}
.scrim{{position:absolute;inset:0;background:{'rgba(0,0,0,.55)' if dark else 'rgba(42,33,24,.38)'};z-index:20}}
/* keyboard */
.kb{{position:absolute;left:0;right:0;bottom:0;height:336px;background:var(--key-bg);z-index:40;padding:8px 3px 0}}
.kr{{display:flex;justify-content:center;gap:6px;margin-bottom:11px}}
.k{{height:42px;width:33px;border-radius:5px;background:var(--key);display:flex;align-items:center;justify-content:center;font:400 22px/1 "Inter";color:{'#F2EBDD' if dark else '#1F1A14'};box-shadow:0 1px 0 rgba(0,0,0,{'.5' if dark else '.25'})}}
.k.w{{width:44px;font-size:15px;background:{'#2A3830' if dark else '#ABB0BA'}}} .k.sp{{width:190px;font-size:16px}} .k.ret{{width:90px;font-size:16px;background:var(--primary);color:var(--on-primary)}}
.kbtools{{display:flex;justify-content:space-around;padding:6px 0 0;font:15px "Inter";color:{'#F2EBDD' if dark else '#1F1A14'}}}
"""

def chrome(o, light=False):
    sig = '<svg width="18" height="12" viewBox="0 0 18 12" fill="currentColor"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5.5" width="3" height="6.5" rx="1"/><rect x="10" y="3" width="3" height="9" rx="1"/><rect x="15" y="0" width="3" height="12" rx="1"/></svg>'
    wifi = '<svg width="17" height="12" viewBox="0 0 17 12" fill="currentColor"><path d="M8.5 2.5c2.4 0 4.6.9 6.3 2.4l1.2-1.3A11 11 0 0 0 8.5.6 11 11 0 0 0 1 3.6l1.2 1.3a9.2 9.2 0 0 1 6.3-2.4zm0 3.6c1.4 0 2.7.5 3.8 1.4l1.2-1.3a7.4 7.4 0 0 0-10 0l1.2 1.3c1-.9 2.4-1.4 3.8-1.4zm0 3.6c.5 0 1 .2 1.4.5L8.5 12 7.1 10.2c.4-.3.9-.5 1.4-.5z"/></svg>'
    bat = '<svg width="27" height="13" viewBox="0 0 27 13" fill="none"><rect x=".5" y=".5" width="23" height="12" rx="3.5" stroke="currentColor" opacity=".4"/><rect x="2" y="2" width="17" height="9" rx="2" fill="currentColor"/><path d="M25 4.5v4c.8-.3 1.3-1 1.3-2s-.5-1.7-1.3-2z" fill="currentColor" opacity=".45"/></svg>'
    return lambda t, offline=False: (f'<div class="sb{" light" if light else ""}"><span>{t}</span><span class="sbr">{sig}{"" if offline else wifi}{bat}</span></div>'
            '<div class="island"></div><div class="hi"></div>')

def keyboard(o, ret="add"):
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    h = '<div class="kb">'
    h += '<div class="kr">' + "".join(f'<div class="k">{ch}</div>' for ch in rows[0]) + '</div>'
    h += '<div class="kr">' + "".join(f'<div class="k">{ch}</div>' for ch in rows[1]) + '</div>'
    h += '<div class="kr"><div class="k w">⇧</div>' + "".join(f'<div class="k">{ch}</div>' for ch in rows[2]) + '<div class="k w">⌫</div></div>'
    h += f'<div class="kr"><div class="k w" style="width:88px">123</div><div class="k sp">space</div><div class="k ret">{ret}</div></div>'
    h += '<div class="kbtools"><span>🌐</span><span></span><span>🎙</span></div></div>'
    return h

def plant_img(stage, w=160, extra=""):
    return f'<img src="{PL(stage)}" style="width:{w}px;display:block;{extra}">'

# ======================= option-specific CSS =======================
CSS = {
"A": """
.hdr{display:flex;justify-content:space-between;align-items:center;padding:8px 22px 0}
.wm{display:flex;align-items:center;gap:6px;font-family:var(--disp);font-weight:600;font-size:24px;color:var(--primary-deep)}
.date{font-size:15px;color:var(--muted);font-weight:600}
.seg{margin:12px 22px 0;display:flex;background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:4px}
.seg span{flex:1;display:flex;gap:6px;align-items:center;justify-content:center;height:36px;border-radius:999px;font-weight:600;font-size:15px;color:var(--muted)}
.seg span.on{background:var(--wash);color:var(--primary-deep)}
.body{flex:1;padding:16px 22px 0;overflow:hidden;position:relative}
h1.t{font-family:var(--disp);font-weight:600;font-size:32px;line-height:1.1;font-variation-settings:"SOFT" 60,"opsz" 72}
.sub{font-size:17px;color:var(--muted);margin-top:4px}
.sill{margin-top:14px;height:118px;border-radius:16px;background:linear-gradient(180deg,#F9F3EA 0%,#F6E6C8 100%);position:relative;overflow:hidden;border:1px solid var(--line)}
.sill .ledge{position:absolute;left:0;right:0;bottom:0;height:16px;background:linear-gradient(#EADBC7,#E1CFB8);border-top:1px solid #D6C2A8}
.sill .tx{position:absolute;left:16px;top:16px;font-size:13px;color:var(--muted);font-weight:600;line-height:1.5}
.sill .tx b{display:block;font-family:var(--disp);font-size:24px;color:var(--primary-deep);font-weight:600}
.lbl{font-size:13px;font-weight:700;color:var(--muted);margin:16px 0 8px;display:flex;justify-content:space-between}
.g{display:flex;align-items:center;gap:12px;background:var(--surface);border:1.5px solid var(--line);border-radius:14px;height:56px;padding:0 14px;margin-bottom:8px;font-size:17px}
.g .n{width:26px;height:26px;border-radius:50%;background:var(--track);display:flex;align-items:center;justify-content:center;font-family:var(--disp);font-size:15px;color:var(--muted)}
.g .n.hit{background:var(--primary);color:var(--on-primary)}
.g .tt{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.g .bx{font-size:14px;color:var(--muted);font-weight:600}
.g .bx.add{color:var(--primary);}
.g.new{border-color:var(--primary);box-shadow:0 0 0 3px var(--wash)}
.foot{padding:10px 22px 10px;background:linear-gradient(transparent,var(--bg) 18%)}
.status{display:flex;gap:6px;align-items:center;justify-content:center;font-size:13px;font-weight:600;color:var(--muted);margin-top:8px;text-align:center}
""",
"B": """
.nav{padding:4px 18px 0;display:flex;justify-content:space-between;align-items:center;height:44px}
.nav .tl{font-size:17px;color:var(--primary);font-weight:500}
.nav .rt{display:flex;gap:16px;color:var(--primary)}
.circ{width:32px;height:32px;border-radius:50%;background:var(--wash);color:var(--primary);display:flex;align-items:center;justify-content:center}
.lt{padding:0 18px}
.lt h1{font-size:34px;font-weight:700;letter-spacing:-0.025em;line-height:1.15}
.lt .sub{font-size:15px;color:var(--muted);margin-top:2px;display:flex;align-items:center;gap:6px}
.body{flex:1;padding:12px 16px 0;overflow:hidden;position:relative}
.sec{font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.02em;padding:14px 16px 7px;display:flex;justify-content:space-between}
.grp{background:var(--surface);border-radius:12px;overflow:hidden}
.row{display:flex;align-items:center;gap:12px;min-height:50px;padding:0 16px;font-size:17px;position:relative}
.row+.row:before{content:"";position:absolute;top:0;left:52px;right:0;border-top:.5px solid var(--line);border-top-width:1px}
.tick{width:24px;height:24px;border-radius:50%;border:1.8px solid var(--muted);display:flex;align-items:center;justify-content:center;flex:none}
.tick.on{background:var(--primary);border-color:var(--primary);color:var(--on-primary)}
.row .tt{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.row .bx{font-size:15px;color:var(--muted)}
.row .bx.add{color:var(--primary)}
.row.addrow{color:var(--primary)}
.row.addrow .tt{color:var(--primary)}
.plantcard{display:flex;align-items:flex-end;gap:12px;padding:12px 16px 0;height:120px;background:linear-gradient(180deg,#FBF4EA,#F5E3C6);border-radius:12px;overflow:hidden;position:relative}
.plantcard .tx{padding-bottom:16px;font-size:15px;color:var(--muted)}
.plantcard .tx b{display:block;font-size:22px;color:var(--text);font-weight:700;letter-spacing:-.02em}
.foot{padding:8px 16px 8px}
.tabs{height:83px;margin-bottom:-34px;background:rgba(255,252,248,.92);border-top:1px solid var(--line);display:flex;justify-content:space-around;padding-top:7px;backdrop-filter:blur(20px)}
.tabs span{display:flex;flex-direction:column;align-items:center;gap:3px;font-size:10.5px;font-weight:600;color:var(--tab-idle);width:90px}
.tabs span.on{color:var(--primary)}
.sheet{position:absolute;left:0;right:0;bottom:0;top:92px;background:var(--surface);border-radius:12px 12px 0 0;z-index:30;padding:6px 16px 0}
.grab{width:36px;height:5px;border-radius:3px;background:var(--line);margin:0 auto 8px}
.status{display:flex;gap:6px;align-items:center;font-size:13px;color:var(--muted)}
""",
"C": """
.top{display:flex;justify-content:space-between;align-items:center;padding:8px 22px 0;font-size:15px;color:var(--muted);font-weight:600}
.dot{display:inline-flex;gap:6px;align-items:center}
.hero{position:relative;height:260px;display:flex;justify-content:center;align-items:flex-end;margin-top:-4px}
.moon{position:absolute;top:10px;left:50%;margin-left:-150px;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(235,217,166,.28) 0%,rgba(235,217,166,.08) 45%,transparent 70%)}
.stars{position:absolute;inset:0;background-image:radial-gradient(1.4px 1.4px at 40px 40px,#EBD9A6,transparent),radial-gradient(1.2px 1.2px at 320px 70px,#EBD9A6,transparent),radial-gradient(1px 1px at 80px 150px,#EBD9A6,transparent),radial-gradient(1.2px 1.2px at 300px 180px,#EBD9A6,transparent),radial-gradient(1px 1px at 200px 22px,#EBD9A6,transparent);opacity:.8}
.ledge{position:absolute;left:24px;right:24px;bottom:0;height:10px;border-radius:5px;background:#24362B}
.greet{padding:12px 22px 0}
.greet h1{font-family:var(--disp);font-weight:500;font-size:30px;line-height:1.1;font-variation-settings:"SOFT" 100,"opsz" 72}
.greet .sub{font-size:16px;color:var(--muted);margin-top:4px}
.body{flex:1;padding:12px 16px 0;overflow:hidden;position:relative}
.g{display:flex;align-items:center;gap:12px;background:var(--surface);border-radius:20px;min-height:58px;padding:0 16px;margin-bottom:8px;font-size:17px}
.ring{width:28px;height:28px;flex:none}
.g .tt{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.g .bx{font-size:14px;color:var(--muted);font-weight:600}
.g .bx.add{color:var(--primary)}
.g.new{box-shadow:inset 0 0 0 1.5px var(--primary)}
.foot{padding:10px 16px 10px;display:flex;gap:10px;align-items:center}
.foot .btn.pri{flex:1;height:56px;font-size:18px}
.fab{width:56px;height:56px;border-radius:50%;background:var(--surface);color:var(--primary);display:flex;align-items:center;justify-content:center;border:1.5px solid var(--line)}
.status{display:flex;gap:6px;align-items:center;font-size:13px;color:var(--muted)}
.lbl{font-size:13px;font-weight:700;color:var(--muted);margin:4px 6px 8px;display:flex;justify-content:space-between;letter-spacing:.04em;text-transform:uppercase}
""",
}

# ======================= builders =======================
EXTRA_CSS = """
.demo{position:absolute;top:54px;left:0;right:0;height:24px;background:#F6D9A8;color:#5A3A12;font:600 13px/24px var(--ui);text-align:center;z-index:45;letter-spacing:0}
body.hasdemo .scr{padding-top:78px}
.pk{display:inline-flex;align-items:center;height:30px;padding:0 13px;border-radius:999px;font-size:14px;font-weight:600;background:var(--primary);color:var(--on-primary);white-space:nowrap}
.pk.off{background:var(--track);color:var(--muted)}
.hint{font-size:13px;color:var(--muted);padding:6px 16px 0}
.src{display:block;font-size:13px;color:var(--muted);margin-top:1px}
.v2{font-size:12px;font-weight:700;color:var(--warn-ink);background:var(--warn-bg);padding:2px 7px;border-radius:999px;margin-left:6px}
.us{color:var(--muted);margin-left:4px}
.removed{font-size:15px;color:var(--muted);padding:10px 4px;display:flex;justify-content:space-between}
.removed b{color:var(--primary);font-weight:700}
.tzh{display:flex;gap:4px;align-items:center;font-size:12.5px;font-weight:600;color:var(--muted);margin-top:3px}
.full{font-size:15px;color:var(--warn-ink);font-weight:600;line-height:1.35}
"""

def page(o, inner, t="9:41", demo=False, offline=False, light_sb=False):
    css = base_css(o) + CSS[o["key"]] + EXTRA_CSS
    ch = chrome(o, light_sb)(t, offline)
    d = '<div class="demo">Demo data, not synced</div>' if demo else ""
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>'
            f'<body class="{"hasdemo" if demo else ""}">{ch}{d}{inner}</body></html>')

def ring(o, frac, hit=False):
    c = o["c"]
    if hit:
        return f'<svg class="ring" viewBox="0 0 28 28"><circle cx="14" cy="14" r="13" fill="{c["primary"]}"/><path d="M8.5 14.5l3.8 3.8 7.2-8" stroke="{c["on_primary"]}" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    L = 2*3.14159*11
    if frac <= 0:
        return f'<svg class="ring" viewBox="0 0 28 28"><circle cx="14" cy="14" r="11" stroke="{c["track"]}" stroke-width="3.2" fill="none"/></svg>'
    return (f'<svg class="ring" viewBox="0 0 28 28"><circle cx="14" cy="14" r="11" stroke="{c["track"]}" stroke-width="3.2" fill="none"/>'
            f'<circle cx="14" cy="14" r="11" stroke="{c["primary"]}" stroke-width="3.2" fill="none" stroke-dasharray="{L*frac:.1f} {L:.1f}" transform="rotate(-90 14 14)" stroke-linecap="round"/></svg>')

def frac(detail):
    try:
        a, b = detail.replace(" min", "").split(" / "); return int(a)/int(b)
    except Exception: return 0

def rows(o, goals):
    k = o["key"]; h = ""
    for i, g in enumerate(goals, 1):
        title, box, detail, hit = g[:4]; fl = g[4] if len(g) > 4 else ""
        extra = ""
        if "unsynced" in fl: extra += f'<span class="us">{ic("cloudoff", 15)}</span>'
        if "twov" in fl: extra += '<span class="v2">2 versions</span>'
        det = detail if box or detail == "Not yet" else ""
        bxcls = "bx"
        if k == "A":
            h += (f'<div class="g{" new" if "new" in fl else ""}"><span class="n{" hit" if hit else ""}">{ic("check",14,2.4) if hit else i}</span>'
                  f'<span class="tt">{title}{extra}</span><span class="{bxcls}">{det}</span></div>')
        elif k == "B":
            h += (f'<div class="row"><span class="tick{" on" if hit else ""}">{ic("check",14,2.6) if hit else ""}</span>'
                  f'<span class="tt">{title}{extra}</span><span class="{bxcls}">{det}</span></div>')
        else:
            h += (f'<div class="g{" new" if "new" in fl else ""}">{ring(o, frac(detail), hit)}'
                  f'<span class="tt">{title}{extra}</span><span class="{bxcls}">{det}</span></div>')
    return h

def status_line(kind):
    return {"ok": (ic("check", 14), "Last synced 9:40 PM"), "syncing": (ic("sync", 14), "Syncing…"),
            "offline": (ic("cloudoff", 14), "Offline"), "failed": (ic("alert", 14), "Not synced"),
            "demo": (ic("phone", 14), "Demo data"),
            "queued": (ic("cloud", 14), "2 changes waiting to upload"),
            "waiting": (ic("laptop", 14), "Waiting for your Mac"),
            "clock": (ic("timer", 14), "Phone clock is off. Times are being corrected."),
            "macupdate": (ic("laptop", 14), "Your Mac needs an update to sync. Your changes are saved here.")}[kind]

def banner(kind, title, body="", act=""):
    icn = {"info": "cloudoff", "warn": "alert", "ok": "sync", "park": "list"}[kind]
    cls = "warn" if kind == "warn" else "info"
    return (f'<div class="banner {cls}">{ic(icn, 18)}<div>{"<b>"+title+"</b>" if body else title}{body}</div>'
            f'{"<span class=act>"+act+"</span>" if act else ""}</div>')

def today_view(o, goals, *, status="ok", banners="", after="", plant="mid", tally=("2 plants", "1h 10m"),
               greet=("Good evening.", "What matters today?"), counter=None, add_row=True, foot=True,
               date="Thursday 26 Nov", tab="today", pre="", tz=False):
    k = o["key"]; si, st = status_line(status)
    n = counter if counter is not None else len(goals)
    warn = ' style="color:var(--warn-ink)"' if status == "failed" else ""
    six = "Six goals — plenty for one day."
    tzh = f'<div class="tzh">{ic("moon",13)}Days follow India time</div>' if tz else ""
    if k == "A":
        h = (f'<div class="scr"><div class="hdr"><span class="wm">{ic("sprout",22,2)}Cadence</span><span class="date">{date}{tzh}</span></div>'
             f'<div class="seg"><span class="{"on" if tab=="today" else ""}">{ic("list",17)}Today</span><span class="{"on" if tab=="focus" else ""}">{ic("timer",17)}Focus</span></div>'
             f'<div class="body">{pre}<h1 class="t">{greet[0]}</h1><p class="sub">{greet[1]}</p>'
             + (f'<div style="margin-top:12px;display:flex;flex-direction:column;gap:8px">{banners}</div>' if banners else "")
             + (f'<div class="sill"><div class="tx">Today’s sill<b>{tally[0]} · {tally[1]}</b></div>'
                f'<div style="position:absolute;right:26px;bottom:6px">{plant_img(plant, 92)}</div><div class="ledge"></div></div>' if plant else "")
             + f'<div class="lbl"><span>Goals</span><span>{n} of 6</span></div>{rows(o, goals)}'
             + (f'<div class="g" style="border-style:dashed;color:var(--primary);font-weight:600">{ic("plus",20)}Add a goal</div>' if add_row and n < 6 else "")
             + (f'<p class="cap" style="display:flex;gap:6px;align-items:center;margin:4px 2px">{ic("check",15)}{six}</p>' if n >= 6 and add_row else "")
             + after + '</div>'
             + (f'<div class="foot"><div class="btn pri">Start focusing</div><div class="status"{warn}>{si}{st}</div></div>' if foot else "")
             + '</div>')
    elif k == "B":
        h = (f'<div class="scr"><div class="nav"><span class="tl"></span><span class="rt"><span class="circ">{ic("plus",18,2.2)}</span></span></div>'
             f'<div class="lt"><h1>{"Today" if tab=="today" else "Focus"}</h1><div class="sub">{date}{" · " if len(st) < 30 else ""}{f'<span class="status"{warn}>{si}{st}</span>' if len(st) < 30 else ""}</div>{"" if len(st) < 30 else f'<div class="status" style="margin-top:4px;align-items:flex-start;line-height:1.35">{si}<span>{st}</span></div>'}{tzh}</div>'
             f'<div class="body">{pre}'
             + (f'<div style="display:flex;flex-direction:column;gap:8px;margin-bottom:12px">{banners}</div>' if banners else "")
             + (f'<div class="plantcard">{plant_img(plant, 82, "margin-bottom:-4px")}<div class="tx"><b>{tally[0]} · {tally[1]}</b>Focused today</div></div>' if plant else "")
             + f'<div class="sec"><span>Goals</span><span>{n} of 6</span></div><div class="grp">{rows(o, goals)}'
             + (f'<div class="row addrow"><span style="width:24px;display:flex;justify-content:center">{ic("plus",20,2.2)}</span><span class="tt">Add goal</span></div>' if add_row and n < 6 else "")
             + '</div>'
             + (f'<p class="hint">{six}</p>' if n >= 6 and add_row else "")
             + after + '</div>'
             + (f'<div class="foot"><div class="btn pri">{ic("timer",20,2)}Start focusing</div></div>' if foot else "")
             + f'<div class="tabs"><span class="{"on" if tab=="today" else ""}">{ic("list",24)}Today</span><span class="{"on" if tab=="focus" else ""}">{ic("timer",24)}Focus</span></div></div>')
    else:
        h = ((f'<div class="scr"><div class="top"><span>{date}{tzh}</span><span class="status"{warn}>{si}{st}</span></div>' if len(st) < 30 else f'<div class="scr"><div class="top"><span>{date}{tzh}</span></div><div class="status" style="padding:4px 22px 0;align-items:flex-start;line-height:1.35">{si}<span>{st}</span></div>')
             + (f'<div class="hero" style="height:150px"><div class="moon" style="top:-60px"></div><div class="stars"></div>{plant_img(plant, 108, "position:relative;z-index:2;margin-bottom:4px")}<div class="ledge"></div></div>' if plant else "")
             + f'<div class="greet"><h1>{greet[0]}</h1><p class="sub">{greet[1]}</p></div>'
             + f'<div class="body">{pre}'
             + (f'<div style="display:flex;flex-direction:column;gap:8px;margin-bottom:10px">{banners}</div>' if banners else "")
             + f'<div class="lbl"><span>Goals</span><span>{n} of 6</span></div>{rows(o, goals)}'
             + (f'<p class="cap" style="padding:2px 8px">{six}</p>' if n >= 6 and add_row else "")
             + after + '</div>'
             + (f'<div class="foot"><div class="btn pri">Start focusing</div>' + (f'<div class="fab">{ic("plus",24,2.2)}</div>' if n < 6 else "") + '</div>' if foot else "")
             + '</div>')
    return h

def parked_block(o, items, enabled, hint=True, past=False):
    k = o["key"]; h = ""
    for t, src in items:
        btn = "" if past else f'<span class="pk{"" if enabled else " off"}" aria-disabled="{str(not enabled).lower()}">Move in</span>'
        if k == "B":
            h += f'<div class="row" style="min-height:58px"><span style="width:24px;color:var(--muted);display:flex;justify-content:center">{ic("list",18)}</span><span class="tt" style="white-space:normal;padding:8px 0">{t}<span class="src">{src}</span></span>{btn}</div>'
        else:
            h += f'<div class="g" style="height:auto;min-height:62px;padding:8px 14px;border:1.5px dashed var(--line)">{ic("list",18)}<span class="tt" style="white-space:normal">{t}<span class="src">{src}</span></span>{btn}</div>'
    hint_html = '<p class="hint">Remove one of today’s goals first.</p>' if (hint and not enabled and not past) else ""
    if k == "B":
        return f'<div class="sec"><span>Parked</span><span>not counted</span></div><div class="grp">{h}</div>{hint_html}'
    lbl = f'<div class="lbl" style="margin-top:14px"><span>Parked</span><span>not counted</span></div>'
    return lbl + h + hint_html.replace('padding:6px 16px 0', '')

# ======================= screens =======================
def s_today(o): return page(o, today_view(o, GOALS), demo=o["key"] == "B")

def s_focus(o):
    k = o["key"]; c = o["c"]
    if k == "A":
        inner = (f'<div class="scr" style="background:radial-gradient(120% 60% at 30% 70%,#F6D9A8 0%,rgba(246,217,168,.25) 45%,transparent 75%),var(--bg)">'
                 f'<div class="hdr"><span class="wm">{ic("sprout",22,2)}Cadence</span><span class="date">Focusing</span></div>'
                 f'<div style="padding:34px 26px 0"><p class="cap" style="font-weight:700;letter-spacing:.08em">FOCUSING ON</p>'
                 f'<h2 class="disp" style="font-size:27px;font-weight:600;margin-top:4px">Write the weekly review</h2>'
                 f'<div class="disp" style="font-size:84px;font-weight:600;color:var(--primary-deep);font-variant-numeric:tabular-nums;line-height:1;margin-top:14px">31:14</div>'
                 f'<p class="muted" style="font-size:16px;margin-top:8px">remaining of 50:00 · ends 10:12 PM</p>'
                 f'<div class="bar" style="margin-top:14px"><i style="width:38%"></i></div>'
                 f'<div style="display:flex;gap:14px;align-items:center;margin-top:20px"><div class="btn out" style="width:130px;height:46px;color:var(--warn-ink)">Give up</div>'
                 f'<span class="cap">Your session keeps counting if you switch apps.</span></div></div>'
                 f'<div style="flex:1;position:relative"><div style="position:absolute;left:50%;margin-left:-95px;bottom:26px">{plant_img("mid",190)}</div>'
                 f'<div style="position:absolute;left:0;right:0;bottom:0;height:30px;background:linear-gradient(#EADBC7,#E1CFB8);border-top:1px solid #D6C2A8"></div></div></div>')
        return page(o, inner)
    if k == "B":
        inner = (f'<div class="scr"><div class="nav"><span class="tl">{ic("chev",18,2.2).replace("M9 5l7 7-7 7","M15 5l-7 7 7 7")} Today</span><span style="font-weight:600;font-size:17px">Focus</span><span style="width:60px"></span></div>'
                 f'<div style="margin:10px 16px 0;height:300px;border-radius:16px;background:linear-gradient(180deg,#FBF4EA,#F5E3C6);position:relative;overflow:hidden">'
                 f'<div style="position:absolute;left:50%;margin-left:-85px;bottom:14px">{plant_img("mid",170)}</div>'
                 f'<div style="position:absolute;left:0;right:0;bottom:0;height:18px;background:linear-gradient(#EADBC7,#E1CFB8)"></div></div>'
                 f'<div style="padding:18px 20px 0;text-align:center"><p class="cap" style="font-weight:600;letter-spacing:.06em">FOCUSING ON</p>'
                 f'<h2 style="font-size:22px;font-weight:700;margin-top:3px">Write the weekly review</h2>'
                 f'<div class="disp" style="font-size:76px;font-weight:600;color:var(--primary-deep);font-variant-numeric:tabular-nums;line-height:1.05;margin-top:6px">31:14</div>'
                 f'<p class="muted" style="font-size:15px">remaining of 50:00 · ends 10:12 PM</p>'
                 f'<div class="bar" style="margin:14px 20px 0"><i style="width:38%"></i></div></div>'
                 f'<div style="flex:1"></div><div style="padding:0 16px 14px"><div class="btn out" style="color:var(--warn-ink)">Give up</div>'
                 f'<p class="cap" style="text-align:center;margin-top:8px">Your session keeps counting if you switch apps.</p></div></div>')
        return page(o, inner, demo=True)
    inner = (f'<div class="scr" style="background:radial-gradient(70% 45% at 50% 38%,rgba(235,217,166,.20),transparent 70%),var(--bg)">'
             f'<div class="top"><span>Focusing</span><span>ends 10:12 PM</span></div>'
             f'<div style="position:relative;height:420px;display:flex;align-items:center;justify-content:center">'
             f'<div class="stars"></div>'
             f'<svg width="330" height="330" viewBox="0 0 330 330" style="position:absolute"><circle cx="165" cy="165" r="155" stroke="{c["track"]}" stroke-width="6" fill="none"/>'
             f'<circle cx="165" cy="165" r="155" stroke="{c["primary"]}" stroke-width="6" fill="none" stroke-dasharray="{2*3.14159*155*0.38:.0f} 2000" transform="rotate(-90 165 165)" stroke-linecap="round"/></svg>'
             f'{plant_img("mid",170,"position:relative;margin-top:30px")}</div>'
             f'<div style="text-align:center;padding:0 24px"><p class="cap" style="font-weight:700;letter-spacing:.1em">FOCUSING ON</p>'
             f'<h2 class="disp" style="font-size:24px;font-weight:500;margin-top:4px">Write the weekly review</h2>'
             f'<div style="font:300 72px/1 Inter;color:var(--primary-deep);font-variant-numeric:tabular-nums;margin-top:10px;letter-spacing:-0.03em">31:14</div>'
             f'<p class="muted" style="font-size:15px;margin-top:6px">remaining of 50:00</p></div>'
             f'<div style="flex:1"></div><div style="padding:0 24px 14px;text-align:center"><div class="btn out" style="background:transparent;color:var(--warn-ink);border-color:var(--line)">Give up</div>'
             f'<p class="cap" style="margin-top:8px">Your session keeps counting if you switch apps.</p></div></div>')
    return page(o, inner)

def add_sheet(o, typed, at_six=False):
    k = o["key"]
    msg = '<p class="full" style="margin-top:10px">Today already has 6 goals. Remove one to add this.</p>' if at_six else ""
    if k == "B":
        return (f'<div class="scrim"></div><div class="sheet"><div class="grab"></div>'
                f'<div style="display:flex;justify-content:space-between;align-items:center;height:40px;font-size:17px"><span style="color:var(--primary)">Cancel</span><b>New goal</b><b style="color:var(--primary)">Add</b></div>'
                f'<div class="grp" style="margin-top:14px;background:var(--bg)"><div class="row" style="background:var(--bg)"><span class="tt">{typed}<span style="display:inline-block;width:2px;height:20px;background:var(--primary);vertical-align:-4px;margin-left:1px"></span></span></div>'
                f'<div class="row" style="background:var(--bg)"><span class="tt">Time box</span><span class="bx">30 min</span>{ic("chev",16)}</div></div>{msg}</div>')
    if k == "A":
        return (f'<div class="scrim"></div><div class="sheet" style="position:absolute;left:0;right:0;bottom:336px;background:var(--surface);border-radius:24px 24px 0 0;z-index:30;padding:20px 22px 18px">'
                f'<h3 class="disp" style="font-size:24px;font-weight:600">Add a goal</h3>'
                f'<div style="margin-top:12px;height:56px;border:2px solid var(--primary);border-radius:12px;display:flex;align-items:center;padding:0 14px;font-size:17px">{typed}<span style="width:2px;height:22px;background:var(--primary);margin-left:1px"></span></div>'
                f'<div style="display:flex;gap:8px;margin-top:10px;align-items:center"><span class="chip">No time box</span><span class="chip ok">30 min</span><span class="chip">45 min</span><span class="chip">60 min</span></div>{msg}'
                f'<div class="btn pri" style="margin-top:14px">Add goal</div></div>')
    return (f'<div class="scrim"></div><div style="position:absolute;left:10px;right:10px;bottom:346px;background:var(--surface);border-radius:26px;z-index:30;padding:16px">'
            f'<div style="display:flex;gap:10px;align-items:center"><div style="flex:1;height:50px;border-radius:999px;background:var(--bg);display:flex;align-items:center;padding:0 18px;font-size:17px">{typed}<span style="width:2px;height:22px;background:var(--primary);margin-left:1px"></span></div>'
            f'<div class="fab" style="width:50px;height:50px;background:var(--primary);color:var(--on-primary);border:0">{ic("plus",22,2.4)}</div></div>'
            f'<div style="display:flex;gap:8px;margin-top:10px"><span class="chip">No box</span><span class="chip ok">30 min</span><span class="chip">45</span><span class="chip">60</span></div>{msg}</div>')

def s_add(o):
    return page(o, today_view(o, GOALS) + add_sheet(o, "Call the bank") + keyboard(o), demo=o["key"] == "B")

def s_six(o):
    return page(o, today_view(o, SIX, plant=None) + add_sheet(o, "Call the bank", at_six=True) + keyboard(o), demo=o["key"] == "B")

def s_empty(o):
    k = o["key"]
    if k == "B":  # first-run sign-in (MOCKED) for the lead option
        inner = (f'<div class="scr"><div style="margin:20px 16px 0;height:290px;border-radius:16px;background:linear-gradient(180deg,#FBF4EA,#F5E3C6);position:relative;overflow:hidden">'
                 f'<div style="position:absolute;left:50%;margin-left:-80px;bottom:12px">{plant_img("empty",160)}</div>'
                 f'<div style="position:absolute;left:0;right:0;bottom:0;height:18px;background:linear-gradient(#EADBC7,#E1CFB8)"></div>'
                 f'<span class="chip warn" style="position:absolute;top:12px;right:12px">MOCKED sign-in</span></div>'
                 f'<div style="padding:22px 22px 0"><h1 style="font-size:28px;font-weight:700;letter-spacing:-.02em;line-height:1.15">Grow a plant for every focus session.</h1>'
                 f'<p class="muted" style="font-size:17px;line-height:1.4;margin-top:10px">Sign in with the Microsoft account that holds your Cadence folder, so this iPhone shares today’s goals with your Mac.</p></div>'
                 f'<div style="flex:1"></div><div style="padding:0 16px 10px"><div class="btn pri">Sign in with Microsoft</div><div class="btn txt" style="margin-top:4px">Try with demo data</div>'
                 f'<p class="cap" style="text-align:center;margin-top:4px">Cadence reads and writes one file in your OneDrive folder. Nothing else.</p></div></div>')
        return page(o, inner, demo=True)
    hint = '<p class="cap" style="margin:10px 4px 0;font-size:15px;line-height:1.4">Up to 6 goals a day. Focus on one and a money plant grows. Only Give up withers it.</p>'
    return page(o, today_view(o, [], plant="empty", tally=("No plants yet", "0m"), greet=("Good evening.", "What matters today?"), after=hint, status="ok"))

def s_loading(o):
    k = o["key"]
    sk = lambda w, h=14, r=8, extra="": f'<div class="skel shimmer" style="width:{w};height:{h}px;border-radius:{r}px;{extra}"></div>'
    if k == "B":
        rows_ = "".join(f'<div class="row"><span class="tick" style="border-color:var(--track)"></span>{sk(f"{w}%")}</div>' for w in (62, 44, 30, 52))
        inner = (f'<div class="scr"><div class="nav"></div><div class="lt"><h1>Today</h1><div class="sub">Thursday 26 Nov · <span class="status">{ic("sync",14)}Loading…</span></div></div>'
                 f'<div class="body">{sk("100%",120,12)}<div class="sec"><span>Goals</span></div><div class="grp">{rows_}</div></div>'
                 f'<div class="foot"><div class="btn pri" style="opacity:.45">{ic("timer",20,2)}Start focusing</div></div>'
                 f'<div class="tabs"><span class="on">{ic("list",24)}Today</span><span>{ic("timer",24)}Focus</span></div></div>')
        return page(o, inner, demo=True)
    if k == "A":
        g = "".join(f'<div class="g">{sk("26px",26,13)}{sk(f"{w}%")}</div>' for w in (62, 44, 30, 52))
        inner = (f'<div class="scr"><div class="hdr"><span class="wm">{ic("sprout",22,2)}Cadence</span><span class="date">Thursday 26 Nov</span></div>'
                 f'<div class="seg"><span class="on">{ic("list",17)}Today</span><span>{ic("timer",17)}Focus</span></div>'
                 f'<div class="body"><h1 class="t">Good evening.</h1><p class="sub">Loading today’s goals…</p>{sk("100%",118,16,"margin-top:14px")}<div class="lbl"><span>Goals</span></div>{g}</div>'
                 f'<div class="foot"><div class="btn pri" style="opacity:.45">Start focusing</div></div></div>')
        return page(o, inner)
    g = "".join(f'<div class="g">{sk("28px",28,14)}{sk(f"{w}%")}</div>' for w in (62, 44, 30, 52))
    inner = (f'<div class="scr"><div class="top"><span>Thursday 26 Nov</span><span class="status">{ic("sync",14)}Loading…</span></div>'
             f'<div class="hero" style="height:150px"><div class="moon" style="top:-60px"></div><div class="stars"></div>{sk("90px",100,45,"position:relative;z-index:2;margin-bottom:8px")}<div class="ledge"></div></div>'
             f'<div class="greet"><h1>Good evening.</h1><p class="sub">Loading today’s goals…</p></div><div class="body"><div class="lbl"><span>Goals</span></div>{g}</div>'
             f'<div class="foot"><div class="btn pri" style="opacity:.45">Start focusing</div></div></div>')
    return page(o, inner)

OFFLINE_B = banner("info", "You’re offline.", " Changes stay on this phone and sync when you’re back.")
def s_offline(o):
    g = [GOALS[0], (GOALS[1][0], GOALS[1][1], GOALS[1][2], True, "unsynced"), GOALS[2], GOALS[3], ("Call the bank", "", "Not yet", False, "unsynced new")]
    return page(o, today_view(o, g, status="offline", banners=OFFLINE_B, plant=None), offline=True)

def s_error(o):
    k = o["key"]
    box = (f'<div style="display:flex;flex-direction:column;align-items:center;text-align:center;padding:60px 26px 0">'
           f'<div style="width:64px;height:64px;border-radius:50%;background:var(--wash);color:var(--primary-deep);display:flex;align-items:center;justify-content:center">{ic("cloudoff",30)}</div>'
           f'<h2 style="font-size:22px;font-weight:700;margin-top:18px" class="{"disp" if k!="B" else ""}">We couldn’t load today.</h2>'
           f'<p class="muted" style="font-size:17px;line-height:1.4;margin-top:8px">Cadence couldn’t reach your goals. Nothing has been lost.</p>'
           f'<div class="btn pri" style="width:200px;margin-top:22px">Try again</div></div>')
    if k == "B":
        inner = (f'<div class="scr"><div class="nav"></div><div class="lt"><h1>Today</h1><div class="sub">Thursday 26 Nov · <span class="status" style="color:var(--warn-ink)">{ic("alert",14)}Not loaded</span></div></div>'
                 f'<div class="body">{box}</div><div class="tabs"><span class="on">{ic("list",24)}Today</span><span>{ic("timer",24)}Focus</span></div></div>')
    elif k == "A":
        inner = (f'<div class="scr"><div class="hdr"><span class="wm">{ic("sprout",22,2)}Cadence</span><span class="date">Thursday 26 Nov</span></div>'
                 f'<div class="seg"><span class="on">{ic("list",17)}Today</span><span>{ic("timer",17)}Focus</span></div><div class="body">{box}</div></div>')
    else:
        inner = (f'<div class="scr"><div class="top"><span>Thursday 26 Nov</span><span class="status" style="color:var(--warn-ink)">{ic("alert",14)}Not loaded</span></div>'
                 f'<div class="hero" style="height:150px"><div class="moon" style="top:-60px"></div><div class="stars"></div>{plant_img("empty",100,"position:relative;z-index:2")}<div class="ledge"></div></div>{box}</div>')
    return page(o, inner, offline=True)

def s_dayboundary(o):
    k = o["key"]
    disp = 'class="disp" style="font-size:40px;font-weight:600;line-height:1.05;color:var(--primary-deep)"'
    note = banner("info", "It’s Friday now.", " Today starts with a fresh list.").replace(ic("cloudoff",18), ic("moon",18))
    body = (f'<h1 {disp}>Grew.</h1>'
            f'<p class="muted" style="font-size:16px;line-height:1.45;margin-top:8px">Plan Friday’s demo · 40-minute session<br>Started 11:50 PM Thursday · ended 12:30 AM</p>'
            f'<p style="font-size:17px;margin-top:10px">The plant joins Thursday’s grove. A session counts for the day it started.</p>'
            f'<div style="margin-top:14px">{note}</div>')
    btns = '<div class="btn pri">Go to today</div>'
    if k == "C":
        inner = (f'<div class="scr"><div class="top"><span>Friday 27 Nov</span><span class="status">{ic("check",14)}Last synced 12:30 AM</span></div>'
                 f'<div class="hero" style="height:250px"><div class="moon"></div><div class="stars"></div>{plant_img("full",170,"position:relative;z-index:2")}<div class="ledge"></div></div>'
                 f'<div style="padding:18px 22px 0">{body}</div><div style="flex:1"></div><div style="padding:0 16px 12px">{btns}</div></div>')
    else:
        bg = "linear-gradient(180deg,#FBF4EA,#F5E3C6)"
        top = (f'<div class="hdr"><span class="wm">{ic("sprout",22,2)}Cadence</span><span class="date">Friday 27 Nov</span></div>' if k == "A"
               else f'<div class="nav"><span class="tl"></span><b style="font-size:17px">Session ended</b><span style="width:20px"></span></div>')
        inner = (f'<div class="scr">{top}<div style="margin:10px 16px 0;height:230px;border-radius:16px;background:{bg};position:relative;overflow:hidden">'
                 f'<div style="position:absolute;left:50%;margin-left:-75px;bottom:12px">{plant_img("full",150)}</div><div style="position:absolute;left:0;right:0;bottom:0;height:16px;background:linear-gradient(#EADBC7,#E1CFB8)"></div></div>'
                 f'<div style="padding:18px 22px 0">{body}</div><div style="flex:1"></div><div style="padding:0 16px 12px">{btns}</div></div>')
        if k == "B": inner = inner.replace('class="disp" style="font-size:40px', 'class="disp" style="font-size:36px')
    return page(o, inner, t="12:30")

def s_sync(o):
    k = o["key"]
    sheet_rows = (f'<div class="grp" style="background:var(--bg);border-radius:14px">'
                  f'<div class="row" style="min-height:56px;padding:0 14px;display:flex;gap:12px;align-items:center">{ic("phone",20)}<span class="tt" style="flex:1">This iPhone<span class="src">2 changes waiting</span></span><span class="status">{ic("sync",14)}Syncing…</span></div>'
                  f'<div class="row" style="min-height:56px;padding:0 14px;display:flex;gap:12px;align-items:center">{ic("laptop",20)}<span class="tt" style="flex:1">MacBook<span class="src">Same OneDrive file</span></span><span class="status">{ic("check",14)}9:40 PM</span></div></div>')
    sheet = (f'<div class="scrim"></div><div style="position:absolute;left:0;right:0;bottom:0;background:var(--surface);border-radius:{"12px" if k=="B" else "24px"} {"12px" if k=="B" else "24px"} 0 0;z-index:30;padding:8px 18px 50px">'
             f'<div style="width:36px;height:5px;border-radius:3px;background:var(--line);margin:0 auto 14px"></div>'
             f'<h3 style="font-size:22px;font-weight:700" class="{"disp" if k!="B" else ""}">Sync</h3><p class="muted" style="font-size:15px;margin:4px 0 14px">Last synced 9:40 PM · Syncing 2 changes…</p>'
             f'{sheet_rows}<div class="btn out" style="margin-top:14px">{ic("sync",18)}Sync now</div></div>')
    return page(o, today_view(o, GOALS, status="syncing") + sheet)

def s_syncfail(o):
    b = banner("warn", "Couldn’t sync.", " Your changes are safe on this phone.", "Try again")
    g = [GOALS[0], (GOALS[1][0], GOALS[1][1], GOALS[1][2], True, "unsynced"), GOALS[2], GOALS[3]]
    return page(o, today_view(o, g, status="failed", banners=b, plant=None))

def s_conflict(o):
    k = o["key"]
    def card(icn, who, when, title, box, sel):
        return (f'<div style="border:{"2px solid var(--primary)" if sel else "1.5px solid var(--line)"};border-radius:14px;padding:12px 14px;margin-top:10px;background:var(--bg)">'
                f'<div class="cap" style="display:flex;gap:6px;align-items:center;font-weight:600">{ic(icn,15)}{who} · {when}</div>'
                f'<div style="font-size:17px;font-weight:600;margin-top:4px">{title}</div><div class="muted" style="font-size:15px">Time box {box}</div></div>')
    sheet = (f'<div class="scrim"></div><div style="position:absolute;left:0;right:0;bottom:0;background:var(--surface);border-radius:{"12px 12px" if k=="B" else "24px 24px"} 0 0;z-index:30;padding:8px 18px 46px">'
             f'<div style="width:36px;height:5px;border-radius:3px;background:var(--line);margin:0 auto 14px"></div>'
             f'<h3 style="font-size:22px;font-weight:700" class="{"disp" if k!="B" else ""}">Edited on both devices</h3>'
             f'<p class="muted" style="font-size:15px;margin-top:4px">Nothing is lost. Choose which version to keep.</p>'
             f'{card("laptop","On your Mac","8:12 PM","Read two papers","45 min",False)}{card("phone","On this iPhone","8:20 PM, made offline","Read one paper","30 min",True)}'
             f'<div style="display:flex;gap:10px;margin-top:14px"><div class="btn out" style="flex:1;font-size:16px">Keep Mac version</div><div class="btn pri" style="flex:1;font-size:16px">Keep iPhone version</div></div>'
             f'<div class="btn txt" style="margin:2px auto 0">Decide later</div></div>')
    g = [GOALS[0], (GOALS[1][0], GOALS[1][1], GOALS[1][2], True, "twov"), GOALS[2], GOALS[3]]
    return page(o, today_view(o, g, plant=None) + sheet)

INLINE = "This goal didn’t fit today’s 6. It’s in Parked."
MACG = ("Morning pages", "15 min", "0 / 15 min", False)
BASE5 = [SIX[0], SIX[1], SIX[2], SIX[3], SIX[5]]
def park_note_row(o):
    return parked_block(o, [("Call the bank", INLINE)], False)

def s_park_before(o):
    g = BASE5 + [("Call the bank", "", "Not yet", False, "unsynced new")]
    return page(o, today_view(o, g, status="queued", plant=None, foot=False, add_row=False), offline=False)

ANN = "#6B3FD4"
def s_park_moving(o):
    ANN = "#C4ADFF" if o["dark"] else "#6B3FD4"
    g = BASE5[:4] + [(MACG[0], MACG[1], MACG[2], False, "new"), BASE5[4]]
    ghost = parked_block(o, [("Call the bank", INLINE)], False, hint=False)
    ann = (f'<div style="position:relative;margin:8px 0 0;padding:6px 10px;border:1.5px dashed {ANN};border-radius:10px;color:{ANN};font:600 13px/1.3 Inter;background:rgba(107,63,212,.06);display:flex;gap:8px;align-items:center">'
           f'<svg width="22" height="30" style="flex:none" viewBox="0 0 22 30" fill="none" stroke="{ANN}" stroke-width="2" stroke-linecap="round"><path d="M11 2v24M4 19l7 7 7-7"/></svg>'
           f'Annotation: sync brings “Morning pages” from the Mac (earlier commit time). “Call the bank” (added offline, later) slides from today’s list into Parked, about 300 ms. The goals already showing never move.</div>')
    return page(o, today_view(o, g, status="syncing", plant=None, after=ann + '<div style="opacity:.55">' + ghost + '</div>', foot=False, add_row=False))

def s_park1(o):
    g = BASE5[:4] + [MACG, BASE5[4]]
    return page(o, today_view(o, g, plant=None, after=park_note_row(o), foot=False, add_row=False))

def s_park2(o):
    g = [BASE5[0], BASE5[1], BASE5[3], MACG, BASE5[4]]
    rem = '<div class="removed"><span>Removed Gym.</span><b>Undo</b></div>'
    return page(o, today_view(o, g, plant=None, after=rem + parked_block(o, [("Call the bank", INLINE)], True), foot=False, add_row=False))

def s_park3(o):
    g = [BASE5[0], BASE5[1], BASE5[3], MACG, BASE5[4], ("Call the bank", "", "Not yet", False, "new")]
    done = '<p class="cap" style="padding:10px 6px;display:flex;gap:6px;align-items:center">' + ic("check", 15) + 'Moved in. Parked is empty.</p>'
    return page(o, today_view(o, g, plant=None, after=done, foot=False, add_row=False))

def s_queued(o):
    g = [GOALS[0], (GOALS[1][0], GOALS[1][1], GOALS[1][2], True, "unsynced"), GOALS[2], GOALS[3], ("Call the bank", "", "Not yet", False, "unsynced")]
    return page(o, today_view(o, g, status="queued", plant=None))

def s_waiting(o):
    return page(o, today_view(o, GOALS, status="waiting", plant=None))

def s_macupdate(o):
    g = [GOALS[0], (GOALS[1][0], GOALS[1][1], GOALS[1][2], True, "unsynced"), GOALS[2], GOALS[3], ("Call the bank", "", "Not yet", False, "unsynced")]
    return page(o, today_view(o, g, status="macupdate", plant=None))

def s_clock(o):
    return page(o, today_view(o, GOALS, status="clock", plant=None))

def s_tz(o):
    return page(o, today_view(o, GOALS, tz=True), t="5:11")

def s_expired(o):
    b = banner("warn", "Sign in again to sync.", " Your Microsoft sign-in expired. Your changes are safe on this phone.", "Sign in")
    return page(o, today_view(o, GOALS, status="failed", banners=b, plant=None))

SCREENS = [
 ("01-today", "Today: goals + plant", s_today, ""),
 ("02-focus", "Running focus session", s_focus, ""),
 ("03-add-goal", "Add a goal, keyboard up", s_add, ""),
 ("04-six-goal-limit", "6-goal limit", s_six, ""),
 ("05-empty-first-run", "Empty / first run", s_empty, ""),
 ("06-loading", "Loading", s_loading, ""),
 ("07-offline", "Offline, still working", s_offline, ""),
 ("08-error", "Error with Try again", s_error, ""),
 ("09-day-boundary", "Session past midnight IST", s_dayboundary, ""),
 ("10-sync-status", "Sync: syncing / last synced", s_sync, "depends on sync decision"),
 ("11-sync-failed", "Sync failed", s_syncfail, "depends on sync decision"),
 ("12-conflict", "Edited on both devices", s_conflict, "depends on sync decision"),
 ("13-parked-a-before-sync", "Parked 1/5: offline goal showing", s_park_before, "depends on sync decision"),
 ("14-parked-b-moving", "Parked 2/5: sync moves it (annotated)", s_park_moving, "depends on sync decision"),
 ("15-parked-c-move-in-disabled", "Parked 3/5: Move in disabled at 6", s_park1, ""),
 ("16-parked-d-move-in-enabled", "Parked 4/5: after removing one", s_park2, ""),
 ("17-parked-e-moved-in", "Parked 5/5: after Move in", s_park3, ""),
 ("18-sign-in-expired", "Sign-in expired", s_expired, "depends on sync decision"),
 ("19-sync-queued", "Queued: waiting to upload", s_queued, "depends on sync decision"),
 ("20-waiting-for-mac", "Uploaded, waiting for your Mac", s_waiting, "depends on sync decision"),
 ("21-mac-needs-update", "Mac needs update (older schema)", s_macupdate, "depends on sync decision"),
 ("22-not-ist-hint", "Phone not on IST", s_tz, ""),
 ("23-phone-clock-off", "Phone clock off by >5 min", s_clock, "depends on sync decision"),
]
