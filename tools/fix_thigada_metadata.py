import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('production/youtube_lyrics_overrides.json', 'r', encoding='utf-8') as f:
    ovr = json.load(f)

works = ovr.get('_works', {})
thigada = works.get('thigada', {})

with open('live_youtube_metadata.json', 'r', encoding='utf-8') as f:
    meta = json.load(f)

# Update mQpQEuXiEZ4 and Yvlg_8JBHL4 with authentic Thigada Sakkaram
for tid in ['mQpQEuXiEZ4', 'Yvlg_8JBHL4']:
    if tid in meta:
        title = "கந்த புராணம்: திகட சக்கர சண்முகத்தோன் (காப்பு) | Kandha Puranam: Thigada Sakkara [Film]"
        new_desc = f'''═════════════════════════════════════════════════════════════
🕉️ குரு குல தேசம் | GURUKULA DESAM PRESENTS
═════════════════════════════════════════════════════════════

{title}
அருளாளர்: கச்சியப்ப சிவாச்சாரியார் (Saint Kachiyappa Sivachariyar)

═════════════════════════════════════════════════════════════
📜 பாடல் வரிகள் (FULL TAMIL LYRICS)
═════════════════════════════════════════════════════════════

{thigada['lyrics']}

═════════════════════════════════════════════════════════════
📖 பொருள் விளக்கம் (DEVOTIONAL MEANING & ESSENCE)
═════════════════════════════════════════════════════════════

{thigada['meaning']}

═════════════════════════════════════════════════════════════
🌐 GURUKULA DESAM DIGITAL SANCTUARY
Official Educational & Devotional Archive
Explore complete hymns, commentaries & courses:
https://gurukuladesam.com

#GurukulaDesam #Vinayagar #KandhaPuranam #DevotionalTamil #TamilHymns'''
        meta[tid]['description'] = new_desc
        meta[tid]['has_lyrics'] = True
        print(f"Updated live_youtube_metadata for {tid} -> Thigada Sakkara")

with open('live_youtube_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print("Updated live_youtube_metadata.json for Vinayagar Thigada Sakkaram!")
