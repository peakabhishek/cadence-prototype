import sys, pathlib, time, json
from playwright.sync_api import sync_playwright
OUT = pathlib.Path(__file__).resolve().parent.parent / "screens"; OUT.mkdir(exist_ok=True)
URL = "file://" + str(pathlib.Path(__file__).resolve().parent.parent / "index.html")
INTER = "html,body,button,input{font-family:Inter,-apple-system,sans-serif !important}"
errs = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    def ctx(**kw):
        c = b.new_context(viewport={"width":390,"height":844}, device_scale_factor=3, is_mobile=True, has_touch=True, timezone_id="Asia/Kolkata", **kw)
        pg = c.new_page(); pg.set_default_timeout(5000); pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
        return c, pg
    def shot(pg, name):
        pg.wait_for_timeout(450); pg.screenshot(path=str(OUT/f"{name}.png"))
    c, pg = ctx()
    def go(q=""):
        pg.goto(URL+"?frame=1"+q); pg.evaluate("localStorage.clear()"); pg.goto(URL+"?frame=1"+q); pg.add_style_tag(content=INTER)
    def js(code): return pg.evaluate(code)
    def tap(sel): pg.locator(sel).first.click()
    go(); shot(pg,"01-today")
    tap('[data-act=tick][data-id="3"]'); shot(pg,"02-today-ticked")
    tap('[data-act=add]'); pg.wait_for_timeout(300); shot(pg,"03-add-sheet-empty")
    pg.fill('#gtitle',"Reply to Priya"); tap('[data-b="25"]'); shot(pg,"04-add-sheet-filled")
    tap('#addbtn'); shot(pg,"05-today-added")
    go("&fakekb=1"); tap('[data-act=add]'); pg.fill('#gtitle',"Reply to Priya"); shot(pg,"06-add-sheet-keyboard")
    # six limit
    go(); js("__cadence.scn('six')"); shot(pg,"07-six-goals"); tap('[data-act=add]'); shot(pg,"08-six-goals-add-blocked")
    # focus
    go(); tap('.tabs [data-tab=focus]'); shot(pg,"09-focus-pick")
    tap('[data-d="1"]'); tap('[data-act=begin]'); pg.wait_for_timeout(1200); shot(pg,"10-session-live")
    # background: shift clock by rewriting startedAt (simulating 30s lock)
    t0 = pg.inner_text('#tm'); js("(function(){var s=__cadence.S();s.session.startedAt-=30000;})()"); pg.wait_for_timeout(500); t1 = pg.inner_text('#tm'); print("timer", t0, "->", t1)
    shot(pg,"11-session-after-30s-away")
    tap('[data-act=giveup]'); shot(pg,"12-giveup-confirm"); tap('[data-act=giveup-yes]'); shot(pg,"13-gave-up")
    tap('[data-act=try-again]'); tap('[data-d="1"]'); tap('[data-act=begin]'); js("(function(){var s=__cadence.S();s.session.startedAt-=61000;})()"); pg.wait_for_timeout(600); shot(pg,"14-grew")
    tap('[data-act=go-today]'); shot(pg,"15-today-after-grew")
    # reload persistence
    pg.reload(); pg.add_style_tag(content=INTER); shot(pg,"16-reload-persisted")
    # parked sequence
    go(); js("__cadence.scn('menu')") if False else None
    tap('[data-act=menu]'); shot(pg,"17-states-menu"); tap('[data-k=parked]'); tap('[data-act=sheet-close]') if pg.locator('.sheet').count() else None
    shot(pg,"18-parked-1-offline-added")
    tap('[data-act=syncsheet]'); shot(pg,"19-sync-sheet"); tap('[data-act=sync-now]'); pg.wait_for_timeout(200); shot(pg,"20-syncing"); pg.wait_for_timeout(1500)
    shot(pg,"21-parked-2-move-in-disabled")
    print("movein disabled:", pg.locator('.pk').first.get_attribute('aria-disabled'))
    pg.locator('.pk').first.click(force=True); print("tap while disabled count goals:", js("__cadence.S().goals.length"))
    js("document.querySelector('[data-act=remove][data-id=\"3\"]').click()"); pg.wait_for_timeout(300); shot(pg,"22-parked-3-removed-slot-free")
    tap('.pk'); pg.wait_for_timeout(400); shot(pg,"23-parked-4-moved-in")
    go(); bb=pg.locator('.swipe .row').nth(2).bounding_box()
    pg.mouse.move(bb['x']+250,bb['y']+20); pg.mouse.down(); pg.mouse.move(bb['x']+200,bb['y']+22,steps=4); pg.mouse.move(bb['x']+120,bb['y']+22,steps=6); pg.mouse.up(); shot(pg,"24-swipe-remove-open")
    tap('[data-act=remove][data-id="3"]'); shot(pg,"25-removed-undo"); print('after remove goals', js("__cadence.S().goals.length")); tap('[data-act=undo]'); print('after undo', js("__cadence.S().goals.length"))
    # states
    states = ["empty","loading","error","offline","syncing","queued","waiting","macupdate","syncheld","failed","conflict","expired","clock","tz","midnight","newday","firstrun"]
    for i,k in enumerate(states):
        go(); js(f"__cadence.scn('{k}')"); shot(pg, f"s{i+1:02d}-{k}")
    go(); js("__cadence.scn('conflict')"); tap('[data-act=decide-later]'); shot(pg,"s11b-conflict-decide-later"); tap('[data-act=conflict-open]'); tap('[data-act=keep-mac]'); shot(pg,"s11c-conflict-keep-mac")
    c.close()
    # auto tz hint
    c2, pg = ctx(); c2.close() if False else None
    c3 = b.new_context(viewport={"width":390,"height":844}, device_scale_factor=3, is_mobile=True, has_touch=True, timezone_id="America/New_York")
    pg3 = c3.new_page(); pg3.goto(URL+"?frame=1"); pg3.add_style_tag(content=INTER); pg3.wait_for_timeout(400); print("tz hint auto:", pg3.locator('.tzh').count()); pg3.screenshot(path=str(OUT/"s14b-tz-auto-detected.png"))
    b.close()
print("errors:", errs)
