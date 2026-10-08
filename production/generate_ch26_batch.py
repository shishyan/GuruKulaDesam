# -*- coding: utf-8 -*-
"""
Direct High-Speed Vedic Artwork Generator for Chapter 26 (Pulaal Unnaamai - Ahimsa)
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
DEST_DIR = ROOT / "production" / "visuals" / "thirukkural" / "26-pulaal-unnaamai"
DEST_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY and (ROOT / ".env").exists():
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

FILES = sorted([f for f in os.listdir(DEST_DIR) if f.endswith('.jpg')])

BASE_PROMPT = (
    "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. "
    "Set in ancient classical Tamil Nadu. Theme of Thirukkural Chapter 26 (Abstinence from Meat / Universal Ahimsa). "
    "Visual subject: {subject}. "
    "Atmosphere: sacred riverbanks, ancient Dravidian stone temples, flowering champaka and parijatha groves, "
    "sacred hump-backed Gomata cows with painted horns, gentle deer, pure sattvic vegetarian offerings of fruits and lotuses. "
    "Lighting: golden dawn or twilight rays filtering through mountain mist, glowing bronze deepam oil lamps. "
    "Strictly no modern items, no western clothing, no electrical wires, no text overlays, no watermarks."
)

SUBJECTS = {
    "01-moral-dilemma-feast.jpg": "At a royal feast in ancient Tamil Nadu, a righteous guest pushes away cooked meat dishes with solemn sorrow, refusing to nourish his own flesh with the flesh of slain creatures (Kural 251)",
    "02-creature-eyes-fear.jpg": "An intimate macro shot of the luminous, innocent dark eyes of a young calf or lamb looking out with tender vulnerability and sacred breath (Kural 251)",
    "03-two-bodies-contrast.jpg": "A living mother deer and her suckling fawn grazing peacefully in emerald grass, contrasted with an altar where only fresh pink lotuses and bilva leaves are offered (Kural 251)",
    "04-saint-turning-away-meat.jpg": "A venerable Tamil Rishi with Tripundra Vibhuti and Rudraksha turning his head away with quiet sorrow from meat, guiding the giver toward golden grains and coconuts",
    "05-ruin-of-compassion-hollow.jpg": "A shadow-drenched stone chamber where an unrighteous man holding meat looks into water and sees his soul stripped of divine grace (Kural 252)",
    "06-loss-of-wealth-vs-grace.jpg": "A visual contrast between lost worldly coins and a radiant sage sitting before a Tulsi Thara in golden dawn overflowing with spiritual Ahimsa (Kural 252)",
    "07-withered-heart-shadow.jpg": "A petrified, withered tree in an arid wasteland casting a skeletal shadow, metaphor of a heart that has lost mercy by slaughtering innocent beings (Kural 252)",
    "08-spring-water-cleanse.jpg": "A crystal-clear mountain spring gushing over mossy granite stones in a sacred forest at sunrise, where a devotee cups the pure water in worship (Kural 252)",
    "09-butcher-blade-reflection.jpg": "A dark iron blade reflecting the cold, hardened eyes of someone whose mind has become indifferent to suffering through eating meat (Kural 253)",
    "10-hardened-merciless-eyes.jpg": "An intimate portrait of a grim hunter whose face has lost tenderness from years of slaughter, contrasted with the innocent forest world (Kural 253)",
    "11-slaughterhouse-threshold.jpg": "The solemn threshold of an ancient slaughterhouse in evening shadows, as a wise Tamil scholar turns his back forever and walks toward a temple sanctum (Kural 253)",
    "12-trembling-lamb-shadow.jpg": "In a moonlit courtyard, a small white lamb huddles in fear as a shadow approaches, but the hand gently opens and drops the tether in mercy (Kural 253)",
    "13-tasting-flesh-dulling-heart.jpg": "An enlightened thinker pushes a meat dish aside in revulsion, holding his chest, realizing spiritual liberation and slaughter cannot coexist (Kural 254)",
    "14-hands-untying-rope.jpg": "A compassionate Tamil youth gently unties coarse jute ropes binding a trapped calf, setting the animal free to run back to its mother (Kural 254)",
    "15-hunter-lowering-bow.jpg": "In a mist-draped forest at sunrise, a hunter aiming at a deer locks eyes with the creature and tremblingly lowers his bow forever (Kural 254)",
    "16-sacred-breath-life.jpg": "A gentle hump-backed calf breathing softly in golden morning light, warm breath visible like fine mist as it nuzzles a lotus blossom (Kural 254)",
    "17-the-sin-of-consumption.jpg": "On a stormy mountain ledge, a consumer of flesh stands looking into an abyss of remorse, his soul barred from celestial ascension (Kural 255)",
    "18-blood-on-stone-rain.jpg": "A solemn macro shot of dark ancient granite stones washed clean by pure torrential monsoon rain, purifying the sacred earth into pristine life (Kural 255)",
    "19-gates-of-alaru-hell.jpg": "A mythic visual of the dark gates of Alaru that never open to release those who slaughter and consume living beings (Kural 255)",
    "20-inescapable-torment.jpg": "In a shadowy cavern, an oppressor of animals sits clutching his head as visions of the gentle creatures he harmed surround him in moral accusation (Kural 255)",
    "21-living-earth-sanctuary.jpg": "A vast sun-drenched sanctuary of life in Tamil Nadu: emerald valleys and temple towers where cows, deer, birds, and humans coexist in divine peace (Kural 255)",
    "22-nightmare-of-conscience.jpg": "A troubled man wakes in cold sweat from a nightmare of conscience, vowing by a flickering oil lamp never again to partake of animal flesh (Kural 256)",
    "23-chains-of-retribution.jpg": "Heavy rusted iron chains breaking and falling away onto temple flagstones as a man embraces Ahimsa and vegetarianism, liberating his soul (Kural 256)",
    "24-healing-the-wounded-lamb.jpg": "In an ashram garden, a gentle Vedic householder tenderly binds the bruised leg of a little white lamb with clean cotton and soothing herbal oil (Kural 256)",
    "25-gentle-cow-and-calf.jpg": "A majestic white hump-backed mother cow (Gomata) with painted horns lovingly licks her newborn calf nursing contentedly beside fresh grass (Kural 256)",
    "26-deer-and-fawn-kinship.jpg": "In a lush emerald forest clearing in the Western Ghats at sunrise, a wild spotted deer and her fawn leap joyfully through dewy grass without fear of hunters (Kural 256)",
    "27-ascetic-forest-kinship.jpg": "In an ancient forest hermitage, an austere Tamil Rishi in padmasana sits while wild deer, peacocks, and squirrels eat grains from his open palms (Kural 256)",
    "28-scholar-ahimsa-manuscript.jpg": "In a Gurukulam library, a scholar inscribes palm leaves: if the world did not purchase meat, none would ever slaughter animals for sale! (Kural 256)",
    "29-ahimsa-stone-reliefs.jpg": "Ancient thousand-year-old carved granite temple reliefs in Tamil Nadu depicting Rishis protecting animals and feeding calves from brass bowls (Kural 256)",
    "30-warrior-renouncing-sword.jpg": "At the granite altar of a Shiva temple at twilight, a decorated warrior unbuckles his sword and places it before the Nandi bull, taking a vow of Ahimsa (Kural 257)",
    "31-warrior-bows-to-sage.jpg": "Outside a thatched forest hermitage at sunrise, the reformed warrior in white cotton bows in deep prostration before a tranquil sage who blesses him (Kural 257)",
    "32-spear-with-jasmine-vines.jpg": "An antique bronze hunting spear permanently retired against an ancient temple wall, wrapped in fragrant white climbing jasmine vines and green leaves (Kural 257)",
    "33-siddha-herbal-healer.jpg": "Inside an ancient Siddha herbal pharmacy at dawn, a master grinds healing neem, tulsi, and brahmi leaves in a granite mortar, celebrating plant-based healing (Kural 257)",
    "34-wildlife-sanctuary-peace.jpg": "A wide shot of an ancient sanctuary grove where a Tamil family walks alongside wild peacocks and spotted deer that show zero fear of humans (Kural 257)",
    "35-deer-drinking-stream.jpg": "A wild spotted deer and fawn drinking from a crystal-clear forest brook reflecting pink lotuses and morning sunbeams (Kural 257)",
    "36-hermitage-universal-refuge.jpg": "At sunset, an ancient Tamil Vedic hermitage stands open as a universal sanctuary where cows, deer, and sadhus gather safely as evening lamps are lit (Kural 258)",
    "37-scholar-empathy-deer.jpg": "A Tamil scholar with sacred thread and Vibhuti gently strokes the neck of a wild deer with deep empathy: those of faultless vision never eat severed flesh (Kural 258)",
    "38-sage-olai-chuvadi.jpg": "An ancient Tamil sage's ink-free hands tying a sacred silk cord around a palm-leaf manuscript containing Thiruvalluvar's verses on Ahimsa (Kural 258)",
    "39-disciples-circle-neem.jpg": "Under the cooling shade of a neem tree, young disciples sit cross-legged around their Guru, listening with reverent eyes to the merits of vegetarianism (Kural 258)",
    "40-kural-259-pure-yajna.jpg": "A sacred Vedic Agnihotra homam fire pit where pure ghee, sesame, and samidha twigs are offered, declaring non-killing is superior to 1,000 burnt sacrifices (Kural 259)",
    "41-pure-vegetarian-havan.jpg": "A devout Tamil couple in madisar and silk veshti offer golden grains, coconuts, bananas, and tulsi leaves into the sacred fire kunda beside a peaceful Gomata (Kural 259)",
    "42-lotus-offering-altar.jpg": "A carved black granite altar before a Shiva Lingam where a bronze Uruli is filled with hundreds of pink lotuses and bilva leaves in place of any animal sacrifice (Kural 259)",
    "43-sage-walking-with-animals.jpg": "An enlightened Tamil Rishi with silver hair and Vibhuti walks along the Kaveri riverbank as deer, peacocks, calves, and birds follow him in reverence (Kural 260)",
    "44-animals-gathering-harmony.jpg": "Dozens of diverse animals—cows, deer, peacocks, rabbits, swans—gather in mutual peace around a meditating saint, natural predatory instincts stilled by Ahimsa (Kural 260)",
    "45-universal-reverence-anjali.jpg": "In an ancient temple town at sunset, citizens and elders join hands in reverent Anjali mudra as a saintly vegetarian elder with sacred Vibhuti passes by (Kural 260)",
    "46-universal-ahimsa-creatures.jpg": "A vast panoramic grand finale of sacred Tamil Nadu at golden dawn: Dravidian Gopurams, lush paddy fields, and herds of Gomata cows grazing peacefully in Ahimsa (Kural 260)"
}

def generate_shot(fname, subject):
    out_path = DEST_DIR / fname
    prompt = BASE_PROMPT.format(subject=subject)
    print(f"\n[Chapter 26] Generating {fname}...")
    
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
    print(f"Starting direct high-speed generation for Chapter 26 ({len(SUBJECTS)} shots)...")
    success = 0
    start_time = time.time()
    
    for fname, subject in sorted(SUBJECTS.items()):
        ok = generate_shot(fname, subject)
        if ok:
            success += 1
        time.sleep(2.5)
        
    elapsed = time.time() - start_time
    print(f"\nCompleted Chapter 26! Generated {success}/{len(SUBJECTS)} shots in {elapsed/60:.1f} minutes.")

if __name__ == "__main__":
    main()
