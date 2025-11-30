import os
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Configuration
WIDTH = 800
HEIGHT = 600 # Increased height for text
FONT_SIZE = 15
NUM_DROPS = 60
FRAMES = 40 # Increased frames for smoother loop
BG_COLOR = (0, 0, 0)
RAIN_COLOR = (0, 120, 255) # Blue
BRIGHT_RAIN_COLOR = (150, 200, 255) # Brighter Blue
TEXT_COLOR = (255, 255, 255) # White for content
HEADER_COLOR = (0, 255, 255) # Cyan for headers
FONT_PATH = "/System/Library/Fonts/Monaco.ttf" 

CONTENT = [
    ("Chrome Extension – Productivity Tools", "Lightweight tools to help organize online research and improve focus during browsing."),
    ("Brightview", "A project focused on improving accessibility and user-centered design—built with principles from HCI and information architecture."),
    ("Enterprise Solutions (1 & 2)", "Hands-on systems applying database logic, front‑end structures, and real information workflows."),
    ("Firebase Apps", "Apps exploring cloud‑based data storage, authentication, and information retrieval (Moody App, MeGustaFirebase, etc.)")
]

def generate_matrix_rain_with_text():
    # Create drops
    drops = []
    for _ in range(NUM_DROPS):
        drops.append({
            'x': random.randint(0, WIDTH // FONT_SIZE) * FONT_SIZE,
            'y': random.randint(-HEIGHT, 0),
            'speed': random.randint(5, 15),
            'chars': [chr(random.randint(33, 126)) for _ in range(HEIGHT // FONT_SIZE + 5)]
        })

    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        # Load a larger font for the text overlay
        text_font_header = ImageFont.truetype("Arial", 24)
        text_font_body = ImageFont.truetype("Arial", 16)
    except IOError:
        font = ImageFont.load_default()
        text_font_header = ImageFont.load_default()
        text_font_body = ImageFont.load_default()

    images = []

    for _ in range(FRAMES):
        img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(img)

        # 1. Draw Matrix Rain Background
        for drop in drops:
            for i, char in enumerate(drop['chars']):
                y_pos = drop['y'] - i * FONT_SIZE
                if 0 <= y_pos < HEIGHT:
                    alpha = max(0, 255 - (i * 20))
                    if i == 0:
                        color = BRIGHT_RAIN_COLOR
                    else:
                        color = (0, int(120 * (alpha/255)), int(255 * (alpha/255)))
                    draw.text((drop['x'], y_pos), char, font=font, fill=color)
            
            drop['y'] += drop['speed']
            if drop['y'] - len(drop['chars']) * FONT_SIZE > HEIGHT:
                drop['y'] = random.randint(-50, 0)
                drop['x'] = random.randint(0, WIDTH // FONT_SIZE) * FONT_SIZE

        # 2. Draw Semi-transparent Overlay to make text readable
        overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 180))
        img.paste(Image.alpha_composite(img.convert('RGBA'), overlay), (0, 0))
        
        # 3. Draw Text Content
        draw = ImageDraw.Draw(img)
        y_offset = 40
        draw.text((WIDTH//2 - 100, 10), "DEPLOYED SYSTEMS", font=text_font_header, fill=HEADER_COLOR)
        
        for title, desc in CONTENT:
            y_offset += 40
            draw.text((50, y_offset), f"🔹 {title}", font=text_font_header, fill=HEADER_COLOR)
            y_offset += 35
            
            lines = textwrap.wrap(desc, width=80)
            for line in lines:
                draw.text((70, y_offset), line, font=text_font_body, fill=TEXT_COLOR)
                y_offset += 20
            y_offset += 10

        images.append(img)

    # Save as GIF
    images[0].save(
        'assets/achievements-matrix.gif',
        save_all=True,
        append_images=images[1:],
        duration=100,
        loop=0
    )
    print("Generated assets/achievements-matrix.gif")

if __name__ == "__main__":
    generate_matrix_rain_with_text()
