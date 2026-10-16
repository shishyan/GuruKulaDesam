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

_CLIENT = None
def get_client():
    global _CLIENT
    if _CLIENT is not None:
        return _CLIENT
    key = os.environ.get("GEMINI_API_KEY")
    if not key and (ROOT / ".env").exists():
        for ln in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
            if ln.startswith("GEMINI_API_KEY="):
                key = ln.split("=", 1)[1].strip().strip('"').strip("'")
    if not key:
        try:
            from google.colab import userdata
            key = userdata.get("GEMINI_API_KEY")
        except Exception:
            pass
    if not key:
        raise ValueError("GEMINI_API_KEY not found. Please set GEMINI_API_KEY environment variable or Colab secret.")
    _CLIENT = genai.Client(api_key=key, http_options=types.HttpOptions(timeout=120000))
    return _CLIENT

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
            client = get_client()
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
    # S23: Devotees singing Thevaram hymns at the outer rock corridor
    "Group of elder Tamil devotees seated in the breezy rock-cut corridor chanting ancient Thevaram verses with hand cymbals, peaceful amber temple lighting.",
    # S24: Starry night over the illuminated monolithic rock
    "The massive sacred rocky hill of Thirupparamkunram glowing in the night illuminated by temple floodlights under a brilliant star-filled sky."
]

THIRUAVINANKUDI_PROMPTS = [

    # S01: Palani foothills and sacred lake at dawn
    "Epic panoramic sunrise vista over the sacred foothills of Palani (திருஆவினன்குடி - Third Arupadai Veedu), lush coconut palm groves and morning mist rising over Shanmugha river.",
    # S02: Divine Child Ascetic Bala Dandayudhapani
    "Luminous sacred sanctum of young Lord Murugan as Bala Dandayudhapani, ascetic child wearing kaupeenam with shaved head and vibhuti, holding the divine staff (danda) and glowing golden Vel.",
    # S03: Sacred holy cow Kamadhenu worship
    "Divine Kamadhenu white sacred cow adorned with floral garlands and golden horn tips, standing gracefully by the lotus pond worshiping the baby Murugan.",
    # S04: Sage Agastya receiving divine Tamil wisdom
    "Venerable Sage Agastya with flowing white beard and rudraksha beads receiving sacred wisdom from Lord Murugan under the sacred Kadamba tree, glowing golden halos.",
    # S05: Devotees offering Kavadi at temple base
    "Colorful festive crowd of Tamil devotees carrying curved flower-decked Mayil and Theertha Kavadis with peacock feathers at the entrance of Thiruavinankudi temple.",
    # S06: Sacred Panchamirtham preparation with mountain fruits
    "Temple priests in traditional silk preparing authentic Palani Panchamirtham with pure mountain hill bananas, palm sugar, honey, cardamom, and pure ghee in massive bronze vessels.",
    # S07: Golden chariot circumambulation at sunset
    "Splendid golden chariot (Thanga Ther) radiating warm light carrying the Utsava deity around the temple outer praharam as dusk turns the sky into deep amber.",
    # S08: Shanmugha river holy bathing ghats
    "Devotees taking sacred morning dip in the gentle waters of Shanmugha Nadi (river) carrying bronze pots of holy theertham for abhishekam.",
    # S09: Ancient temple elephant blessing pilgrims
    "Majestic decorated temple elephant with auspicious gopuram thilagam gently touching a child pilgrim's head with its trunk outside the ancient stone gopuram.",
    # S10: Sannidhi of Goddess Lakshmi and Bhooma Devi
    "Sacred shrine inside Thiruavinankudi depicting Goddess Lakshmi and Bhooma Devi who worshiped Lord Murugan here, glowing oil deepams casting warm divine rays.",
    # S11: Devotee tonsuring head in pure devotion
    "A humble Tamil devotee sitting on temple courtyard steps offering hair tonsure (Mottai) in fulfillment of prayer, pure white sandalwood paste cooling the head.",
    # S12: Stone carved pillars of the Nayak mandapam
    "Magnificent pillared hall carved with life-size statues of Sangam warriors and divine guardians, sunlight filtering through stone eaves creating dramatic beams.",
    # S13: Golden Vel decorated with fresh red Kanthal flowers
    "Artistic macro view of the gleaming golden Vel spear adorned with vibrant flame lilies (Kanthal - state flower of Tamil Nadu) and fragrant jasmine buds.",
    # S14: Traditional musicians playing pipe and drums
    "Temple musicians playing resonant Thavil drums and long golden Nadaswaram pipes during the noon pooja procession in the mandapam.",
    # S15: Hilltop temple visible from the foot shrine
    "Breathtaking view from Thiruavinankudi looking up at the high cliff summit of the Palani hill temple crowned with golden vimanam against vibrant azure sky.",
    # S16: Paal Kudam milk pot procession at sunrise
    "Dozens of devoted women in traditional saffron sarees carrying shining brass Paal Kudams topped with neem leaves and coconut in single file toward the sanctum.",
    # S17: Sage Bogar crafting the Navapashanam idol
    "Mystic Siddha master Bogar in deep concentration preparing the miraculous nine-herbal medicine amalgam (Navapashanam) statue inside a cave workshop.",
    # S18: Camphor aarti reflecting on granite floors
    "Bright blazing camphor flames of the multi-level brass aarti lamp held high by the chief priest, illuminating the holy deity with dramatic reflections.",
    # S19: Ancient sacred Kadamba tree shrine
    "Spreading ancient Kadamba tree surrounded by thousands of yellow and red cloth cradles tied by childless couples praying for blessings.",
    # S20: Devotees singing Thiruppugazh hymns
    "Group of elder Tamil devotees singing Arunagirinathar's rhythmic Thiruppugazh with small bronze cymbals (Jalar), tears of devotion and joy.",
    # S21: Night view of the hill illuminated with lamps
    "The entire Palani mountain stairway and summit glowing with ten thousand golden electric lights and deepams under a velvet night sky.",
    # S22: Bronze peacock mount facing sanctum
    "Graceful antique bronze statue of the royal peacock mount with curved neck and delicate plumage standing sentinel before the holy sanctum.",
    # S23: Distributing holy vibhuti and panchamirtham
    "Smiling temple priest offering fragrant vibhuti packets and sweet panchamirtham on fresh banana leaves to grateful pilgrims.",
    # S24: Sunset peace over the Western Ghats from temple
    "Serene twilight view over the silhouettes of the Western Ghats mountains and green plains from the temple corridor, lone evening star appearing."
]

