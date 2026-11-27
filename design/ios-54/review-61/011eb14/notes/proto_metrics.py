import json,subprocess,time,sys
from playwright.sync_api import sync_playwright
js=open('/workspace/design-review-61/metrics.js').read()
srv=subprocess.Popen(['python3','-m','http.server','8799','--bind','127.0.0.1'],cwd='/workspace/proto-d60c889',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
out={}
try:
  with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
    pg=b.new_context(viewport={"width":1440,"height":900},device_scale_factor=2,timezone_id="Asia/Kolkata").new_page()
    for st in ["one","many","error","loading","mixed","empty","remove-restore","undo-all"]:
        pg.goto("http://127.0.0.1:8799/prototype/mac-review/?state=%s&frame=1"%st); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(600)
        out[st]=pg.evaluate(js)
    b.close()
finally: srv.terminate()
json.dump(out,open('/workspace/design-review-61/proto-metrics.json','w'),indent=1)
