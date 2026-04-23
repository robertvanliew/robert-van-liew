import os
from PIL import Image, ImageDraw, ImageFilter

def create_glass_pane(img_path, target_w, radius_percent=0.02):
    img = Image.open(img_path).convert("RGBA")
    
    # Scale width
    ratio = target_w / img.width
    target_h = int(img.height * ratio)
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Radius based on width
    radius = int(target_w * radius_percent)
    
    # Transparency canvas
    canvas = Image.new("RGBA", (target_w, target_h), (0,0,0,0))
    
    # Mask
    mask = Image.new("L", (target_w, target_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, target_w, target_h), radius=radius, fill=255)
    
    # Paste
    canvas.paste(img, (0, 0), mask=mask)
    
    # Optional super subtle 1px border for edge definition on dark backgrounds
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((0, 0, target_w-1, target_h-1), radius=radius, outline=(255, 255, 255, 30), width=1)
    
    return canvas

print("Loading screenshots...")
desktop_path = r"C:\Users\12124\.gemini\antigravity\brain\df29b702-527d-430e-b282-52b2055ea2ed\media__1776401767104.png"
mobile_path = r"C:\Users\12124\.gemini\antigravity\brain\df29b702-527d-430e-b282-52b2055ea2ed\media__1776402278535.jpg" 

print("Generating borderless, maximum-visibility UI panes...")
mac = create_glass_pane(desktop_path, target_w=2000, radius_percent=0.015)
phone = create_glass_pane(mobile_path, target_w=600, radius_percent=0.07) # Mobile has more rounded corners

if mac and phone:
    out_dir = r"C:\Users\12124\Documents\Robert-Vanliew-Website\images"
    mac_out = os.path.join(out_dir, "dmc_mac_mockup.png")
    phone_out = os.path.join(out_dir, "dmc_phone_mockup.png")
    
    mac.save(mac_out, format="PNG")
    phone.save(phone_out, format="PNG")
    
    print("SUCCESS: Pure floating design planes saved to:", mac_out, "and", phone_out)
