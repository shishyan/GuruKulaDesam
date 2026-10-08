# -*- coding: utf-8 -*-
"""
Direct High-Speed Vedic Artwork Generator for Chapter 25 (Aruludaimai - Universal Grace)
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
DEST_DIR = ROOT / "production" / "visuals" / "thirukkural" / "25-aruludaimai"
DEST_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY and (ROOT / ".env").exists():
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
client = genai.Client(api_key=API_KEY)

SHOTS = {
    1: (
        "01-n01_gold_coins_scattered_ground.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Directly illustrating Kural 241 (அருட்செல்வம் செல்வத்துள் செல்வம் பொருட்செல்வம் பூரியார் கண்ணும் உள). In the dusty outer courtyard of an ancient Tamil bazaar, heaps of gold coins, bronze urns, and glittering jewels lie scattered on a woven mat beside a coarse, haughty merchant, showing that mere material wealth belongs even to vulgar, unrefined men. In striking contrast, gentle morning sunbeams stream through ancient carved temple pillars onto a serene passing sadhu with Tripundra Vibhuti and a warm, glowing countenance of divine grace. Visual allegory of true spiritual wealth outshining transient worldly gold. No modern items, no text."
    ),
    2: (
        "02-n02_compassionate_hands_cradling_fawn.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. An intimate, high-detail macro close-up of the gentle, caring hands of an ancient Tamil Vedic Rishi adorned with sacred Rudraksha malas and white Vibhuti ash lines. The Rishi tenderly cradles a fragile, newborn spotted chital fawn whose mother was separated by a storm. The gentle fawn looks up with luminous, trusting black eyes as the sage softly feeds it warm cow's milk from an antique bronze ladle. Ancient ashram banyan tree and flowering tulsi garden in soft golden dawn light, profound Ahimsa and divine universal grace (Kural 241). No modern items, no text."
    ),
    3: (
        "03-n03_radiant_smile_of_saintly_soul.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A majestic, luminous portrait of a venerable 65-year-old Tamil saint / householder adorned with sacred three horizontal Tripundra Vibhuti lines, red kumkum bindi, and sacred white cotton thread. His face is filled with radiant divine sweetness, unconditional benevolence, and glowing spiritual equanimity. He sits on a woven kusha grass mat beside an ancient temple pillar as golden morning sunbeams create a subtle, celestial aura around his silver hair and beard. Embodying the supreme wealth of universal grace (Kural 241). No modern clothes, no text."
    ),
    4: (
        "04-n04_sharing_wealth_with_humble_creatures.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Along a shaded earthen pathway beside an ancient Dravidian stone temple at sunrise, a compassionate Tamil householder in an unstitched white cotton dhoti and sacred thread gently scatters handfuls of golden unhusked grain and fresh fruits on flat granite stones. Flocks of wild green parrots, sparrows, squirrels, and a docile mother cow (Gomata with painted horns) gather fearlessly around his feet, eating in peaceful trust. Morning mist, temple vimana in background, pure selfless sharing of life's blessings (Kural 242). No modern items, no text."
    ),
    5: (
        "05-n05_walking_the_righteous_forest_path.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A tranquil, cinematic wide shot of a sacred forest trail in ancient Tamil Nadu at golden dawn. An ascetic Tamil hermit clad in simple bark-cloth and rudraksha beads walks barefoot with a wooden staff along a moss-draped stone pathway. He carefully watches each step to avoid treading on tiny insects and blossoming wild parijatha petals fallen on the path. Sunbeams pierce through dense canopy of teak and peepal trees, illuminating drifting forest mist and wild spotted deer grazing peacefully nearby. Embodying Kural 242: walking the path of universal compassion. No modern roads, no text."
    ),
    6: (
        "06-n06_saving_fallen_insects_from_water.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A high-detail macro close-up at the granite edge of an ancient temple lotus pool. A gentle Tamil youth adorned with sacred thread and Vibhuti lines kneels down with infinite reverence for life. Using a broad, dry green leaf, he carefully lifts a struggling honeybee and dragonfly from the water ripples, gently placing them onto warm, dry temple stones to dry their wings. Water droplets glistening in golden sunrise light, pink lotus petals floating nearby, the sacred practice of Ahimsa extending to the tiniest living creatures (Kural 242). No modern items, no text."
    ),
    7: (
        "07-n07_monk_clearing_thorns_from_public_road.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Along an ancient red-dirt pilgrimage path leading to a grand South Indian Shiva temple at dawn, an elderly, humble Tamil monk with silver beard and saffron veshti bends down with selfless devotion. With bare hands, he gently clears sharp acacia thorns and jagged stones from the middle of the road, placing them safely into roadside bushes so that barefoot pilgrims, children, and cattle will not be hurt. Distant temple Rajagopuram glowing in morning sun, pure selfless service of grace (Kural 242). No modern tools, no text."
    ),
    8: (
        "08-n08_guiding_lantern_in_misty_night.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. On a foggy, dark village crossroad in ancient Tamil Nadu at midnight, a generous householder stands on an elevated stone platform holding high an antique brass oil lantern with steady, bright golden flames. The warm amber beam cuts through the dense swirling mist, guiding weary, lost travelers and wandering ascetics safely toward the warm shelter of an ashram. Visually illustrating Kural 242: in whatever way one examines life, grace is the only true companion and guide. Dramatic atmospheric lighting, ancient tiled homes, no modern lights, no text."
    ),
    9: (
        "09-n09_celestial_heavens_closed_to_the_callous.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A dramatic, powerful philosophical allegory directly illustrating Kural 243 (அருள்சேர்ந்த நெஞ்சினார்க் கில்லை இருள்சேர்ந்த இன்னா உலகம் புகல்). A stark composition: in the lower foreground, a cold-hearted, merciless oppressor stands trapped in murky, shadow-choked gloom of barren rocks and thorny brambles, his face clouded in dread and spiritual blindness. Above, the glorious celestial heavens glow with brilliant golden and violet light, but remain entirely closed and barred to those lacking compassion. Heavy dramatic shadows, visual contemplation of spiritual darkness. No modern elements, no text."
    ),
    10: (
        "10-n10_radiant_temple_welcoming_compassionate.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In radiant contrast to darkness, a magnificent, towering Dravidian stone temple gateway (Rajagopuram) bathed in ethereal golden light welcomes a humble, compassionate devotee whose heart is filled with universal grace. Hundreds of glowing bronze Agal Vilakku lamps illuminate the carved granite stairway draped in fragrant white jasmine and pink lotus garlands. Temple bells chime softly, sambrani dhoopam curls toward the purple twilight sky, visually illustrating Kural 243: those with hearts of grace never enter the dark world of misery. Sublime spiritual sanctuary, no modern items, no text."
    ),
    11: (
        "11-n11_feeding_stray_animals_in_rain.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. During a soft, gentle monsoon rain in an ancient Tamil village at dusk, a kind-hearted young Tamil woman in a traditional cotton saree steps out under the sheltered eave of her tiled porch. With tender, loving eyes, she kneels to share warm steamed rice and porridge on clean broad banana leaves with a shivering stray puppy and wet calico cat sheltered beside the threshold. Glowing bronze Kuthuvilakku lamp casting amber light on wet granite stones, pure unconditional compassion in adversity (Kural 244). No modern plastic, no text."
    ),
    12: (
        "12-n12_guardian_of_forest_wildlife.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In a sunlit clearing of an ancient sacred grove (Kavu) in Tamil Nadu, a serene Tamil forest hermit / sage with long matted hair, holy Vibhuti, and Rudraksha malas stands in peaceful harmony with wild creatures. Wild peacocks with shimmering emerald feathers spread their plumage beside him, wild langur monkeys sit quietly on mossy stone boulders, and a spotted chital stag rests its head against his palm with absolute fearlessness. Illustrating Kural 244: those who protect and cherish all living beings are free from the dread of bodily peril. Golden morning sunbeams, no modern items, no text."
    ),
    13: (
        "13-n13_sheltering_nesting_birds.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In the thatched and clay-tiled veranda of an ancient traditional Tamil courtyard home, a gentle householder with sacred thread and Vibhuti looks up with warm affectionate smile at a family of weaver birds and swallows who have built intricate grass nests under the wooden rafters. Instead of disturbing them, he places a small carved stone saucer filled with fresh water and millet seeds on a wooden beam beside them. Morning sunbeams filtering through carved pillars, sacred domestic harmony with all life (Kural 244). No modern items, no text."
    ),
    14: (
        "14-n14_fearless_sleep_under_the_stars.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. On the open, clean stone terrace of an ancient forest ashram at night under a vast canopy of brilliant stars, a saintly Tamil ascetic sleeps in deep, tranquil, fearless repose on a simple woven grass mat. Because his heart has never harmed or wished ill on any living being, no nightmare, guilt, or fear of danger ever touches his soul (Kural 244). A gentle night breeze rustles palm leaves, cool moonlight illuminates his serene peaceful face and sacred white ash marks, absolute innocence and divine protection. No modern furniture, no text."
    ),
    15: (
        "15-n15_animals_drinking_at_peaceful_pool.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A breathtaking, peaceful wide landscape in an ancient Tamil forest hermitage at sunrise. Around a crystal-clear natural pool fed by a gentle mountain stream, diverse animals—a gentle royal leopard, spotted deer, wild boars, and white cranes—drink together in absolute tranquility, their natural enmities dissolved in the holy aura of non-violence. Pink lotuses float on the water, ancient banyan roots drape overhead, visual embodiment of the sacred power of universal grace (Kural 245). No modern elements, no text."
    ),
    16: (
        "16-n16_bountiful_earth_yielding_fruits.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Directly illustrating Kural 245 (அல்லல் அருளாள்வார்க் கில்லை வளிவழங்கும் மல்லல்மா ஞாலங் கரி). A panoramic view of the prosperous, wind-swept fertile plains of ancient Tamil Nadu. Ripe golden mango orchards, flowering coconut groves, and swaying emerald paddy fields flourish under an expansive azure sky with gentle monsoon clouds. The wind-swept vast Earth stands as living witness that true sorrow never befalls those who live in universal grace. Ancient temple towers on horizon, soaring egrets, divine agricultural abundance. No modern structures, no text."
    ),
    17: (
        "17-n17_free_from_grief_in_old_age.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. An intimate, high-detail portrait of an 80-year-old Tamil patriarch and matriarch sitting together on the pillared veranda of their ancestral home at golden twilight. Their weathered faces are radiant with deep inner peace, unburdened by any regret, bitterness, or grief, having spent their long lives in selfless charity and universal grace toward all beings (Kural 245). Grandchildren play happily around a sacred Tulsi Thara in the courtyard, warm oil lamps glowing on granite pillars, supreme sunset of a righteous life. No modern clothes, no text."
    ),
    18: (
        "18-n18_healer_curing_sick_village_cow.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In the sun-dappled courtyard of an ancient Tamil village at sunrise, an elderly Ayurvedic cow-doctor (Govaidya) with sacred thread and Tripundra Vibhuti gently treats an ailing white cow (Gomata). With tender care, he applies a soothing poultice of green herbal paste and turmeric to the cow's shoulder, while a young farm boy holds a brass bowl of warm medicated water. The cow rests her chin trustingly on the healer's knee, eyes full of gratitude. Pure veterinary compassion rooted in Sanatana Dharma (Kural 245). No modern medical tools, no text."
    ),
    19: (
        "19-n19_cruel_hunter_snaring_beasts.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Directly illustrating Kural 246 (பொருள்நீங்கிப் பொச்சாந்தார் என்பர் அருள்நீங்கி அல்லவை செய்து ஒழுகுவார்). In the dark, gloomy shadows of a tangled forest at dusk, a cruel hunter with harsh, hardened features sets a sharp iron snare to trap innocent forest animals. His face reflects internal spiritual blindness, greed, and moral ruin—having abandoned grace to commit merciless acts. Behind him, ominous storm clouds gather and dead twisted branches loom, showing that those who abandon mercy have lost all true purpose and memory of Dharma. Dramatic shadowy lighting, no modern weapons, no text."
    ),
    20: (
        "20-n20_haunted_sleepless_night_of_oppressor.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Inside an opulent but cold, shadow-drenched stone palace chamber at late night, a merciless, cruel lord sits upright on his silk-cushioned couch, tormented by severe insomnia and haunted guilt. Shadows cast by a guttering oil lamp warp menacingly on the cold granite walls, reflecting his tormented conscience and the heavy burden of unrighteous acts committed without grace (Kural 246). Cold blue moonlight contrasting with dim flickering amber lamp, profound moral agony of the merciless. No modern furniture, no text."
    ),
    21: (
        "21-n21_freeing_caged_birds_into_sky.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In an ancient Tamil temple courtyard at golden sunrise, a compassionate young woman in a traditional silk saree opens the door of an antique woven wicker basket, gently releasing a pair of green ringneck parakeets into the open azure sky. The birds soar joyfully toward the sun, their iridescent emerald feathers catching morning light, with the towering Dravidian temple gopuram and blooming champaka trees in the background. Pure spiritual liberation and joy of showing mercy (Kural 246). No modern items, no text."
    ),
    22: (
        "22-n22_penniless_man_turned_from_market.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Directly illustrating Kural 247 (அருளிலார்க் கவ்வுலகம் இல்லை பொருளிலார்க் கிவ்வுலகம் இல்லாகி யாங்கு). In a bustling, crowded ancient Tamil marketplace at noon, an impoverished, penniless man in a ragged loincloth with empty hands is turned away from merchants' stalls selling rice and fruits. Just as the penniless have no standing or enjoyment in this material world, so do those devoid of grace have no place in the celestial world of bliss. Dusty sunbeams, ancient mud and timber shop fronts, poignant philosophical analogy. No modern clothes, no text."
    ),
    23: (
        "23-n23_the_spiritual_currency_of_grace.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A luminous, allegorical visual illustrating Kural 247. Inside a divine temple mandapam bathed in golden twilight, a humble sage whose only possession is an overflowing heart of universal grace stands before the celestial altar. His soul radiates pure golden light like the most radiant currency of heaven, while heavenly flowers drift softly from the celestial sky. Visual allegory proving that grace is the eternal currency that opens the gates of higher spiritual realms. Ancient granite pillars, glowing oil lamps, no modern items, no text."
    ),
    24: (
        "24-n24_monk_sharing_water_with_thirsting_dog.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. At an ancient, scorched stone wayside pavilion along a dusty Tamil road at blistering midday. A wandering Tamil ascetic (sannyasi) with wooden staff and single earthen water bowl kneels generously in the dust. Despite his own severe thirst, he pours his precious remaining cool water into a cupped granite hollow so that a panting, parched stray dog can drink. The dog laps gratefully with wagging tail, while the monk watches with a smile of divine fulfillment (Kural 247). Golden sun glare, ancient banyan roots, no modern items, no text."
    ),
    25: (
        "25-n25_bankrupt_merchant_rebuilding_enterprise.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Directly illustrating Kural 248 (பொருளற்றார் பூப்பர் ஒருகால் அருளற்றார் அற்றார்மற் றாதல் அரிது). At an ancient Tamil port (Poompuhar / Korkai) at sunrise, a formerly ruined merchant who had lost his ships works determinedly with carpentry tools and timber to rebuild a new seafaring vessel with the help of supportive friends, proving that those who lose material wealth can flourish again through effort. But those who lose the soul's grace are utterly lost forever. Ocean waves, morning golden sun, stitched-plank ships in harbor. No modern vessels, no text."
    ),
    26: (
        "26-n26_hollow_ruin_of_a_callous_tyrant.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A dramatic, haunting visual illustrating the second half of Kural 248. The overgrown, crumbling stone ruins of a once-mighty tyrant's palace who ruled without mercy. Cracked granite pillars covered in wild thorns and dried vines stand abandoned under a stark grey sky, with vultures circling high above. A stark visual contemplation: while material poverty can be reversed, the spiritual bankruptcy of a merciless life can never be redeemed. Dramatic architectural ruin, no modern debris, no text."
    ),
    27: (
        "27-n27_restoring_fading_plant_with_water.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In a sun-parched ashram courtyard at golden morning, a gentle Tamil child wearing an aranjanam cord and vermilion tilak carefully pours cool consecrated water from a small brass lota over a wilting, thirsty Tulsi plant in a terracotta pedestal. Under the gentle watering, the dry green leaves perk up immediately with glistening dew, blossoming in gratitude. Morning sunbeams filtering through leaves, touching symbol of how compassion revives what was perishing (Kural 248). No modern plastic, no text."
    ),
    28: (
        "28-n28_blind_man_stumbling_in_the_dark.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Directly illustrating Kural 249 (தெருளாதான் மெய்ப்பொருள் கண்டற்றால் தேரின் அருளாதான் செய்யும் அறம்). In a treacherous, rocky mountain terrain enveloped in thick pitch darkness and fog at night, a confused man without a lamp stumbles blindly among jagged stones and perilous crevices, unable to see the true path. Visual allegory: just as a confused man without light can never perceive reality, so the righteous deeds performed by someone lacking genuine compassion are completely blind, hollow, and devoid of spiritual truth. High-contrast chiaroscuro, no modern flashlights, no text."
    ),
    29: (
        "29-n29_lamp_of_grace_illuminating_all_dharma.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In brilliant contrast to blindness, inside an ancient granite temple sanctum at dawn, a venerable Tamil sage holds a multi-tiered brass Kuthuvilakku lamp whose bright, steady golden flames illuminate every corner of the carved granite mandapam, revealing intricate carvings of Dharma, deities, and sacred scriptures in radiant clarity. Symbolizing how genuine grace is the supreme illuminating lamp that gives true meaning and life to all righteous actions (Kural 249). Incense smoke curling softly, no modern lights, no text."
    ),
    30: (
        "30-n30_mechanical_ritual_without_heart.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. At an ancient stone homam altar at midday, an ostentatious, haughty priest mechanically pours ghee into the sacred fire with cold, vacant eyes, showing zero genuine love or compassion for the poor beggars seated outside the temple gate. Despite the grand fire and bronze vessels, the scene conveys profound spiritual hollowness—a ritual devoid of the living heart of grace (Kural 249). Smoke curling without warmth, cold grey stone background, no modern items, no text."
    ),
    31: (
        "31-n31_child_hugging_mother_pure_grace.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In an ancient Tamil courtyard home at sunrise, an intimate and deeply touching scene of unconditional love. A graceful mother in a traditional madisar saree kneels down with an overflowing smile of pure tenderness as her 4-year-old child runs and wraps small arms tightly around her neck with complete, joyous trust. Golden morning sunlight streaming through carved pillars, jasmine in mother's hair, sacred kolam on floor, the purest earthly reflection of divine universal grace (Kural 249). No modern items, no text."
    ),
    32: (
        "32-n32_bully_oppressing_fragile_peasant.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Directly illustrating the first half of Kural 250 (வலியார்முன் தன்னை நினைக்கத்தான் தன்னின் மெலியார்மேல் செல்லு மிடத்து). On a dusty village lane in ancient Tamil Nadu at midday, a powerful, muscular village bully brandishing a wooden staff aggressively intimidates and threatens a frail, trembling elderly peasant in ragged clothes. The elder cowers with hands raised in helplessness, while the bully looms with arrogant pride, completely forgetting his own mortality and vulnerability. Dramatic tension, harsh sun, no modern clothes, no text."
    ),
    33: (
        "33-n33_the_same_bully_trembling_before_king.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Directly illustrating the profound moral lesson of Kural 250. The very same muscular bully now kneels on the polished granite floor of the grand royal court, trembling in absolute terror with bowed head and shaking hands before the majestic, towering righteous King and royal guards. Illustrating Kural 250: when a man is tempted to oppress those weaker than himself, let him remember how he trembles when standing before those who are mightier than him! Golden torchlight on carved stone, moral justice, no modern items, no text."
    ),
    34: (
        "34-n34_releasing_the_weak_with_mercy.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In the quiet courtyard of an ancient Tamil village at golden afternoon, the once-arrogant man, having learned the lesson of Kural 250, voluntarily lowers his staff and reaches down with humble, trembling hands to lift the frail elderly peasant from the dust. He wraps his own clean cotton shawl around the elder's shoulders with tears of sincere repentance and newfound compassion. Villagers looking on with relieved, approving smiles, golden sunlight bathing the scene in redemption. No modern clothes, no text."
    ),
    35: (
        "35-n35_sanctuary_of_grace_for_all_beings.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A panoramic, breathtaking wide shot of an ancient South Indian temple hermitage (Abhayaranya / Goshala) at golden dusk. Gentle cows (Gomata), playful calves, deer, peacocks, wandering sadhus, and poor villagers all rest and receive food together in a vast, peaceful sanctuary of unconditional grace. Glowing bronze oil lamps illuminate carved stone pillars and sacred banyan roots, reflecting off a calm lotus pond. The supreme triumph of Ahimsa and universal refuge (Kural 250). No modern vehicles, no text."
    ),
    36: (
        "36-n36_sunset_glow_over_river_ferry.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. At deep golden-magenta sunset over the sacred Kaveri river, an ancient wooden ferry boat gently glides across calm, shimmering waters. On board, a compassionate boatman with Tripundra Vibhuti gently helps an elderly blind pilgrim and a mother with her infant onto the safe stone steps of the riverbank without asking for any fare. Distant temple gopuram silhouetted against the vibrant amber afterglow, cool evening breeze rustling riverside reeds, serene spiritual crossing of life. No modern motors, no text."
    ),
    37: (
        "37-n37_golden_dawn_of_universal_compassion.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. The monumental, transcendent grand finale masterwork for Chapter 25 (*அருளுடைமை*). The brilliant golden sun rises over the sacred temple lands of Tamil Nadu, sending radiant celestial light rays across majestic ancient Dravidian Rajagopurams, lush emerald paddy fields, and winding holy river waters. In the foreground at an ashram hermitage, smoke from a morning Agnihotra homam fire rises heavenward, while a venerable Vedic Rishi folds his hands in universal prayer (Lokah Samastah Sukhino Bhavantu). Sacred Gomata cows graze peacefully, and flocks of white egrets soar across the golden sky, celebrating the eternal triumph of universal grace. No modern buildings, no wires, no text."
    ),
}

def generate_shot(shot_num, filename, prompt):
    out_path = DEST_DIR / filename
    print(f"\n[Chapter 25 - Shot {shot_num}/37] Generating {filename}...")
    
    for attempt in range(1, 4):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash-image',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['IMAGE'],
                    image_config=types.ImageConfig(
                        aspect_ratio='16:9'
                    )
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
            print(f" -> No image found in response parts (attempt {attempt})")
        except Exception as e:
            print(f" -> Error on attempt {attempt}: {e}")
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                print(" -> Rate limit hit, sleeping 20s...")
                time.sleep(20)
            else:
                time.sleep(5)
    return False

def main():
    print(f"Starting direct high-speed generation for Chapter 25 (37 shots)...")
    print(f"Destination: {DEST_DIR}")
    
    total = len(SHOTS)
    success = 0
    start_time = time.time()
    
    for num, (fname, prompt) in sorted(SHOTS.items()):
        ok = generate_shot(num, fname, prompt)
        if ok:
            success += 1
        time.sleep(2.5)
        
    elapsed = time.time() - start_time
    print(f"\nCompleted Chapter 25! Generated {success}/{total} shots in {elapsed/60:.1f} minutes.")

if __name__ == "__main__":
    main()
