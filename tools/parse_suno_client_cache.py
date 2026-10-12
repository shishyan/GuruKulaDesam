import re, json, sys, os

sys.stdout.reconfigure(encoding='utf-8')

blob_path = r"C:\Users\Shishyan\AppData\Local\Microsoft\Edge\User Data\Default\IndexedDB\https_suno.com_0.indexeddb.blob\1\06\644"

print(f"Reading {blob_path} ({os.path.getsize(blob_path)} bytes)...")
with open(blob_path, "rb") as f:
    content = f.read()

# Pattern for JSON-like strings in V8 serialization
# In V8 serialized objects, string properties often have length prefixes or quotes
uuid_pattern = re.compile(rb'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

# Let's find clips: find occurrences of UUIDs and see if nearby we have prompt or title
# We can search for Tamil strings
tamil_pattern = re.compile(r'[\u0b80-\u0bff][\u0b80-\u0bff\s\d\w\(\)\-\,\.\!\?\[\]]{5,}')

print("Searching for Tamil song titles and lyrics fragments...")
# Decode bytes ignoring errors
text = content.decode('utf-8', errors='ignore')

# Find all clips / prompts
prompts = re.findall(r'"prompt"[:\s\x00-\x1f]*"([^"]{20,})"', text)
print(f"Found {len(prompts)} potential lyrics/prompts via quote match!")

# Also look for clip blocks
# Suno clip JSON structure has "id": "...", "title": "...", "metadata": {"prompt": "..."}
clip_blocks = re.findall(r'\{[^{}]*"id"\s*:\s*"([0-9a-f\-]{36})"[^{}]*"title"\s*:\s*"([^"]+)"[^{}]*\}', text)
print(f"Found {len(clip_blocks)} direct clip blocks!")

# Extract all UUIDs
all_uuids = set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', text))
print(f"Total unique UUIDs in blob: {len(all_uuids)}")

with open('production/metadata/all_blob_uuids.json', 'w', encoding='utf-8') as f:
    json.dump(list(all_uuids), f, indent=2)

print("Saved production/metadata/all_blob_uuids.json")
