"""capture_mobile.py — captures mobile scroll frames at 390x844 (iPhone 14 size)"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

URL         = "https://www.dmcdjcanada.com/"
OUT_DIR     = Path(r"C:\Users\12124\Documents\Robert-Vanliew-Website\mobile_frames")
VP_W, VP_H  = 390, 844
SCROLL_STEP = 60
PAUSE_MS    = 60

async def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for f in OUT_DIR.glob("frame_*.png"): f.unlink()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": VP_W, "height": VP_H},
            device_scale_factor=2,      # retina
            is_mobile=True,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"
        )
        page = await ctx.new_page()
        await page.goto(URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)

        total_h = await page.evaluate("document.body.scrollHeight")
        print(f"Mobile page height: {total_h}px")

        idx = 0
        def snap():
            nonlocal idx
            path = OUT_DIR / f"frame_{idx:04d}.png"
            return str(path), idx

        # Hold at top
        for _ in range(10):
            p_str, i = snap()
            await page.screenshot(path=p_str, clip={"x":0,"y":0,"width":VP_W,"height":VP_H})
            idx += 1

        cur_y = 0
        while cur_y < total_h - VP_H:
            cur_y = min(cur_y + SCROLL_STEP, total_h - VP_H)
            await page.evaluate(f"window.scrollTo(0,{cur_y})")
            await page.wait_for_timeout(PAUSE_MS)
            p_str, i = snap()
            await page.screenshot(path=p_str, clip={"x":0,"y":0,"width":VP_W,"height":VP_H})
            idx += 1

        # Hold at bottom
        for _ in range(15):
            p_str, i = snap()
            await page.screenshot(path=p_str, clip={"x":0,"y":0,"width":VP_W,"height":VP_H})
            idx += 1

        await browser.close()
        print(f"Captured {idx} mobile frames")

asyncio.run(main())
