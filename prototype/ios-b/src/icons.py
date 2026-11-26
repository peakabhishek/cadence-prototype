import pathlib, base64
from playwright.sync_api import sync_playwright
HERE=pathlib.Path(__file__).resolve().parent; OUT=HERE.parent
svg=(HERE.parent.parent.parent/"design/ios-54/src/plants/full.svg").read_bytes()
uri="data:image/svg+xml;base64,"+base64.b64encode(svg).decode()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
    for size,name in [(180,"icon-180.png"),(192,"icon-192.png"),(512,"icon-512.png")]:
        pg=b.new_page(viewport={"width":size,"height":size})
        pg.set_content(f'<body style="margin:0;background:#F7F0E6;display:flex;align-items:center;justify-content:center;width:{size}px;height:{size}px"><img src="{uri}" style="height:78%;width:auto"></body>')
        pg.wait_for_timeout(200); pg.screenshot(path=str(OUT/name)); pg.close()
