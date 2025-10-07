#!/usr/bin/env python3
"""
STUMARCOT QR Code Generator
Generates a branded QR code for https://stumarcot.co.tz/link-tree
"""

import qrcode, os
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from PIL import Image, ImageDraw, ImageFont


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def center_text(draw, text, font, y, fill, total_width):
    """Center text horizontally"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (total_width - text_width) // 2
    draw.text((x, y), text, fill=fill, font=font)


def create_stumarcot_qr():
    """
    Create a well-designed QR code for STUMARCOT link tree
    """
    # URL to encode
    url = "https://stumarcot.co.tz/link-tree"
    
    # STUMARCOT brand colors
    primary_color = "#1a365d"      # Dark blue
    secondary_color = "#2d5a87"    # Medium blue
    background_color = "#f7fafc"   # Light gray background
    
    # Convert to RGB tuples
    primary_rgb = hex_to_rgb(primary_color)
    secondary_rgb = hex_to_rgb(secondary_color)
    background_rgb = hex_to_rgb(background_color)
    
    # QR code configuration
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=25,
        border=6,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create styled QR code with gradient
    qr_image = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=RadialGradiantColorMask(
            back_color=background_rgb,
            center_color=primary_rgb,
            edge_color=secondary_rgb
        )
    )
    
    return qr_image


def create_simple_qr():
    """
    Create a simple QR code with basic styling
    """
    url = "https://stumarcot.co.tz/link-tree"
    
    # Brand colors
    primary_color = "#1a365d"
    background_color = "#f7fafc"
    
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=5,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code with brand colors
    qr_image = qr.make_image(
        fill_color=hex_to_rgb(primary_color),
        back_color=hex_to_rgb(background_color)
    )
    
    return qr_image


def create_minimal_qr():
    """
    Create a minimal QR code
    """
    url = "https://stumarcot.co.tz/link-tree"
    
    # Create basic QR code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=18,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code with brand colors
    qr_image = qr.make_image(
        fill_color=(26, 54, 93),  # STUMARCOT blue
        back_color=(247, 250, 252)  # Light background
    )
    
    return qr_image


def main():
    """
    Generate and save QR codes
    """
    print("🏗️  STUMARCOT QR Code Generator")
    print("=" * 40)
    
    try:
        # Create minimal QR code (most reliable)
        print("Creating minimal QR code...")
        minimal_qr = create_minimal_qr()
        minimal_qr.save("stumarcot_qr_minimal.png", "PNG")
        print("✅ Minimal QR code saved as 'stumarcot_qr_minimal.png'")
        
        # Create simple QR code
        print("Creating simple QR code...")
        simple_qr = create_simple_qr()
        simple_qr.save("stumarcot_qr_simple.png", "PNG")
        print("✅ Simple QR code saved as 'stumarcot_qr_simple.png'")
        
        # Create gradient QR code
        print("Creating gradient QR code...")
        gradient_qr = create_stumarcot_qr()
        gradient_qr.save("stumarcot_qr_gradient.png", "PNG")
        print("✅ Gradient QR code saved as 'stumarcot_qr_gradient.png'")
        
        # Display QR code info
        print("\n📱 QR Code Details:")
        print(f"URL: https://stumarcot.co.tz/link-tree")
        print(f"Minimal version: {minimal_qr.size[0]}x{minimal_qr.size[1]} pixels")
        print(f"Simple version: {simple_qr.size[0]}x{simple_qr.size[1]} pixels")
        print(f"Gradient version: {gradient_qr.size[0]}x{gradient_qr.size[1]} pixels")
        
        print("\n🎨 Brand Colors Used:")
        print("Primary: #1a365d (Dark Blue)")
        print("Secondary: #2d5a87 (Medium Blue)")
        print("Accent: #e53e3e (Red)")
        print("Background: #f7fafc (Light Gray)")
        
        print("\n✨ QR codes generated successfully!")
        
    except Exception as e:
        print(f"❌ Error generating QR code: {e}")
        print("Make sure you have the required packages installed:")
        print("pip install qrcode[pil] pillow")

def add_logo_to_qr(qr_image, logo_path, logo_size_ratio=0.2):
    """
    Add a logo to the center of the QR code
    """
    try:
        # Open and process logo
        logo = Image.open(logo_path)
        
        # Convert logo to RGBA if it isn't already
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        
        # Calculate logo size (20% of QR code size by default)
        qr_width, qr_height = qr_image.size
        logo_size = int(min(qr_width, qr_height) * logo_size_ratio)
        
        # Resize logo maintaining aspect ratio
        logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Create a white background for the logo
        logo_bg = Image.new('RGBA', (logo_size, logo_size), (255, 255, 255, 255))
        
        # Paste logo onto white background
        logo_x = (logo_size - logo.width) // 2
        logo_y = (logo_size - logo.height) // 2
        logo_bg.paste(logo, (logo_x, logo_y), logo)
        
        # Calculate position to center the logo
        logo_position_x = (qr_width - logo_size) // 2
        logo_position_y = (qr_height - logo_size) // 2
        
        # Convert QR code to RGBA if needed
        if qr_image.mode != 'RGBA':
            qr_image = qr_image.convert('RGBA')
        
        # Create a new image with the logo
        qr_with_logo = qr_image.copy()
        qr_with_logo.paste(logo_bg, (logo_position_x, logo_position_y), logo_bg)
        
        return qr_with_logo
        
    except Exception as e:
        print(f"⚠️  Warning: Could not add logo: {e}")
        return qr_image

def find_logo():
    """
    Look for STUMARCOT logo in common locations
    """
    possible_logos = [
        "website/static/Minimalist House Logo Design.png",
        "website/static/Minimalist_House_Logo_Design-removebg-preview.png",
        "logo.png",
        "stumarcot_logo.png",
        "logo.jpg",
        "stumarcot_logo.jpg"
    ]
    
    for logo_path in possible_logos:
        if os.path.exists(logo_path):
            return logo_path
    
    return None
        

if __name__ == "__main__":
    logo_path = find_logo()
    print(f"Logo path: {logo_path}")
    qr_image = create_stumarcot_qr()
    qr_image_with_logo = add_logo_to_qr(qr_image, logo_path)
    qr_image_with_logo.save("qr_with_logo.png", "PNG")
    print("✅ QR code with logo saved as 'qr_with_logo.png'")