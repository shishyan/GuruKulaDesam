# -*- coding: utf-8 -*-
"""
Vedic Artwork Generator for Chapter 40: கல்வி (Kalvi - Sacred Vedic Learning & Knowledge)
Uses official Google Gemini Image API with user-provided API key.
Strict Sanatana Vedic & Tamil spiritual heritage:
Gurukulam, palm-leaf manuscripts (Olais), bronze styluses, Vedic Acharyas with Tripundra Vibhuti and Rudraksha,
Brahmachari disciples, temple lotus tanks, Sandhyavandanam, sacred geometry of Yantras.
Strictly NO modern clothing, NO eyeglasses, NO printed books, NO European furniture.
"""

import os
import sys
import time
import io
from pathlib import Path
from PIL import Image
from google import genai
from google.genai import types

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

CH40_DIR = ROOT / "production" / "visuals" / "thirukkural" / "40-kalvi"
CH40_DIR.mkdir(parents=True, exist_ok=True)

CH40_SUBJECTS = {
    "01-n01_mastering_the_palm_leaf_scroll.jpg": "In an open-air Gurukulam portico at sunrise, a young Tamil brahmachari student in saffron veshti and Tripundra Vibhuti attentively unrolls and reads an ancient palm-leaf manuscript (Olai) (Kural 391)",
    "02-n02_scrutinizing_every_verse_for_truth.jpg": "An austere Vedic Acharya with full silver beard, sacred thread, and rudraksha malas carefully guiding a disciple's finger along inscribed Tamil verses on an Olai leaf (Kural 391)",
    "03-n03_walking_the_talk_of_wisdom.jpg": "A noble Tamil scholar householder practicing what he learned, bowing respectfully to an elderly beggar and offering alms with humble grace (Kural 391)",
    "04-n04_dawn_recitation_at_temple_pond.jpg": "At the granite steps of a sacred temple lotus tank at dawn, young Gurukulam disciples recite Vedic hymns facing the golden rising sun (Kural 392)",
    "05-n05_applying_geometry_in_architecture.jpg": "An ancient Tamil Sthapathi (master architect) using wooden compasses and charcoal cords on stone floor to draw sacred Vedic temple mandala geometry (Kural 392)",
    "06-n06_letters_and_numbers_the_two_eyes.jpg": "A close-up of an inscribed palm leaf showing Tamil script alongside ancient numeral symbols, illuminated by the warm golden flame of a bronze oil lamp (Kural 392)",
    "07-n07_blind_without_wisdom_in_darkness.jpg": "Visual contrast between a confused man wandering blindly in shadowy overgrown ruins and a radiant seeker holding a burning ghee lamp of wisdom (Kural 393)",
    "08-n08_the_eyes_of_the_spirit_opened.jpg": "An intimate spiritual portrait of a 20-year-old Tamil seeker whose face glows with illumination as his Guru whispers a sacred mantra into his ear (Kural 393)",
    "09-n09_delight_in_scholarly_communion.jpg": "Under the shade of a sacred banyan tree, a gathering of learned Tamil scholars and poets warmly debating and smiling in intellectual joy (Kural 394)",
    "10-n10_sorrow_at_parting_from_the_wise.jpg": "On a dusty village path at twilight, two venerable scholars clasping hands with wistful smiles as they part ways after days of shared study (Kural 394)",
    "11-n11_humble_service_to_the_guru.jpg": "A devoted young disciple respectfully washing the dust from the bare feet of his revered Vedic Guru with water from a copper vessel (Kural 395)",
    "12-n12_rising_from_servant_to_master.jpg": "Visual transformation: the once humble student now sitting with dignity as an Acharya, teaching the next generation of seekers (Kural 395)",
    "13-n13_the_sandy_spring_yielding_water.jpg": "In the dry sandy bed of the Kaveri river at dawn, villagers dig with bare hands, finding cool, crystal-clear spring water welling up from the sand (Kural 396)",
    "14-n14_the_fountain_of_knowledge_deepening.jpg": "A scholar sitting by an ancient circular granite stone well in an ashram garden, drawing a golden jar of sweet water, allegorizing learning (Kural 396)",
    "15-n15_every_country_is_the_scholars_home.jpg": "A wandering Tamil scholar with palm-leaf scrolls in cloth pouch welcomed warmly into the courtyard of a distant village home in another realm (Kural 397)",
    "16-n16_the_imperishable_treasure_of_learning.jpg": "Visual contrast between piles of tarnished coins in a decayed palace and a serene illuminated sage surrounded by attentive children (Kural 398)",
    "17-n17_learning_transcending_seven_births.jpg": "An ancient temple corridor with stone carvings depicting the cycle of life, while an eternal soul sits in steady spiritual realization (Kural 398)",
    "18-n18_the_joy_of_bringing_light_to_all.jpg": "A wise elder teacher smiling with maternal joy as a circle of young village boys and girls clap in delight upon understanding a great truth (Kural 399)",
    "19-n19_inscribing_olai_with_bronze_stylus.jpg": "Extreme macro close-up of weathered brown fingers holding a pointed bronze stylus, etching crisp ancient Tamil characters into dried palmyra leaf (Kural 400)",
    "20-n20_evening_prayers_in_gurukulam.jpg": "At dusk in a forest Gurukulam, all disciples and Acharyas sit in padmasana around a consecrated havan kunda as fragrant dhoopam smoke rises toward the evening star (Kural 400)",
}

def generate_chapter(ch_num: int, subjects: dict, dest_dir: Path):
    print("=" * 70)
    print(f"GENERATING VEDIC ARTWORKS FOR CHAPTER {ch_num}")
    print(f"Target Directory: {dest_dir}")
    print(f"Total Subjects: {len(subjects)}")
    print("=" * 70)

    base_prompt = (
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. "
        "Set in ancient classical Tamil Nadu. Theme of Thirukkural Chapter 40 (Kalvi - Sacred Vedic Learning). "
        "Visual subject: {subject}. "
        "Atmosphere: ancient open-air Gurukulam hermitages, stone temple courtyards, sacred Kaveri river, "
        "Vedic Acharyas and brahmachari disciples with Tripundra Vibhuti, Rudraksha malas, sacred cotton thread (Yajnopavita), "
        "palm-leaf manuscripts (Olais), bronze styluses, kusha grass mats, brass oil lamps. "
        "Lighting: radiant golden morning sunlight filtering through banyan canopy, or warm twilight oil lamp glow. "
        "Strictly NO modern clothing, NO eyeglasses, NO printed books, NO European furniture, NO text overlays, NO watermarks."
    )

    success_count = 0
    for filename, subject_desc in subjects.items():
        out_path = dest_dir / filename
        if out_path.exists() and out_path.stat().st_size > 20000:
            print(f"  [Exists] {filename}")
            success_count += 1
            continue

        prompt = base_prompt.format(subject=subject_desc)
        print(f"  Generating: {filename}...")

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="16:9"),
                ),
            )
            saved = False
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    img = Image.open(io.BytesIO(part.inline_data.data)).convert("RGB")
                    img.save(out_path, quality=95)
                    print(f"  ✅ Saved: {filename} ({img.size})")
                    saved = True
                    success_count += 1
                    break
            if not saved:
                print(f"  ⚠️ No image in response for {filename}")
            time.sleep(2.5)
        except Exception as e:
            print(f"  ❌ Error on {filename}: {e}")
            time.sleep(5.0)

    print(f"\nChapter {ch_num} Complete: {success_count}/{len(subjects)} images generated!\n")

if __name__ == "__main__":
    generate_chapter(40, CH40_SUBJECTS, CH40_DIR)
