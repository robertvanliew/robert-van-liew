"""
create_mockup_video.py
──────────────────────
Renders each website scroll frame inside a crisp MacBook-style laptop frame
using Pillow (full RGB – no palette quantization), then encodes them with
ffmpeg into a high-quality MP4 (H.264) + WebM (VP9) for lossless-looking
results in the case study mockup section.
"""

import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── PATHS ──────────────────────────────────────────────────────────────────
FRAMES_DIR  = Path(r"C:\Users\12124\Documents\Robert-Vanliew-Website\gif_frames")
RENDER_DIR  = Path(r"C:\Users\12124\Documents\Robert-Vanliew-Website\render_frames")
OUT_MP4     = Path(r"C:\Users\12124\Documents\Robert-Vanliew-Website\images\dmc_mockup.mp4")
OUT_WEBM    = Path(r"C:\Users\12124\Documents\Robert-Vanliew-Website\images\dmc_mockup.webm")

# ── CANVAS ────────────────────────────────────────────────────────────────
# Must be even numbers (H.264 requirement)
CANVAS_W = 1400
CANVAS_H = 900

# ── LAPTOP GEOMETRY ───────────────────────────────────────────────────────
LID_X  = 60
LID_Y  = 30
LID_W  = CANVAS_W - LID_X * 2   # 1280
LID_H  = int(LID_W * 0.627)     # ≈ 802

BEZEL      = 20
URL_BAR_H  = 40

SCREEN_X = LID_X + BEZEL
SCREEN_Y = LID_Y + BEZEL + URL_BAR_H
SCREEN_W = LID_W - BEZEL * 2
SCREEN_H = LID_H - BEZEL * 2 - URL_BAR_H

# ── COLOURS (full RGB, no palette limits!) ───────────────────────────────
BG          = (22,  24,  30)
FRAME_OUTER = (36,  36,  38)
FRAME_INNER = (52,  52,  56)
FRAME_EDGE  = (70,  70,  75)
CHROME_BG   = (28,  28,  30)
CHROME_BAR  = (48,  48,  52)
ADDR_BG     = (58,  58,  62)
ADDR_TXT    = (160, 160, 165)
DOT_R       = (255, 95,  86)
DOT_Y       = (255, 189, 46)
DOT_G       = (39,  201, 63)
NOTCH_COL   = (20,  20,  22)
STAND_COL   = (58,  58,  62)
BASE_COL    = (64,  64,  68)
SCREEN_CORN = (12,  12,  14)   # Inner screen corner fill

# Stand
STAND_TOP_W = int(LID_W * 0.28)
STAND_BOT_W = int(LID_W * 0.52)
STAND_H     = 24
STAND_Y     = LID_Y + LID_H
STAND_TOP_X = LID_X + (LID_W - STAND_TOP_W) // 2
STAND_BOT_X = LID_X + (LID_W - STAND_BOT_W) // 2
BASE_H      = 14
BASE_Y      = STAND_Y + STAND_H
BASE_X      = LID_X - 50
BASE_W      = LID_W + 100

# ── VIDEO SETTINGS ────────────────────────────────────────────────────────
FPS         = 24
HOLD_SEC    = 1.2   # seconds to hold at top and bottom
HOLD_FRAMES = int(HOLD_SEC * FPS)
FRAME_SKIP  = 1     # use every frame (75 frames ÷ 1 ≈ 3-4 sec scroll)


