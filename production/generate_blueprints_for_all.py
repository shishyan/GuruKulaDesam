# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Universal Google Flow Blueprint Generator
Generates authentic Sanatana Vedic prompt blueprints for all remaining songs
in the catalog based on deity, scripture source, and genre.
"""

import os
import sys
import re
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "master_all_598_songs_catalog.json"
PROMPTS_DIR = ROOT / "production" / "google_flow_prompts"

GENRE_FOLDER_MAP = {
    "சிவபெருமான் (Lord Shiva)": "shiva",
    "முருகப் பெருமான் (Lord Murugar)": "murugan",
    "வள்ளலார் / சன்மார்க்கம் (Thiruvarutpa / Sanmargam)": "vallalar_cultural",
    "அம்மன் / சக்தி (Goddess Amman)": "amman",
    "விநாயகர் (Lord Vinayagar)": "vinayagar",
    "விஷ்ணு / கிருஷ்ணர் (Lord Vishnu & Krishna)": "vishnu_krishna",
    "மரபு & கலாச்சாரம் (Cultural & Heritage)": "vallalar_cultural",
    "திருக்குறள் (Thirukkural)": "thirukkural",
}

THEME_TEMPLATES = {
    "shiva": {
        "cat_name": "SHIVA",
        "continuity": {
            "Atmosphere": "Natural sacred Shaivite ambience, predawn misty Brahmamuhurtham, warm bronze kuthuvilakku flames, subtle natural dhoopam haze.",
            "Architecture": "Ancient South Indian Chola/Pandya monolithic granite mandapams, pillared corridors, sanctum carved Nandi, temple tank steps.",
            "Lighting": "Warm golden lamp light, soft predawn indigo and rose gold, deep shadows along weathered granite stone.",
            "Hard Exclusions": "No text, no subtitles, no watermarks, no logos, no modern vehicles, no electric wiring, no plastic, no morphing fingers/limbs, no floating objects."
        },
        "scenes": [
            {
                "num": 1,
                "title": "Sanctum Threshold & Sacred Flame",
                "prompt": "Create a single continuous 16:9 cinematic photorealistic video shot at 24 fps. In warm predawn indigo and amber temple light, show an ancient South Indian granite sanctum entrance. Slow forward dolly move past carved stone pillars toward an ancient Shiva Lingam gently illuminated by flickering bronze oil lamps. Fresh Bilva leaves and white parijatha blossoms rest upon the polished black stone pedestal. A brass dhoopam burner sits on a stone ledge, curling gentle translucent grey incense smoke into the dawn air. Sacred silence, natural lighting, 8k resolution.",
                "exclusions": "No text, no modern items, no digital zoom, no camera shake."
            },
            {
                "num": 2,
                "title": "Temple Corridors & Devotional Solitude",
                "prompt": "Create a single continuous 16:9 cinematic live-action video shot at 24 fps. Slow lateral tracking shot through a magnificent Dravidian thousand-pillared granite corridor. Beams of early morning sunlight cut through morning mist, illuminating intricate carvings of Rishis, devas, and sacred motifs. A lone devotee in an unstitched white cotton veshti and sacred Tripundra Vibhuti walks peacefully toward the sanctum. Profound spiritual surrender, authentic historical atmosphere.",
                "exclusions": "No morphing limbs, no cartoon styling, no modern clothes, no text."
            },
            {
                "num": 3,
                "title": "Cosmic Temple Tower & Mountain Dawn",
                "prompt": "Create a single continuous 16:9 cinematic slow crane rise at 24 fps. Reveal the towering Rajagopuram stone temple tower silhouetted against the rising morning sun behind sacred mountain ridges resembling Annamalai. Morning mist drifts across the serene temple tank reflecting the golden sky. Divine tranquility, eternal presence.",
                "exclusions": "No lens flare artifacts, no rapid motion, no modern buildings, no text."
            }
        ]
    },
    "murugan": {
        "cat_name": "MURUGAN",
        "continuity": {
            "Atmosphere": "Sacred hilltop breezes, morning mist over flowering kadamba and marukozhundhu groves, bronze kuthuvilakku glow, fragrant sandal and rose water mist.",
            "Architecture": "Ancient Tamil Sangam hill-shrine, monolithic granite steps, carved peacock motifs, sanctum threshold.",
            "Lighting": "Golden sunrise amber light breaking through emerald mountain foliage, soft glowing dawn.",
            "Hard Exclusions": "No text, no subtitles, no watermarks, no modern vehicles, no electric wiring, no plastic."
        },
        "scenes": [
            {
                "num": 1,
                "title": "Sacred Hilltop & Golden Spear",
                "prompt": "Create a single continuous 16:9 cinematic photorealistic video shot at 24 fps. On a tranquil sacred hilltop in ancient Tamil Nadu at sunrise, slow dolly move toward an ancient granite shrine where a gleaming bronze Vel (sacred spear of wisdom) stands enshrined, adorned with fresh garlands of red viruchi flowers and fragrant green marukozhundhu. Soft morning mountain breeze, glowing oil lamps, 8k resolution.",
                "exclusions": "No modern items, no digital zoom, no text."
            },
            {
                "num": 2,
                "title": "Sacred Peacock & Temple Steps",
                "prompt": "Create a single continuous 16:9 cinematic live-action video shot at 24 fps. Slow lateral slider shot across ancient carved granite temple steps overlooking mist-shrouded green valleys. A majestic wild peacock with iridescent emerald-blue plumage rests calmly on a stone balustrade in morning sunbeams. Fragrant dhoopam incense curls softly into the mountain breeze.",
                "exclusions": "No cartoon effects, no morphing feathers, no text."
            },
            {
                "num": 3,
                "title": "Hilltop Gopuram & Distant Ocean",
                "prompt": "Create a single continuous 16:9 cinematic crane rise at 24 fps. Panoramic view of an ancient seaside Dravidian temple gopuram illuminated by radiant dawn sunlight against the sparkling blue ocean waters of Thiruchendur. Flocks of white sea birds soar past in peaceful morning air. Sublime spiritual majesty.",
                "exclusions": "No rapid motion, no modern ships, no text."
            }
        ]
    },
    "amman": {
        "cat_name": "AMMAN",
        "continuity": {
            "Atmosphere": "Divine maternal grace, fragrance of fresh turmeric, kumkum, neem leaves, and red hibiscus, soft glow of hundreds of small clay agal vilakkus.",
            "Architecture": "Ancient South Indian Devi sanctum, carved granite pillars, brass ornamental doorways, sacred temple courtyard.",
            "Lighting": "Rich warm amber and crimson twilight glow, golden temple lamps reflecting on polished brass.",
            "Hard Exclusions": "No text, no subtitles, no watermarks, no modern clothing, no plastic."
        },
        "scenes": [
            {
                "num": 1,
                "title": "Devi Sanctum & Sacred Lamps",
                "prompt": "Create a single continuous 16:9 cinematic photorealistic video shot at 24 fps. Slow forward dolly move through an ancient temple courtyard illuminated by dozens of glowing bronze oil lamps. In the sanctum, offerings of fresh red hibiscus garlands, green neem leaves, and consecrated brass kalasams glow with divine warmth. Translucent incense smoke rises gently toward the carved stone ceiling.",
                "exclusions": "No text, no modern artifacts, no digital jitter."
            },
            {
                "num": 2,
                "title": "Lotus Tank & Evening Aarti",
                "prompt": "Create a single continuous 16:9 cinematic live-action video shot at 24 fps. Across the wide carved granite steps of a sacred temple lotus tank at dusk, traditional brass deepams float gently on the mirror-like water among blooming pink lotuses. Warm twilight reflections of carved temple pillars, peaceful and deeply sacred.",
                "exclusions": "No morphing water, no neon lights, no text."
            },
            {
                "num": 3,
                "title": "Majestic Gopuram & Evening Sky",
                "prompt": "Create a single continuous 16:9 cinematic crane rise at 24 fps. Looking up at the towering intricately sculpted Gopuram of an ancient South Indian temple against a deep velvet twilight sky adorned with the first evening star. Fragrant evening breeze, holy tranquility.",
                "exclusions": "No electric lights, no text, no modern wires."
            }
        ]
    },
    "vallalar_cultural": {
        "cat_name": "VALLALAR_CULTURAL",
        "continuity": {
            "Atmosphere": "Universal compassion (Jeeva Karunyam), pristine morning light, white lotus ponds, fragrant camphor flame (Arutperunjothi), pure tranquil air.",
            "Architecture": "Traditional Tamil pillared hermitage, open-sky courtyards (muttram), sacred village sabha, ancient river ghats.",
            "Lighting": "Luminous pure white and golden sunlight, dawn breaking over Kaveri watercourses and paddy fields.",
            "Hard Exclusions": "No text, no watermarks, no modern vehicles, no plastic, no Western elements."
        },
        "scenes": [
            {
                "num": 1,
                "title": "The Eternal Light of Grace (Arutperunjothi)",
                "prompt": "Create a single continuous 16:9 cinematic photorealistic video shot at 24 fps. In a quiet, serene white marble and granite meditation hall at dawn, slow dolly forward toward a pure, steady golden flame glowing within an ancient bronze deepam. White lotus blossoms float peacefully in shallow brass vessels on the stone floor. Divine stillness and universal peace, 8k resolution.",
                "exclusions": "No text, no modern fixtures, no camera shake."
            },
            {
                "num": 2,
                "title": "Universal Compassion & Fertile Fields",
                "prompt": "Create a single continuous 16:9 cinematic live-action video shot at 24 fps. Panoramic ground-level tracking shot across ancient emerald-green Tamil paddy fields bordered by majestic coconut palms and water lilies. Gentle calves and white cows graze peacefully in morning dew as farmers in simple cotton veshtis tend irrigation channels. Epitome of Jeeva Karunyam and rural harmony.",
                "exclusions": "No modern tractors, no plastic, no text."
            },
            {
                "num": 3,
                "title": "Ancient Hermitage & Rising Sun",
                "prompt": "Create a single continuous 16:9 cinematic gentle crane rise at 24 fps. An ancient Tamil ashram hermitage surrounded by flowering jasmine gardens, banyan trees, and tranquil water tanks bathed in radiant morning sunlight. Complete spiritual clarity and grace.",
                "exclusions": "No rapid motion, no modern artifacts, no text."
            }
        ]
    },
    "thirukkural": {
        "cat_name": "THIRUKKURAL",
        "continuity": {
            "Atmosphere": "Sangam era classical dignity, mountain mist over Western Ghats, morning sunlight filtering through ancient banyan groves, gentle procedural dhoopam haze.",
            "Architecture": "Ancient Tamil rural mandapams, granite steps, open courtyards, village sabhas with stone benches.",
            "Lighting": "Warm 6:00 AM golden dawn sunlight, backlight through lush tropical foliage.",
            "Hard Exclusions": "No text, no subtitles, no watermarks, no modern vehicles, no electric wires, no plastic."
        },
        "scenes": [
            {
                "num": 1,
                "title": "Sangam Dawn & Sacred Valley",
                "prompt": "Create a single continuous 16:9 cinematic photorealistic video shot at 24 fps. Wide aerial glide over majestic Western Ghats mountain ridges in ancient Tamil Nadu at predawn. Layered misty green peaks, morning clouds drifting gently across forested valleys, pristine mountain stream flowing through weathered granite boulders. 8k resolution, calm spiritual grandeur.",
                "exclusions": "No modern items, no roads, no buildings, no text."
            },
            {
                "num": 2,
                "title": "Vedic Courtyard & Moral Contemplation",
                "prompt": "Create a single continuous 16:9 cinematic live-action video shot at 24 fps. Ground-level slow dolly forward along an ancient carved granite courtyard surrounded by lush tropical trees and blooming parijatha flowers. Bronze oil lamps glow on stone ledges with natural flickering flames. An elder in traditional veshti sits in noble reflection with palm-leaf manuscripts.",
                "exclusions": "No morphing limbs, no text, no modern artifacts."
            },
            {
                "num": 3,
                "title": "Tranquil Temple Tank & Horizon",
                "prompt": "Create a single continuous 16:9 cinematic slow crane rise at 24 fps. Looking across a serene temple lotus tank reflecting the rising sun and distant Dravidian temple gopuram in soft mist. Profound inner peace, ethical clarity, timeless wisdom.",
                "exclusions": "No rapid motion, no modern artifacts, no text."
            }
        ]
    }
}

def generate_blueprint_content(item, template):
    title = item.get("tamil_title") or item.get("canonical_title")
    eng_title = item.get("english_title") or item.get("canonical_title")
    tid = item.get("video_id")
    cat = template["cat_name"]
    
    cb = template["continuity"]
    scenes = template["scenes"]
    
    lines = [
        f"# Google Flow Cinematic Video Plan — {title}",
        f"**English Title:** {eng_title}  ",
        f"**Track ID:** `{tid}`  ",
        f"**Category:** {cat}  ",
        f"**Soundtrack:** Original master release from Guru Kula Desam (`{tid}.m4a`).  ",
        f"**Visual Grammar:** Photorealistic 16:9, 24 fps, authentic South Indian spiritual temple aesthetic, 8k resolution.",
        "",
        "---",
        "",
        "## Locked Continuity Bible",
        f"- **Atmosphere:** {cb['Atmosphere']}",
        f"- **Architecture:** {cb['Architecture']}",
        f"- **Lighting:** {cb['Lighting']}",
        f"- **Hard Exclusions:** {cb['Hard Exclusions']}",
        "",
        "---",
        "",
        "## 10-Second Continuous Scene Prompts for Google Flow",
        ""
    ]
    
    for s in scenes:
        lines.append(f"### Scene {s['num']} (00:0{s['num']-1} - 00:0{s['num']}): {s['title']}")
        lines.append("**Prompt:**  ")
        lines.append(s["prompt"])
        lines.append(f"*Exclusions:* {s['exclusions']}")
        lines.append("")
        
    return "\n".join(lines)

def main():
    cat_items = json.load(open(CATALOG, encoding="utf-8"))
    print(f"Loaded {len(cat_items)} songs from master catalog.")
    
    created_count = 0
    skipped_count = 0
    
    for item in cat_items:
        tid = item.get("video_id")
        genre = item.get("genre", "")
        
        folder = GENRE_FOLDER_MAP.get(genre, "vallalar_cultural")
        target_dir = PROMPTS_DIR / folder
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if a blueprint for this track_id already exists anywhere in PROMPTS_DIR
        existing = list(PROMPTS_DIR.glob(f"*/{tid}*.md"))
        if existing:
            skipped_count += 1
            continue
            
        tmpl_key = folder
        if tmpl_key not in THEME_TEMPLATES:
            tmpl_key = "vallalar_cultural"
        template = THEME_TEMPLATES[tmpl_key]
        
        safe_title = re.sub(r'[^a-zA-Z0-9_\-]', '_', item.get("english_title") or "track")[:25].strip('_')
        out_filename = f"{tid}_{safe_title}.md"
        out_path = target_dir / out_filename
        
        content = generate_blueprint_content(item, template)
        out_path.write_text(content, encoding="utf-8")
        created_count += 1
        
    print(f"Blueprint generation complete!")
    print(f"Created new blueprints: {created_count}")
    print(f"Existing blueprints preserved: {skipped_count}")
    print(f"Total blueprints now in production/google_flow_prompts/: {len(list(PROMPTS_DIR.glob('*/*.md')))}")

if __name__ == "__main__":
    main()
