# -*- coding: utf-8 -*-
"""
tools/update_master_prompts_dual_grammar.py

Updates master_317_song_prompts.json with the strict dual grammar:
1. Devotional songs: Maha Kumbabishekam colorful gopurams, glowing gold kalasams,
   sacred inner garbhagriha, alternating solitary yogis in deep tapas vs vibrant crowd gatherings.
2. Thirukkural songs: Living virtues, domestic harmony, traditional Tamil family life,
   caring for elderly, welcoming guests, village banyan sabhas, Kaveri riverbanks, paddy harvesting.
"""

import json, os, unicodedata, re
from pathlib import Path

ROOT = Path("/home/nagaraj957/GuruKulaDesam")
REG_PATH = ROOT / "production" / "master_317_song_prompts.json"

DEVOTIONAL_STYLE = (
    "A 16:9 cinematic photorealistic devotional photograph, 8k resolution, authentic South Indian Tamil Nadu spiritual aesthetic. "
    "Ancient Chola and Pandyan Dravidian granite temple architecture, majestically carved towering gopurams post-maha-kumbabishekam with "
    "colourful crisp stucco deities and glowing gold kalasams shining in early morning dawn sunlight. "
    "Polished granite sanctum floors reflecting flickering brass agal vilakku deepam lamps, fresh fragrant marigold and jasmine garlands, "
    "gentle swirling sacred dhoopam sambrani incense haze. Devotees with sacred white Tripundra vibhuti on forehead and rudraksha malas, "
    "wearing traditional silk veshti, angavastram, and Kanchipuram silk sarees. "
    "Full-frame 16:9 composition, NO text, NO watermarks, NO modern western items, NO foreign fantasy. Scene: "
)

THIRUKKURAL_STYLE = (
    "A 16:9 cinematic photorealistic cultural photograph, 8k resolution, authentic ancient South Indian Tamil Sangam living traditions. "
    "Traditional Tamil courtyard home with terracotta tiled roof, open pillared thinnai verandah, intricate geometric white rice-flour kolam at sunrise threshold. "
    "Surroundings of lush Kaveri riverbanks, fragrant jasmine gardens, fertile green paddy fields, and ancient shady banyan trees. "
    "Tamil family and community depicting noble virtues: respect for elders, hospitality to guests, harmonious domestic life, mutual love, and selfless integrity. "
    "Traditional attire: clean unbleached cotton and silk veshtis, traditional sarees, authentic South Indian facial features. "
    "Warm natural golden morning light, serene peaceful atmosphere of dharma and human virtue. "
    "Full-frame 16:9 composition, NO temple sanctum idols, NO religious worship, NO modern vehicles, NO text, NO watermarks. Scene: "
)

with open(REG_PATH, "r", encoding="utf-8") as f:
    registry = json.load(f)

# Load batch 2 reference prompts for Thirukkural if available
batch2_file = ROOT / "production" / "generate_batch2_prompts.py"
ch_prompts = {}
if batch2_file.exists():
    text = batch2_file.read_text(encoding="utf-8")
    # extract tuples of ("filename", "title", "prompt")
    matches = re.findall(r'\("([^"]+)",\s*"([^"]+)",\s*"([^"]+)"\)', text)
    for fn, t, p in matches:
        ch = fn.split("/")[0].split("-")[0]
        try:
            c_int = int(ch)
            ch_prompts.setdefault(c_int, []).append(p)
        except Exception:
            pass

