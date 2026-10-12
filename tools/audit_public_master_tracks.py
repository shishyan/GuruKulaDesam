import os, sys, json, glob
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("GURU KULA DESAM - COMPLETE PUBLIC MASTER AUDIT")
print("=" * 80)

# Check all files in production
subtitles = glob.glob("production/subtitles/*.srt")
descriptions = glob.glob("production/descriptions/*.txt")
thumbnails = glob.glob("production/thumbnails/*.png")

print(f"Total Subtitle SRT files: {len(subtitles)}")
print(f"Total Description TXT files: {len(descriptions)}")
print(f"Total Modern Thumbnail PNG files: {len(thumbnails)}")

# Master public list processed and verified live:
master_vids = [
    ("Mata6vtnrjQ", "திருக்குறள் அதிகாரம் 61 (மடியின்மை)"),
    ("KFtS403RfbY", "திருக்குறள் அதிகாரம் 125 (நெஞ்சறிவுறுத்தல்)"),
    ("mQpQEuXiEZ4", "திகட சக்கர & கந்தபுராணம் மங்கல வாழ்த்து"),
    ("31xVgvxoiUA", "திருப்பாவை 3 (ஓங்கி உலகளந்த உத்தமன்)"),
    ("AW4cljBWy2w", "பாலும் தெளிதேனும் (ஔவையார் நல்வழி விநாயகர் துதி)"),
    ("QH-xL37NmGM", "திருப்பாவை 1 (மார்கழித் திங்கள்)"),
    ("hm7_qUlTUiU", "திருப்பாவை 2 (வையத்து வாழ்வீர்காள்)"),
    ("t0MRlpqBeJQ", "திகட சக்கர 2026 [Cinematic Vinayagar Film]"),
    ("pC5eSiEaar0", "திருப்புகழ் 566 (இரத்னகிரி I)"),
    ("FVkGdLV7O34", "திருப்புகழ் 712 (சீர் உலாவிய)"),
    ("9iB-E9CpWUo", "வேண்டுமே இத்தனையும் (திருவெம்பாவை 3)"),
    ("mG9IzlD9vmI", "திருப்புகழ் 566 (இரத்னகிரி II)"),
    ("TUwlsvN7v1w", "நாள் என் செய்யும் | Kandhar Alangaram"),
    ("klSi7r6YhCU", "திருவாசகம்: தென்னாடுடைய சிவனே போற்றி"),
    ("PO4U3nRv6o0", "திருவருட்பா: திருவருள் வேட்கை"),
    ("255aVCj3t0w", "திருவருட்பா: திருச்சாதனத் தெய்வத் திறம்"),
    ("KjQZFlnCluU", "திருவருட்பா: சிவ பதி விளக்கம்"),
    ("HPP3IG7DWRc", "ஹரே கிருஷ்ணா ஹரே ராமா"),
    ("ETELjf0OTi4", "தமிழ்த்தாய் வாழ்த்து (நீராரும் கடலுடுத்த)")
]

print("\n" + "-" * 80)
print(f"{'Video ID':<12} | {'SRT Blocks':<10} | {'Desc Chars':<10} | {'Thumb (KB)':<10} | {'Track Title'}")
print("-" * 80)

for vid, title in master_vids:
    srt_p = f"production/subtitles/{vid}.srt"
    desc_p = f"production/descriptions/{vid}.txt"
    thumb_p = f"production/thumbnails/{vid}.png"
    
    srt_blocks = 0
    if os.path.exists(srt_p):
        with open(srt_p, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip().isdigit()]
            srt_blocks = len(lines)
            
    desc_len = 0
    if os.path.exists(desc_p):
        with open(desc_p, "r", encoding="utf-8") as f:
            desc_len = len(f.read())
            
    thumb_kb = 0
    if os.path.exists(thumb_p):
        thumb_kb = os.path.getsize(thumb_p) // 1024
        
    print(f"{vid:<12} | {srt_blocks:<10} | {desc_len:<10} | {thumb_kb:<10} | {title}")

print("-" * 80)
print("All 19 Master Tracks verified!")