def draw_laptop_frame(canvas: Image.Image) -> None:
    """Draw a crisp, anti-aliased MacBook frame onto canvas."""
    d = ImageDraw.Draw(canvas, "RGBA")

    # ── Outer lid shadow (soft dark gradient approximation via layering) ──
    for offset, alpha in [(6, 15), (4, 25), (2, 35), (0, 0)]:
        shadow_col = (0, 0, 0, alpha) if alpha else None
        if shadow_col:
            d.rounded_rectangle(
                [LID_X - offset, LID_Y - offset,
                 LID_X + LID_W + offset, LID_Y + LID_H + offset],
                radius=18 + offset, fill=shadow_col
            )

    # ── Lid body ──
    d.rounded_rectangle(
        [LID_X, LID_Y, LID_X + LID_W, LID_Y + LID_H],
        radius=16, fill=FRAME_OUTER
    )
    # Inner lid inset (2px rim effect)
    d.rounded_rectangle(
        [LID_X + 2, LID_Y + 2, LID_X + LID_W - 2, LID_Y + LID_H - 2],
        radius=14, outline=FRAME_EDGE, width=1
    )

    # ── Camera notch (top-center) ──
    notch_w, notch_h = 90, 22
    notch_x = LID_X + (LID_W - notch_w) // 2
    notch_y = LID_Y - 1
    d.rounded_rectangle(
        [notch_x, notch_y, notch_x + notch_w, notch_y + notch_h],
        radius=8, fill=NOTCH_COL
    )
    # Camera lens
    cam_cx = notch_x + notch_w // 2
    cam_cy = notch_y + notch_h // 2
    d.ellipse([cam_cx - 5, cam_cy - 5, cam_cx + 5, cam_cy + 5], fill=(30, 30, 32))
    d.ellipse([cam_cx - 3, cam_cy - 3, cam_cx + 3, cam_cy + 3], fill=(18, 18, 20))

    # ── Browser chrome area (tab bar) ──
    chrome_top = LID_Y + BEZEL
    d.rectangle(
        [SCREEN_X, chrome_top, SCREEN_X + SCREEN_W, SCREEN_Y],
        fill=CHROME_BG
    )
    # Thin separator under tabs
    d.line(
        [(SCREEN_X, SCREEN_Y - 1), (SCREEN_X + SCREEN_W, SCREEN_Y - 1)],
        fill=(22, 22, 24), width=2
    )

    # ── Traffic lights ──
    dot_y    = chrome_top + (URL_BAR_H // 2)
    dot_size = 8
    dot_gap  = 22
    for i, col in enumerate([DOT_R, DOT_Y, DOT_G]):
        cx = SCREEN_X + 20 + i * dot_gap
        d.ellipse(
            [cx - dot_size, dot_y - dot_size, cx + dot_size, dot_y + dot_size],
            fill=col
        )

    # ── Address bar ──
    ab_margin = 20
    ab_x = SCREEN_X + 80
    ab_y = chrome_top + 8
    ab_h = URL_BAR_H - 16
    ab_w = SCREEN_W - 100
    d.rounded_rectangle(
        [ab_x, ab_y, ab_x + ab_w, ab_y + ab_h],
        radius=7, fill=ADDR_BG
    )
    # URL text
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 14)
    except Exception:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
        except Exception:
            font = ImageFont.load_default()

    text_y = ab_y + (ab_h - 14) // 2
    d.text(
        (ab_x + 30, text_y),
        "dmcdjcanada.com",
        fill=ADDR_TXT, font=font
    )
    # Lock icon (small circle + rectangle)
    lock_x, lock_y = ab_x + 12, ab_y + (ab_h // 2)
    d.ellipse([lock_x - 4, lock_y - 7, lock_x + 4, lock_y - 1], outline=ADDR_TXT, width=1)
    d.rounded_rectangle([lock_x - 5, lock_y - 2, lock_x + 5, lock_y + 5], radius=2, fill=ADDR_TXT)

    # ── Screen inner corner radii (mask sharp corners of the screen content) ──
    screen_r = 6
    # We'll handle this by drawing small corner fills over the screen area later

    # ── Stand ──
    stand_pts = [
        (STAND_TOP_X,               STAND_Y),
        (STAND_TOP_X + STAND_TOP_W, STAND_Y),
        (STAND_BOT_X + STAND_BOT_W, STAND_Y + STAND_H),
        (STAND_BOT_X,               STAND_Y + STAND_H),
    ]
    d.polygon(stand_pts, fill=STAND_COL)
    # Stand top edge highlight
    d.line(
        [(STAND_TOP_X, STAND_Y), (STAND_TOP_X + STAND_TOP_W, STAND_Y)],
        fill=FRAME_EDGE, width=1
    )

    # ── Base bar ──
    d.rounded_rectangle(
        [BASE_X, BASE_Y, BASE_X + BASE_W, BASE_Y + BASE_H],
        radius=5, fill=BASE_COL
    )
    # Base highlight line
    d.line(
        [(BASE_X + 4, BASE_Y), (BASE_X + BASE_W - 4, BASE_Y)],
        fill=FRAME_EDGE, width=1
    )


def composite_frame(site_frame: Image.Image, frame_base: Image.Image) -> Image.Image:
    """Paste a website screenshot into the laptop screen on a copy of frame_base."""
    canvas = frame_base.copy()

    # Resize website to fill the screen exactly
    site = site_frame.resize((SCREEN_W, SCREEN_H), Image.LANCZOS)
    canvas.paste(site, (SCREEN_X, SCREEN_Y))

    # Re-draw the laptop chrome OVER the pasted content so the bezel sits on top cleanly
    draw_laptop_frame(canvas)

    return canvas


def render_all_frames():
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    for f in RENDER_DIR.glob("frame_*.png"):
        f.unlink()

    source_files = sorted(FRAMES_DIR.glob("frame_*.png"))
    if not source_files:
        print("ERROR: No source frames found in", FRAMES_DIR)
        sys.exit(1)

    print(f"Rendering {len(source_files)} frames into laptop mockup…")
    print(f"  Screen: {SCREEN_W}x{SCREEN_H} px  |  Canvas: {CANVAS_W}x{CANVAS_H}")

    # Pre-draw the background + an empty laptop (no screen content yet)
    # We'll composite the screen in composite_frame()
    frame_base = Image.new("RGB", (CANVAS_W, CANVAS_H), BG)
    # Draw a placeholder laptop (will be overdrawn in composite_frame)
    # — we actually draw the full frame each time so the chrome sits on top

    idx = 0

    def save_frame(site_img: Image.Image, repeat: int = 1):
        nonlocal idx
        composed = composite_frame(site_img, Image.new("RGB", (CANVAS_W, CANVAS_H), BG))
        for _ in range(repeat):
            composed.save(str(RENDER_DIR / f"frame_{idx:05d}.png"))
            idx += 1

    # Hold first frame
    first = Image.open(source_files[0]).convert("RGB")
    save_frame(first, repeat=HOLD_FRAMES)

    # Scroll frames
    for i, fp in enumerate(source_files):
        if i % FRAME_SKIP != 0:
            continue
        site = Image.open(fp).convert("RGB")
        save_frame(site, repeat=1)
        if (i + 1) % 15 == 0:
            pct = (i + 1) / len(source_files) * 100
            print(f"  …{pct:.0f}%")

    # Hold last frame
    last = Image.open(source_files[-1]).convert("RGB")
    save_frame(last, repeat=HOLD_FRAMES)

    print(f"  Rendered {idx} total frames.")
    return idx


def encode_video(frame_count: int):
    # Input pattern
    input_pattern = str(RENDER_DIR / "frame_%05d.png")

    # ── MP4 (H.264, widely supported) ──────────────────────────────────
    print("Encoding MP4 (H.264)…")
    cmd_mp4 = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", input_pattern,
        "-c:v", "libx264",
        "-crf", "16",            # near-lossless (0=lossless, 23=default, 18=great)
        "-preset", "slow",       # better compression at same quality
        "-pix_fmt", "yuv420p",   # universal browser compatibility
        "-movflags", "+faststart",
        "-vf", "scale=1400:900",
        str(OUT_MP4)
    ]
    result = subprocess.run(cmd_mp4, capture_output=True, text=True)
    if result.returncode == 0:
        mb = OUT_MP4.stat().st_size / 1e6
        print(f"  MP4 saved → {OUT_MP4}  ({mb:.1f} MB)")
    else:
        print("  MP4 FAILED:", result.stderr[-500:])

    # ── WebM (VP9, better quality at same bitrate, for Chrome/Firefox) ──
    print("Encoding WebM (VP9)…")
    cmd_webm = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", input_pattern,
        "-c:v", "libvpx-vp9",
        "-crf", "24",            # quality (lower = better, 0=lossless)
        "-b:v", "0",             # constant-quality mode
        "-pix_fmt", "yuv420p",
        "-deadline", "good",
        "-cpu-used", "2",
        str(OUT_WEBM)
    ]
    result = subprocess.run(cmd_webm, capture_output=True, text=True)
    if result.returncode == 0:
        mb = OUT_WEBM.stat().st_size / 1e6
        print(f"  WebM saved → {OUT_WEBM}  ({mb:.1f} MB)")
    else:
        print("  WebM FAILED:", result.stderr[-500:])


if __name__ == "__main__":
    count = render_all_frames()
    encode_video(count)
    print("\nDone! Update case-study-dmc.html to use the <video> tag.")
