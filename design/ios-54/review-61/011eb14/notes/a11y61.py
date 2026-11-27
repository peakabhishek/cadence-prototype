import sys, json
sys.argv=['x','/workspace/design-review-61/build-a11y']
import importlib.util
spec=importlib.util.spec_from_file_location('c61','/workspace/design-review-61/capture61.py'); c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
from playwright.sync_api import sync_playwright
DESC="""() => { const e=document.activeElement; if(!e) return null; const r=e.closest('#review-root')?'sheet':(e.closest('#review-toast')?'toast':'page'); return r+': '+e.tagName.toLowerCase()+(e.dataset&&e.dataset.act?'[act='+e.dataset.act+']':'')+' "'+(e.textContent||'').trim().slice(0,28)+'" aria="'+(e.getAttribute('aria-label')||'')+'"'; }"""
out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]); h=c.H(p,b)
    pg=h.start(c.three(), c.at(2026,11,27,14,0))
    link=pg.locator('.today .sync-note [data-act="review"]')
    link.focus(); out['link_tag']=pg.evaluate("document.activeElement.tagName+' '+document.activeElement.textContent")
    pg.keyboard.press('Enter'); pg.wait_for_selector('#review-root .sheet'); pg.wait_for_timeout(600)
    out['after_open_focus']=pg.evaluate(DESC)
    out['dialog_attrs']=pg.evaluate("""()=>{const s=document.querySelector('#review-root .sheet');const sc=document.querySelector('#review-root .scrim');return {role:s.getAttribute('role'),modal:s.getAttribute('aria-modal'),labelledby:s.getAttribute('aria-labelledby'),describedby:s.getAttribute('aria-describedby'),tabindex:s.getAttribute('tabindex'),scrimRole:sc&&sc.getAttribute('role'), shellInert:[...document.querySelectorAll('[inert]')].map(e=>e.id||e.tagName), rootLive:document.querySelector('#review-toast').getAttribute('role')+'/'+document.querySelector('#review-toast').getAttribute('aria-live')}}""")
    tabs=[]
    for i in range(14):
        pg.keyboard.press('Tab'); tabs.append(pg.evaluate(DESC))
    out['tab_order']=tabs
    sh=[]
    for i in range(3):
        pg.keyboard.press('Shift+Tab'); sh.append(pg.evaluate(DESC))
    out['shift_tab']=sh
    # focus ring screenshot
    pg.keyboard.press('Tab'); pg.wait_for_timeout(100)
    out['focus_outline']=pg.evaluate("(()=>{const e=document.activeElement;const s=getComputedStyle(e);return s.outlineStyle+' '+s.outlineWidth+' '+s.outlineColor+' offset '+s.outlineOffset})()")
    pg.screenshot(path='/workspace/design-review-61/build/focus-ring.png')
    # Esc
    pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    out['esc_closed']=pg.query_selector('#review-root .sheet') is None
    out['esc_focus']=pg.evaluate(DESC)
    # scrim click
    pg.locator('.today .sync-note [data-act="review"]').click(); pg.wait_for_selector('#review-root .sheet'); pg.wait_for_timeout(500)
    pg.mouse.click(30,450); pg.wait_for_timeout(400)
    out['scrim_closed']=pg.query_selector('#review-root .sheet') is None
    out['scrim_focus']=pg.evaluate(DESC)
    # sheet click doesn't close
    pg.locator('.today .sync-note [data-act="review"]').click(); pg.wait_for_selector('#review-root .sheet'); pg.wait_for_timeout(500)
    pg.mouse.click(720,300); pg.wait_for_timeout(300); out['inside_click_stays_open']=pg.query_selector('#review-root .sheet') is not None
    # keyboard resolve: Use on first group, then focus handling + toast reachability
    pg.wait_for_function("()=>!document.querySelector('#review-root [aria-busy=\"true\"]')")
    pg.locator('#review-root [data-act="keep"]').first.focus(); pg.keyboard.press('Enter'); pg.wait_for_timeout(500)
    out['after_resolve_focus']=pg.evaluate(DESC)
    out['toast_visible']=pg.query_selector('#review-toast:not([hidden])') is not None
    t=[]
    for i in range(12):
        pg.keyboard.press('Tab'); t.append(pg.evaluate(DESC))
    out['tab_after_resolve']=t
    out['toast_inert?']=pg.evaluate("document.querySelector('#review-toast').closest('[inert]')!==null")
    # close via x then bg scroll lock
    out['body_overflow_open']=pg.evaluate("getComputedStyle(document.body).overflow")
    # reduced motion + spinner
    # last-resolve: close all, focus where
    h.stop(); 
    # 200% zoom / small viewport: 800x600
    ctx=b.new_context(viewport={"width":800,"height":560},device_scale_factor=1,timezone_id="Asia/Kolkata"); 
    b.close()
print(json.dumps(out,indent=1,ensure_ascii=False))
