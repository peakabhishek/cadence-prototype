import json, os, sys, time, socket, subprocess, tempfile, shutil
from pathlib import Path
import capture as C
from playwright.sync_api import sync_playwright
out={}
def serve(label, held):
    tmp=Path(tempfile.mkdtemp()); folder=tmp/"OneDrive - Peak Routine"/"Cadence"; folder.mkdir(parents=True)
    (tmp/"cfg").mkdir(); (tmp/"cfg"/"config.json").write_text(json.dumps({"data_dir":str(folder)}))
    tree=C.TREES[label]; C.seed(tree,folder,held,True); port=C.free_port()
    env=dict(os.environ,CADENCE_CONFIG_DIR=str(tmp/"cfg"),CADENCE_SUGGESTED_DIR=str(folder),CADENCE_PORT=str(port),CADENCE_QUIET="1")
    proc=subprocess.Popen([sys.executable,str(tree/"server"/"cadence_server.py")],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,cwd=str(tree))
    for _ in range(50):
        try: socket.create_connection(("127.0.0.1",port),0.2).close(); break
        except OSError: time.sleep(0.2)
    return proc,port,tmp
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
    for label,held,name in (("before",None,"normal"),("after",None,"normal"),("after",[1,2,3],"held3")):
        proc,port,tmp=serve(label,held)
        try:
            ctx=b.new_context(viewport={"width":1440,"height":854},device_scale_factor=2,timezone_id="Asia/Kolkata"); pg=ctx.new_page()
            for tab in ("today","focus","week"):
                pg.goto("http://127.0.0.1:%d/#%s"%(port,tab)); pg.wait_for_selector("body[data-loaded]"); pg.wait_for_timeout(700)
                n=pg.evaluate("document.querySelectorAll('.sync-note').length")
                out["%s/%s/%s notes"%(label,name,tab)]=n
                if tab=="today":
                    cta=pg.evaluate("(()=>{const e=document.querySelector('.btn.primary.start');const r=e.getBoundingClientRect();return {top:Math.round(r.top),bottom:Math.round(r.bottom),vh:innerHeight,scrollH:document.documentElement.scrollHeight}})()")
                    out["%s/%s/today cta"%(label,name)]=cta
                    pg.screenshot(path="/workspace/design-review-55/%s/1440x854-today-%s.png"%(label,name))
                    pg.screenshot(path="/workspace/design-review-55/%s/1440x854-today-%s-fullpage.png"%(label,name),full_page=True)
            ctx.close()
        finally:
            proc.terminate(); shutil.rmtree(tmp,ignore_errors=True)
    # phone banner with a Dynamic Island inset emulated
    proc,port,tmp=serve("after",None)
    try:
        for inset in (47,54):
            ctx=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,timezone_id="Asia/Kolkata"); pg=ctx.new_page()
            pg.add_init_script("window.Capacitor={isNativePlatform:function(){return true;}};window.CADENCE_CONFIG={phoneStore:'mock-onedrive'};")
            pg.goto("http://127.0.0.1:%d/#today"%port); pg.wait_for_selector("#demo-banner"); pg.wait_for_timeout(500)
            pg.add_style_tag(content=":root{--ios-safe-top:%dpx}"%inset); pg.wait_for_timeout(200)
            m=pg.evaluate("""()=>{const e=document.getElementById('demo-banner');const c=getComputedStyle(e);const r=e.getBoundingClientRect();
              const nxt=e.nextElementSibling.getBoundingClientRect();
              return {rect:[r.x,r.y,r.width,r.height],bg:c.backgroundColor,color:c.color,font:c.fontSize+'/'+c.lineHeight+' '+c.fontWeight+' '+c.fontFamily.slice(0,40),radius:c.borderRadius,align:c.textAlign,nextTop:nxt.top,role:e.getAttribute('role'),text:e.innerText,btns:e.querySelectorAll('button').length}}""")
            out["phone inset %d banner"%inset]=m
            pg.screenshot(path="/workspace/design-review-55/after/phone-390-demo-banner-inset%d.png"%inset)
            ctx.close()
    finally:
        proc.terminate(); shutil.rmtree(tmp,ignore_errors=True)
    b.close()
json.dump(out,open("extra2-results.json","w"),indent=1)
print(json.dumps(out,indent=1))
