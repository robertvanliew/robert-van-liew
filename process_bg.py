import os
from rembg import remove
from PIL import Image

input_path = r'C:\Users\12124\Downloads\IMG_2216.JPG'
bg_path = r'C:\Users\12124\.gemini\antigravity\brain\df29b702-527d-430e-b282-52b2055ea2ed\office_background_1776398090707.png'
output_path = r'C:\Users\12124\Downloads\linkedin_headshot_ai_office.png'

try:
    print("Loading image...")
    # Load original image
    img = Image.open(input_path).convert("RGBA")
    
    print("Extracting subject (Face is completely untouched)...")
    # Get just the subject with a transparent background
    subject = remove(img)
    
    print("Loading new professional office background...")
    bg = Image.open(bg_path).convert("RGBA")
    
    # Resize the new background to match the original image size, cropping if necessary to maintain aspect ratio
    bg_ratio = bg.width / bg.height
    img_ratio = img.width / img.height
    
    if bg_ratio > img_ratio:
        # Background is wider
        new_width = int(bg.height * img_ratio)
        offset = (bg.width - new_width) // 2
        bg = bg.crop((offset, 0, offset + new_width, bg.height))
    else:
        # Background is taller
        new_height = int(bg.width / img_ratio)
        offset = (bg.height - new_height) // 2
        bg = bg.crop((0, offset, bg.width, offset + new_height))
        
    bg = bg.resize((img.width, img.height), Image.Resampling.LANCZOS)
    
    print("Compositing subject onto new background...")
    # Paste perfectly sharp subject onto the office background
    bg.paste(subject, (0, 0), subject)
    
    print("Saving to Downloads...")
    final_img = bg.convert("RGB")
    final_img.save(output_path)
    print("Success! Image is at:", output_path)
    
except Exception as e:
    print("Error:", e)