updated = 0
for wav_name, data in registry.items():
    cat = data.get("category", "")
    is_kural = "thirukkural" in cat.lower() or "திருக்குறள்" in wav_name or "குறள்" in wav_name
    
    # Check if chapter has dedicated batch2 prompts
    m = re.search(r'Chapter\s*(\d+)', data.get("title", ""))
    c_num = int(m.group(1)) if m else None
    
    new_scenes = []
    if is_kural:
        # Build 24 virtue scenes
        virtue_elements = [
            "Noble Tamil householder lighting the morning brass oil lamp in the central open courtyard, fresh jasmine flowers strewn around, soft dawn light through banana leaves",
            "Welcoming young gurukulam students and travelers on the pillared verandah, offering cool water from a brass kooja, gentle morning breeze",
            "Respectfully offering steaming cooked rice and ghee into the bowls of guests on a stone threshold, mango leaves tied at the doorway",
            "Gently draping a woven shawl over the shoulders of an elderly grandfather resting on a carved wooden cot on the veranda, warm amber lantern glow",
            "Weary travelers seated under a flowering tamarind tree being served warm curd rice and sweet fruits on fresh green banana leaves, golden afternoon sun",
            "Kind Tamil householder giving shelter to a family under the tiled pavilion during heavy tropical monsoon rain, warm oil lamp light on wet flagstones",
            "Measuring golden unhusked paddy from a wicker granary into cloth sacks to share with needy villagers, dust motes in sunbeams",
            "Sitting beside an old village poet on a stone bench under a parijatha tree, listening with deep reverence and attentive care",
            "Standing in Kaveri river at dawn offering cool water from cupped palms to the rising sun, ripples catching pink and gold reflections",
            "Three generations of a loving Tamil family gathered for evening feast on reed mats, smiling warmth, brass platters with wholesome food",
            "Husband and wife together planting a sacred banyan sapling in their garden, pouring water from a clay jug with tender smiles",
            "Husband and wife reviewing palm-leaf family accounts together by the soft glow of a bronze lamp on the veranda, mutual respect and shared harmony",
            "Carved wooden cradle rocking gently under an arbor blooming with fragrant white jasmine flowers, morning light dappling the clay floor",
            "Parents gazing down at their sleeping baby wrapped in soft cotton, profound peace and gentle devotion in their expressions",
            "Upright householder mediating a community discussion beneath a spreading banyan tree with calm wisdom, respected by all",
            "Householders and farmers working together desilting and reinforcing the stone embankments of the village lotus tank in morning sun",
            "Traditional wooden handloom in an open workshop, rhythmic weaving of fine cotton shawls intended as gifts, golden side-lighting",
            "Gathering neem and thulasi leaves into a woven basket in a sunlit herb garden to heal sick neighbors, compassionate smile",
            "Patient elder teaching village children how to carve Tamil script onto palm leaves on a raised stone pyol, warm guidance",
            "Restoring peace between two formerly quarreling farmers on a rustic village lane, joining their hands with gentle upright words",
            "Placing an oil lamp into a carved stone niche at a rural crossroads as night falls, warm beacon guiding lone travelers",
            "Circular threshing floor in golden sunlight, bullocks treading grain stalks, family tossing chaff into the breeze in joyful abundance",
            "High-angle view of a woman drawing an intricate geometric white rice-flour kolam on red mud ground before the wooden doorway at dawn",
            "Aged venerable Tamil sage with snow-white hair and serene luminous eyes, seated beneath a peepal tree overlooking peaceful village at sunset"
        ]
        
        # If we have specific chapter prompts from batch 2
        if c_num and c_num in ch_prompts and len(ch_prompts[c_num]) >= 12:
            base_p = ch_prompts[c_num]
            for i in range(24):
                p_text = base_p[i % len(base_p)]
                new_scenes.append(THIRUKKURAL_STYLE + p_text)
        else:
            ch_title = data.get("title", "")
            for i, elem in enumerate(virtue_elements):
                new_scenes.append(f"{THIRUKKURAL_STYLE} Celebrating {ch_title}. {elem}.")
    else:
        # Devotional Track: Alternate solo individual tapas vs vibrant group gatherings with colorful gopuram
        for i, old_s in enumerate(data.get("scenes", [])):
            clean_s = re.sub(r'^A 16:9 cinematic.*?Scene:\s*', '', old_s)
            clean_s = re.sub(r'^photorealistic.*?Scene:\s*', '', clean_s)
            if i % 2 == 0:
                mix = "Wide majestic view of towering Dravidian temple gopuram post-maha-kumbabishekam with vibrant painted stucco deities and golden kalasams, joyful crowd of devotees in colorful silk procession. "
            else:
                mix = "Intimate close-up of a solitary devout Tamil seeker with Tripundra vibhuti and rudraksha malas, deeply absorbed in meditation with a glowing brass deepam lamp. "
            new_scenes.append(DEVOTIONAL_STYLE + mix + clean_s)
            
    data["scenes"] = new_scenes
    updated += 1

with open(REG_PATH, "w", encoding="utf-8") as f:
    json.dump(registry, f, ensure_ascii=False, indent=2)

print(f"✅ Successfully updated {updated} songs in Master Registry with authentic dual grammar!")
