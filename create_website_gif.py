"""
create_website_gif.py
Captures a smooth scroll-through of https://www.dmcdjcanada.com/
and exports it as an animated GIF for mockup use.
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw

# ── CONFIG ──────────────────────────────────────────────────────────────────
URL         = "https://www.dmcdjcanada.com/"
OUT_DIR     = Path(r"C:\Users\12124\Documents\Robert-Vanliew-Website\gif_frames")
GIF_PATH    = Path(r"C:\Users\12124\Documents\Robert-Vanliew-Website\dmcdjcanada_mockup.gif")

# Viewport – 1440×900 looks great for desktop mockups
VP_WIDTH    = 1440
VP_HEIGHT   = 900

# How many pixels to scroll per step
SCROLL_STEP = 80          # smaller = smoother
PAUSE_MS    = 60          # ms between each scroll step (lower = faster gif)

# GIF frame duration in ms  (100 = 10 fps)
FRAME_DURATION_MS = 80

# Resize frames to this width for a reasonable GIF file size
GIF_WIDTH   = 1200
# --------------------------------------------------------------------------


async def capture_frames():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # clear any previous frames
    for f in OUT_DIR.glob("frame_*.png"):
        f.unlink()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": VP_WIDTH, "height": VP_HEIGHT},
            device_scale_factor=1,
        )
        page = await context.new_page()

        print(f"[1/4] Loading {URL} …")
        await page.goto(URL, wait_until="networkidle", timeout=30000)
        # Wait extra for animations to settle
        await page.wait_for_timeout(2000)

        # Get total scroll height
        total_height = await page.evaluate("document.body.scrollHeight")
        print(f"[2/4] Page height: {total_height}px — capturing frames …")

        frame_idx = 0
        current_y  = 0

        # ── HOLD at top for ~1 second ──
        for _ in range(12):
            path = OUT_DIR / f"frame_{frame_idx:04d}.png"
            await page.screenshot(path=str(path), clip={
                "x": 0, "y": 0,
                "width": VP_WIDTH,
                "height": VP_HEIGHT,
            })
            frame_idx += 1

        # ── SCROLL DOWN ──
        while current_y < total_height - VP_HEIGHT:
            current_y = min(current_y + SCROLL_STEP, total_height - VP_HEIGHT)
            await page.evaluate(f"window.scrollTo(0, {current_y})")
            await page.wait_for_timeout(PAUSE_MS)

            path = OUT_DIR / f"frame_{frame_idx:04d}.png"
            await page.screenshot(path=str(path), clip={
                "x": 0, "y": 0,
                "width": VP_WIDTH,
                "height": VP_HEIGHT,
            })
            frame_idx += 1

        # ── HOLD at bottom for ~1.5 seconds ──
        for _ in range(18):
            path = OUT_DIR / f"frame_{frame_idx:04d}.png"
            await page.screenshot(path=str(path), clip={
                "x": 0, "y": 0,
                "width": VP_WIDTH,
                "height": VP_HEIGHT,
            })
            frame_idx += 1

        await browser.close()
        print(f"[3/4] Captured {frame_idx} frames.")
        return frame_idx


def assemble_gif(frame_count: int):
    print("[4/4] Assembling GIF …")
    frames = sorted(OUT_DIR.glob("frame_*.png"))

    pil_frames = []
    for fp in frames:
        img = Image.open(fp).convert("RGB")
        # Resize proportionally to GIF_WIDTH
        ratio = GIF_WIDTH / img.width
        new_h = int(img.height * ratio)
        img = img.resize((GIF_WIDTH, new_h), Image.LANCZOS)
        # Convert to P mode (palette) for GIF
        img = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
        pil_frames.append(img)

    pil_frames[0].save(
        str(GIF_PATH),
        format="GIF",
        save_all=True,
        append_images=pil_frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,          # loop forever
        optimize=True,
    )
    size_mb = GIF_PATH.stat().st_size / 1_048_576
    print(f"✅  GIF saved → {GIF_PATH}")
    print(f"    Size: {size_mb:.1f} MB  |  Frames: {len(pil_frames)}  |  Resolution: {pil_frames[0].size[0]}×{pil_frames[0].size[1]}")


async def main():
    frame_count = await capture_frames()
    assemble_gif(frame_count)


if __name__ == "__main__":
    asyncio.run(main())
