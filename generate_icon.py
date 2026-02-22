#!/usr/bin/env python3
"""Generate PNG apple touch icon from SVG."""
import subprocess
import sys

# Check if we need to install dependencies
try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Installing Pillow...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw

def create_apple_touch_icon():
    """Create a 180x180 PNG icon for Apple devices."""
    # Create image with blue background
    size = 180
    img = Image.new('RGB', (size, size), color='#4A90E2')
    draw = ImageDraw.Draw(img)

    # Draw sun (golden circle)
    sun_center = (90, 70)
    sun_radius = 30
    sun_bbox = (
        sun_center[0] - sun_radius,
        sun_center[1] - sun_radius,
        sun_center[0] + sun_radius,
        sun_center[1] + sun_radius
    )
    draw.ellipse(sun_bbox, fill='#FFB800')

    # Draw sun rays
    ray_color = '#FFB800'
    ray_width = 4

    # Vertical and horizontal rays
    rays = [
        # Top, bottom, left, right
        (90, 20, 90, 40),
        (90, 100, 90, 120),
        (40, 70, 60, 70),
        (120, 70, 140, 70),
        # Diagonals
        (54, 34, 66, 46),
        (114, 94, 126, 106),
        (126, 34, 114, 46),
        (66, 94, 54, 106),
    ]

    for x1, y1, x2, y2 in rays:
        draw.line([(x1, y1), (x2, y2)], fill=ray_color, width=ray_width)

    # Draw white cloud at bottom
    cloud_y = 130
    # Main cloud body
    draw.ellipse((65, 120, 135, 150), fill='white')
    # Left puff
    draw.ellipse((50, 125, 110, 155), fill='white')
    # Right puff
    draw.ellipse((90, 125, 140, 150), fill='white')

    # Save
    output_path = 'static/apple-touch-icon.png'
    img.save(output_path, 'PNG')
    print(f"✓ Created {output_path}")

if __name__ == '__main__':
    create_apple_touch_icon()
