import os
import random
from PIL import Image, ImageDraw, ImageFont

# Configuration
WIDTH = 800
HEIGHT = 200
FONT_SIZE = 15
NUM_DROPS = 50
FRAMES = 30
BG_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 120, 255) # Blue
BRIGHT_TEXT_COLOR = (150, 200, 255) # Brighter Blue
FONT_PATH = "/System/Library/Fonts/Monaco.ttf" # Default Mac font

def generate_matrix_rain():
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
    except IOError:
        font = ImageFont.load_default()

    images = []

    for _ in range(FRAMES):
        img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(img)

        for drop in drops:
            # Draw the trail
            for i, char in enumerate(drop['chars']):
                y_pos = drop['y'] - i * FONT_SIZE
                if 0 <= y_pos < HEIGHT:
                    # Fade out effect
                    alpha = max(0, 255 - (i * 20))
                    if i == 0:
                        color = BRIGHT_TEXT_COLOR
                    else:
                        # Dim the blue based on position in trail
                        color = (0, int(120 * (alpha/255)), int(255 * (alpha/255)))
                    
                    draw.text((drop['x'], y_pos), char, font=font, fill=color)
            
            # Update drop position
            drop['y'] += drop['speed']
            
            # Reset if off screen
            if drop['y'] - len(drop['chars']) * FONT_SIZE > HEIGHT:
                drop['y'] = random.randint(-50, 0)
                drop['x'] = random.randint(0, WIDTH // FONT_SIZE) * FONT_SIZE
                drop['speed'] = random.randint(5, 15)

        images.append(img)

    # Save as GIF
    images[0].save(
        'assets/blue-matrix.gif',
        save_all=True,
        append_images=images[1:],
        duration=100,
        loop=0
    )
    print("Generated assets/blue-matrix.gif")

if __name__ == "__main__":
    generate_matrix_rain()