THIRUERAGAM_PROMPTS = [
    # S01: Swamimalai sacred hillock representing 60 Tamil years
    "Sweeping golden sunrise view of Swamimalai temple (திருஏரகம் - Fourth Arupadai Veedu) perched atop its sacred artificial hillock with 60 stone steps representing the 60 Tamil years, overlooking the Kaveri river delta.",
    # S02: Lord Murugan teaching Pranava Mantra OM to Lord Shiva
    "Sacred divine darshan of child Lord Murugan (Swaminatha Swami) seated as the Supreme Preceptor (Guru) imparting the secret cosmic Pranava Mantra 'OM' into the ear of Lord Shiva who listens reverently with bowed head.",
    # S03: Sacred Sanctum of Swaminatha Swami
    "Luminous granite inner sanctum of Lord Swaminatha Swami standing majestic in golden armour, holding the divine Vel, adorned with diamond crown, fragrant bilva and jasmine garlands under flickering brass lamps.",
    # S04: Sixty sacred granite steps
    "Devotees climbing barefoot up the steep flight of 60 granite steps, each step inscribed with the name of a Tamil year (Prabhava to Kshaya) lit by brass oil deepams at twilight.",
    # S05: Sthapathi artisans sculpting traditional bronze icons
    "Famous Swamimalai master bronze sculptors (Sthapathis) applying the ancient lost-wax casting technique (cire perdue), molten bronze glowing orange as it pours into clay moulds.",
    # S06: Netra Dhanam ceremony of newly cast bronze icon
    "Master bronze sculptor gently opening the eyes (Netra Dhanam) of a newly crafted sacred Murugan bronze idol with a golden stylus, surrounded by incense smoke.",
    # S07: Sacred elephant vehicle (Airavatam) shrine
    "White divine elephant Airavatam statue standing proudly as the mount before Lord Murugan's sanctum, draped in silk brocade and marigold garlands.",
    # S08: Kaveri river flowing through Kumbakonam delta
    "Lush green paddy fields and coconut groves flanking the sacred Kaveri (Cauvery) river near Swamimalai, sparkling under gentle morning rays.",
    # S09: Priests performing Vibhuti Abhishekam
    "Cascades of cool sacred white vibhuti (holy ash) cascading over the six-foot stone moolavar idol of Swaminatha Swami, creating an awe-inspiring divine presence.",
    # S10: Devotee family chanting Pranava Mantra
    "Devout Tamil family with folded hands chanting 'Om Saravanabhava' and 'Om' in deep meditation inside the quiet hypostyle stone hall.",
    # S11: Golden kavadi procession
    "Spectacular procession of devotees carrying ornate brass and gold-plated Kavadis up the 60 sacred steps to the sound of blowing conches and thunderous thavil drums.",
    # S12: Inner corridor of sixty lingams
    "Quiet ancient corridor housing shrines to Lord Shiva and Goddess Meenakshi at the base of the hill, soft rays of morning sun illuminating intricate stonework.",
    # S13: Golden Vel decorated with yellow champaka flowers
    "Intricate close-up of the divine golden Vel anointed with pure sandalwood paste and decorated with rare fragrant golden Champaka flowers.",
    # S14: Traditional Nadaswaram recital on temple steps
    "Eminent traditional musicians playing melodic ragas on the Nadaswaram pipe accompanied by thavil drums on the temple courtyard steps at sunset.",
    # S15: Golden Vimanam above the sanctum
    "Pristine golden Vimanam tower directly above the sanctum shining brilliantly against a crystal blue sky, sculpted with miniature gold Murugan avatars.",
    # S16: Paal Abhishekam with pure cow milk
    "Streams of pure white fresh cow milk bathing the radiant bronze Utsava Murti, splashing into silver drainage trays adorned with pink rose petals.",
    # S17: Devotees lighting 60 ghee lamps
    "Rows of 60 golden brass ghee lamps lit along the stone parapet walls, reflecting across the smooth granite floor in the cool temple breeze.",
    # S18: Ancient palm leaf library of Agamic treatises
    "Revered Tamil Agama scholars studying ancient palm-leaf manuscripts containing temple architecture and bronze casting canons (Shilpa Shastras).",
    # S19: Sunset over the temple tank (Vajra Theertham)
    "Vajra Theertham temple sacred water tank glowing like liquid copper at dusk, reflecting the illuminated hillock shrine and palm trees.",
    # S20: Chariot car festival of Swamimalai
    "Grand wooden temple chariot decorated with rich crimson and saffron silks moving through temple streets surrounded by tens of thousands of joyful pilgrims.",
    # S21: Devotee receiving golden crown satari blessing
    "Priest placing the sacred golden Sadari (crown representing the Lord's feet) upon a kneeling pilgrim's head with Vedic mantras.",
    # S22: Bronze peacock lamp (Mayil Vilakku) glowing
    "Antique bronze hanging oil lamp shaped like an elegant peacock with oil burning in its deep bowl, casting intricate geometric shadows on carved granite pillars.",
    # S23: Distributing prasadam of sakkarai pongal
    "Piping hot aromatic ghee-laden Sakkarai Pongal garnished with roasted cashews and raisins served on fresh green banana leaves to eager devotees.",
    # S24: Panoramic night view of Swamimalai hillock
    "Magical night view of Swamimalai hilltop temple illuminated with golden lights, rising like a jewel above the tranquil Tanjore delta landscape under the stars."
]

