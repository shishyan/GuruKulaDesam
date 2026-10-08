# -*- coding: utf-8 -*-
"""
Direct High-Speed Vedic Artwork Generator for Chapter 27 (Thavam - Penance / Tapas)
Uses official Google Gemini Image API with user-provided API key.
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
DEST_DIR = ROOT / "production" / "visuals" / "thirukkural" / "27-thavam"
DEST_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY and (ROOT / ".env").exists():
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

BASE_PROMPT = (
    "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. "
    "Set in ancient classical Tamil Nadu. Theme of Thirukkural Chapter 27 (Penance / Tapas / Spiritual Endurance). "
    "Visual subject: {subject}. "
    "Atmosphere: Western Ghats misty granite mountains, sacred Kaveri river, ancient forest hermitages under banyan trees, "
    "sacred Shiva Lingams with bilva leaves, burning agnihotra havan fires, austere sages with Tripundra Vibhuti and Rudraksha malas. "
    "Lighting: golden sunrise rays cutting through mountain mist, or full moon silvery radiance over ancient stone temple towers. "
    "Strictly no modern items, no western clothing, no electrical wires, no text overlays, no watermarks."
)

SUBJECTS = {
    "00-ghats-hermitage-dawn-wide.jpg": "A panoramic wide shot of an ancient Vedic hermitage in the mist-shrouded Western Ghats mountains at dawn with mountain stream and curling havan smoke",
    "01-ascetic-dawn-boulder.jpg": "On a high mountain granite boulder at golden sunrise, an austere Tamil Tapasvi sits in immovable padmasana enduring dawn chill in serene stillness (Kural 261)",
    "02-serene-endurance-face.jpg": "An intimate macro portrait of a venerable Tamil sage in deep meditation with dewdrops on beard and inward tranquil gaze of self-realization (Kural 261)",
    "03-ascetic-sparing-ants.jpg": "A close-up of a meditating ascetic gently lifting his bare hand to let a trail of black ants pass safely across the stone, embodying Ahimsa in Tapas (Kural 261)",
    "04-sage-in-monsoon.jpg": "In a dense ancient forest hermitage during a heavy monsoon downpour, a steadfast Tamil Rishi sits under a banyan root canopy in unwavering meditation (Kural 261)",
    "05-offering-alms-to-ascetic.jpg": "At the granite threshold of a traditional village at dawn, a devout Tamil mother offers warm steamed rice and fruits into the begging bowl of a wandering ascetic (Kural 262)",
    "06-wealth-and-the-renouncer.jpg": "Visual contrast between anxious palace nobles counting gold and a solitary ascetic with nothing but a water pot sitting in supreme bliss under the open sky (Kural 262)",
    "07-sage-power-foe-and-friend.jpg": "In an ancient temple courtyard, a sage of immense penance radiates a golden aura of spiritual gravity (Tejas), transforming adversaries and friends with instant peace (Kural 264)",
    "08-desires-fulfilled-by-tapas.jpg": "In a sunlit forest glade, a seeker sits before a sacred havan fire as divine wisdom and auspicious spiritual attainments manifest like blossoming celestial flowers (Kural 265)",
    "09-panchagni-tapas.jpg": "Vedic Panchagni Tapas: an ascetic in padmasana sits at blistering midday surrounded by four burning fire kundas with the blazing sun as fifth fire, absorbed in Brahman (Kural 265)",
    "10-desire-vs-stillness-market.jpg": "Through a clamorous ancient market street where people chase fleeting desires, a calm ascetic in saffron cloth with Vibhuti walks serenely like an unruffled swan (Kural 266)",
    "11-gold-in-the-fire.jpg": "A close-up in an ancient goldsmith workshop: raw gold in a crucible amidst burning embers, shining brighter as heat burns away dross, allegorizing Tapas (Kural 267)",
    "12-dull-to-radiant-gold.jpg": "From the fiery crucible, a magnificent luminous gold icon of a meditating Shiva is lifted, glowing with divine brilliance that illuminates the stone sanctum (Kural 267)",
    "13-all-bow-to-self-conqueror.jpg": "In a sacred forest clearing at golden sunrise, an enlightened sage who has conquered his ego sits serenely as forest animals and traveling pilgrims bow in homage (Kural 268)",
    "14-ego-dissolving-reflection.jpg": "In a tranquil temple lotus pond at dawn, an ascetic gazes into the water as his reflection dissolves into the radiant golden reflection of the rising sun and cosmos (Kural 268)",
    "15-tapas-before-death.jpg": "On a granite temple terrace at twilight, an enlightened Tapasvi sits in immortal composure as even the shadow of Time and Death stands back in reverence (Kural 269)",
    "16-storm-parts-for-sage.jpg": "A raging tempest over the Western Ghats parts its dark clouds, revealing a shaft of brilliant golden celestial sunlight descending upon a meditating Tamil Rishi (Kural 269)",
    "17-many-wanting-few-ascetics.jpg": "A wide panorama showing multitudes on the plains pursuing worldly goods, while high above on misty ridges only a few solitary ascetics sit in deep Tapas (Kural 270)",
    "18-the-narrow-path-of-tapas.jpg": "A steep ancient stone stairway carved into living rock climbing toward a sunlit summit hermitage as an ascetic ascends through swirling mountain mist (Kural 270)",
    "20-bare-feet-on-hot-rock.jpg": "A close-up of the bare, calloused feet of a wandering Tamil ascetic walking steadily across sun-scorched granite stones with patient equanimity and sacred ash on ankles",
    "21-ascetic-in-cold-stream-sunrise.jpg": "In the icy waters of a mountain stream in the Western Ghats at predawn, an ascetic stands waist-deep offering consecrated arghyam water toward the rising golden sun",
    "22-sage-blesses-poor-family.jpg": "Outside a thatched Tamil cottage at sunset, a wandering sage raises his hand in abhaya mudra to bless an impoverished farmer and family who offered him water",
    "23-hands-with-blooming-lotus.jpg": "A close-up of a meditating ascetic's weathered hands in dhyana mudra upon his lap, holding an opening pink lotus blossom catching morning sunbeams",
    "24-empty-luxury.jpg": "An abandoned, cold royal banquet chamber where golden goblets lie empty in twilight, contrasting with the living sacred glow of a mountain hermitage oil lamp",
    "25-molten-gold-pour.jpg": "In a bronze foundry at sunset, master sthapathis with Vibhuti markings pour glowing liquid bronze into a carved lost-wax mold to create a temple deity",
    "26-king-lays-crown-at-sage-feet.jpg": "In a forest hermitage under a banyan tree at sunset, a King in silk robes voluntarily removes his golden crown, placing it at the bare feet of a serene hermit",
    "27-sage-halo-moonlit-river.jpg": "On the granite steps of the Kaveri river at midnight under a full moon, a meditating Rishi radiates a luminous silvery halo of spiritual aura (Tejas) across water",
    "28-frost-on-the-meditating-sage.jpg": "On a high mountain peak at freezing dawn, white frost clings to the shoulders of a meditating Tapasvi who has sat motionless through the night, melting snow around his seat",
    "29-woman-feeds-the-sage.jpg": "In an ancient Tamil courtyard at midday, a devoted woman in a madisar saree reverently places fresh fruits and tender coconut before a silent visiting sage on a grass mat",
    "30-cave-fire-meditation.jpg": "Inside an ancient granite cave hermitage carved with ancient Tamil Brahmi inscriptions, a lone Rishi sits before a burning oil deepam casting golden light on a stone Lingam",
    "31-disciple-serving-guru.jpg": "In a sunlit Gurukulam courtyard at dawn, a young disciple gently washes the lotus feet of his revered Guru with consecrated water from a brass kamandalu",
    "32-ascetic-carries-injured-bird.jpg": "Along a rocky mountain trail, a gentle ascetic tenderly carries a wounded white dove in the crook of his arm, shielding it with his shawl as he carries it to his ashram",
    "33-unwavering-flame.jpg": "An intimate macro shot inside a temple sanctum: an antique bronze Agal Vilakku burns with an unwavering, perfectly still teardrop flame of golden light in a windless alcove",
    "34-village-lane-reverence.jpg": "In an ancient village lane at sunrise, villagers and women with brass milk pots stand aside with folded hands as a venerable Tapasvi walks silently with wooden sandals",
    "35-sunrise-silhouette-sage.jpg": "An ascetic stands atop a high granite mountain peak at dawn with arms raised in upward adoration (Urdhva Bahu) toward a colossal radiant rising sun filling the horizon",
    "36-solitary-figure-vast-mountain.jpg": "Amidst colossal, misty granite mountain ranges in the Western Ghats under celestial clouds, a tiny solitary ascetic sits on an outcropping in deep meditation",
    "37-sage-with-cobra-and-deer.jpg": "In an ashram clearing, a king cobra with spread hood rests peacefully beside a gentle spotted deer and calf at the feet of a meditating Tamil Rishi in Ahimsa",
    "38-offering-grain-to-sage.jpg": "On the carved granite steps of a temple tank at dawn, an honest farmer offers the first sheaf of golden harvested paddy to a passing ascetic who touches it in blessing",
    "39-emerging-from-cave-radiant.jpg": "After years of deep penance in a mountain cave, an enlightened Tamil Rishi steps into morning sunlight, his countenance radiating a blinding golden light of liberation",
    "40-scholars-honour-ascetic.jpg": "In a grand temple mandapam, venerable Vedic scholars and Rajagurus with palm-leaf manuscripts bow low with folded hands to receive the blessing of a humble ascetic",
    "41-moon-breaks-through-storm.jpg": "Over a sacred temple mountain at midnight, dark storm clouds break apart, revealing a radiant full moon casting silvery luminescence over the temple gopuram and sage",
    "42-hermitage-golden-hour-closing.jpg": "At serene golden hour in an ancient hermitage, disciples sit in meditation while the master performs evening Arati with a flaming camphor deepam before the Shiva Lingam",
    "43-gold-lotus-on-altar.jpg": "On a polished dark granite pedestal before an eternal burning oil lamp, a sculpted golden lotus blossom gleams with radiant perfection, adorned with fresh bilva leaves"
}

def generate_shot(fname, subject):
    out_path = DEST_DIR / fname
    prompt = BASE_PROMPT.format(subject=subject)
    print(f"\n[Chapter 27] Generating {fname}...")
    
    for attempt in range(1, 4):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash-image',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['IMAGE'],
                    image_config=types.ImageConfig(aspect_ratio='16:9')
                )
            )
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    img = Image.open(io.BytesIO(part.inline_data.data))
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    img.save(out_path, format='JPEG', quality=95)
                    print(f" -> SUCCESS! Saved {out_path.name} ({img.size[0]}x{img.size[1]})")
                    return True
            print(f" -> No image found (attempt {attempt})")
        except Exception as e:
            print(f" -> Error on attempt {attempt}: {e}")
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                print(" -> Rate limit hit, sleeping 20s...")
                time.sleep(20)
            else:
                time.sleep(5)
    return False

def main():
    print(f"Starting direct high-speed generation for Chapter 27 ({len(SUBJECTS)} shots)...")
    success = 0
    start_time = time.time()
    
    for fname, subject in sorted(SUBJECTS.items()):
        ok = generate_shot(fname, subject)
        if ok:
            success += 1
        time.sleep(2.5)
        
    elapsed = time.time() - start_time
    print(f"\nCompleted Chapter 27! Generated {success}/{len(SUBJECTS)} shots in {elapsed/60:.1f} minutes.")

if __name__ == "__main__":
    main()
