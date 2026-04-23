"""
create_mockup_video_v2.py
──────────────────────────
Corrected version: website screenshot is pasted into screen area,
THEN the bezel/chrome frame is drawn on top. Saves all frames as PNGs
then encodes to MP4 + WebM via ffmpeg.
"""

import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── PATHS ──────────────────────────────────────────────────────────────────
FRAMES_DIR  = Path(r"C:\Users\12124\Documents\Robert-Vanliew-Website\gif_frames")
RENDER_DIR  = Path(r"C:\Users\12124\Documents\Robert-Vanliew-Website\render_frames")
OUT_MP4     = Path(r"C:\Users\12124\Documents\Robert-Vanliew-Website\images\dmc_mockup.mp4")
OUT_WEBM    = Path(r"C:\Users\12124\Documents\Robert-Vanliew-Website\images\dmc_mockup.webm")

# ── CANVAS ────────────────────────────────────────────────────────────────
CANVAS_W = 1400
CANVAS_H = 900

# ── LAPTOP GEOMETRY ───────────────────────────────────────────────────────
LID_X  = 60
LID_Y  = 30
LID_W  = CANVAS_W - LID_X * 2   # 1280
LID_H  = int(LID_W * 0.627)     # ~802

BEZEL      = 20
URL_BAR_H  = 40

# The screen viewport (where website frames are composited)
SCREEN_X = LID_X + BEZEL
SCREEN_Y = LID_Y + BEZEL + URL_BAR_H
SCREEN_W = LID_W - BEZEL * 2
SCREEN_H = LID_H - BEZEL * 2 - URL_BAR_H

# ── COLOURS ──────────────────────────────────────────────────────────────
BG          = (22,  24,  30)
FRAME_OUTER = (38,  38,  40)
FRAME_EDGE  = (65,  65,  68)
CHROME_BG   = (28,  28,  30)
ADDR_BG     = (52,  52,  56)
ADDR_TXT    = (155, 155, 162)
DOT_R       = (255, 95,  86)
DOT_Y       = (255, 189, 46)
DOT_G       = (39,  201, 63)
NOTCH_COL   = (18,  18,  20)
STAND_COL   = (55,  55,  58)
BASE_COL    = (62,  62,  66)

# Stand
STAND_TOP_W = int(LID_W * 0.28)
STAND_BOT_W = int(LID_W * 0.52)
STAND_H     = 22
STAND_Y     = LID_Y + LID_H
STAND_TOP_X = LID_X + (LID_W - STAND_TOP_W) // 2
STAND_BOT_X = LID_X + (LID_W - STAND_BOT_W) // 2
BASE_H      = 12
BASE_Y      = STAND_Y + STAND_H
BASE_X      = LID_X - 50
BASE_W      = LID_W + 100

# ── VIDEO ──────────────────────────────────────────────────────────────────
FPS         = 24
HOLD_FRAMES = int(1.0 * FPS)   # 1 second hold at start/end
FRAME_SKIP  = 1                 # use every source frame


def get_font(size: int):
    for name in ["arialbd.ttf", "arial.ttf", "segoeui.ttf"]:
        try:
            return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)
        except Exception:
            pass
    return ImageFont.load_default()