## Track 9: குன்றுதோறாடல் (Thiruthani - Fifth Arupadai Veedu)
KUNRUTHORADAL_PROMPTS = [
    # S01: Thiruthani Hill Temple Dawn
    "Epic panoramic sunrise over Thiruthani Thanikasalam hill, the Fifth Arupadai Veedu of Lord Murugan where His divine wrath cooled into supreme peace, glowing pink dawn skies over granite temple spires.",
    # S02: Divine Darshan of Lord Thanikachalam
    "Glorious darshan of Lord Thanikachalam standing in profound peace (Shanthan), adorned in green silk pitambaram with golden Vel resting gracefully across His chest, gentle compassionate smile.",
    # S03: The 365 Sacred Steps
    "Devotees climbing the 365 sacred stone steps representing the 365 days of the year, carrying offerings of tender coconuts, milk pots, and fragrant flowers under leafy shade trees.",
    # S04: Wedding of Lord Murugan and Goddess Valli
    "Sacred celestial wedding of Lord Murugan and Kuravar tribal maiden Goddess Valli on Thiruthani hill, showered with sacred yellow akshata rice and fragrant red lotus petals by devas.",
    # S05: Sacred Peacock Resting in Hillside Mandapam
    "Majestic emerald-blue royal peacock perched gracefully on an ancient stone balustrade overlooking the wide green plains of Thondaimandalam at golden hour.",
    # S06: Priests performing Sarva Vadya Upacharam
    "Temple priests in traditional silk dhotis sounding conches, cymbals, and bronze bells before the sanctum sanctorum during dawn Vishwaroopa seva.",
    # S07: Golden Vel with Sandalwood and Jasmine
    "Intricate close-up of the divine Vel made of glowing gold, anointed with thick cool Malayagiri sandalwood paste and adorned with a single fragrant red rose garland.",
    # S08: Nandi Theertham sacred water spring
    "Sacred Nandi Theertham mountain spring pool on Thiruthani hill, clear holy waters reflecting carved stone elephant reliefs and morning sunlight.",
    # S09: Pilgrims carrying floral Paal Kudam
    "Devoted Tamil women dressed in vibrant yellow sarees carrying brass milk pots (Paal Kudam) topped with fresh neem leaves and coconuts in disciplined procession.",
    # S10: Sannidhi of Goddess Valli
    "Peaceful separate shrine of Goddess Valli amman adorned in red silk and gold jewellery, lamps glowing warmly on stone floor.",
    # S11: Sacred Chanting of Thiruppugazh
    "Group of elder Othuvars seated in pillared mandapam singing Arunagirinathar's Thiruthani Thiruppugazh verses with intense bhakti devotion and cymbals.",
    # S12: Inner Prakaram with Camphor Aarti
    "Ancient granite corridor illuminated by massive brass camphor lamps, sacred smoke billowing toward hand-carved temple ceilings.",
    # S13: Sunrise over Thiruthani Rajagopuram
    "Magnificent 9-tiered Rajagopuram of Thiruthani bathed in pure golden morning sunbeams, crisp sculpted figurines of Murugan leelas vividly painted.",
    # S14: Traditional Nadaswaram recital
    "Temple vidwans seated in silk angavastrams playing the soothing raga Shanmukhapriya on silver-banded Nadaswarams during the morning procession.",
    # S15: Mountain steps illuminated with oil lamps at dusk
    "Long stairway of 365 steps lit end-to-end with thousands of clay agal vilakkus forming a glowing serpentine garland up the dark mountain.",
    # S16: Lord Murugan in elephant vahana
    "Magnificent Utsava deity of Lord Murugan holding Vel seated atop a majestic gold-plated elephant vahana during temple Brahmotsavam.",
    # S17: Devotees applying holy Vibhuti
    "Temple Sivachariyar applying three horizontal stripes of fragrant white sacred ash (Vibhuti) and vermilion kumkum on a young devotee's forehead.",
    # S18: Carved stone relief of Sage Agastya worship
    "Ancient bas-relief granite carving depicting Sage Agastya receiving Tamil grammar wisdom from Lord Murugan at the foothills of Thanigai.",
    # S19: Sacred temple garden (Nandavanam)
    "Lush sacred temple garden with blooming red hibiscus, fragrant white parijatham flowers, and holy tulasi plants glistening with morning dew.",
    # S20: Devotees singing in ecstasy
    "Devotees clapping and chanting 'Thanigai Muruga Vel Muruga' with hands raised in surrender inside the 100-pillar stone mandapam.",
    # S21: Kumkum and Sandalwood offering on brass plates
    "Traditional brass thali plate filled with freshly ground green cardamom, vermilion kumkum, yellow turmeric, and jasmine buds.",
    # S22: Divine blessing with Golden Vel
    "Temple priest gently touching the sacred golden Vel to the heads of kneeling devotees as the final blessing of peace and fearlessness.",
    # S23: Temple kitchen preparing holy Prasadam
    "Temple madapalli chefs stirring aromatic hot Panchamirtham and Laddu in massive traditional brass caldrons over wood fire.",
    # S24: Twilight serenity over Thiruthani
    "Breathtaking twilight vista of Thiruthani temple perched on the hill peak, shining like a lighthouse of eternal peace against a deep indigo sky."
]

