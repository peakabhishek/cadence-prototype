import sys, pathlib, asyncio
from playwright.async_api import async_playwright
OUT = pathlib.Path(__file__).resolve().parent.parent
TMP = pathlib.Path("/workspace/ios54-tmp"); TMP.mkdir(exist_ok=True)

async def render_all(jobs, w=390, h=844):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2)
        pg = await ctx.new_page()
        for path, html, *size in jobs:
            if size: await pg.set_viewport_size({"width": size[0], "height": size[1]})
            else: await pg.set_viewport_size({"width": w, "height": h})
            f = TMP / (pathlib.Path(path).stem + ".html"); f.write_text(html)
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(150)
            pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
            await pg.screenshot(path=str(path))
        await b.close()
