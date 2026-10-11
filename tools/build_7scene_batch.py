import json
from pathlib import Path
import re

ROOT = Path("c:/GitHub/Gurukuladesam")
manifest = json.load(open(ROOT / 'production' / 'pending_google_flow_manifest.json', encoding='utf-8'))
ready = manifest.get('ready_to_generate', [])

seven_scene_batch = []

angles = [
    ('Wide low-angle dolly along ancient temple granite flagstones', 'illuminated by evening deepam oil lamps with sacred golden warmth'),
    ('Majestic telephoto tracking shot through sacred lotus pond', 'reflecting the towering Dravidian temple gopuram in gentle morning breeze'),
    ('Close atmospheric pan over bronze Kuthuvilakku oil lamps', 'sacred dhoopam sambrani incense smoke drifting softly against carved temple pillars'),
    ('Slow cinematic crane rise looking out from the temple mandapam', 'panoramic view of Kaveri river ghats and coconut palm groves under soft dawn skies')
]

for item in ready:
    bp_rel = item.get('blueprint_file')
    bp = ROOT / bp_rel if bp_rel else None
    if not bp or not bp.exists():
        continue
    content = bp.read_text(encoding='utf-8')
    blocks = re.findall(r'### Scene (\d+)[^\n]*\n(?:\*\*Prompt:\*\*\s*)?([\s\S]*?)(?=(?:### Scene|\Z))', content)
    if not blocks:
        continue
        
    scenes = []
    for num, block in blocks:
        prompt_match = re.search(r'Prompt:\s*([\s\S]*?)(?=(?:\*Exclusions:\*|Exclusions:|\Z))', block)
        prompt = prompt_match.group(1).strip() if prompt_match else block.strip()
        prompt = ' '.join(prompt.split())
        excl_match = re.search(r'Exclusions:\s*([\s\S]*?)$', block)
        excl = excl_match.group(1).strip() if excl_match else 'No text, no subtitles, no modern clothes'
        scenes.append({
            'scene_num': int(num),
            'prompt': prompt,
            'negative_prompt': 'No text, no subtitles, no watermarks, no modern clothing, no western clothes, no shoes, no plastic, no anime, ' + excl
        })
    
    if len(scenes) >= 7:
        selected_scenes = scenes[:7]
    else:
        selected_scenes = list(scenes)
        var_idx = 0
        while len(selected_scenes) < 7:
            base = scenes[var_idx % len(scenes)]
            angle_prefix, mood_suffix = angles[(len(selected_scenes) - len(scenes)) % len(angles)]
            base_prompt = base['prompt']
            mod_prompt = f"{angle_prefix}. {base_prompt}. {mood_suffix}."
            selected_scenes.append({
                'scene_num': len(selected_scenes) + 1,
                'prompt': mod_prompt,
                'negative_prompt': base['negative_prompt']
            })
            var_idx += 1
            
    seven_scene_batch.append({
        'track_id': item.get('video_id'),
        'category': item.get('category'),
        'title': item.get('title'),
        'scenes': selected_scenes
    })

out_file = ROOT / 'production' / 'colab_handoff' / 'pending_7scenes_batch_prompts.json'
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump({'total_tracks': len(seven_scene_batch), 'target_scenes_per_track': 7, 'tracks': seven_scene_batch}, f, indent=2, ensure_ascii=False)

print(f'Successfully built 7-scene packages for {len(seven_scene_batch)} tracks at {out_file}!')
