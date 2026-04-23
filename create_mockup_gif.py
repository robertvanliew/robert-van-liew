"""
create_mockup_gif.py
────────────────────
Takes the captured website scroll frames and composites them inside a
stylish MacBook-style laptop frame, producing an animated GIF perfect
for the case study mockup section.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

# ── PATHS ────────────────────────────────────────────────────────────────
FRAMES_DIR = Path(r"C:\Users\12124\Documents\Robert-Vanliew-Website\gif_frames")
OUT_GIF    = Path(r"C:\Users\12124\Documents\Robert-Vanliew-Website\images\dmc_mockup_animated.gif")

# ── OUTPUT SIZE ───────────────────────────────────────────────────────────
# Final GIF canvas size (the full laptop image)
CANVAS_W = 1400
CANVAS_H = 900

# ── LAPTOP FRAME GEOMETRY ─────────────────────────────────────────────────
# Laptop body (the display lid) takes up most of the canvas
LID_X      = 60        # left edge of lid from canvas left
LID_Y      = 30        # top edge of lid from canvas top
LID_W      = CANVAS_W - LID_X * 2   # 1280
LID_H      = int(LID_W * 0.627)     # 16:10-ish display ratio → ~802

BEZEL      = 18        # uniform bezel so it looks like >16:10 laptop
URL_BAR_H  = 38        # browser chrome at top of screen

# Screen area (where website renders) inside the lid
SCREEN_X   = LID_X + BEZEL
SCREEN_Y   = LID_Y + BEZEL + URL_BAR_H
SCREEN_W   = LID_W - BEZEL * 2
SCREEN_H   = LID_H - BEZEL * 2 - URL_BAR_H

# ── COLOURS ──────────────────────────────────────────────────────────────
BG          = (22, 24, 30)        # dark page background
FRAME_DARK  = (28, 28, 30)        # laptop lid outer colour
FRAME_MID   = (44, 44, 46)        # lid rim / thin inner edge
CHROME_BG   = (30, 30, 32)        # browser tab bar  
CHROME_CTRL = (58, 58, 60)        # browser address bar
ADDRESS_TXT = (160, 160, 165)
DOT_R       = (255, 95,  86)
DOT_Y       = (255, 189, 46)
DOT_G       = (39,  201, 63)
NOTCH_COL   = (18, 18, 18)        # camera notch

# Stand (trapezoid below the lid)
STAND_TOP_W  = int(LID_W * 0.30)
STAND_BOT_W  = int(LID_W * 0.55)
STAND_H      = 22
STAND_Y      = LID_Y + LID_H
STAND_TOP_X  = LID_X + (LID_W - STAND_TOP_W) // 2
STAND_BOT_X  = LID_X + (LID_W - STAND_BOT_W) // 2

# Base bar
BASE_H  = 12
BASE_Y  = STAND_Y + STAND_H
BASE_X  = LID_X - 40
BASE_W  = LID_W + 80

# ── TIMING ───────────────────────────────────────────────────────────────
# Source frames - pick every Nth to control speed
FRAME_SKIP    = 1        # 1 = use every frame, 2 = every other …
HOLD_FRAMES   = 10       # extra hold at start and end
FRAME_DURATION_MS = 80   # ms per frame in final GIF


def draw_laptop_frame(canvas: Image.Image):
    """Draw the MacBook-style frame onto *canvas* (modifies in-place)."""
    d = ImageDraw.Draw(canvas)

    # ── Lid (display housing) ──
    r = 14  # corner radius
    d.rounded_rectangle(
        [LID_X, LID_Y, LID_X + LID_W, LID_Y + LID_H],
        radius=r, fill=FRAME_DARK, outline=FRAME_MID, width=2
    )

    # ── Bezel inside lid ──
    d.rectangle(
        [LID_X + 6, LID_Y + 6, LID_X + LID_W - 6, LID_Y + LID_H - 6],
        fill=FRAME_DARK
    )

    # ── Camera notch (top-center, small rectangle) ──
    notch_w, notch_h = 80, 20
    notch_x = LID_X + (LID_W - notch_w) // 2
    notch_y = LID_Y
    d.rounded_rectangle(
        [notch_x, notch_y, notch_x + notch_w, notch_y + notch_h],
        radius=6, fill=NOTCH_COL
    )
    # camera dot
    cam_r = 4
    cam_cx = notch_x + notch_w // 2
    cam_cy = notch_y + notch_h // 2
    d.ellipse([cam_cx - cam_r, cam_cy - cam_r, cam_cx + cam_r, cam_cy + cam_r],
              fill=(40, 40, 42))

    # ── Browser chrome (tab bar + address bar) ──
    chrome_top = LID_Y + BEZEL
    chrome_bot = SCREEN_Y
    d.rectangle(
        [SCREEN_X, chrome_top, SCREEN_X + SCREEN_W, chrome_bot],
        fill=CHROME_BG
    )

    # ── Traffic lights ──
    dot_y   = chrome_top + 14
    dot_size = 7
    for i, col in enumerate([DOT_R, DOT_Y, DOT_G]):
        cx = SCREEN_X + 18 + i * 22
        d.ellipse([cx - dot_size, dot_y - dot_size, cx + dot_size, dot_y + dot_size], fill=col)

    # ── Address bar ──
    ab_x = SCREEN_X + 90
    ab_y = chrome_top + 5
    ab_w = SCREEN_W - 120
    ab_h = URL_BAR_H - 10
    d.rounded_rectangle(
        [ab_x, ab_y, ab_x + ab_w, ab_y + ab_h],
        radius=6, fill=CHROME_CTRL
    )
    # URL text (small, centered in bar)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
    except Exception:
        font = ImageFont.load_default()
    d.text(
        (ab_x + 12, ab_y + (ab_h - 13)//2 + 1),
        "dmcdjcanada.com", fill=ADDRESS_TXT, font=font
    )

    # ── Stand (trapezoid) ──
    stand_pts = [
        (STAND_TOP_X, STAND_Y),
        (STAND_TOP_X + STAND_TOP_W, STAND_Y),
        (STAND_BOT_X + STAND_BOT_W, STAND_Y + STAND_H),
        (STAND_BOT_X, STAND_Y + STAND_H),
    ]
    d.polygon(stand_pts, fill=FRAME_MID)

    # ── Base bar ──
    d.rounded_rectangle(
        [BASE_X, BASE_Y, BASE_X + BASE_W, BASE_Y + BASE_H],
        radius=4, fill=FRAME_MID
    )


def make_frame(site_frame: Image.Image, frame_img: Image.Image) -> Image.Image:
    """
    Composite *site_frame* (the website screenshot) into the laptop screen
    on *frame_img* (the pre-drawn laptop with blank screen).
    Returns a new RGBA image.
    """
    canvas = frame_img.copy()

    # Resize website frame to fit the screen exactly
    site_resized = site_frame.resize((SCREEN_W, SCREEN_H), Image.LANCZOS)

    # Paste website into screen area
    canvas.paste(site_resized, (SCREEN_X, SCREEN_Y))
    return canvas


def build_gif():
    print("Building laptop mockup GIF...")

    # 1. Load all source frames
    source_files = sorted(FRAMES_DIR.glob("frame_*.png"))
    print(f"  Found {len(source_files)} source frames")

    # 2. Pre-draw the empty laptop frame (reused every frame)
    base = Image.new("RGBA", (CANVAS_W, CANVAS_H), BG)
    draw_laptop_frame(base)
    print(f"  Screen area: {SCREEN_W}x{SCREEN_H} at ({SCREEN_X},{SCREEN_Y})")

    # 3. Composite each website frame into the laptop
    gif_frames: list[Image.Image] = []

    def add_frame(site_img: Image.Image, count: int = 1):
        f = make_frame(site_img, base)
        f_rgb = f.convert("RGB")
        for _ in range(count):
            gif_frames.append(f_rgb.quantize(colors=220, method=Image.Quantize.MEDIANCUT))

    # Hold on first frame
    first_img = Image.open(source_files[0]).convert("RGB")
    add_frame(first_img, count=HOLD_FRAMES)

    # Scroll frames
    for i, fp in enumerate(source_files):
        if i % FRAME_SKIP != 0:
            continue
        site = Image.open(fp).convert("RGB")
        add_frame(site, count=1)

    # Hold on last frame
    last_img = Image.open(source_files[-1]).convert("RGB")
    add_frame(last_img, count=HOLD_FRAMES)

    print(f"  Total GIF frames: {len(gif_frames)}")

    # 4. Save GIF
    OUT_GIF.parent.mkdir(parents=True, exist_ok=True)
    gif_frames[0].save(
        str(OUT_GIF),
        format="GIF",
        save_all=True,
        append_images=gif_frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=True,
    )
    size_mb = OUT_GIF.stat().st_size / 1_048_576
    print(f"  Saved: {OUT_GIF}")
    print(f"  Size: {size_mb:.1f} MB | Frames: {len(gif_frames)} | Canvas: {CANVAS_W}x{CANVAS_H}")


if __name__ == "__main__":
    build_gif()
