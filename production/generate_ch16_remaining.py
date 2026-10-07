# -*- coding: utf-8 -*-
"""
Direct High-Speed Vedic Artwork Generator for Chapter 16 (Poraiyudaimai)
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
DEST_DIR = ROOT / "production" / "visuals" / "thirukkural" / "16-poraiyudaimai"
DEST_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

SHOTS = {
    21: (
        "21-n21_ancient_olive_tree_bearing_fruit.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In an ancient sacred Tamil temple orchard at golden sunrise, an ancient, gnarled, spreading Bilva / Vengai tree stands with weathered bark that has endured centuries of monsoons and scorch. Despite deep scars on its trunk, it patiently yields abundant glossy green leaves and fragrant golden fruits. Beneath its sheltering canopy, a gentle calf and cow (Gomata with painted horns) rest peacefully in morning sunbeams. Ancient stone temple gopuram in soft mist, visual allegory of patient endurance bearing sweet spiritual fruit (Kural 156). No modern items, no text."
    ),
    22: (
        "22-n22_scholar_inscribing_virtue_on_copper.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Inside a quiet, granite-pillared temple library at golden hour, a venerable Tamil Vedic epigraphist and scholar with white Tripundra Vibhuti, Rudraksha beads, and sacred cotton thread carefully chisels an ancient inscription of virtue onto a burnished copper plate (Tamra Sasanam) using a bronze stylus. Golden dust motes dance in sunbeams through carved stone lattices, stacks of inscribed palm-leaf manuscripts (Olais) resting on carved teakwood stands. Reverent recording of eternal Dharma (Kural 156), no modern tools, no text overlays."
    ),
    23: (
        "23-n23_sunrise_over_timeless_hills.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A breathtaking, panoramic wide shot of sunrise breaking over the timeless, ancient granite mountain ridges of Tamil Nadu. Glorious golden rays pierce purple-blue mountain mists, illuminating lush green valleys, sacred forest hermitages, and distant Dravidian temple spires. A lone ascetic in an unstitched saffron veshti stands atop a high stone promontory with hands folded in reverent Surya Namaskaram. Sublime majesty of nature and eternal spiritual patience, no modern structures, no text."
    ),
    24: (
        "24-n24_noble_statue_unmoved_by_birds.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A majestic close-up of a thousand-year-old carved dark granite sculpture of a contemplative Rishi or guardian deity standing in an open temple courtyard. Wild emerald ringneck parrots and blue kingfishers perch gently upon the statue's shoulders and headdress; the ancient stone face remains utterly serene, unblinking, and immovable in eternal meditation. Golden morning sunlight playing across carved stone contours, fragrant temple jasmine blossoms at the base, profound metaphor of unbroken stillness. No modern items, no text."
    ),
    25: (
        "25-n25_goldsmith_testing_gold_touchstone.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In a traditional Tamil workshop, an elderly master goldsmith with sacred thread, Vibhuti markings, and silver hair tests a nugget of pure refined gold against a black touchstone (Urai Kal). A bright, unalloyed golden streak gleams against the dark stone, proving its pure 24-karat purity. Beside him, an earthenware charcoal brazier glows with steady amber coals. Illustrating Kural 155: just as fire and touchstone reveal pure gold, adversity proves the true gold of a forbearing soul. Glowing firelight, antique brass scales, no modern tools, no text."
    ),
    26: (
        "26-n26_hasty_wrathful_man_derided_by_crowd.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In an ancient Tamil village square under a neem tree, an impulsive, wrathful man flails his arms with flushed red face and bulging veins, yelling in uncontrolled anger. The gathered village elders and householders in white veshtis and Vibhuti look upon him with sorrowful pity and silent shakes of the head, turning away from his disgraceful loss of self-control. Illustrating Kural 156: the wrathful are counted as nothing. Ancient mud cottages, dust in late afternoon sun, no modern clothes, no text."
    ),
    27: (
        "27-n27_casket_of_pure_gems_opened.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A high-detail intimate close-up inside a temple treasury chamber. A carved sandalwood and brass casket lined with crimson silk is opened, revealing radiant, flawless navaratna gems—rubies, pearls, and diamonds—that catch the golden flame of a nearby bronze oil lamp. Swirls of sacred sambrani incense smoke curl softly around the treasure. Metaphor of Kural 155: those who exercise forbearance are cherished like precious gems wrapped in gold. Intricate South Indian metalwork, no modern jewelry, no text."
    ),
    28: (
        "28-n28_elders_honoring_the_patient_peacemaker.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In the grand assembly hall of an ancient Tamil village, revered council elders with white hair, sacred threads, and Tripundra Vibhuti rise with folded hands (Anjali mudra) to honor a humble, patient householder who resolved a fierce dispute without raising his voice. The village headman places a fine silk angavastram and a fragrant garland of yellow marigolds and tulsi around his neck. Warm oil lamp lighting on granite pillars, deep spiritual veneration of forbearance (Kural 155), no modern items, no text."
    ),
    29: (
        "29-n29_pure_pearl_drawn_from_ocean.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. On the sun-drenched rocky shore of ancient Korkai (the ancient Pandya pearl harbor) at sunrise, a weather-beaten Tamil diver in simple loincloth gently opens an oyster shell resting in his palms, revealing a large, luminous, perfectly spherical white pearl. Morning sunbeams illuminate the pearl's iridescent glow, with breaking ocean waves and distant wooden catamarans on the turquoise sea. Symbolizing the rare, priceless pearl of patience formed through enduring irritation. No modern boats, no text."
    ),
    30: (
        "30-n30_peaceful_haven_amidst_storm.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A dramatic contrast scene: outside, a dark monsoon storm lashes an ancient Tamil landscape with torrential rain and bending coconut palms. Inside a warm, stone-pillared ashram hermitage with deep overhanging eaves, a calm Vedic family and wandering sadhus sit in serene peaceful sanctuary around a warm bronze hearth. Gentle oil lamps glow, steam rises from earthen tea bowls, pure spiritual haven amidst external turmoil (Kural 156). No modern furniture, no text."
    ),
    31: (
        "31-n31_short_lived_hollow_triumph_of_spite.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Directly illustrating Kural 157 (திறனல்ல தற்பிறர் செய்யினும் நோநொந்து). In a shadowy stone street at twilight, a spiteful man who has just taken petty revenge laughs with boastful pride, but his hollow triumphant grin instantly fades as an overwhelming sense of guilt, shame, and bitter moral emptiness washes over his face. He stands alone in the cold shadows while in the distance, a warm temple procession carries glowing lamps and divine chants. Tragic moral bankruptcy of spite. No modern clothes, no text."
    ),
    32: (
        "32-n32_timeless_song_of_the_forgiving_hero.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In an ancient Tamil courtyard at golden hour, a revered blind Sangam bard (Panar) with sacred ash and rudraksha plays an ancient stringed Yaazh (harp). His serene face is uplifted toward the heavens as he sings timeless verses celebrating a noble chieftain whose greatest valor was forgiving his enemies. Around him, village youths listen spellbound with shining eyes. Golden afternoon sunlight filtering through parijatha trees, sacred culture of forgiveness, no modern instruments, no text."
    ),
    33: (
        "33-n33_memorial_hero_stone_with_palm_shade.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In a serene meadow on the outskirts of an ancient Tamil village at sunset, an ancient carved granite Hero Stone (Natukkal) stands under the cool shade of palmyra palms. The stone is carved with a noble warrior placing down his bow and sword before an altar in voluntary peace. Fresh red kumkum and yellow chandan markings on the stone, adorned with fresh wild flower garlands and a small burning earthen lamp at its base. Eternal honor for moral heroism (Kural 157), no modern elements, no text."
    ),
    34: (
        "34-n34_epigraph_recording_peace_treaty.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A high-detail macro shot of the ancient weathered granite wall of a South Indian Shiva temple sanctum. Deeply incised, rounded ancient Tamil Brahmi and Vatteluttu script records a historic covenant of everlasting peace and mutual forgiveness between two ancient kingdoms. Soft golden morning light rakes across the carved stone inscriptions, highlighting the chiseled contours, with a bronze oil lamp casting warm light from a niche below. Enduring stone testament to forbearance, no modern items, no text."
    ),
    35: (
        "35-n35_starry_night_over_ancient_city.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A breathtaking panoramic wide shot of an ancient Dravidian temple city under a vast, clear midnight sky filled with brilliant twinkling stars and the glowing arc of the Milky Way. The dark silhouettes of grand Rajagopurams rise gracefully toward the heavens, with soft amber flickers of burning oil lamps glowing along quiet granite streets and the sacred temple tank reflecting the starry expanse. Supreme cosmic peace and timeless stillness, no modern electrical lighting, no text."
    ),
    36: (
        "36-n36_children_learning_of_magnanimity.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In a shaded open-air Gurukulam courtyard at sunrise, a kindly elder Tamil teacher with white Tripundra Vibhuti and sacred thread shows young pupils an inscribed palm-leaf manuscript (Olai) depicting the story of forbearance. The children—with traditional tufts (kudumi) and bright eager eyes—listen attentively with folded hands, their faces glowing with understanding and virtue. Fragrant morning breeze, blooming hibiscus in garden, passing of Vedic dharma across generations (Kural 157). No modern clothes, no text."
    ),
    37: (
        "37-n37_sandalwood_tree_perfuming_axe.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Directly illustrating the supreme classical proverb of Indian philosophy (as sandalwood perfumes the very axe that hews it). In a misty South Indian forest at dawn, an ancient fragrant Sandalwood tree (Chandanam) with mossy bark has been struck by an iron woodsman's axe; yet from the fresh wound, precious, sweet, aromatic sap flows, perfuming the sharp iron blade with divine fragrance. Golden sunbeams piercing through forest mist, dew on leaves, sublime visual allegory of returning sweet blessing for injury (Kural 158). No modern tools, no text."
    ),
    38: (
        "38-n38_physician_dressing_enemy_wounds.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Inside an ancient Tamil Ayurveda / Siddha healing hut at sunrise, a compassionate Vedic physician with sacred thread, Vibhuti, and Rudraksha tenderly dresses the wounds of a wounded soldier from an opposing army. He applies cooling green neem and turmeric herbal paste and binds the wound with clean white cotton strips with utter gentleness and love. Terracotta medicine jars, brass pestle, sacred tulsi nearby, illustrating Kural 158: conquering malice through noble goodness. No modern medicine, no text."
    ),
    39: (
        "39-n39_giving_sweet_water_to_the_insolent.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. At an ancient roadside stone water shelter (Thanneer Pandal) under a shady banyan tree on a scorching afternoon. An insolent, haughty traveler who had mocked the shelter stands parched and panting with thirst; with boundless patience and a gentle, welcoming smile, a virtuous Tamil householder in a white veshti and Vibhuti pours cool, fragrant vetiver-infused water from an earthen pitcher into the traveler's trembling hands. The traveler looks up in profound astonishment and humbling remorse (Kural 158). No modern bottles, no text."
    ),
    40: (
        "40-n40_returning_lost_cattle_to_rival.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Along a sunlit country lane between lush green paddy fields at dusk, a righteous Tamil farmer with Vibhuti markings and wooden staff gently herds a lost mother cow (Gomata) and her calf back to the homestead of his rival neighbor who had previously wronged him. The rival neighbor stands at his courtyard gate, overcome with gratitude and ashamed of his past enmity, folding his hands in reverent salute. Warm sunset glow across emerald fields, triumph of noble conduct (Kural 158). No modern fences, no text."
    ),
    41: (
        "41-n41_planting_fruit_trees_on_border.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Along the shared boundary of two adjoining farmland plots in ancient Tamil Nadu at sunrise, a generous Tamil farmer with sacred thread and Vibhuti lovingly plants a young mango and pomegranate sapling, directing their future shade and fruit toward his neighbor's courtyard. He waters the fertile red earth from a brass pot with a smile of unconditional goodwill, dissolving past boundary disputes into lasting harmony. Morning mist, distant temple gopuram, no modern tools, no text."
    ),
    42: (
        "42-n42_lighting_lamp_for_estranged_kin.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. At tranquil twilight, a graceful Tamil mother in a traditional madisar saree carrying a tall bronze Agal Vilakku with a steady golden flame walks across the stone lane to the threshold of an estranged relative's home. She gently places the glowing lamp on their outer stone ledge, illuminating their dark doorway with warmth and reconciliation. Jasmine flowers in her hair, sacred kolam on the ground, dispelling darkness through love and initiative (Kural 158). No modern lights, no text."
    ),
    43: (
        "43-n43_insolent_man_hanging_head_in_shame.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Directly illustrating Kural 158 (மிகையினால் மிக்கவை செய்தாரைத் தாம்தம் தகையினால் வென்று விடல்). In an ancient village square bathed in warm late afternoon light, an arrogant man who committed grave wrongs stands with deeply bowed head, eyes cast down in total remorse and shame, completely disarmed not by violence, but by the overwhelming, dignified nobility and forgiveness of the man he wronged. The noble victim stands poised with folded hands, radiating moral triumph. Ancient stone pillars, no modern clothes, no text."
    ),
    44: (
        "44-n44_mirror_of_unbroken_peace.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A symbolic visual meditation on inner tranquility. A pristine, polished antique round bronze mirror (Valkannadi) resting on a carved granite plinth reflects a pure, cloudless azure sky and the golden tip of a temple vimana. Though storms rage in the world, the mirror remains crystal clear, unscratched, and unclouded. Soft dhoopam smoke drifts around its carved bronze frame, conveying the pristine soul whose inner peace cannot be tarnished by insults (Kural 159). No modern items, no text."
    ),
    45: (
        "45-n45_cool_snow_quenching_embers.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A high-contrast philosophical visual metaphor. A bed of harsh, glowing red charcoal embers lies upon ancient stone; pure, pristine white mountain snow and cool crystal spring water gently descend upon the embers, instantly quenching their burning fury into soft, harmless cool steam and grey ash. Beautiful steam rising in morning mountain light, visually allegorizing how pure forbearance effortlessly quenches the scorching fire of hostility (Kural 159). No modern items, no text."
    ),
    46: (
        "46-n46_aggressor_dropping_weapons.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In an ancient temple courtyard at sunset, a fierce, armed attacker stands trembling as his bronze battle-axe and dagger slip from his open hands, clattering harmlessly onto the granite flagstones. Facing him is a gentle Tamil sage adorned with Vibhuti and Rudraksha, whose utterly fearless, radiant smile of pure compassion disarms the violent heart without lifting a finger. Golden hour lighting, temple mandapam pillars, sublime victory of Ahimsa (Kural 159). No modern weapons, no text."
    ),
    47: (
        "47-n47_reformed_offender_seeking_pardon.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. At the granite threshold of an ancient Tamil ashram hermitage at dawn, a former thief and wrongdoer prostrates in humble Shastanga Namaskaram on the stone ground, weeping tears of genuine repentance. The venerable Rishi, clothed in saffron with sacred thread and Vibhuti, gently reaches down with compassionate hands to lift the man up, placing a hand on his head in divine blessing and complete pardon. Glowing oil lamps, sacred Gomata looking on, moral redemption. No modern clothes, no text."
    ),
    48: (
        "48-n48_crowd_murmuring_respect_for_patience.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In a bustling ancient temple street market in Madurai or Thanjavur at golden afternoon, a large crowd of traditional citizens, scholars, and merchants in dhotis and sarees look with murmurs of awe and deep respect toward a righteous man who calmly walked away from an insulting provocation without a harsh word. People fold their hands in spontaneous reverence as he passes by in noble silence. Towering temple Rajagopuram in background, cultural elevation of patience (Kural 159). No modern items, no text."
    ),
    49: (
        "49-n49_austere_ascetic_on_mountain_peak.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. On a windswept, misty granite mountain peak in the Western Ghats at sunrise, an austere Tamil ascetic (Tapasvi) sits in unmoving padmasana amidst swirling mountain clouds. He has long matted locks (Jata), ash-smeared body (Bhasma), and Rudraksha malas. Though he has renounced all food and comforts, the scene introduces Kural 160: those who fast and perform severe austerities are great, but even greater are those who bear the bitter words of others. Epic Himalayan/Ghat grandeur, golden sunrays, no modern items, no text."
    ),
    50: (
        "50-n50_humble_householder_absorbing_revilement.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Directly illustrating Kural 160 (உண்ணாது நோற்பார் பெரியர் பிறர்சொல்லும் இன்னாச்சொல் நோற்பாரின் பின்). In an ancient village lane at midday, a humble Tamil householder with sacred thread and Vibhuti markings walks serenely with his brass water pot while a cynical critic shouts bitter revilement behind him. The householder's face remains as tranquil as a calm lake, his lips curled in a quiet blessing, embodying the supreme asceticism of bearing verbal insults with grace. Warm sunlit lane, thatched roofs, no modern clothes, no text."
    ),
    51: (
        "51-n51_scales_weighing_fasting_vs_forbearance.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A profound philosophical allegory directly visualizing Kural 160. An ancient, intricately carved bronze balance scale (Thula) hangs inside a temple sanctum. On one scale pan rests an ascetic's begging bowl and fasting grass mat; on the other pan rests a glowing, luminous white pearl representing patient endurance of harsh words. The scale pan with the pearl of forbearance outweighs the fasting pan, proving that bearing insult is higher than physical mortification. Candlelight, dhoopam smoke, carved granite pillars, no modern items, no text."
    ),
    52: (
        "52-n52_pure_radiance_of_patient_soul.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A luminous, intimate portrait of an enlightened Tamil saint / householder whose entire being radiates a subtle, warm golden halo of spiritual light. Adorned with white Tripundra Vibhuti, Rudraksha, and a pristine white angavastram, his eyes are wells of unconditional compassion and divine equanimity. He sits before a sacred home shrine where a bronze oil lamp flickers steadily, conveying the supreme majesty of a soul that has conquered anger and resentment forever (Kural 160). No modern items, no text."
    ),
    53: (
        "53-n53_monsoon_downpour_unmoved_lotus.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A high-detail macro shot during a torrential monsoon downpour over a sacred temple lotus pond. Heavy raindrops splatter forcefully onto the surface, yet a majestic pink lotus blossom stands completely tall, untorn, and radiant, with rain droplets rolling harmlessly off its waxy green leaves like pearls. In the misty background, an ancient Dravidian temple gopuram is silhouetted in the rain. Perfect allegory of the forbearing soul that remains pristine amidst external storms. No modern items, no text."
    ),
    54: (
        "54-n54_saintly_presence_calming_village.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. At golden dusk in an ancient Tamil village square where an angry crowd had assembled, an elderly saintly sage with white beard, saffron robe, and Tripundra Vibhuti walks slowly through the gathering with open palms and deep peaceful aura. As he passes, angry shouts turn to reverent whispers; men lower their fists, women fold their hands, and an overwhelming wave of sacred peace settles over the entire village. Golden hour lighting, temple tank reflections, no modern clothes, no text."
    ),
    55: (
        "55-n55_hermit_abstaining_from_food.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. Inside a sacred cave hermitage in the hills of ancient Tamil Nadu, a dedicated ascetic sits in silent penance, ignoring a brass plate of fresh fruits and cooked rice placed beside him, observing strict religious fasting (Upavasa). Sunlight streams through the cave mouth onto carved stone Shiva Lingam. A visual reverence for ascetic fasting, setting up the philosophical truth that patient endurance of harsh words is even greater (Kural 160). No modern items, no text."
    ),
    56: (
        "56-n56_hero_swallowing_his_own_anger.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A powerful, intense close-up portrait of a noble Tamil warrior / householder with sacred thread and Vibhuti lines who has been provoked. For a single heartbeat, his jaw clenches and his eyes flare; then, with supreme internal mastery and spiritual strength, he deliberately breathes in, softens his brow, releases his clenched fist, and lets the poison of anger dissolve into calm forbearance like Lord Shiva drinking the halahala poison. Golden morning light, profound psychological victory, no modern clothes, no text."
    ),
    57: (
        "57-n57_cooling_stream_in_forest_sanctuary.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A wide, tranquil shot of a pristine crystal-clear mountain stream flowing gently through a sacred forest hermitage in Tamil Nadu. The cool water cascades over smooth moss-covered granite boulders, creating soft pools where white swans float and spotted deer drink in peace. Fragrant parijatha flowers drift on the surface, and ancient rishis meditate under flowering kadamba trees. Sublime cooling peace of nature that soothes all worldly fever, no modern items, no text."
    ),
    58: (
        "58-n58_sacred_bull_calmly_resting.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In the sunlit stone courtyard of an ancient Shiva temple, a magnificent, regal white hump-backed temple bull (Nandi bull / Bos indicus with sacred Vibhuti markings and turmeric on his curved horns) rests majestically on the cool granite stones. Small playful sparrows hop fearlessly around his hooves and horns; the sacred bull chews cud with absolute, unbothered gentleness and patient dignity, a living emblem of supreme forbearance. Carved Dravidian temple pillars, incense smoke, no modern items, no text."
    ),
    59: (
        "59-n59_open_heavens_above_patient_earth.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A breathtaking, epic wide-angle composition looking from a fertile Tamil river valley toward the vast, radiant sky at dawn. Mother Earth below spreads rich green paddy fields, flowing Kaveri waters, and ancient stone temple towers, while the endless blue sky above opens with golden light rays breaking through celestial clouds. Unbroken harmony between patient Earth and forgiving Heavens, embodying the cosmic universality of forbearance. No modern buildings, no electrical wires, no text."
    ),
    60: (
        "60-n60_community_celebrating_in_reconciliation.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. In an ancient Tamil village square at golden twilight, two former rival families celebrate a sacred feast of reconciliation together. Under a canopy of fresh green mango leaves and fragrant marigold torans, elders, men, women, and children sit in a joyous circle sharing sweet payasam served on green banana leaves. Warm bronze oil lamps illuminate their radiant, forgiving faces, and traditional flute music plays, marking the sacred victory of mutual forbearance. No modern items, no text."
    ),
    61: (
        "61-n61_temple_gopuram_against_setting_sun.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. A monumental, breathtaking silhouette shot of an ancient South Indian Dravidian stone temple Rajagopuram rising majestically against a blazing crimson and gold setting sun. The intricate tiers of carved deities, kalasams, and dwarapalakas stand against the glowing sky, while gentle flocks of white egrets fly home across the twilight horizon. Smoke from evening temple homam fires rises heavenward, eternal sentinel of Dharma and timeless spiritual peace. No modern buildings, no wires, no text."
    ),
    62: (
        "62-n62_eternal_flame_in_granite_sanctum.jpg",
        "A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. The grand finale shot of Chapter 16. Inside the deepest dark granite sanctum sanctorum (Garbhagriha) of an ancient thousand-year-old Shiva temple. An antique bronze Akhanda Deepam (eternal flame) burns with an unwavering, pure golden teardrop flame on a carved stone pedestal before the sacred Lingam adorned with Bilva leaves. Intricately carved Tamil inscriptions on the dark granite walls catch the sacred amber glow, with fragrant sambrani incense smoke curling into the sacred stillness. The eternal, indestructible flame of forbearance and truth that never dies. No modern items, no text."
    ),
}

def generate_shot(shot_num, filename, prompt):
    out_path = DEST_DIR / filename
    print(f"\n[Shot {shot_num}/62] Generating {filename}...")
    
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
                    # Save and convert to high quality JPEG
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
    print(f"Starting direct high-speed generation for Chapter 16 shots 21-62...")
    print(f"Destination: {DEST_DIR}")
    
    total = len(SHOTS)
    success = 0
    start_time = time.time()
    
    for num, (fname, prompt) in sorted(SHOTS.items()):
        ok = generate_shot(num, fname, prompt)
        if ok:
            success += 1
        time.sleep(2.5)  # Safe delay between calls
        
    elapsed = time.time() - start_time
    print(f"\nCompleted! Generated {success}/{total} shots in {elapsed/60:.1f} minutes.")

if __name__ == "__main__":
    main()

