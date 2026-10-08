# -*- coding: utf-8 -*-
import os
import sys
import time
import io
import shutil
from pathlib import Path
from PIL import Image
from google import genai
from google.genai import types

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'production'))
from generate_batch3_prompts import CH42_PROMPTS, CH44_PROMPTS, CH45_PROMPTS, CH46_PROMPTS

API_KEY = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=API_KEY)

CHAPTERS = [
    (42, 'Kelvi - கேள்வி - Sacred Oral Listening & Shruti', '42-kelvi', CH42_PROMPTS),
    (44, 'Kutrangadithal - குற்றங்கடிதல் - Guarding against Faults & Moral Vigilance', '44-kutrangadithal', CH44_PROMPTS),
    (45, 'Periyaaraith Thunaikkodal - பெரியாரைத் துணைக்கோடல் - Cherishing Wise Elders & Rishis', '45-periyaaraith-thunaikkodal', CH45_PROMPTS),
    (46, 'Sitrinanjeraamai - சிற்றினஞ்சேராமை - Avoiding Base Association & Pure Sangha', '46-sitrinanjeraamai', CH46_PROMPTS),
]

BASE_PROMPT = (
    'A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. '
    'Set in ancient classical Tamil Nadu. Theme of Thirukkural Chapter {ch_num} ({ch_name}). '
    'Visual subject: {subject}. '
    'Atmosphere: ancient granite royal courtyards, open-air Gurukulam hermitages, stone temple mandapams, sacred Kaveri river, '
    'Vedic Acharyas, Rishis, kings, and seekers with Tripundra Vibhuti, Rudraksha malas, sacred cotton thread (Yajnopavita), '
    'palm-leaf manuscripts (Olais), bronze oil lamps, kusha grass mats, brass water vessels. '
    'Lighting: radiant golden morning sunlight filtering through banyan canopy, or warm twilight oil lamp glow. '
    'Strictly NO modern clothing, NO eyeglasses, NO printed books, NO European furniture, NO text overlays, NO watermarks.'
)

def run():
    print('=' * 70)
    print('STARTING COMPREHENSIVE VEDIC IMAGE GENERATION FOR BATCH 2 (Ch 42, 44, 45, 46)')
    print('=' * 70)

    for ch_num, ch_name, folder_name, prompts in CHAPTERS:
        target_dir = ROOT / 'production' / 'visuals' / 'thirukkural' / folder_name
        old_secular = ROOT / 'production' / 'visuals' / 'thirukkural' / f'{folder_name}-old-secular'

        # Backup old secular if not backed up yet
        if target_dir.exists() and not old_secular.exists():
            print(f'Backing up {target_dir.name} -> {old_secular.name}...')
            shutil.copytree(target_dir, old_secular)
            # wipe target dir
            for f in target_dir.glob('*.jpg'):
                f.unlink()
            for f in target_dir.glob('*.png'):
                f.unlink()
            print('Cleaned target directory for authentic Vedic imagery.')

        target_dir.mkdir(parents=True, exist_ok=True)
        print(f'\n>>> CHAPTER {ch_num}: {ch_name} ({len(prompts)} artworks)')

        for rel_path, title, desc in prompts:
            fname = Path(rel_path).name
            out_file = target_dir / fname

            if out_file.exists() and out_file.stat().st_size > 25000:
                print(f'  [Exists] {fname}')
                continue

            prompt = BASE_PROMPT.format(ch_num=ch_num, ch_name=ch_name, subject=f'{title}. {desc}')
            print(f'  Generating: {fname}...')

            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash-image',
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_modalities=['IMAGE'],
                            image_config=types.ImageConfig(aspect_ratio='16:9'),
                        ),
                    )
                    saved = False
                    if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                        for part in response.candidates[0].content.parts:
                            if part.inline_data:
                                img = Image.open(io.BytesIO(part.inline_data.data)).convert('RGB')
                                img.save(out_file, quality=95)
                                print(f'  ✅ Saved: {fname} ({img.size})')
                                saved = True
                                break
                    if saved:
                        break
                    else:
                        print(f'  ⚠️ Retrying {fname} (attempt {attempt+1})...')
                        time.sleep(3)
                except Exception as e:
                    print(f'  ⚠️ Error on attempt {attempt+1} for {fname}: {e}')
                    time.sleep(4)

            time.sleep(2.5)

    print('\n' + '=' * 70)
    print('ALL BATCH 2 VEDIC ARTWORKS GENERATED SUCCESSFULLY!')
    print('=' * 70)

if __name__ == '__main__':
    run()
