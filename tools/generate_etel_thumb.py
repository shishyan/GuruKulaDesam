import os, sys
from pathlib import Path

# Add repo to sys.path
sys.path.insert(0, r"c:\GitHub\Gurukuladesam")
from tools.generate_modern_thumbnail import render_thumbnail

vid = "ETELjf0OTi4"
custom_info = {
    'theme': 'thirukkural', # Deep Antique Maroon & Gold
    'badge': 'தமிழ்த்தாய் வாழ்த்து',
    'tamil_title': 'நீராரும் கடலுடுத்த',
    'subtitle': 'TAMIL THAI VAZHTHU • MANONMANIAM'
}

path = render_thumbnail(vid, 'தமிழ்த்தாய் வாழ்த்து', custom_info)
print(f"Generated refined thumbnail: {path}")
