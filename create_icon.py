"""
Script to create an icon for the NewsAPI Automation executable.
Run this script to generate the icon.ico file.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a simple icon for the application."""
    
    # Create a new image with transparent background
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a blue circle background (LinkedIn-like color)
    center = size // 2
    radius = size // 2 - 10
    draw.ellipse([center - radius, center - radius, center + radius, center + radius],
                 fill='#0a66c2')
    
    # Draw a newspaper icon (white)
    # Main rectangle
    paper_left = center - 60
    paper_top = center - 70
    paper_right = center + 60
    paper_bottom = center + 70
    draw.rectangle([paper_left, paper_top, paper_right, paper_bottom],
                   fill='white', outline='white', width=2)
    
    # Draw text lines
    line_height = 12
    line_spacing = 8
    start_y = paper_top + 20
    for i in range(6):
        y = start_y + i * (line_height + line_spacing)
        if i == 0:
            # Title line (longer)
            draw.rectangle([paper_left + 15, y, paper_right - 15, y + line_height],
                          fill='#0a66c2')
        else:
            # Body lines (shorter)
            draw.rectangle([paper_left + 15, y, paper_right - 30, y + line_height],
                          fill='#cccccc')
    
    # Save as .ico file with multiple sizes
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
    img.save(icon_path, format='ICO', sizes=icon_sizes)
    
    print(f"✓ Icon created: {icon_path}")
    return icon_path

if __name__ == "__main__":
    create_icon()