def draw_chrome_overlay(canvas: Image.Image) -> None:
    """
    Draw the laptop bezel + browser chrome ON TOP of the already-pasted
    website screenshot. This must run AFTER the website is pasted.
    """
    d = ImageDraw.Draw(canvas)

    # === STAND (behind the lid visually, drawn before lid) ===
    stand_pts = [
        (STAND_TOP_X,               STAND_Y),
        (STAND_TOP_X + STAND_TOP_W, STAND_Y),
        (STAND_BOT_X + STAND_BOT_W, STAND_Y + STAND_H),
        (STAND_BOT_X,               STAND_Y + STAND_H),
    ]
    d.polygon(stand_pts, fill=STAND_COL)
    d.line([(STAND_TOP_X, STAND_Y), (STAND_TOP_X + STAND_TOP_W, STAND_Y)],
           fill=FRAME_EDGE, width=1)

    # === BASE BAR ===
    d.rounded_rectangle([BASE_X, BASE_Y, BASE_X + BASE_W, BASE_Y + BASE_H],
                         radius=4, fill=BASE_COL)
    d.line([(BASE_X + 6, BASE_Y), (BASE_X + BASE_W - 6, BASE_Y)],
           fill=FRAME_EDGE, width=1)

    # === LID OUTER FRAME (draws over the screen edges, creating the bezel) ===
    r = 16

    # Left bezel
    d.rectangle([LID_X, LID_Y, SCREEN_X, LID_Y + LID_H], fill=FRAME_OUTER)
    # Right bezel
    d.rectangle([SCREEN_X + SCREEN_W, LID_Y, LID_X + LID_W, LID_Y + LID_H], fill=FRAME_OUTER)
    # Top bezel (above screen, includes URL bar area)
    d.rectangle([LID_X, LID_Y, LID_X + LID_W, SCREEN_Y], fill=FRAME_OUTER)
    # Bottom bezel
    d.rectangle([LID_X, SCREEN_Y + SCREEN_H, LID_X + LID_W, LID_Y + LID_H], fill=FRAME_OUTER)

    # Rounded corner caps (to give the full lid rounded corners)
    # Draw the lid outline with rounded corners — fill the rounded areas
    d.rounded_rectangle([LID_X, LID_Y, LID_X + LID_W, LID_Y + LID_H],
                         radius=r, outline=FRAME_OUTER, width=r)
    # A second pass for the outer edge stroke
    d.rounded_rectangle([LID_X, LID_Y, LID_X + LID_W, LID_Y + LID_H],
                         radius=r, outline=FRAME_EDGE, width=1)

    # === BROWSER CHROME (URL BAR area inside the top bezel) ===
    chrome_top = LID_Y + BEZEL
    chrome_bot = SCREEN_Y
    d.rectangle([SCREEN_X, chrome_top, SCREEN_X + SCREEN_W, chrome_bot],
                fill=CHROME_BG)

    # Separator line between chrome and page
    d.line([(SCREEN_X, chrome_bot - 1), (SCREEN_X + SCREEN_W, chrome_bot - 1)],
           fill=(20, 20, 22), width=2)

    # ── Traffic lights ──
    dot_cy   = chrome_top + URL_BAR_H // 2
    dot_r    = 8
    dot_gap  = 22
    for i, col in enumerate([DOT_R, DOT_Y, DOT_G]):
        cx = SCREEN_X + 20 + i * dot_gap
        d.ellipse([cx - dot_r, dot_cy - dot_r, cx + dot_r, dot_cy + dot_r], fill=col)
        # subtle inner shadow highlight on dot
        d.ellipse([cx - dot_r + 2, dot_cy - dot_r + 2, cx - 2, dot_cy - 2],
                  fill=tuple(min(255, c + 50) for c in col))

    # ── Address bar ──
    ab_x = SCREEN_X + 78
    ab_y = chrome_top + 9
    ab_h = URL_BAR_H - 18
    ab_w = SCREEN_W - 96
    d.rounded_rectangle([ab_x, ab_y, ab_x + ab_w, ab_y + ab_h],
                         radius=6, fill=ADDR_BG)

    # Lock icon
    lock_cx = ab_x + 14
    lock_cy = ab_y + ab_h // 2
    d.ellipse([lock_cx - 4, lock_cy - 7, lock_cx + 4, lock_cy - 1],
              outline=ADDR_TXT, width=1)
    d.rounded_rectangle([lock_cx - 5, lock_cy - 2, lock_cx + 5, lock_cy + 5],
                         radius=2, fill=ADDR_TXT)

    # URL text
    font = get_font(14)
    d.text((ab_x + 28, ab_y + (ab_h - 14) // 2 + 1),
           "dmcdjcanada.com", fill=ADDR_TXT, font=font)

    # ── Camera notch ──
    notch_w, notch_h = 88, 22
    notch_x = LID_X + (LID_W - notch_w) // 2
    notch_y = LID_Y - 1
    d.rounded_rectangle([notch_x, notch_y, notch_x + notch_w, notch_y + notch_h],
                         radius=8, fill=NOTCH_COL)
    cam_cx = notch_x + notch_w // 2
    cam_cy = notch_y + notch_h // 2
    d.ellipse([cam_cx - 4, cam_cy - 4, cam_cx + 4, cam_cy + 4], fill=(30, 30, 32))
    d.ellipse([cam_cx - 2, cam_cy - 2, cam_cx + 2, cam_cy + 2], fill=(16, 16, 18))


def build_frame(site_img: Image.Image) -> Image.Image:
    """Compose one video frame: background + website in screen + chrome overlay."""
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), BG)

    # 1. Paste website into screen area
    site_resized = site_img.resize((SCREEN_W, SCREEN_H), Image.LANCZOS)
    canvas.paste(site_resized, (SCREEN_X, SCREEN_Y))

    # 2. Draw the laptop chrome ON TOP
    draw_chrome_overlay(canvas)

    return canvas


