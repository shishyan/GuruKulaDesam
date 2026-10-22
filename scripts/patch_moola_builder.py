import re

# Read files
with open('scripts/build_moola_nool_library.py', 'r', encoding='utf-8') as f:
    builder_code = f.read()

# Add categories to build_moola_nool_library.py if not present
new_categories = '''        {"id": "puranas-epics", "name": "ஈழத்து மூலப் பதிப்புகள் — புராணங்கள் & இதிகாசங்கள் (Authentic Jaffna Recensions)", "count": 10},'''

if '"id": "puranas-epics"' not in builder_code:
    builder_code = builder_code.replace(
        '{"id": "school-ethics",',
        new_categories + '\n        {"id": "school-ethics",'
    )

with open('scripts/build_moola_nool_library.py', 'w', encoding='utf-8') as f:
    f.write(builder_code)

print("Updated build_moola_nool_library.py category definitions.")
