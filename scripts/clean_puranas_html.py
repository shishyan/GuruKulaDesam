import re

with open("puranas.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the top header in puranas.html with a clean, clutter-free book header
header_pattern = r"<!-- Top Hero Header -->\s*<header[\s\S]*?</header>"
new_header = """<!-- Clean Minimal Book Header -->
    <header style="background:rgba(15, 23, 42, 0.8); border:1px solid rgba(212, 175, 55, 0.25); border-radius:16px; padding:18px 24px; margin-bottom:16px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
      <div>
        <h1 id="puranaDisplayTitle" style="color:#ffffff; font-size:1.85rem; font-weight:900; line-height:1.2; margin:0 0 4px 0;">
          வில்லிபாரதம் &amp; வியாச மகாபாரதம் (Mahabharatam)
        </h1>
        <div id="puranaDisplayAuthor" style="color:#38bdf8; font-size:0.95rem; font-weight:600;">
          அருளியவர்: வேத வியாசர்
        </div>
      </div>
      <div id="puranaDisplayBadge" style="display:none;"></div>
      <p id="puranaDisplaySummary" style="display:none;"></p>
    </header>"""

content = re.sub(header_pattern, new_header, content)

with open("puranas.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated puranas.html header!")
