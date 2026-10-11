import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

with open('production/releases_chapter_analysis.json', encoding='utf-8') as f:
    analysis = json.load(f)

with open('production/master_133_athikarams.json', encoding='utf-8') as f:
    master = json.load(f)

matched = analysis['matched_releases']
# Also include the 7 unmatched that we manually mapped:
unmatched_map = {
    'வரைவின்மகளிர்': (92, 'வரைவின் மகளிர்'),
    'பெண்வழிச்சேறல்': (91, 'பெண்வழிச் சேறல்'),
    'பொருள்செயல்வகை': (76, 'பொருள் செயல்வகை'),
    'அவை அஞ்சாமை': (73, 'அவையஞ்சாமை'),
    'குற்றம் கடிதல்': (44, 'குற்றங்கடிதல்'),
    'இறை மாட்சி': (39, 'இறைமாட்சி'),
    'அவா அறுத்தல்': (37, 'அவாவறுத்தல்')
}

all_target_releases = {}
for ch_str, r in matched.items():
    ch_num = int(ch_str)
    all_target_releases[ch_num] = r

for u in analysis.get('unmatched_kural', []):
    clean = u.get('clean', '')
    if clean in unmatched_map:
        ch_num, ch_name = unmatched_map[clean]
        all_target_releases[ch_num] = {
            'chapter_num': ch_num,
            'chapter_name': ch_name,
            'release_title': u.get('title', ''),
            'href': u.get('href', ''),
            'rowText': u.get('rowText', '')
        }

print(f"Total target Thirukkural chapter releases: {len(all_target_releases)}")
sorted_ch_nums = sorted(all_target_releases.keys())
print(f"Chapters covered: {sorted_ch_nums}")

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9225')
    ctx = browser.contexts[0]
    page = ctx.pages[0]

    tracks_by_chapter = {}
    
    # Process each chapter release
    for idx, ch_num in enumerate(sorted_ch_nums, 1):
        rel = all_target_releases[ch_num]
        href = rel.get('href', '')
        # href is like https://studio.youtube.com/release/b_zOXoDZxwePN/overview
        if '/release/' not in href:
            # Let's extract release id from rowText or href
            import re
            m = re.search(r'b_[a-zA-Z0-9_-]+', href + ' ' + rel.get('rowText', ''))
            if m:
                rel_id = m.group(0)
            else:
                print(f"[{idx}/{len(sorted_ch_nums)}] Warning: No release ID for Ch {ch_num}")
                continue
        else:
            rel_id = href.split('/release/')[1].split('/')[0]

        browse_id = f"MPRE{rel_id}"
        print(f"[{idx}/{len(sorted_ch_nums)}] Fetching Ch {ch_num} ({rel['chapter_name']}) - {browse_id} ...", flush=True)

        tracks = page.evaluate('''async (bid) => {
            const resp = await fetch('/youtubei/v1/browse?prettyPrint=false', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    context: window.ytcfg ? window.ytcfg.get('INNERTUBE_CONTEXT') : {},
                    browseId: bid
                })
            });
            const data = await resp.json();
            const results = [];
            
            // Search mutations for musicTrack
            try {
                const mutations = data.frameworkUpdates.entityBatchUpdate.mutations;
                for (const m of mutations) {
                    if (m.payload && m.payload.musicTrack) {
                        const mt = m.payload.musicTrack;
                        results.push({
                            videoId: mt.videoId,
                            title: mt.title,
                            artist: mt.artistNames
                        });
                    }
                }
            } catch(e) {}

            // Fallback: search regex for videoIds
            if (results.length === 0) {
                const str = JSON.stringify(data);
                const matches = [];
                const regex = /"videoId":"([a-zA-Z0-9_-]{11})"/g;
                let m;
                while ((m = regex.exec(str)) !== null) {
                    matches.push(m[1]);
                }
                const uniq = [...new Set(matches)];
                for (const vid of uniq) {
                    results.push({ videoId: vid, title: 'Track', artist: '' });
                }
            }
            return results;
        }''', browse_id)

        print(f"    Found {len(tracks)} tracks for Ch {ch_num}: {[t['videoId'] for t in tracks]}", flush=True)
        tracks_by_chapter[ch_num] = {
            'chapter_num': ch_num,
            'chapter_name': rel['chapter_name'],
            'release_title': rel['release_title'],
            'release_id': rel_id,
            'browse_id': browse_id,
            'tracks': tracks
        }
        time.sleep(0.2)

    total_tracks_count = sum(len(v['tracks']) for v in tracks_by_chapter.values())
    print(f"\nSuccessfully resolved {total_tracks_count} audio tracks across {len(tracks_by_chapter)} chapters!")

    # Flatten sequential tracklist
    sequential_tracklist = []
    for ch_num in sorted(tracks_by_chapter.keys()):
        ch_data = tracks_by_chapter[ch_num]
        for t_idx, track in enumerate(ch_data['tracks'], 1):
            sequential_tracklist.append({
                'chapter_num': ch_num,
                'chapter_name': ch_data['chapter_name'],
                'track_index_in_chapter': t_idx,
                'videoId': track['videoId'],
                'title': track['title'],
                'artist': track.get('artist', '')
            })

    output_data = {
        'total_chapters': len(tracks_by_chapter),
        'total_tracks': len(sequential_tracklist),
        'chapters': tracks_by_chapter,
        'sequential_tracklist': sequential_tracklist
    }

    with open('production/thirukkural_audio_master_tracks.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print("Saved to production/thirukkural_audio_master_tracks.json")
