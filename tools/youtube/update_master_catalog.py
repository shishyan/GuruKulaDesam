import sys, json, os

sys.stdout.reconfigure(encoding='utf-8')

new_5_entries = [
    {
        "video_id": "n9lAyAdzo60",
        "canonical_title": "திருக்குறள்: அதிகாரம் 26 - புலால் உண்ணாமை | Thirukkural: Pulaal Unnaamai [Film]",
        "tamil_title": "திருக்குறள்: அதிகாரம் 26 - புலால் உண்ணாமை",
        "english_title": "Thirukkural: Pulaal Unnaamai",
        "descriptor": "Film",
        "length": 76,
        "genre": "திருக்குறள் (Thirukkural)",
        "track_type": "Cinematic Film / Video",
        "author": "திருவள்ளுவர் (Thiruvalluvar)",
        "source": "திருக்குறள்",
        "playlists": ["Discography", "திருக்குறள் | Thirukkural — Master Collection"],
        "youtube_url": "https://www.youtube.com/watch?v=n9lAyAdzo60",
        "duration": "PT4M40S",
        "published_at": "2026-10-07T09:00:00Z",
        "scripture_source": "திருக்குறள்"
    },
    {
        "video_id": "FvpGjzaW2TA",
        "canonical_title": "திருக்குறள்: அதிகாரம் 27 - தவம் | Thirukkural: Thavam [Film]",
        "tamil_title": "திருக்குறள்: அதிகாரம் 27 - தவம்",
        "english_title": "Thirukkural: Thavam",
        "descriptor": "Film",
        "length": 62,
        "genre": "திருக்குறள் (Thirukkural)",
        "track_type": "Cinematic Film / Video",
        "author": "திருவள்ளுவர் (Thiruvalluvar)",
        "source": "திருக்குறள்",
        "playlists": ["Discography", "திருக்குறள் | Thirukkural — Master Collection"],
        "youtube_url": "https://www.youtube.com/watch?v=FvpGjzaW2TA",
        "duration": "PT4M37S",
        "published_at": "2026-10-07T09:00:00Z",
        "scripture_source": "திருக்குறள்"
    },
    {
        "video_id": "F6PrK6E9qB0",
        "canonical_title": "திருக்குறள்: அதிகாரம் 52 - தெரிந்து வினையாடல் | Thirukkural: Therinthu Vinaiyaadal [Film]",
        "tamil_title": "திருக்குறள்: அதிகாரம் 52 - தெரிந்து வினையாடல்",
        "english_title": "Thirukkural: Therinthu Vinaiyaadal",
        "descriptor": "Film",
        "length": 86,
        "genre": "திருக்குறள் (Thirukkural)",
        "track_type": "Cinematic Film / Video",
        "author": "திருவள்ளுவர் (Thiruvalluvar)",
        "source": "திருக்குறள்",
        "playlists": ["Discography", "திருக்குறள் | Thirukkural — Master Collection"],
        "youtube_url": "https://www.youtube.com/watch?v=F6PrK6E9qB0",
        "duration": "PT6M23S",
        "published_at": "2026-10-07T09:00:00Z",
        "scripture_source": "திருக்குறள்"
    },
    {
        "video_id": "oEH4ztdn2Nc",
        "canonical_title": "திருக்குறள்: அதிகாரம் 54 - பொச்சாவாமை | Thirukkural: Pochchaavaamai [Film]",
        "tamil_title": "திருக்குறள்: அதிகாரம் 54 - பொச்சாவாமை",
        "english_title": "Thirukkural: Pochchaavaamai",
        "descriptor": "Film",
        "length": 72,
        "genre": "திருக்குறள் (Thirukkural)",
        "track_type": "Cinematic Film / Video",
        "author": "திருவள்ளுவர் (Thiruvalluvar)",
        "source": "திருக்குறள்",
        "playlists": ["Discography", "திருக்குறள் | Thirukkural — Master Collection"],
        "youtube_url": "https://www.youtube.com/watch?v=oEH4ztdn2Nc",
        "duration": "PT5M20S",
        "published_at": "2026-10-07T09:00:00Z",
        "scripture_source": "திருக்குறள்"
    },
    {
        "video_id": "Mata6vtnrjQ",
        "canonical_title": "திருக்குறள்: அதிகாரம் 61 - மடியின்மை | Thirukkural: Madiyinmai [Film]",
        "tamil_title": "திருக்குறள்: அதிகாரம் 61 - மடியின்மை",
        "english_title": "Thirukkural: Madiyinmai",
        "descriptor": "Film",
        "length": 70,
        "genre": "திருக்குறள் (Thirukkural)",
        "track_type": "Cinematic Film / Video",
        "author": "திருவள்ளுவர் (Thiruvalluvar)",
        "source": "திருக்குறள்",
        "playlists": ["Discography", "திருக்குறள் | Thirukkural — Master Collection"],
        "youtube_url": "https://www.youtube.com/watch?v=Mata6vtnrjQ",
        "duration": "PT4M10S",
        "published_at": "2026-10-07T09:00:00Z",
        "scripture_source": "திருக்குறள்"
    }
]

targets = [
    'master_all_598_songs_catalog.json',
    'assets/data/master_all_598_songs_catalog.json',
    'docs/assets/data/master_all_598_songs_catalog.json',
    'site/assets/data/master_all_598_songs_catalog.json'
]

for t in targets:
    if os.path.exists(t):
        master = json.load(open(t, encoding='utf-8'))
        existing_ids = {m['video_id'] for m in master}
        added = 0
        for entry in new_5_entries:
            if entry['video_id'] not in existing_ids:
                master.append(entry)
                existing_ids.add(entry['video_id'])
                added += 1
        with open(t, 'w', encoding='utf-8') as f:
            json.dump(master, f, ensure_ascii=False, indent=2)
        print(f"Updated {t}: added {added}, total count is now {len(master)}")

