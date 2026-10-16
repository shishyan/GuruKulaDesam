#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/gen_non_kural_scene_images.py
Generates thematic 16:9 photorealistic devotional images for Non-Kural audio tracks
using gemini-2.5-flash-image (or gemini text + flash-image).
"""
import os, sys, io, json, time, argparse
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

ROOT = Path(__file__).resolve().parents[1]

KEY = os.environ.get("GEMINI_API_KEY")
if not KEY and (ROOT / ".env").exists():
    for ln in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if ln.startswith("GEMINI_API_KEY="):
            KEY = ln.split("=", 1)[1].strip().strip('"').strip("'")
client = genai.Client(api_key=KEY, http_options=types.HttpOptions(timeout=120000))

BASE_STYLE = (
    "A 16:9 cinematic photorealistic devotional photograph, 8k, Tamil Nadu, vivid, warm, and sacred. "
    "Temples look pristine and majestic after a sacred maha kumbabishekam: intricately carved gopuram with "
    "colourful crisp stucco deities, glowing gold kalasams shining in early morning sunlight, polished granite "
    "sanctum floors reflecting flickering brass oil lamps (deepams), fragrant fresh marigold and jasmine garlands, "
    "sacred dhoopam incense smoke gently wafting. Devotees in clean traditional festive attire (silk veshti, angavastram, silk sarees). "
    "Full-frame edge-to-edge 16:9 composition, NO letterbox borders, no text, no watermark. Scene: "
)

def clean_frame(img):
    import numpy as np
    a = np.asarray(img.convert("L"))
    rows = np.where(a.mean(axis=1) > 14)[0]
    cols = np.where(a.mean(axis=0) > 14)[0]
    if len(rows) and len(cols):
        img = img.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))
    w, h = img.size
    tw = int(h * 16 / 9)
    if tw <= w:
        x = (w - tw) // 2
        img = img.crop((x, 0, x + tw, h))
    else:
        th = int(w * 9 / 16)
        y = (h - th) // 2
        img = img.crop((0, y, w, y + th))
    return img.resize((1280, 720), Image.LANCZOS)

def render_image(prompt, out_path, style=BASE_STYLE):
    out_path = Path(out_path)
    if out_path.exists() and out_path.stat().st_size > 10000:
        print(f"  ⏩ {out_path.name} already exists.")
        return True

    print(f"  🎨 Generating {out_path.name}: {prompt[:80]}...")
    for attempt in range(1, 6):
        try:
            r = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=style + prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="16:9")
                )
            )
            for part in r.candidates[0].content.parts:
                if part.inline_data:
                    img = Image.open(io.BytesIO(part.inline_data.data)).convert("RGB")
                    img = clean_frame(img)
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    img.save(out_path, "JPEG", quality=95)
                    print(f"  ✔ Saved {out_path.name} ({out_path.stat().st_size // 1024} KB)")
                    return True
        except Exception as e:
            s = str(e)
            print(f"   [attempt {attempt}] {s[:120]}")
            if "429" in s or "RESOURCE_EXHAUSTED" in s:
                time.sleep(25)
            else:
                time.sleep(5)
    return False

## Preset visual scene scripts for key tracks
KUNRAM_ERINTHAI_PROMPTS = [
    # S01: Grand Krauncha Mountain & Vel
    "Epic panoramic view of sacred granite mountain peak Krauncha split by a glowing golden Vel (divine spear) of Lord Murugan, rays of divine golden dawn sunlight breaking through misty mountain clouds over lush Western Ghats.",
    # S02: Morning Temple Gopuram & Devotees
    "Grand view of Thirupparamkunram rock-cut hill temple at dawn, towering gopuram with golden kalasam, colorful painted stucco figures, early morning mist, flock of sacred temple pigeons flying.",
    # S03: Devotees singing Thirumurugatruppadai
    "Devout Tamil people gathered on temple steps in white silk veshtis and green silk sarees, holding bronze thalams with flowers and sacred lamps, singing divine devotional hymns with peaceful bhakti expressions.",
    # S04: Lord Murugan Sanctum Shrine
    "Glowing inner garbhagriha sanctum shrine of Lord Murugan holding the shining golden Vel, surrounded by multiple bronze standing deepams flickering warmly, red chembaruthi hibiscus and fragrant white jasmine garlands.",
    # S05: Sacred Royal Peacock in Temple Courtyard
    "A majestic royal blue peacock with fully unfurled radiant iridescent feathers perched gracefully on an ancient carved granite pillar in the morning temple courtyard.",
    # S06: Bronze Aarti & Sacred Smoke
    "Close-up of a multi-tiered bronze camphor aarti lamp being waved by temple priests, glowing orange flames, fine swirling aromatic dhoopam incense haze wafting through stone mandapam pillars.",
    # S07: Devotees Carrying Kavadi
    "Group of devotees carrying decorated arched wooden Mayil Kavadis adorned with peacock feathers, chanting Vel Muruga with deep devotional ecstasy during sunrise temple festival procession.",
    # S08: Mountain Stream & Waterfall
    "Crystal clear mountain stream cascading down mossy granite boulders in Kurinji landscape, surrounded by wild blooming flame lilies (Kanthal flowers) and morning mountain mist.",
    # S09: Ancient Carved Stone Mandapam
    "Pillared temple corridor carved with sacred Sangam period sculptures of warriors and sages, warm golden morning sunbeams streaming through stone pillars onto polished granite floor.",
    # S10: Devotee Offering Lotus Flowers
    "Hands of a Tamil devotee offering freshly picked pink lotus flowers at the sacred lotus feet of the bronze Murugan deity, brass water pot and sandalwood paste nearby.",
    # S11: Golden Vel Close-up with Vibhuti
    "Artistic close-up of a divine golden Vel spear decorated with three sacred horizontal white vibhuti stripes and a bright red kumkum thilagam, surrounded by fragrant jasmine garlands.",
    # S12: Majestic Sunset over Mountain Temple
    "Breathtaking twilight sunset silhouette of the hilltop Murugan temple perched high on the rocky cliff against a fiery orange, purple and golden sky, solitary temple bell ringing.",
    # S13: Sacred Rooster flag fluttering at sunrise
    "Radiant red silk Seval Kodi (sacred rooster flag of Lord Murugan) fluttering victoriously in morning breeze atop an ancient brass flagstaff (Dhwajasthambam) against sunrise skies.",
    # S14: Murugan Abhishekam with milk and sandalwood
    "Sacred sanctum abhishekam ritual: pure white milk and golden sandalwood paste gently pouring over the ancient bronze idol of Lord Murugan, holy chants reverberating.",
    # S15: Sangam poet Nakkirar reciting verses
    "Venerable Sangam Tamil poet Nakkirar with flowing beard and rudraksha beads seated in meditation on a smooth granite rock near the temple theertham, holding palm leaf stylus.",
    # S16: Paal Kudam (Milk pot) procession of women
    "Solemn procession of Tamil women devotees wearing bright yellow sarees, gracefully carrying brass milk pots (Paal Kudam) crowned with neem leaves and coconut on their heads.",
    # S17: Rock-cut cave sculptures of Thirupparamkunram
    "Ancient rock-hewn bas-relief panels carved directly into monolithic granite mountain walls depicting Lord Murugan's wedding to Deivayanai, soft oil lamp illumination.",
    # S18: Holy ash (Vibhuti) distribution to devotees
    "Temple priest placing sacred fragrant white vibhuti and vermillion kumkum on the forehead of a humble Tamil devotee with folded hands, warm divine tranquility.",
    # S19: Kurinji mountain blossoms in full bloom
    "Rolling misty mountain slopes blanketed by rare purple Kurinji flowers in full bloom under misty blue sky, sacred haven of Lord Murugan.",
    # S20: Brass Nadaswaram and Thavil musicians
    "Traditional temple musicians playing ornate brass Nadaswaram pipes and Thavil drums with rhythmic devotion during the morning festive pooja in the mandapam.",
    # S21: Devotee ascending thousand stone steps
    "Ancient stone stairway ascending the sacred hill, dotted with devotees climbing barefoot with lamps and offerings, panoramic view of green Tamil plains below.",
    # S22: Bronze Utsava Murti procession under silk umbrella
    "Glittering bronze Utsava Murti of Lord Murugan flanked by Valli and Deivayanai seated on an ornate golden peacock palanquin sheltered by a royal velvet umbrella.",
    # S23: Temple tank water lilies and lamps
    "Sacred temple tank at twilight with floating clay lamps (Agal vilakku) casting golden ripples amongst blooming purple water lilies, reflecting temple towers.",
    # S24: Grand Maha Deepam on mountain summit
    "Colossal sacred brass Maha Deepam cauldron ablaze with pure ghee fire atop the mountain summit, illuminating the entire valley under night starry sky."
]


PAZHAMAI_PROMPTS = [
    # S01: Two lifelong Tamil elders conversing under ancient banyan tree
    "Two distinguished elderly Tamil scholars with silver hair and warm smiling eyes, dressed in pristine white silk veshtis and angavastrams, sitting affectionately under the vast shade of an ancient sacred banyan tree with hanging aerial roots, reflecting profound ancient friendship (பழைமை).",
    # S02: Sangam era Thinnai (verandah) intimate conversation
    "Traditional Chettinad/Tamil heritage home open front verandah (thinnai) with polished rosewood pillars and Athangudi terracotta tiles, two lifelong companion friends sharing tender betel leaf and warm filter coffee in bronze davara tumblers at morning sunbeam.",
    # S03: Sacred courtyard lamp lit between families
    "Grand ancestral courtyard mutham illuminated by the warm golden glow of a traditional tall brass Kuthuvilakku, two generations of bonded lifelong family friends greeting each other with folded palms and deep affection.",
    # S04: Palm leaf manuscript reading together
    "Close-up cinematic shot of two revered scholars gently unrolling ancient Tamil palm leaf manuscripts (olai chuvadi) on a wooden table, warm oil lamp light casting sacred amber highlights, shared wisdom and unreserved intimacy.",
    # S05: Sacred temple tank steps at dawn
    "Serene ancient temple theertham (sacred water tank) with stone steps, two devoted Tamil companions in traditional attire standing side side watching the reflection of the towering temple gopuram in calm rippling water at golden hour.",
    # S06: Offering prasadam with uninhibited right and love
    "Hands of a loving lifelong friend offering sweet sakkarai pongal in a banana leaf directly to another companion without formality or hesitation, embodying Thiruvalluvar's verse on rights earned through timeless affection.",
    # S07: Ancient stone pavilion in village groves
    "Historic carved stone ambalam pavilion nestled amidst lush green coconut groves and paddy fields, two village elders walking arm-in-arm, sharing joyous laughter that spans five decades.",
    # S08: Brass Urli with fragrant jasmine and floating diyas
    "Close-up of a heavy antique bronze urli vessel filled with fresh water, floating fragrant white madurai malli jasmine flowers and miniature clay oil lamps, soft evening temple smoke drifting in background.",
    # S09: Grand Tamil library / sanctum of learning
    "Ancient Gurukulam hall lined with teakwood book racks and sacred sculptures, two gurus in meditation and silent understanding beside a glowing brass oil lamp.",
    # S10: Welcoming an old companion at the carved wooden threshold
    "An open carved teakwood double-door entrance of an ancestral Tamil home, a host smiling with unconditional joy and extended hands as his oldest friend arrives across the threshold.",
    # S11: Village riverbank sunset with cows and companions
    "Peaceful Tamil village Cauvery riverbank at sunset, golden rays turning the river into liquid gold, gentle cows walking home, two companions sitting quietly on the grassy bank watching the sun dip below the horizon.",
    # S12: Inner sanctum blessings of long-standing devotion
    "Warm sanctuary of an ancient granite temple, two devoted friends receiving sacred vibhuti and tulasi theertham from the temple priest, golden glow illuminating their peaceful, enlightened faces.",
    # S13: Traditional outdoor feast with lifelong comrades
    "Traditional open-air Tamil feast under banana plant canopy, long row of green banana leaves served with aromatic ghee rice, sambar, and payasam, lifelong companions dining together with deep familial warmth.",
    # S14: Young childhood friends playing pallanguzhi
    "Two young Tamil village children in traditional pavadai and veshti playing the ancient wooden Pallanguzhi game with shiny tamarind seeds on a sunlit veranda floor, innocence and seed of timeless bond.",
    # S15: Walking side-by-side through golden paddy fields
    "Wide cinematic vista of lush emerald-green Tamil Nadu paddy fields stretching to the horizon under golden late-afternoon sun, two farmer companions carrying wooden ploughs and walking along the narrow bund.",
    # S16: Temple car (Ther) festival participation together
    "Towering intricately carved wooden temple chariot (Ther) during festive procession, ocean of joyful devotees, two lifelong friends pulling the thick sacred coconut ropes together with united devotion.",
    # S17: Ancient village well and stone tub
    "Mossy stone village well surrounded by shade trees, an elder pulling up a brass pot of sweet well water to pour into his tired companion's cupped hands on a hot afternoon, gentle compassion.",
    # S18: Shared music and Veena recital
    "Carved pillared hall where a maestro plays the Saraswati Veena while his dearest lifelong companion listens with eyes closed and tears of musical ecstasy, brass oil lamp casting amber glow.",
    # S19: Antique brass swing (Oonjal) in ancestral home
    "Heavy carved brass and teakwood swing (Oonjal) swaying gently in a breezy central courtyard, an elderly couple and their lifelong family friends conversing warmly surrounded by fragrant flower garlands.",
    # S20: Chanting hymns at the village Shiva temple Nandi
    "Granite stone Nandi statue anointed with sandalwood and fresh bilva leaves, two companion elders chanting ancient Thevaram verses together with radiant devotional smiles.",
    # S21: Strolling along ancient seashore at dusk
    "Ancient shore temple of Mamallapuram silhouettes against crashing ocean waves and lavender-gold dusk sky, two lifelong friends walking quietly along the sandy shoreline reflecting on years passed.",
    # S22: Sharing medicinal herbal tea in brass cups
    "Cozy kitchen hearth corner with terracotta pots, steam rising from warm sukku karupatti herbal tea poured into shining brass tumbler sets, shared smiles and tender care between old friends.",
    # S23: Deep discussion beside antique grandfather clock
    "Study room filled with vintage leather-bound Tamil literary works, antique pendulum clock ticking gently, two intellectual companions engaged in animated philosophical dialogue over poetry.",
    # S24: Starry night sky on open terrace
    "Open terrace of an ancestral village home under a clear sky sparkling with thousands of stars, gentle night breeze moving jasmine creepers, two lifelong friends sitting on a coir cot gazing at the heavens in peaceful contentment."
]


THIRUPPARAMKUNRAM_PROMPTS = [
    # S01: First Arupadai Veedu panoramic dawn vista
    "Epic sweeping cinematic dawn panorama of Thirupparamkunram hill and temple, the sacred first abode of Lord Murugan (முதல் படை வீடு), golden morning light breaking over ancient carved granite gopurams.",
    # S02: Divine celestial wedding (Deivayanai Thirukalyanam)
    "Vibrant Sangam-period depiction of Lord Murugan in royal golden attire seated beside Goddess Deivayanai on an ornate throne in the celestial wedding mandapam, holy rishis chanting auspicious Vedic hymns.",
    # S03: Sacred Saravana Poigai temple theertham
    "Sacred crystal-clear waters of Saravana Poigai theertham at sunrise, blooming pink lotuses, sacred stone ghats reflecting towering carved hill shrines.",
    # S04: Rock-hewn sanctum and underground passages
    "Ancient granite rock-cut sanctum cut deep into the monolithic mountain side, multiple brass oil lamps flickering warmly against timeless stone bas-relief carvings.",
    # S05: Devotees carrying towering Mayil Kavadis
    "Spiritual procession of Tamil devotees climbing the sacred hill carrying tall curved Mayil Kavadis decorated with peacock feathers and holy bells, intense bhakti atmosphere.",
    # S06: Grand silver Vel procession
    "Palanquin carrying the sacred Silver Vel anointed with sandalwood paste and fragrant jasmine garlands, surrounded by waving silk fans and torchbearers at twilight.",
    # S07: Ancient Shiva sanctum inside Murugan temple
    "Intricate granite shrine of Lord Shiva and Goddess Parvati within the rock-cut cave temple, soft incense smoke swirling past monolithic pillars.",
    # S08: Sacred peacocks dancing on mountain rocks
    "Two magnificent wild peacocks dancing with unfurled iridescent royal blue and green feathers on sun-warmed rocky crags overlooking the green Madurai valley.",
    # S09: Traditional Tamil wedding blessings at temple hall
    "Traditional Tamil couple receiving wedding blessings before the deity in the grand stone pillar mandapam of Thirupparamkunram, surrounded by smiling elders in silk pattu sarees.",
    # S10: Devotee lighting 108 clay agal deepams
    "Devout hands reverently lighting rows of 108 small terracotta oil lamps (agal deepams) along the granite temple steps as night falls.",
    # S11: Chanting Sangam hymns in pillared hall
    "Scholars and Othuvars seated in silk shawls chanting Thiruppugazh and Thirumurugatruppadai hymns with bronze cymbals, warm amber temple lighting.",
    # S12: Royal flagpole (Dhwajasthambam) with peacock mount
    "Towering brass-plated Dhwajasthambam with the radiant peacock mount facing the sanctum, adorned with fresh mango leaves and marigold garlands.",
    # S13: Abhishekam with tender coconut and holy water
    "Sacred abhishekam of the mountain deity with tender coconut water, milk, and honey, divine droplets glistening against ancient bronze sculpture.",
    # S14: Cave carvings of Lord Ganesha and Murugan
    "Ancient monolith rock panel depicting Lord Vinayagar (Karpaga Vinayagar) alongside his brother Murugan, glowing under pure ghee oil lamps.",
    # S15: Women making floral thoranams and garlands
    "Temple women stringing thousands of fragrant Madurai malli jasmine flowers and red oleanders into exquisite long garlands under carved stone eaves.",
    # S16: Temple priests offering Mahadeeparadhana
    "Chief priests in silk dhotis lifting a five-tiered camphor brass deepam, bright sacred flame casting radiant reflections across polished granite floors.",
    # S17: Sunset view of the Madurai plains from hill top
    "Breathtaking golden-hour view from the Thirupparamkunram hill peak looking toward the distant Madurai Meenakshi gopurams against a violet and gold twilight sky.",
    # S18: Holy ash and Panchamirtham prasadam distribution
    "Devotees receiving fragrant Palani-style panchamirtham and blessed white vibhuti into their hands with gratitude and radiant smiles.",
    # S19: Sacred banyan tree shrine with tridents
    "Ancient spreading banyan tree at the base of the sacred hill with several iron and brass tridents (Vel) tied with red sacred threads, rustic folk devotion.",
    # S20: Chariot festival night procession
    "Illuminated temple chariot (Ther) draped in colorful silk tapestries moving through cheering crowds under festive fireworks and starry night sky.",
    # S21: Devotee performing Angapradakshinam
    "Humble devotee performing devotional rolling circumambulation (Angapradakshinam) around the cool stone outer corridors of the sanctum.",
    # S22: Bronze Nataraja shrine in rock cave
    "Rare rock-cut representation of Lord Nataraja performing the cosmic dance within the cave pavilion, shadows and highlights dancing in lamplight.",
    # S23: Holy temple elephant showering blessings
    "Decorated temple elephant with vibhuti marks and brass head ornaments gently tapping a devotee's head in affectionate blessing at the temple entrance.",
    # S24: Starry night over the illuminated monolithic rock
    "The massive sacred rocky hill of Thirupparamkunram glowing in the night illuminated by temple floodlights under a brilliant star-filled sky."
]

THEME_REGISTRY = {
    "kunram_erinthai": KUNRAM_ERINTHAI_PROMPTS,
    "pazhamai": PAZHAMAI_PROMPTS,
    "thirupparamkunram": THIRUPPARAMKUNRAM_PROMPTS,
}

def generate_track_scenes(theme_key, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if theme_key not in THEME_REGISTRY:
        raise ValueError(f"Unknown theme: {theme_key}. Available: {list(THEME_REGISTRY.keys())}")

    prompts = THEME_REGISTRY[theme_key]
    print(f"Generating {len(prompts)} scene images for '{theme_key}' in {out_dir}...")
    for idx, prompt in enumerate(prompts):
        out_file = out_dir / f"scene_{idx+1:02d}.jpg"
        render_image(prompt, out_file)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--theme", default="kunram_erinthai", choices=list(THEME_REGISTRY.keys()))

    p.add_argument("--out-dir", default=None)
    args = p.parse_args()

    if args.out_dir is None:
        args.out_dir = str(ROOT / "production" / "scene_images" / args.theme)

    generate_track_scenes(args.theme, args.out_dir)