## Track 10: பழமுதிர் சோலை (Pazhamudircholai - Sixth Arupadai Veedu)
PAZHAMUDIRCHOLAI_PROMPTS = [
    # S01: Alagar Hill Forest Dawn
    "Epic panoramic sunrise over the dense sacred forest hills of Alagar Malai, the Sixth Arupadai Veedu Pazhamudircholai, misty green canopy and singing birds.",
    # S02: Sanctum of Murugan with Valli and Deivayanai
    "Majestic sanctum darshan of Lord Murugan flanked by both consorts Goddess Valli and Goddess Deivayanai in Pazhamudircholai, adorned in pure silk and fragrant garlands.",
    # S03: Sacred Jupura Spring (Noopura Gangai)
    "Pristine crystal-clear holy waters of Noopura Gangai natural mountain spring flowing over polished stone ghats, devotees taking sacred bath.",
    # S04: The Sacred Navel Tree (Nava Maram)
    "Ancient venerated Jamun tree (Nava Maram) bearing luscious purple fruits, the legendary spot where Lord Murugan tested poet Avvaiyar with ripe and cooked fruits.",
    # S05: Child Murugan as Shepherd Boy testing Avvaiyar
    "Divine child Murugan disguised as a playful Tamil shepherd boy sitting on a high tree branch, conversing with the wise elderly poetess Avvaiyar holding her walking staff.",
    # S06: Wild Peacocks in Temple Forest
    "Flock of wild iridescent green-and-blue peacocks dancing freely on the mossy stone steps of the forest shrine in cool morning drizzle.",
    # S07: Morning Abhishekam with Spring Water
    "Priests pouring sacred Noopura Gangai spring water from carved silver vessels over the black granite deity of Lord Murugan, water splashing over flower petals.",
    # S08: Devotees walking through Bamboo Groves
    "Pilgrims clad in green and saffron climbing the tranquil forest path lined with towering bamboo trees and wild orchids toward the hilltop temple.",
    # S09: Golden Vel amidst Wild Forest Flowers
    "Close-up of the divine golden Vel surrounded by wild jungle flame lilies (Kanthal), red hibiscus, and fragrant champaka blossoms.",
    # S10: Priest waving Panchamukha Deepam
    "Temple priest in white silk dhoti holding a massive five-flame bronze Panchamukha Deepam, illuminating the smiling face of the Lord.",
    # S11: Sacred Elephant offering lotus garland
    "Decorated temple elephant gently lifting its trunk to place a fresh pink lotus garland at the entrance of the Pazhamudircholai sanctum.",
    # S12: Chanting of Avvaiyar Vinayagar Agaval & Murugan Hymns
    "Group of Tamil children seated on stone floor chanting sweet devotional verses with devotion, morning sunlight streaming between tree branches.",
    # S13: Fresh Wild Honey and Fruit Offering
    "Sacred Panchamirtham made from pure forest honey, bananas, dates, and rock candy served in traditional leaf cups.",
    # S14: Deep forest mist embracing the temple tower
    "Ethereal view of the colourful temple vimanam piercing through soft white mountain clouds on Alagar hill at sunrise.",
    # S15: Stone Mandapam with intricate leaf motifs
    "Ancient Pandya-style open stone mandapam carved with delicate creeper and forest bird motifs, peaceful shadows on granite flagstones.",
    # S16: Forest streams cascading over rocks
    "Sparkling cool mountain stream flowing through the sacred grove of Pazhamudircholai, surrounded by aromatic medicinal herbs.",
    # S17: Devotees singing Thiruppugazh at golden hour
    "Joyful pilgrims gathered beneath ancient flowering trees singing Arunagirinathar's Pazhamudircholai hymns with small cymbals.",
    # S18: Traditional brass bell ringing
    "Heavy bronze temple bell vibrating in the open forest courtyard, sound reverberating through the wooded valley.",
    # S19: Sunset over the Madurai plains from Alagar hill
    "Panoramic golden-hour view from Pazhamudircholai looking down at the vast green plains and temple city of Madurai far below.",
    # S20: Priest applying Chandanam (Sandalwood Paste)
    "Devotees receiving fragrant Malayagiri sandalwood paste prasadam on their palms, cooling and auspicious.",
    # S21: Utsava Murti in floral chariot procession
    "Exquisite bronze deities of Murugan, Valli, and Deivayanai carried on an ornate palanquin covered with thousands of fresh jasmine strings.",
    # S22: Rows of brass ghee lamps in forest twilight
    "Hundreds of small brass oil lamps glowing gently against the dark green forest backdrop as night descends upon the mountain shrine.",
    # S23: Devotees prostrating in humble surrender
    "Pilgrims performing Sashtanga Namaskaram on the smooth stone temple floor in deep grateful surrender before the sanctum.",
    # S24: Serene starry night over Pazhamudircholai
    "Enchanting nighttime view of the Pazhamudircholai sanctuary enveloped in deep emerald forest silence beneath a starry sky."
]

