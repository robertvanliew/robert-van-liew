import os
from PIL import Image, ImageDraw, ImageFilter

def create_rounded_rect(size, radius, fill):
    img = Image.new('RGBA', size, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=fill)
    return img

def make_iphone_mockup(screenshot_path):
    try:
        screen = Image.open(screenshot_path).convert("RGBA")
    except Exception as e:
        print(f"Error opening iPhone screenshot: {e}")
        return None
        
    s_w, s_h = 400, 866  # roughly iPhone ratio
    screen = screen.resize((s_w, s_h), Image.Resampling.LANCZOS)
    
    bezel = 20
    radius = 45
    frame_w = s_w + bezel*2
    frame_h = s_h + bezel*2
    
    frame = create_rounded_rect((frame_w, frame_h), radius + bezel, (25, 25, 25, 255))
    
    # Outer thin silver ring to look 3D
    silver_ring = create_rounded_rect((frame_w+4, frame_h+4), radius + bezel + 2, (180, 180, 180, 255))
    ring_base = Image.new("RGBA", (frame_w+10, frame_h+10), (0,0,0,0))
    ring_base.paste(silver_ring, (3,3), silver_ring)
    ring_base.paste(frame, (5,5), frame)
    frame = ring_base
    
    # Screen Mask
    mask = create_rounded_rect((s_w, s_h), radius, (255, 255, 255, 255))
    screen_masked = Image.new('RGBA', screen.size, (0,0,0,0))
    screen_masked.paste(screen, (0,0), mask=mask.convert("L"))
    
    frame.paste(screen_masked, (bezel+5, bezel+5), screen_masked)
    
    # Notch
    draw = ImageDraw.Draw(frame)
    notch_w = 170
    notch_h = 30
    notch_x = (frame.width - notch_w) // 2
    draw.rounded_rectangle((notch_x, bezel+5, notch_x + notch_w, bezel+5 + notch_h), radius=12, fill=(25, 25, 25, 255))
    
    return frame

def make_mac_mockup(screenshot_path):
    try:
        screen = Image.open(screenshot_path).convert("RGBA")
    except Exception as e:
        print(f"Error opening Mac screenshot: {e}")
        return None
        
    s_w, s_h = 1200, 750
    screen = screen.resize((s_w, s_h), Image.Resampling.LANCZOS)
    
    bezel = 25
    radius = 15
    frame_w = s_w + bezel*2
    frame_h = s_h + bezel + 35 # bottom bezel thicker
    
    # Screen back
    frame = create_rounded_rect((frame_w, frame_h), radius, (20, 20, 20, 255))
    
    # Screen inner border (very dark)
    inner = create_rounded_rect((frame_w-4, frame_h-4), radius-2, (10, 10, 10, 255))
    frame.paste(inner, (2,2), inner)
    
    frame.paste(screen, (bezel, bezel), screen)
    
    # Bottom chin text "MacBook Pro"
    draw = ImageDraw.Draw(frame)
    # fake text line
    draw.line((frame_w//2 - 25, frame_h - 15, frame_w//2 + 25, frame_h - 15), fill=(80,80,80,255), width=2)
    
    # Base block
    base_h = 15
    base_w = frame_w + 100
    base = create_rounded_rect((base_w, base_h), 5, (200, 200, 200, 255))
    
    # Composite
    comp_w = base_w
    comp_h = frame_h + base_h
    comp = Image.new("RGBA", (comp_w, comp_h), (0,0,0,0))
    comp.paste(frame, ((comp_w - frame_w)//2, 0), frame)
    comp.paste(base, (0, frame_h - 5), base)
    
    # Touch pad notch
    draw = ImageDraw.Draw(comp)
    draw.rectangle(((comp_w//2 - 40, frame_h - 5), (comp_w//2 + 40, frame_h + 2)), fill=(150,150,150,255))
    
    return comp

def add_shadow(img, offset=(0, 30), blur=50, alpha=100):
    shadow = Image.new('RGBA', img.size, (0, 0, 0, alpha))
    shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(blur))
    canvas = Image.new('RGBA', (img.width + blur*2 + abs(offset[0]), img.height + blur*2 + abs(offset[1])), (0, 0, 0, 0))
    canvas.paste(shadow_blurred, (blur + offset[0], blur + offset[1]))
    canvas.paste(img, (blur, blur), img)
    return canvas

desktop_path = r"C:\Users\12124\.gemini\antigravity\brain\df29b702-527d-430e-b282-52b2055ea2ed\media__1776401767104.png"
mobile_path = r"C:\Users\12124\.gemini\antigravity\brain\df29b702-527d-430e-b282-52b2055ea2ed\media__1776402278535.jpg" # Clean mobile

print("Building Mac...")
mac = make_mac_mockup(desktop_path)
print("Building Phone...")
phone = make_iphone_mockup(mobile_path)

if mac and phone:
    mac_shadow = add_shadow(mac)
    phone_shadow = add_shadow(phone)
    
    # Shrink phone relative to mac
    ratio = 0.45
    phone_shadow = phone_shadow.resize((int(phone_shadow.width * ratio), int(phone_shadow.height * ratio)), Image.Resampling.LANCZOS)
    
    # Composite onto transparent canvas
    bg_canvas = Image.new("RGBA", (1800, 1000), (20,20,20,0)) 
    
    mac_x = 50
    mac_y = 50
    bg_canvas.paste(mac_shadow, (mac_x, mac_y), mac_shadow)
    
    # Paste phone overlapping front right
    phone_x = mac_x + mac_shadow.width - int(phone_shadow.width*0.75)
    phone_y = mac_y + mac_shadow.height - phone_shadow.height - 40
    bg_canvas.paste(phone_shadow, (phone_x, phone_y), phone_shadow)
    
    bbox = bg_canvas.getbbox()
    if bbox:
        bg_canvas = bg_canvas.crop(bbox)
        
    out_path = r"C:\Users\12124\Documents\Robert-Vanliew-Website\images\dmc_pro_mockup.png"
    import os
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    bg_canvas.save(out_path)
    print("Pro mockup saved to", out_path)
