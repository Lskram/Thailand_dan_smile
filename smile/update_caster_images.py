#!/usr/bin/env python
"""
Script to update Caster profile images with base64 encoded images
Usage: python update_caster_images.py <gift_image_path> <shi_image_path>

Example:
    python update_caster_images.py ~/Desktop/gift.jpg ~/Desktop/shi.jpg
"""

import os
import sys
import django
import base64
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smile.settings')
django.setup()

from videos.models import Caster


def image_to_base64(image_path):
    """Convert image file to base64 data URI"""
    try:
        with open(image_path, 'rb') as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')

            # Detect image type from extension
            ext = Path(image_path).suffix.lower()
            if ext in ['.jpg', '.jpeg']:
                mime_type = 'image/jpeg'
            elif ext == '.png':
                mime_type = 'image/png'
            elif ext == '.gif':
                mime_type = 'image/gif'
            elif ext == '.webp':
                mime_type = 'image/webp'
            else:
                mime_type = 'image/jpeg'  # default

            return f"data:{mime_type};base64,{encoded}"
    except FileNotFoundError:
        print(f"❌ Error: File not found - {image_path}")
        return None
    except Exception as e:
        print(f"❌ Error reading {image_path}: {e}")
        return None


def main():
    if len(sys.argv) != 3:
        print("Usage: python update_caster_images.py <gift_image_path> <shi_image_path>")
        print("\nExample:")
        print("    python update_caster_images.py ~/Desktop/gift.jpg ~/Desktop/shi.jpg")
        sys.exit(1)

    gift_path = sys.argv[1]
    shi_path = sys.argv[2]

    print("🔄 Converting images to base64...")

    # Convert images
    gift_base64 = image_to_base64(gift_path)
    shi_base64 = image_to_base64(shi_path)

    if not gift_base64 or not shi_base64:
        print("❌ Failed to convert images")
        sys.exit(1)

    print(f"✅ GIFT C YOU image: {len(gift_base64)} characters")
    print(f"✅ Shi Ozzy image: {len(shi_base64)} characters")

    # Update database
    print("\n🔄 Updating database...")

    try:
        gift = Caster.objects.get(name="GIFT C YOU")
        gift.image_url = gift_base64
        gift.save()
        print(f"✅ Updated GIFT C YOU profile image")
    except Caster.DoesNotExist:
        print("❌ GIFT C YOU not found in database")

    try:
        shi = Caster.objects.get(name="Shi Ozzy")
        shi.image_url = shi_base64
        shi.save()
        print(f"✅ Updated Shi Ozzy profile image")
    except Caster.DoesNotExist:
        print("❌ Shi Ozzy not found in database")

    print("\n✨ Done! Profile images have been embedded in the database.")
    print("💡 You can now move the project anywhere without losing the images.")

    # Verify
    print("\n📊 Current Casters:")
    for idx, caster in enumerate(Caster.objects.all().order_by('-created_at'), 1):
        img_preview = caster.image_url[:50] + "..." if len(caster.image_url) > 50 else caster.image_url
        print(f"{idx}. {caster.name}")
        print(f"   Image size: {len(caster.image_url)} characters")
        print(f"   Preview: {img_preview}")


if __name__ == "__main__":
    main()
