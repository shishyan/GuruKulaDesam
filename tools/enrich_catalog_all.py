import re
import json

def enrich_thirukkural_items():
    cat_content = open('docs/assets/data/catalog.js', encoding='utf-8').read()
    m_cat = re.search(r'window\.GURUKULA_CATALOG\s*=\s*(\{.*?\});?\s*$', cat_content, re.DOTALL)
    cat_data = json.loads(m_cat.group(1))

    txt = open('docs/thirukkural.html', encoding='utf-8').read()
    m_page = re.search(r'const PAGE_ITEMS = (\[.*?\]);', txt, re.DOTALL)
    page_items = json.loads(m_page.group(1))

    existing_ids = {it['id'] for it in cat_data['thirukkural']}
    missing = [it for it in page_items if it['id'] not in existing_ids]
    print(f"Total Thirukkural items missing from catalog.js: {len(missing)}")

    # Map chapter number to canonical catalog item
    chapter_map = {}
    for it in cat_data['thirukkural']:
        m_ch = re.search(r'அதிகாரம்\s*(\d+)', it.get('title', ''))
        if m_ch:
            ch = int(m_ch.group(1))
            if ch not in chapter_map or (len(it.get('lyrics', '')) > len(chapter_map[ch].get('lyrics', ''))):
                chapter_map[ch] = it

    unmatched = []
    enriched_items = []
    for it in missing:
        m_ch = re.search(r'அதிகாரம்\s*(\d+)', it.get('title', ''))
        if m_ch:
            ch = int(m_ch.group(1))
            if ch in chapter_map:
                canon = chapter_map[ch]
                new_item = {
                    'id': it['id'],
                    'title': it['title'],
                    'type': it.get('type', canon.get('type', 'film')),
                    'playlists': it.get('playlists', canon.get('playlists', ['திருக்குறள் | Thirukkural — Master Collection'])),
                    'category': 'thirukkural',
                    'description': f"{it['title']} - {canon.get('description', '')}",
                    'author': canon.get('author', 'திருவள்ளுவர்'),
                    'source': canon.get('source', 'திருக்குறள்'),
                    'lyrics': canon.get('lyrics', ''),
                    'meaning': canon.get('meaning', '')
                }
                enriched_items.append(new_item)
                print(f"Enriched {it['id']} (ch {ch}): {it['title'][:35]}...")
            else:
                unmatched.append(it)
        else:
            unmatched.append(it)

    print(f"Successfully enriched: {len(enriched_items)}, Unmatched: {len(unmatched)}")
    if unmatched:
        for u in unmatched:
            print("Unmatched:", u)
        return

    # Add enriched items to cat_data['thirukkural']
    cat_data['thirukkural'].extend(enriched_items)
    
    # Save back to docs/assets/data/catalog.js with window.GURUKULA_ITEMS_BY_ID
    new_catalog_json = json.dumps(cat_data, ensure_ascii=False)
    
    catalog_js_content = f"""/**
 * Guru Kula Desam - Complete Devotional & Scripture Catalog
 * Comprehensive video & audio catalog enriched with Tamil lyrics, spiritual meanings, authors and sources
 */
window.GURUKULA_CATALOG = {new_catalog_json};

// Fast ID lookup dictionary for instant lyrics and meaning resolution across all player modals
window.GURUKULA_ITEMS_BY_ID = window.GURUKULA_ITEMS_BY_ID || {{}};
if (window.GURUKULA_CATALOG && typeof window.GURUKULA_CATALOG === 'object') {{
  Object.keys(window.GURUKULA_CATALOG).forEach(function(catKey) {{
    var catItems = window.GURUKULA_CATALOG[catKey];
    if (Array.isArray(catItems)) {{
      catItems.forEach(function(item) {{
        if (item && item.id) {{
          window.GURUKULA_ITEMS_BY_ID[item.id] = Object.assign({{}}, item, {{
            category: item.category || catKey
          }});
        }}
      }});
    }}
  }});
}}
"""
    with open('docs/assets/data/catalog.js', 'w', encoding='utf-8') as f:
        f.write(catalog_js_content)
    print("Updated docs/assets/data/catalog.js successfully!")

    # Also update data/catalogs/site_catalog.json
    try:
        sc_data = json.load(open('data/catalogs/site_catalog.json', encoding='utf-8'))
        sc_ids = {it['id'] for it in sc_data.get('thirukkural', [])}
        for item in enriched_items:
            if item['id'] not in sc_ids:
                sc_data['thirukkural'].append(item)
        with open('data/catalogs/site_catalog.json', 'w', encoding='utf-8') as f:
            json.dump(sc_data, f, ensure_ascii=False, indent=2)
        print("Updated data/catalogs/site_catalog.json successfully!")
    except Exception as e:
        print("Note on site_catalog.json:", e)

if __name__ == '__main__':
    enrich_thirukkural_items()
