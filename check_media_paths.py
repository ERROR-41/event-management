import os
from pathlib import Path
import django
from django.conf import settings

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

BASE_DIR = Path(__file__).resolve().parent

print("Media URL:", settings.MEDIA_URL)
print("Media Root:", settings.MEDIA_ROOT)

# Check if media directory exists
if not os.path.exists(settings.MEDIA_ROOT):
    print(f"WARNING: Media directory {settings.MEDIA_ROOT} does not exist!")
else:
    print(f"Media directory exists at {settings.MEDIA_ROOT}")
    
    # Count images in media directory
    image_count = 0
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_count += 1
                print(f"Found image: {os.path.join(root, file)}")
    
    if image_count == 0:
        print("No images found in media directory!")
    else:
        print(f"Found {image_count} images in media directory")

# Check template static references
from django.template.loader import get_template
try:
    template = get_template('events/event_detail.html')
    print("Template loaded successfully")
except Exception as e:
    print(f"Error loading template: {e}")

print("\nVerify your template is using: {{ event.image.url }} correctly for image paths")
print("Make sure your image field is properly defined in your Event model with upload_to parameter")
