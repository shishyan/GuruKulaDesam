import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load Master Songs Catalog
with open('master_all_598_songs_catalog.json', encoding='utf-8') as f:
    master_songs = json.load(f)

# 2. Load Playlists Backup (contains all playlist video IDs)
with open('production/youtube_backup/playlists.json', encoding='utf-8') as f:
    playlists_backup = json.load(f)

# 3. Load Audio Master tracks
with open('production/thirukkural_audio_master_tracks.json', encoding='utf-8') as f:
    audio_tracks_data = json.load(f)

audio_tracklist = audio_tracks_data['sequential_tracklist']
audio_vids = set(t['videoId'] for t in audio_tracklist)

# Map playlists
pl_dict = {}
for pl in playlists_backup['playlists']:
    pid = pl['id']
    title = pl['snippet']['title']
    pl_dict[pid] = {
        'id': pid,
        'title': title,
        'count': pl['contentDetails']['itemCount'],
        'items': playlists_backup['items'].get(pid, [])
    }

print("="*80)
print("COMPREHENSIVE CATALOG & PLAYLIST COVERAGE AUDIT")
print("="*80)
print(f"Total songs registered in Master Catalog: {len(master_songs)}")
print(f"Total Audio Tracks registered in Audio Master: {len(audio_tracklist)} (across {audio_tracks_data['total_chapters']} chapters)")

print("\n--- CHANNEL PLAYLISTS OVERVIEW ---")
for pid, pdata in pl_dict.items():
    print(f"  [{pid}] {pdata['title']:<48} | {len(pdata['items']):3d} items (metadata count: {pdata['count']})")

# Grand Master is 'Discography' (PLAjtBRKl_IlI)
disco_items = set(pl_dict.get('PLAjtBRKl_IlI', {}).get('items', []))
print(f"\nGrand Master Playlist ('Discography' - PLAjtBRKl_IlI): {len(disco_items)} items")

# Audit all songs against Discography
catalog_vids = {s['video_id']: s for s in master_songs}

missing_from_disco = []
present_in_disco = []

for vid, song in catalog_vids.items():
    if vid in disco_items:
        present_in_disco.append(song)
    else:
        missing_from_disco.append(song)

print(f"\n--- DISCOGRAPHY (GRAND MASTER) AUDIT ---")
print(f"Songs in Master Catalog present in Discography:     {len(present_in_disco):3d} / {len(master_songs)}")
print(f"Songs in Master Catalog MISSING from Discography:     {len(missing_from_disco):3d} / {len(master_songs)}")

# Breakdown of missing by genre
genre_missing = {}
for s in missing_from_disco:
    g = s.get('genre', 'Unknown')
    genre_missing[g] = genre_missing.get(g, 0) + 1

print("\nBreakdown of Missing Songs by Category / Genre:")
for g, cnt in sorted(genre_missing.items(), key=lambda x: -x[1]):
    print(f"  * {g:<40}: {cnt:3d} missing")

# Breakdown of missing by track type
type_missing = {}
for s in missing_from_disco:
    t = s.get('track_type', 'Unknown')
    type_missing[t] = type_missing.get(t, 0) + 1

print("\nBreakdown of Missing Songs by Track Type:")
for t, cnt in sorted(type_missing.items(), key=lambda x: -x[1]):
    print(f"  * {t:<40}: {cnt:3d} missing")

# Also check Audio Master tracks against Discography
audio_in_disco = [vid for vid in audio_vids if vid in disco_items]
audio_missing_disco = [vid for vid in audio_vids if vid not in disco_items]
print(f"\nThirukkural Audio Tracks in Discography: {len(audio_in_disco)} / {len(audio_vids)}")
print(f"Thirukkural Audio Tracks MISSING from Discography: {len(audio_missing_disco)} / {len(audio_vids)}")

# Thirukkural Video Master Collection (PLW7qBZp_Q8Ro) audit
tk_video_items = set(pl_dict.get('PLW7qBZp_Q8Ro', {}).get('items', []))
tk_songs_in_catalog = [s for s in master_songs if 'Thirukkural' in s.get('genre', '') or 'திருக்குறள்' in s.get('genre', '')]
tk_videos_in_catalog = [s for s in tk_songs_in_catalog if s.get('track_type') != 'Audio Track (Master Composition)']

print(f"\n--- THIRUKKURAL VIDEO MASTER (PLW7qBZp_Q8Ro) AUDIT ---")
print(f"Total Thirukkural entries in Master Catalog: {len(tk_songs_in_catalog)}")
print(f"  - Video Compositions / Films: {len(tk_videos_in_catalog)}")
print(f"  - Audio Track Releases: {len(tk_songs_in_catalog) - len(tk_videos_in_catalog)}")
print(f"Videos currently in Video Master Playlist: {len(tk_video_items)}")

# List the first 25 missing songs from Discography for detailed reporting
print("\n" + "="*80)
print("SAMPLE OF SONGS MISSING FROM GRAND MASTER (DISCOGRAPHY):")
print(f"{'No':<3} | {'Video ID':<11} | {'Category':<28} | {'Title'}")
print("-"*80)
for idx, s in enumerate(missing_from_disco[:25], 1):
    vid = s['video_id']
    cat = s.get('genre', '')[:28]
    title = s.get('canonical_title', '')[:45]
    print(f"{idx:2d}  | {vid:<11} | {cat:<28} | {title}")

# Save detailed analysis
with open('production/grand_master_audit_results.json', 'w', encoding='utf-8') as f:
    json.dump({
        'total_master_songs': len(master_songs),
        'present_in_grand_master': len(present_in_disco),
        'missing_from_grand_master': len(missing_from_disco),
        'missing_by_genre': genre_missing,
        'missing_by_type': type_missing,
        'missing_songs_list': [
            {
                'videoId': s['video_id'],
                'title': s.get('canonical_title'),
                'tamil_title': s.get('tamil_title'),
                'genre': s.get('genre'),
                'track_type': s.get('track_type')
            }
            for s in missing_from_disco
        ]
    }, f, indent=2, ensure_ascii=False)
print("\nDetailed results saved to production/grand_master_audit_results.json")