## Track 11 & 12: திருச்செந்தூர் (Thiruchendur - Second Arupadai Veedu)
THIRUCHENDUR_PROMPTS = [
    # S01: Thiruchendur Seashore Dawn & Waves
    "Epic panoramic dawn vista of Thiruchendur seashore temple (Second Arupadai Veedu), majestic 9-tiered Rajagopuram towering right on the azure Bay of Bengal coast with roaring white waves crashing gently on sandy beach.",
    # S02: Luminous Sanctum of Lord Senthilandavar
    "Radiant inner sanctum of Lord Jayanthinathar (Senthilandavar) in Thiruchendur, standing sublime in royal golden kavacham, holding the divine Vel, adorned with diamond crown and emerald chains.",
    # S03: Sacred Nazhi Kinaru Freshwater Well
    "The miracle freshwater spring well (Nazhi Kinaru) bubbling with crystal-clear sweet water right on the salty ocean shore, pilgrims taking holy water in brass lotas.",
    # S04: Cosmic Victory of Soorasamharam
    "Epic sacred cinematic depiction of Lord Murugan with His brilliant golden Vel conquering the titan Soorapadman, transforming ego into the noble Peacock mount and the sacred Rooster flag of victory.",
    # S05: Sacred Peacock Facing the Ocean Breeze
    "Magnificent bronze and living peacock perched atop the seaside parapet wall, colorful tail feathers rustling in the cool ocean wind against the golden morning sun.",
    # S06: Grand Ocean Procession of Shanmukha
    "Grand temple festival procession along the sandy seashore, priests carrying the six-faced Lord Shanmukha bronze deity flanked by massive royal white umbrellas (Venchamaram).",
    # S07: Golden Vel reflecting Sea Waves
    "Close-up of the consecrated golden Vel of Thiruchendur, gleaming with morning sunlight, sea salt breeze blowing fragrant red hibiscus garlands.",
    # S08: Devotees taking Holy Dip in Sea (Samudra Snanam)
    "Thousands of devout pilgrims in yellow and green festive silks taking holy dip in the gentle ocean waves before entering the temple sanctum.",
    # S09: Shanmukha Vilasam Pillared Mandapam
    "The grand monolithic 124-pillar Shanmukha Vilasam hall facing the sea, intricate granite pillars carved with heroic avatars of Murugan, cool sea breeze wafting through.",
    # S10: Priests Performing Sea-Water Abhishekam
    "Priests pouring 108 conch shells of sacred herbal waters (Sankhabhishekam) over the moolavar deity as temple bells and conches resound.",
    # S11: Sacred Valli Cave Shrine
    "Ancient rock-cut seaside cave shrine of Goddess Valli carved deep into the sandstone cliff, flickering oil lamps illuminating mysterious sanctum.",
    # S12: Thiruchendur Rajagopuram touching the Sky
    "Spectacular vertical low-angle view of the massive 137-foot 9-tier Thiruchendur Rajagopuram against a vibrant blue sky with sea gulls soaring overhead.",
    # S13: Devotees Chanting 'Kantharukku Arogara'
    "Ecstatic sea of pilgrims on temple beach courtyard with raised arms chanting 'Vetrivel Muruganukku Arogara' in unified spiritual fervor.",
    # S14: Traditional Nadaswaram playing Sea Ragas
    "Temple musicians in festive attire playing the stirring raga Kalyani on Nadaswaram pipes, sound blending with the natural rhythm of ocean waves.",
    # S15: Golden Chariot rolling by the Ocean
    "Magnificent Golden Chariot (Thanga Ratham) gleaming like molten fire, pulled by hundreds of barefoot devotees along the sandy temple perimeter.",
    # S16: Camphor Aarti illuminating the Lord's 6 Faces
    "Massive multi-wick camphor lamp illuminating all six smiling benevolent faces of Lord Shanmukha in the inner sanctum, glowing eyes full of grace.",
    # S17: Devotees receiving Vibhuti in Ilai (Leaf) Prasadam
    "Priest distributing the famed Thiruchendur Panneer Ilai Vibhuti (holy ash packed in fragrant 12-ribbed rose-apple leaves) to eager pilgrims.",
    # S18: Ancient Sandstone Carvings of Murugan Leelas
    "Detailed close-up of ancient seaside temple stone murals depicting the descent of Saravanabhava from the sparks of Lord Shiva's third eye.",
    # S19: Evening Aarti with Ocean Sunset
    "Golden-red twilight sunset over the Bay of Bengal, the temple gopurams glowing amber as evening Deeparadhana bells echo across the ocean.",
    # S20: Brass lamps reflecting on temple wet sand
    "Devotees lighting rows of earthen ghee lamps along the damp beach sand, golden flames reflecting in the receding surf.",
    # S21: Priest placing the Golden Vel blessing
    "Revered Sivachariyar gently anointing a child's forehead with sandalwood paste and touching the child with the sacred Vel.",
    # S22: Feast of Prasadam in Temple Annadhana Mandapam
    "Vast temple dining hall where thousands of pilgrims are served hot sambar rice and sweet payasam on fresh plantain leaves with utmost hospitality.",
    # S23: Temple Flagstaff (Dhwajasthambam) with Rooster Flag
    "Towering gold-gilded flagstaff rising into the twilight sky with the red silk Seval rooster banner waving triumphantly over the ocean.",
    # S24: Thiruchendur Temple glowing at Night by the Sea
    "Breathtaking night panorama of the entire Thiruchendur seaside temple illuminated with golden lights, reflected infinitely in the dark rippling waters of the Indian Ocean."
]

THEME_REGISTRY = {
    "kunram_erinthai": KUNRAM_ERINTHAI_PROMPTS,
    "pazhamai": PAZHAMAI_PROMPTS,
    "thirupparamkunram": THIRUPPARAMKUNRAM_PROMPTS,
    "thiruavinankudi": THIRUAVINANKUDI_PROMPTS,
    "thirueragam": THIRUERAGAM_PROMPTS,
    "kunruthoradal": KUNRUTHORADAL_PROMPTS,
    "pazhamudircholai": PAZHAMUDIRCHOLAI_PROMPTS,
    "thiruchendur": THIRUCHENDUR_PROMPTS,
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


