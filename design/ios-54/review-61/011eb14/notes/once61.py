import sys, json
sys.argv=['x','/workspace/design-review-61/build-a11y']
import importlib.util
spec=importlib.util.spec_from_file_location('c61','/workspace/design-review-61/capture61.py'); c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
from playwright.sync_api import sync_playwright
N=lambda pg:" ".join(pg.inner_text(".today .sync-note").split()) if pg.query_selector(".today .sync-note") else None
out={}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]); h=c.H(p,b)
    pg=h.start(c.upgrade(), c.at(2026,11,27,23,58))
    out['first']=N(pg)
    pg.reload(); pg.wait_for_selector("body[data-loaded='true']"); pg.wait_for_timeout(300); out['after_reload_unacked']=N(pg)
    h.srv_clock(c.at(2026,11,28,0,3)); pg.reload(); pg.wait_for_selector("body[data-loaded='true']"); pg.wait_for_timeout(300); out['after_midnight_reload']=N(pg)
    pg.click('.today .sync-note [data-act="gotit"]'); pg.wait_for_timeout(500); out['after_gotit']=N(pg)
    pg.reload(); pg.wait_for_selector("body[data-loaded='true']"); pg.wait_for_timeout(300); out['after_gotit_reload']=N(pg)
    h.stop(); b.close()
print(json.dumps(out,indent=1,ensure_ascii=False))