def render_frames():
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    for f in RENDER_DIR.glob("frame_*.png"):
        f.unlink()

    source_files = sorted(FRAMES_DIR.glob("frame_*.png"))
    if not source_files:
        print("ERROR: No source frames found in", FRAMES_DIR)
        return 0

    print(f"Rendering {len(source_files)} frames...")
    print(f"  Screen: {SCREEN_W}x{SCREEN_H} at ({SCREEN_X},{SCREEN_Y})")

    idx = 0

    def save(site_img, repeat=1):
        nonlocal idx
        frame = build_frame(site_img)
        for _ in range(repeat):
            frame.save(str(RENDER_DIR / f"frame_{idx:05d}.png"))
            idx += 1

    # Hold on first frame
    save(Image.open(source_files[0]).convert("RGB"), repeat=HOLD_FRAMES)

    for i, fp in enumerate(source_files):
        if i % FRAME_SKIP != 0:
            continue
        save(Image.open(fp).convert("RGB"), repeat=1)
        if (i + 1) % 20 == 0:
            print(f"  {(i+1)/len(source_files)*100:.0f}%  ({idx} frames written)")

    # Hold on last frame
    save(Image.open(source_files[-1]).convert("RGB"), repeat=HOLD_FRAMES)

    print(f"  Done: {idx} frames total")
    return idx


def encode_videos():
    input_pat = str(RENDER_DIR / "frame_%05d.png")

    print("\nEncoding MP4...")
    r = subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", input_pat,
        "-c:v", "libx264",
        "-crf", "15",
        "-preset", "slow",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(OUT_MP4)
    ], capture_output=True)
    if r.returncode == 0:
        print(f"  MP4: {OUT_MP4.stat().st_size/1e6:.1f} MB")
    else:
        print("  MP4 failed:", r.stderr.decode()[-400:])

    print("Encoding WebM...")
    r = subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", input_pat,
        "-c:v", "libvpx-vp9",
        "-crf", "22",
        "-b:v", "0",
        "-pix_fmt", "yuv420p",
        "-deadline", "good",
        "-cpu-used", "2",
        str(OUT_WEBM)
    ], capture_output=True)
    if r.returncode == 0:
        print(f"  WebM: {OUT_WEBM.stat().st_size/1e6:.1f} MB")
    else:
        print("  WebM failed:", r.stderr.decode()[-400:])


if __name__ == "__main__":
    count = render_frames()
    if count:
        encode_videos()
        print("\nComplete!")
