import subprocess
import json
import re

out = subprocess.check_output(['git', 'show', 'e0938dd1:data/puranas/kandha-puranam.json'], encoding='utf-8')
data = json.loads(out)
raw_chaps = data['chapters']

# Let's inspect how many raw chapters have real padalam synopsis
print("Total raw chapters:", len(raw_chaps))
padalams = []
for i, c in enumerate(raw_chaps):
    t = c['title']
    syn = c.get('synopsis', '')
    # Check if this chapter is a real padalam
    padalams.append((t, syn))

print("Collected padalams:", len(padalams))
