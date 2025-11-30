from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_holographic_button(text, filename, color):
    width = 300
    height = 80
    bg_color = (0, 0, 0, 0) # Transparent
    
    # Create image
    img = Image.new('RGBA', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Colors
    main_color = color
    glow_color = (color[0], color[1], color[2], 100)
    
    # Draw Glow (Outer)
    shape = [5, 5, width-5, height-5]
    draw.rounded_rectangle(shape, radius=15, outline=glow_color, width=4)
    
    # Draw Main Border
    shape = [10, 10, width-10, height-10]
    draw.rounded_rectangle(shape, radius=10, outline=main_color, width=2)
    
    # Draw "Tech" accents (corners)
    corner_len = 20
    # Top-Left
    draw.line([(10, 10), (10 + corner_len, 10)], fill=main_color, width=4)
    draw.line([(10, 10), (10, 10 + corner_len)], fill=main_color, width=4)
    # Bottom-Right
    draw.line([(width-10, height-10), (width-10 - corner_len, height-10)], fill=main_color, width=4)
    draw.line([(width-10, height-10), (width-10, height-10 - corner_len)], fill=main_color, width=4)

    # Add Text
    try:
        # Try to use a system font
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        font = ImageFont.load_default()
        
    # Calculate text position to center it
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) / 2
    y = (height - text_height) / 2 - 2 # Slight adjustment
    
    # Text Glow
    # draw.text((x-1, y), text, font=font, fill=glow_color)
    # draw.text((x+1, y), text, font=font, fill=glow_color)
    draw.text((x, y), text, font=font, fill=main_color)
    
    # Save
    img.save(f"assets/{filename}")
    print(f"Generated assets/{filename}")

if __name__ == "__main__":
    # Blue for Portfolio
    create_holographic_button("ACCESS PORTFOLIO", "btn-portfolio.png", (0, 120, 255))
    # Red for Email
    create_holographic_button("TRANSMIT EMAIL", "btn-email.png", (255, 50, 50))
    # Cyan for LinkedIn
    create_holographic_button("CONNECT LINKEDIN", "btn-linkedin.png", (0, 255, 255))
