# -*- coding: utf-8 -*-
"""
Builder for colab_generate_gurukulam_artworks.ipynb
Configured for A100 GPU utilizing FLUX.1-schnell / SDXL-Lightning
Contains full 136-shot cinematic suites for Chapters 54, 57, and 61.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "colab_generate_gurukulam_artworks.ipynb"

# 46 shots for Chapter 54 (Pochchaavaamai: 319.32s -> 6.94s/shot)
CH54_PROMPTS = [
    # Kural 531: Carelessness destroys glory and wealth
    {"filename": "54-pochchaavaamai/01-n01_king_neglecting_affairs.jpg",
     "title": "Kural 531: King distracted, neglecting royal affairs",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient Tamil palace court, a young crowned king lost in careless reverie staring out the window while unrolled palm-leaf state ledgers sit untended on a carved teak desk, warm afternoon side light, ornate granite pillars."},
    {"filename": "54-pochchaavaamai/02-n02_withering_royal_orchards.jpg",
     "title": "Kural 531: Neglected garden withering from careless oversight",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient Tamil royal botanical grove with dried fallen leaves and neglected water fountains, an overseer walking through with regret, soft golden dusk light."},
    {"filename": "54-pochchaavaamai/03-n03_unattended_ledgers_candle.jpg",
     "title": "Kural 531: Guttering oil lamp near neglected scroll archive",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient stone library, a guttering brass oil lamp flickering dangerously close to stacks of ancient palm-leaf scrolls on a low table, chiaroscuro lighting, deep shadows."},
    {"filename": "54-pochchaavaamai/04-n04_counselor_warning_prince.jpg",
     "title": "Kural 531: Wise elderly counselor warning an aloof prince",
     "prompt": "Photorealistic 16:9 cinematic film still, open pillared terrace of an ancient Chola palace, a venerable grey-bearded minister with folded palms urgently advising a careless prince, distant river city in background."},
    {"filename": "54-pochchaavaamai/05-n05_ruined_dynasty_monoliths.jpg",
     "title": "Kural 531: Parable of a forgotten ruined kingdom",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient weathered stone temple pavilion overgrown with banyan roots, fallen pillars half-buried in dry soil, solemn moody atmospheric lighting."},

    # Kural 532: Forgetfulness kills wisdom as poverty kills glory
    {"filename": "54-pochchaavaamai/06-n06_scholar_sleeping_at_desk.jpg",
     "title": "Kural 532: Scribe falling asleep over fading scrolls",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient Tamil academy room, a tired student nodding off over an iron stylus and palm leaf, oil lamp smoking in the midnight silence."},
    {"filename": "54-pochchaavaamai/07-n07_dying_lamp_in_darkness.jpg",
     "title": "Kural 532: Oil lamp wick dying in the dark",
     "prompt": "Photorealistic 16:9 cinematic close-up, ornate ancient bronze oil lamp with flame dwindling down to a smoking ember, darkness encroaching on a stone altar, warm moody rim light."},
    {"filename": "54-pochchaavaamai/08-n08_vigilant_guru_instructing.jpg",
     "title": "Kural 532: Alert guru guiding students by lamplight",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient gurukulam under a banyan tree, wise preceptor in white dhoti holding an oil lamp illuminating an open scroll for alert attentive students, glowing fireflies in background."},
    {"filename": "54-pochchaavaamai/09-n09_sharp_mind_dawn_study.jpg",
     "title": "Kural 532: Disciplined scholar reciting at dawn",
     "prompt": "Photorealistic 16:9 cinematic film still, serene stone mandapam beside a temple lotus pond at dawn, a focused Tamil scholar chanting verses with clear alert eyes, morning mist over water."},

    # Kural 533: No glory for the forgetful; proclaimed in all books
    {"filename": "54-pochchaavaamai/10-n10_sangam_academy_assembly.jpg",
     "title": "Kural 533: Sangam academy assessing sacred verses",
     "prompt": "Photorealistic 16:9 cinematic film still, grand Sangam assembly hall in ancient Madurai, venerated Tamil poets and scholars seated in a circle critically examining inscribed palm leaves, soft diffused daylight."},
    {"filename": "54-pochchaavaamai/11-n11_poet_presenting_scroll.jpg",
     "title": "Kural 533: Poet presenting flawless palm-leaf manuscript",
     "prompt": "Photorealistic 16:9 cinematic film still, royal Tamil court, an earnest poet presenting an immaculate bound palm-leaf manuscript on a silver tray to royal scholars, pride of dedication."},
    {"filename": "54-pochchaavaamai/12-n12_epigrapher_chiseling_stone.jpg",
     "title": "Kural 533: Inscribing timeless state decree on granite wall",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient temple courtyard, a master epigrapher chiseling Tamil Brahmi characters into a massive granite base wall with mallet and chisel, stone dust in sunlight."},
    {"filename": "54-pochchaavaamai/13-n13_hall_of_wise_elders.jpg",
     "title": "Kural 533: Council of vigilant elders reviewing history",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient stone chamber lined with palm-leaf manuscript cubicles, grey-haired historians consulting rolled records by warm oil lamp glow."},
    {"filename": "54-pochchaavaamai/14-n14_sacred_library_vaults.jpg",
     "title": "Kural 533: Ancient royal library of enduring wisdom",
     "prompt": "Photorealistic 16:9 cinematic film still, grand ancient Tamil royal archive with cedarwood shelves holding thousands of tied palm-leaf manuscripts, beam of golden sunlight cutting through the air."},

    # Kural 534: No fortress for the fearful; no good for the unmindful
    {"filename": "54-pochchaavaamai/15-n15_fortress_gate_sentinels.jpg",
     "title": "Kural 534: Watchful sentinels guarding fortress gates",
     "prompt": "Photorealistic 16:9 cinematic film still, colossal ancient granite fortress gate with iron-studded doors, disciplined Tamil guards with brass-tipped spears standing vigilant at dusk, flaming torchlight."},
    {"filename": "54-pochchaavaamai/16-n16_mountain_watchtower_dawn.jpg",
     "title": "Kural 534: Lone lookout on mountain watchtower at dawn",
     "prompt": "Photorealistic 16:9 cinematic film still, high stone watchtower on a misty mountain ridge overlooking a winding river valley, an alert Tamil sentry scanning the distant frontier passes in morning mist."},
    {"filename": "54-pochchaavaamai/17-n17_warning_sleeping_sentry.jpg",
     "title": "Kural 534: Parable of the sleeping guard and shadow",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient fort rampart at midnight, a negligent sentry slumped against stone while distant shadows move along the wall, tense dramatic moonlight and torch fire."},
    {"filename": "54-pochchaavaamai/18-n18_iron_gate_latched_secure.jpg",
     "title": "Kural 534: Massive brass locks secured by vigilant warden",
     "prompt": "Photorealistic 16:9 cinematic close-up, heavy antique brass and iron latch mechanism being locked into place on a massive teak gateway by a resolute guard's hands, flickering warm torchlight."},

    # Kural 535: Off-guard ruler loses past achievements
    {"filename": "54-pochchaavaamai/19-n19_earthen_canal_breach.jpg",
     "title": "Kural 535: Neglected irrigation canal leaking muddy water",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient earthen reservoir bund showing a dangerous trickle of muddy water escaping through untended masonry, urgent atmospheric warning."},
    {"filename": "54-pochchaavaamai/20-n20_engineers_rushing_inspection.jpg",
     "title": "Kural 535: Hydraulic engineers rushing to repair canal wall",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient Tamil water engineers carrying timber planks and stone blocks along a canal bank in stormy weather, purposeful determined action."},
    {"filename": "54-pochchaavaamai/21-n21_vigilant_waterkeeper_sluice.jpg",
     "title": "Kural 535: Watchful waterkeeper measuring stone depth gauges",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient stone sluice gate of a giant lake, an alert official checking depth markings carved into a granite pillar at sunset, tranquil glowing water."},
    {"filename": "54-pochchaavaamai/22-n22_fertile_delta_preserved.jpg",
     "title": "Kural 535: Lush green river delta saved by foresight",
     "prompt": "Photorealistic 16:9 cinematic wide shot, vast emerald green paddy fields of the Cauvery delta crisscrossed by clean stone canals, farmers smiling in golden morning light."},
    {"filename": "54-pochchaavaamai/23-n23_granary_seal_inspection.jpg",
     "title": "Kural 535: Overseer inspecting royal granary seals",
     "prompt": "Photorealistic 16:9 cinematic film still, stone granary hallway, a diligent officer checking clay seal impressions on heavy wooden grain bin lids with a handheld brass lamp."},

    # Kural 536: The one who is never unmindful never slips
    {"filename": "54-pochchaavaamai/24-n24_charioteer_intense_focus.jpg",
     "title": "Kural 536: Master charioteer holding reins with razor focus",
     "prompt": "Photorealistic 16:9 cinematic close-up, an ancient Tamil royal charioteer with focused resolute eyes gripping leather reins of four proud galloping horses, dust motes in golden sunset light."},
    {"filename": "54-pochchaavaamai/25-n25_helmsman_stormy_seas.jpg",
     "title": "Kural 536: Sea captain navigating wooden ship through surge",
     "prompt": "Photorealistic 16:9 cinematic film still, prow of an ancient Chola wooden merchant vessel slicing through choppy ocean waves, veteran captain holding the steering oar with calm mastery, sea spray."},
    {"filename": "54-pochchaavaamai/26-n26_archer_drawing_bow.jpg",
     "title": "Kural 536: Archer with unwavering concentration at target",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient Tamil archery training ground at dawn, an archer drawing a curved wooden bow to cheek, motionless laser-sharp focus, morning sunlight through trees."},
    {"filename": "54-pochchaavaamai/27-n27_cavalry_patrol_alert.jpg",
     "title": "Kural 536: Disciplined cavalry patrol on frontier border",
     "prompt": "Photorealistic 16:9 cinematic film still, squad of ancient Tamil horsemen on proud stallions pausing atop a rocky outcrop, scouts surveying the forested valley with disciplined vigilance."},
    {"filename": "54-pochchaavaamai/28-n28_night_watch_ramparts.jpg",
     "title": "Kural 536: Midnight perimeter guard with flaming brazier",
     "prompt": "Photorealistic 16:9 cinematic film still, stone castle parapet at midnight under starry sky, two armored guards beside a glowing iron fire basket, absolute alertness and quiet devotion to duty."},

    # Kural 537: Difficult tasks become easy with continuous mindfulness
    {"filename": "54-pochchaavaamai/29-n29_bronze_casting_precision.jpg",
     "title": "Kural 537: Master bronze caster pouring glowing alloy into mold",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient artisan foundry, master bronze sculptor carefully pouring glowing orange molten bronze into an intricate clay lost-wax deity mold, steady unwavering hands."},
    {"filename": "54-pochchaavaamai/30-n30_gem_cutter_delicate_art.jpg",
     "title": "Kural 537: Jeweler faceting a ruby on rotary stone wheel",
     "prompt": "Photorealistic 16:9 cinematic close-up, ancient Tamil gem-cutter holding a raw crimson ruby against a fine grinding wheel with delicate precision, oil lamp highlighting concentrated eyes."},
    {"filename": "54-pochchaavaamai/31-n31_silk_loom_thousand_threads.jpg",
     "title": "Kural 537: Handloom weaver guiding golden silk warp threads",
     "prompt": "Photorealistic 16:9 cinematic film still, wooden pit-loom workshop, master weaver swiftly passing a wooden shuttle through thousands of glistening gold and silk threads, rhythmic effortless mastery."},
    {"filename": "54-pochchaavaamai/32-n32_stone_carver_micro_chisel.jpg",
     "title": "Kural 537: Sculptor carving intricate jewelry on stone goddess",
     "prompt": "Photorealistic 16:9 cinematic close-up, sculptors iron chisel gently shaping delicate stone bead garlands on a granite temple pillar, stone chips falling in sunbeam."},

    # Kural 538: Act with vigilance on what elders praise
    {"filename": "54-pochchaavaamai/33-n33_prince_listening_to_elders.jpg",
     "title": "Kural 538: Prince listening intently to senior statesman",
     "prompt": "Photorealistic 16:9 cinematic film still, sunlit palace colonnade, a young prince with humble folded hands listening to a revered grey-haired minister who points to ancient palm-leaf scrolls."},
    {"filename": "54-pochchaavaamai/34-n34_ceremonial_sacred_altar.jpg",
     "title": "Kural 538: Solemn blessing at ancient temple altar",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient stone mandapam with smoking dhoopam braziers and flower garlands, elders anointing a young leader with sacred sandalwood paste."},
    {"filename": "54-pochchaavaamai/35-n35_royal_council_treaty.jpg",
     "title": "Kural 538: Deliberation over peaceful interstate treaty",
     "prompt": "Photorealistic 16:9 cinematic film still, semicircular council table with ancient map carved on wooden tablet, ministers discussing state boundaries with measured wisdom."},
    {"filename": "54-pochchaavaamai/36-n36_sealing_pact_elephant_ring.jpg",
     "title": "Kural 538: Sealing a solemn decree with royal emblem",
     "prompt": "Photorealistic 16:9 cinematic close-up, heavy gold signet ring with tiger or elephant emblem pressing into warm beeswax on a rolled palm-leaf scroll, crisp legal integrity."},
    {"filename": "54-pochchaavaamai/37-n37_elders_guiding_village_fund.jpg",
     "title": "Kural 538: Village sabha elders reviewing community trust",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient banyan tree platform, village elders in white robes reviewing copper plate endowment records under morning shade."},

    # Kural 539: Remember those destroyed by careless joy
    {"filename": "54-pochchaavaamai/38-n38_reckless_banquet_distraction.jpg",
     "title": "Kural 539: Parable of a reckless court feast off guard",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient banquet hall with fallen wine goblets and drowsy nobles, a stark moral warning against abandoning vigilance in moments of revelry."},
    {"filename": "54-pochchaavaamai/39-n39_watchman_remaining_aloof.jpg",
     "title": "Kural 539: Sentry outside banquet hall standing resolute",
     "prompt": "Photorealistic 16:9 cinematic film still, terrace outside the noisy feast hall, a lone guard standing straight with spear looking out at the dark horizon, unaffected by the revelry inside."},
    {"filename": "54-pochchaavaamai/40-n40_ascetic_in_mountain_cave.jpg",
     "title": "Kural 539: Ascetic meditating in silent cave above city",
     "prompt": "Photorealistic 16:9 cinematic film still, peaceful mountain rock cave overlooking a distant glittering ancient city, a sage seated in tranquil meditative awareness, soft twilight glow."},
    {"filename": "54-pochchaavaamai/41-n41_thiruvalluvar_etching_kural.jpg",
     "title": "Kural 539: Sage Thiruvalluvar etching verses of warning",
     "prompt": "Photorealistic 16:9 cinematic film still, simple thatched hermitage, sage Thiruvalluvar with serene profound countenance inscribing verses onto a dried palm leaf with an iron stylus."},
    {"filename": "54-pochchaavaamai/42-n42_mirror_of_self_reflection.jpg",
     "title": "Kural 539: King examining conscience by candle glow",
     "prompt": "Photorealistic 16:9 cinematic film still, quiet palace bedchamber, an ancient king gazing into a polished bronze mirror by oil candlelight, reflecting deeply on the day's governance."},

    # Kural 540: When careless pride tempts you, remember the fallen
    {"filename": "54-pochchaavaamai/43-n43_king_on_balcony_at_dusk.jpg",
     "title": "Kural 540: King standing on palace balcony meditating on duty",
     "prompt": "Photorealistic 16:9 cinematic film still, high carved granite palace balcony at dusk, an ancient Tamil monarch in regal simplicity looking out over his vast peaceful kingdom with profound humility."},
    {"filename": "54-pochchaavaamai/44-n44_sunset_over_temple_city.jpg",
     "title": "Kural 540: Peaceful city resting securely under watchful rule",
     "prompt": "Photorealistic 16:9 cinematic sweeping wide shot, ancient temple city with towering gopurams bathed in purple and orange sunset light, smoke rising peacefully from domestic hearths."},
    {"filename": "54-pochchaavaamai/45-n45_steady_flame_in_sanctum.jpg",
     "title": "Kural 540: Unflickering oil lamp burning steadily in sanctum",
     "prompt": "Photorealistic 16:9 cinematic close-up, ancient stone temple sanctum, a pure golden flame on a heavy brass deepam burning without the slightest flicker in still air, symbol of unbroken mindfulness."},
    {"filename": "54-pochchaavaamai/46-n46_prosperous_orderly_market.jpg",
     "title": "Kural 540: Climax: A kingdom preserved in flourishing peace",
     "prompt": "Photorealistic 16:9 cinematic wide shot, thriving ancient Tamil marketplace with merchants, artisans, and families walking freely under blue morning skies, the triumph of eternal vigilance."}
]

# 50 shots for Chapter 57 (Veruvantha Seyyaamai: 341.49s -> 6.83s/shot)
CH57_PROMPTS = [
    # Kural 561: Impartial investigation and measured justice
    {"filename": "57-veruvantha-seyyaamai/01-n01_king_patient_hearing.jpg",
     "title": "Kural 561: King listening with deep patience to a poor villager",
     "prompt": "Photorealistic 16:9 cinematic film still, open pillared hall of justice, a compassionate Tamil king on a low carved wooden seat leaning forward to listen attentively to a poor farmer in cotton cloth, warm morning light."},
    {"filename": "57-veruvantha-seyyaamai/02-n02_examining_evidence_scale.jpg",
     "title": "Kural 561: Royal magistrate examining boundary markers",
     "prompt": "Photorealistic 16:9 cinematic film still, village court under a banyan tree, an upright magistrate examining ancient carved boundary stones and land deeds, villagers looking on with trust."},
    {"filename": "57-veruvantha-seyyaamai/03-n03_scales_of_fair_judgment.jpg",
     "title": "Kural 561: Symbolic balance scale held in stone chamber",
     "prompt": "Photorealistic 16:9 cinematic close-up, antique bronze balance scale perfectly level in a sunlit stone hall of justice, soft warm light highlighting polished brass pans."},
    {"filename": "57-veruvantha-seyyaamai/04-n04_counselors_deliberating_fairness.jpg",
     "title": "Kural 561: Legal scholars debating proportionate restitution",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient stone library, legal scholars consulting ancient treatises on dharma, seeking fair and restorative punishment without cruelty."},
    {"filename": "57-veruvantha-seyyaamai/05-n05_reconciliation_of_disputants.jpg",
     "title": "Kural 561: Disputing neighbors clasping hands in peace",
     "prompt": "Photorealistic 16:9 cinematic film still, village square, two former rivals bowing to each other in mutual respect following a fair judicial ruling, relieved families watching."},

    # Kural 562: Threaten severely if needed, but strike gently
    {"filename": "57-veruvantha-seyyaamai/06-n06_royal_scepter_of_restraint.jpg",
     "title": "Kural 562: Royal golden scepter held with calm dignity",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient Tamil monarch holding an ornate gold Sengol scepter resting lightly in hand, commanding respect without tyranny, courtly durbar."},
    {"filename": "57-veruvantha-seyyaamai/07-n07_pardoning_penitent_youth.jpg",
     "title": "Kural 562: Judge offering pardon to a remorseful youth",
     "prompt": "Photorealistic 16:9 cinematic film still, stone judgment hall, a wise magistrate placing a comforting hand on the shoulder of a repentant young apprentice, assigning constructive community service instead of prison."},
    {"filename": "57-veruvantha-seyyaamai/08-n08_guards_as_protectors.jpg",
     "title": "Kural 562: Royal guards standing as friendly protectors",
     "prompt": "Photorealistic 16:9 cinematic film still, ancient city gates, disciplined royal guards smiling kindly and helping an elderly woman carry a basket of fruit through the archway."},
    {"filename": "57-veruvantha-seyyaamai/09-n09_gentle_admonishment_court.jpg",
     "title": "Kural 562: King rebuking an errant official with mild firmness",
     "prompt": "Photorealistic 16:9 cinematic film still, private council chamber, a king speaking firm but dignified corrective words to a seated official, who listens with respectful remorse."},
    {"filename": "57-veruvantha-seyyaamai/10-n10_restoration_of_confiscated_goods.jpg",
     "title": "Kural 562: Restoring wrongfully taken goods to family",
     "prompt": "Photorealistic 16:9 cinematic film still, stone treasury courtyard, royal officers returning cattle and grain bags to a relieved peasant family under state decree."},

    # Kural 563: Despot who terrorizes subjects perishes soon
    {"filename": "57-veruvantha-seyyaamai/11-n11_parable_deserted_tyrant_streets.jpg",
     "title": "Kural 563: Desolate empty street under a cruel ruler's shadow",
     "prompt": "Photorealistic 16:9 cinematic film still, gloomy deserted ancient streets with barred wooden shutters, a harsh shadow cast by fortress walls, stark warning against tyrannical oppression."},
    {"filename": "57-veruvantha-seyyaamai/12-n12_citizens_fleeing_harsh_levy.jpg",
     "title": "Kural 563: Distress of villagers under an extortionate lord",
     "prompt": "Photorealistic 16:9 cinematic film still, dusty village road at dusk, peasants packing simple earthen belongings, a somber warning of how cruelty empties the countryside."},
    {"filename": "57-veruvantha-seyyaamai/13-n13_contrast_just_king_procession.jpg",
     "title": "Kural 563: Joyful citizens welcoming the righteous monarch",
     "prompt": "Photorealistic 16:9 cinematic film still, sun-drenched avenue in ancient Madurai, cheering citizens showering jasmine and lotus petals on the righteous king riding on elephant back."},
    {"filename": "57-veruvantha-seyyaamai/14-n14_loving_greeting_on_road.jpg",
     "title": "Kural 563: Villagers offering fresh coconut water to king",
     "prompt": "Photorealistic 16:9 cinematic film still, palm grove by country road, village elders gladly offering sweet tender coconut water to the traveling king and his retinue, mutual devotion."},
    {"filename": "57-veruvantha-seyyaamai/15-n15_open_doors_peaceful_evening.jpg",
     "title": "Kural 563: Homes with doors open in safety and peace",
     "prompt": "Photorealistic 16:9 cinematic film still, quiet ancient Tamil street at dusk, oil lamps glowing on verandas, doors unlocked without fear of extortion or nighttime intrusion."},

    # Kural 564: "Our king is cruel!" tears that shorten king's life
    {"filename": "57-veruvantha-seyyaamai/16-n16_whispers_of_grief_forbidden.jpg",
     "title": "Kural 564: Parable of suppressed tears under bad ruler",
     "prompt": "Photorealistic 16:9 cinematic film still, dimly lit stone alley, villagers whispering in sorrow, moral teaching that subjects tears burn away a tyrant's sovereignty."},
    {"filename": "57-veruvantha-seyyaamai/17-n17_king_in_disguise_listening.jpg",
     "title": "Kural 564: Righteous king in disguise listening to villagers",
     "prompt": "Photorealistic 16:9 cinematic film still, humble roadside teashop or resting pavilion, a king in simple traveler garb seated among common folk, listening to their honest joys and worries."},
    {"filename": "57-veruvantha-seyyaamai/18-n18_sharing_gruel_with_farmers.jpg",
     "title": "Kural 564: King sharing simple rice gruel with plowmen",
     "prompt": "Photorealistic 16:9 cinematic film still, edge of a muddy paddy field under a tamarind tree, the king sitting on grass sharing fresh kanji with hardworking plowmen, warm smiles."},
    {"filename": "57-veruvantha-seyyaamai/19-n19_wiping_tears_of_widow.jpg",
     "title": "Kural 564: King wiping tears of an aggrieved mother",
     "prompt": "Photorealistic 16:9 cinematic film still, palace steps, the monarch bending down personally to accept a petition from a tearful elderly woman, commanding immediate relief."},
    {"filename": "57-veruvantha-seyyaamai/20-n20_blessings_of_the_elderly.jpg",
     "title": "Kural 564: Village elders raising hands in heartfelt blessing",
     "prompt": "Photorealistic 16:9 cinematic film still, village temple entrance, grey-haired elders blessing the passing sovereign with sacred ash, wishing him long life for his gentle rule."},

    # Kural 565: Inaccessible ruler with fierce gaze loses wealth
    {"filename": "57-veruvantha-seyyaamai/21-n21_inaccessible_palace_iron_gates.jpg",
     "title": "Kural 565: Warning of high intimidating palace walls",
     "prompt": "Photorealistic 16:9 cinematic film still, towering grim fortress gate with stern guards turning away citizens, dramatic cautionary contrast."},
    {"filename": "57-veruvantha-seyyaamai/22-n22_open_accessible_durbar.jpg",
     "title": "Kural 565: Accessible royal pavilion open to all citizens",
     "prompt": "Photorealistic 16:9 cinematic film still, open-air granite pavilion bathed in morning sunlight, the king seated without intimidating barrier, commoners walking up freely with petitions."},
    {"filename": "57-veruvantha-seyyaamai/23-n23_gentle_welcoming_expression.jpg",
     "title": "Kural 565: Monarch greeting a humble artisan with warmth",
     "prompt": "Photorealistic 16:9 cinematic close-up, a wise Tamil kings face illuminated by soft light, eyes filled with warmth and respect as he speaks with an artisan holding a clay bowl."},
    {"filename": "57-veruvantha-seyyaamai/24-n24_children_playing_near_palace.jpg",
     "title": "Kural 565: Children playing near royal courtyard steps",
     "prompt": "Photorealistic 16:9 cinematic film still, wide stone palace forecourt, village children laughing and spinning wooden tops near the guards without fear, relaxed benevolent atmosphere."},
    {"filename": "57-veruvantha-seyyaamai/25-n25_open_durbar_mango_grove.jpg",
     "title": "Kural 565: Council seated beneath blooming mango grove",
     "prompt": "Photorealistic 16:9 cinematic film still, lush shaded mango grove with dappled sunlight, royal assembly meeting outdoors in nature, approachable and serene statecraft."},

    # Kural 566: Harsh words and unmeasured punishment blunt victory
    {"filename": "57-veruvantha-seyyaamai/26-n26_sword_in_scabbard_of_peace.jpg",
     "title": "Kural 566: Royal ceremonial sword resting quietly in velvet",
     "prompt": "Photorealistic 16:9 cinematic close-up, ornate antique steel sword resting inside an engraved brass and velvet scabbard on silk cushions, symbol of martial strength restrained by virtue."},
    {"filename": "57-veruvantha-seyyaamai/27-n27_diplomat_speaking_sweet_words.jpg",
     "title": "Kural 566: Diplomat speaking soft conciliatory words",
     "prompt": "Photorealistic 16:9 cinematic film still, serene audience chamber, a wise envoy with gentle smile presenting olive branch terms, diffusing tension with peaceful eloquence."},
    {"filename": "57-veruvantha-seyyaamai/28-n28_peaceful_frontier_accord.jpg",
     "title": "Kural 566: Two neighboring kings signing peaceful treaty",
     "prompt": "Photorealistic 16:9 cinematic film still, tented pavilion on border riverbank, two kings exchanging auspicious gifts of silk and pearls, averting war through fair words."},
    {"filename": "57-veruvantha-seyyaamai/29-n29_forgiving_minor_infraction.jpg",
     "title": "Kural 566: Royal magistrate dismissing a minor petty claim",
     "prompt": "Photorealistic 16:9 cinematic film still, village mandapam, magistrate smiling and counseling two quarreling fruit sellers, advising reconciliation rather than fines."},
    {"filename": "57-veruvantha-seyyaamai/30-n30_calm_evening_reflection.jpg",
     "title": "Kural 566: King walking quietly through palace gardens at dusk",
     "prompt": "Photorealistic 16:9 cinematic film still, lotus pond in palace courtyard at dusk, king in white silk walking slowly in deep contemplation, evening breeze rustling palm fronds."},

    # Kural 567: Cruel minister and extortion dries land like drought
    {"filename": "57-veruvantha-seyyaamai/31-n31_just_tax_officer_fair_records.jpg",
     "title": "Kural 567: Honest revenue officer assessing fair standard levy",
     "prompt": "Photorealistic 16:9 cinematic film still, village granary courtyard, state officer checking paddy measures fairly with wooden grain vessel (marakkal), recording transparently on palm leaf."},
    {"filename": "57-veruvantha-seyyaamai/32-n32_tax_remission_dry_season.jpg",
     "title": "Kural 567: Granting complete tax remission during dry year",
     "prompt": "Photorealistic 16:9 cinematic film still, sunlit village assembly, royal herald reading an official copper plate proclaiming full tax waiver and seed grain distribution for farmers."},
    {"filename": "57-veruvantha-seyyaamai/33-n33_opening_royal_grain_reserves.jpg",
     "title": "Kural 567: King opening royal granaries during lean months",
     "prompt": "Photorealistic 16:9 cinematic film still, massive stone state granary doors swung open, cartloads of golden paddy being loaded for distribution to needy villages."},
    {"filename": "57-veruvantha-seyyaamai/34-n34_community_relief_kitchen.jpg",
     "title": "Kural 567: Hot food served to all at community kitchen",
     "prompt": "Photorealistic 16:9 cinematic film still, shaded temple dining hall, compassionate volunteers serving steaming hot rice and dal on banana leaves to smiling mothers and children."},
    {"filename": "57-veruvantha-seyyaamai/35-n35_replenishing_farmer_seed_stocks.jpg",
     "title": "Kural 567: Distributing certified seed paddy to plowmen",
     "prompt": "Photorealistic 16:9 cinematic film still, agricultural depot, farmers receiving bags of healthy seed grain from state agronomists for next monsoon sowing season."},

    # Kural 568: Oppressive extortion is worse than forest highwaymen
    {"filename": "57-veruvantha-seyyaamai/36-n36_transparent_treasury_audit.jpg",
     "title": "Kural 568: Open public accounting of treasury receipts",
     "prompt": "Photorealistic 16:9 cinematic film still, stone pavilion in public square, royal auditors displaying accounts and expenditure breakdowns to town elders, total civic trust."},
    {"filename": "57-veruvantha-seyyaamai/37-n37_happy_villagers_paying_due.jpg",
     "title": "Kural 568: Villagers happily contributing reasonable share",
     "prompt": "Photorealistic 16:9 cinematic film still, threshing floor at harvest, prosperous farmers willingly offering the traditional one-sixth share of grain to state collectors with joyous smiles."},
    {"filename": "57-veruvantha-seyyaamai/38-n38_safe_highways_patrolled.jpg",
     "title": "Kural 568: Highway patrolled by trusted royal guards",
     "prompt": "Photorealistic 16:9 cinematic film still, wide tree-lined ancient trade road, merchant ox-carts traveling safely accompanied by courteous royal cavalry escorts."},
    {"filename": "57-veruvantha-seyyaamai/39-n39_rest_houses_for_wayfarers.jpg",
     "title": "Kural 568: Roadside inn providing clean water and shelter",
     "prompt": "Photorealistic 16:9 cinematic film still, stone wayside choultry with freshwater well, weary travelers and merchants resting comfortably under terracotta tile roof."},
    {"filename": "57-veruvantha-seyyaamai/40-n40_trade_caravans_moving_freely.jpg",
     "title": "Kural 568: Rich trade caravans moving securely across realm",
     "prompt": "Photorealistic 16:9 cinematic wide shot, caravan of laden bullock carts and pack horses crossing an arched stone bridge over a sparkling river at sunrise."},

    # Kural 569: Fortress of fear becomes ruler's own prison
    {"filename": "57-veruvantha-seyyaamai/41-n41_gates_open_to_peaceful_commerce.jpg",
     "title": "Kural 569: City gates wide open to traders and scholars",
     "prompt": "Photorealistic 16:9 cinematic film still, majestic ancient city gateway with banners fluttering, peaceful citizens, poets, and foreign merchants walking in and out freely."},
    {"filename": "57-veruvantha-seyyaamai/42-n42_king_walking_unguarded_in_town.jpg",
     "title": "Kural 569: Righteous king walking without guards among people",
     "prompt": "Photorealistic 16:9 cinematic film still, bustling morning street market, the king dressed simply walking calmly among vendors, laughing with an old flower seller, total mutual love."},
    {"filename": "57-veruvantha-seyyaamai/43-n43_gathering_at_temple_pond.jpg",
     "title": "Kural 569: Women and families relaxing at temple tank",
     "prompt": "Photorealistic 16:9 cinematic film still, broad stone steps of an ancient temple tank filled with blooming pink lotuses, families bathing and talking peacefully in morning light."},
    {"filename": "57-veruvantha-seyyaamai/44-n44_trusting_night_watch.jpg",
     "title": "Kural 569: Peaceful nighttime streets guarded by goodwill",
     "prompt": "Photorealistic 16:9 cinematic film still, moonlit street with stone houses, friendly night watchman carrying oil lamp nodding warmly to a resident looking from a balcony."},
    {"filename": "57-veruvantha-seyyaamai/45-n45_monarch_sitting_with_scholars.jpg",
     "title": "Kural 569: King sitting on simple mat with village schoolmasters",
     "prompt": "Photorealistic 16:9 cinematic film still, open school hall, the king seated on a palm mat discussing education with village teachers, humility and mutual respect."},

    # Kural 570: Gentle rule brings timely rains and boundless prosperity
    {"filename": "57-veruvantha-seyyaamai/46-n46_dark_monsoon_rain_clouds.jpg",
     "title": "Kural 570: Benevolent dark monsoon clouds gathering over fields",
     "prompt": "Photorealistic 16:9 cinematic wide shot, dramatic deep indigo monsoon rain clouds rolling over emerald green paddy plains, cool wind bending coconut palms, promise of life."},
    {"filename": "57-veruvantha-seyyaamai/47-n47_refreshing_rains_filling_tanks.jpg",
     "title": "Kural 570: Life-giving rain pouring down on temple reservoir",
     "prompt": "Photorealistic 16:9 cinematic film still, silver rain falling over an ancient stone temple tank, concentric ripples on water surface, children dancing in rain on stone steps."},
    {"filename": "57-veruvantha-seyyaamai/48-n48_bumper_paddy_harvest.jpg",
     "title": "Kural 570: Golden heavy paddy sheaves being gathered",
     "prompt": "Photorealistic 16:9 cinematic film still, expansive sunlit field of ripe golden paddy, Tamil farm women and men singing while harvesting with iron sickles, abundance everywhere."},
    {"filename": "57-veruvantha-seyyaamai/49-n49_joyful_harvest_celebration.jpg",
     "title": "Kural 570: Joyous Pongal harvest festival in village",
     "prompt": "Photorealistic 16:9 cinematic film still, village green decorated with kolam rangoli, clay pots boiling over with fresh milk and sweet rice, sugarcane stalks, festive drumming."},
    {"filename": "57-veruvantha-seyyaamai/50-n50_prosperous_homeland_golden_hour.jpg",
     "title": "Kural 570: Climax: The flourishing righteous Tamil kingdom",
     "prompt": "Photorealistic 16:9 cinematic panoramic vista, ancient Tamil country bathed in glorious golden sunset light, rivers, temples, villages, and mountains thriving in harmonious peace."}
]

# 40 shots for Chapter 61 (Madiyinmai: 249.00s -> 6.23s/shot)
CH61_PROMPTS = [
    # Kural 601: Sloth extinguishes the noble flame of family
    {"filename": "61-madiyinmai/01-n01_flickering_lamp_neglected_house.jpg",
     "title": "Kural 601: Parable of neglected ancestral lamp flickering",
     "prompt": "Photorealistic 16:9 cinematic film still, ancestral teak hall with dust motes and unpolished brass, a faint single lamp flame struggling against shadows, cautionary moral atmosphere."},
    {"filename": "61-madiyinmai/02-n02_youth_waking_and_polishing_lamp.jpg",
     "title": "Kural 601: Industrious youth polishing bright brass lamp",
     "prompt": "Photorealistic 16:9 cinematic film still, courtyard at early dawn, an earnest young Tamil youth vigorously polishing a tall multi-tiered brass oil lamp until it gleams like gold."},
    {"filename": "61-madiyinmai/03-n03_bright_flame_ignited_ancestral_hall.jpg",
     "title": "Kural 601: Bright steady flame re-illuminating the house",
     "prompt": "Photorealistic 16:9 cinematic film still, grand pillared hall glowing with warm golden light from freshly lit oil lamps, dispelling all gloom, revival of family glory."},
    {"filename": "61-madiyinmai/04-n04_honoring_ancestral_lineage_scrolls.jpg",
     "title": "Kural 601: Youth preserving lineage palm-leaf records",
     "prompt": "Photorealistic 16:9 cinematic close-up, young craftsman reverently applying fragrant herbal oil to ancestral palm leaves, preserving hereditary knowledge with devotion."},

    # Kural 602: Treat sloth as sloth if you desire your line to rise
    {"filename": "61-madiyinmai/05-n05_artisan_rising_before_dawn.jpg",
     "title": "Kural 602: Young artisan rising while stars still shine",
     "prompt": "Photorealistic 16:9 cinematic film still, village stone veranda under twilight indigo sky with morning star shining, a disciplined young carpenter splashing cold well water on his face to begin work."},
    {"filename": "61-madiyinmai/06-n06_father_son_crafting_wheel.jpg",
     "title": "Kural 602: Father and son shaping heavy teak chariot wheel",
     "prompt": "Photorealistic 16:9 cinematic film still, open-air workshop, master woodworker and his son using curved adze and mallet on a massive wooden wheel rim, wood shavings flying in dawn light."},
    {"filename": "61-madiyinmai/07-n07_apprentice_practicing_sculpture.jpg",
     "title": "Kural 602: Diligent apprentice chiseling granite at daybreak",
     "prompt": "Photorealistic 16:9 cinematic film still, stone yard, young apprentice practicing delicate chisel strikes on granite block under early morning sunbeams, determined intense eyes."},
    {"filename": "61-madiyinmai/08-n08_rapid_growth_of_family_enterprise.jpg",
     "title": "Kural 602: Prosperous bustling workshop filled with orders",
     "prompt": "Photorealistic 16:9 cinematic film still, large thriving artisan guildhall with multiple craftsmen carving, polishing, and assembling fine furniture, energetic purpose."},

    # Kural 603: The fool nurturing sloth ruins his own house
    {"filename": "61-madiyinmai/09-n09_overgrown_field_broken_plow.jpg",
     "title": "Kural 603: Parable of an untended field overgrown with thorns",
     "prompt": "Photorealistic 16:9 cinematic film still, dry neglected field with weeds and an abandoned weathered wooden plow, somber warning of laziness."},
    {"filename": "61-madiyinmai/10-n10_energetic_farmer_clearing_brambles.jpg",
     "title": "Kural 603: Determined farmer clearing brambles with iron hoe",
     "prompt": "Photorealistic 16:9 cinematic film still, morning hillside, a vigorous muscular Tamil farmer swinging a heavy iron hoe to clear thick weeds, sweat shining on shoulders, willpower."},
    {"filename": "61-madiyinmai/11-n11_tilling_rich_black_soil.jpg",
     "title": "Kural 603: Two strong bullocks tilling neat dark furrows",
     "prompt": "Photorealistic 16:9 cinematic film still, expansive field, pair of white Kangayam humped bulls pulling a wooden plow through fertile moist dark loam, early morning golden light."},
    {"filename": "61-madiyinmai/12-n12_green_shoots_rising_from_earth.jpg",
     "title": "Kural 603: Vibrant young green paddy shoots emerging",
     "prompt": "Photorealistic 16:9 cinematic close-up, dew-kissed emerald green paddy sprouts rising from rich wet soil, morning sunbeam sparkling in water droplets."},

    # Kural 604: Sloth destroys ambition even in noble-born
    {"filename": "61-madiyinmai/13-n13_blacksmith_heating_iron.jpg",
     "title": "Kural 604: Blacksmith stoking roaring charcoal forge",
     "prompt": "Photorealistic 16:9 cinematic film still, stone smithy, blacksmith pumping leather bellows to heat iron bar to brilliant incandescent orange, embers glowing in darkness."},
    {"filename": "61-madiyinmai/14-n14_striking_red_hot_steel.jpg",
     "title": "Kural 604: Hammer striking glowing steel with sparks",
     "prompt": "Photorealistic 16:9 cinematic dynamic action shot, blacksmith bringing down heavy hammer on glowing red steel anvil, exploding shower of brilliant golden sparks, raw industrious energy."},
    {"filename": "61-madiyinmai/15-n15_forging_durable_plowshares.jpg",
     "title": "Kural 604: Row of finished sharp iron plowshares cooling",
     "prompt": "Photorealistic 16:9 cinematic film still, stone floor lined with sharp gleaming iron plow blades, ready for cultivation, fruit of relentless physical exertion."},
    {"filename": "61-madiyinmai/16-n16_pride_of_honest_craftsmanship.jpg",
     "title": "Kural 604: Master smith wiping brow with pride of work",
     "prompt": "Photorealistic 16:9 cinematic close-up, veteran blacksmith smiling with satisfaction, wipe cloth in hand, looking at completed tools, nobility of labor."},

    # Kural 605: Delay, forgetfulness, sloth, excess sleep: ruin's boats
    {"filename": "61-madiyinmai/17-n17_rooster_crowing_first_light.jpg",
     "title": "Kural 605: Dawn breaks over village with first rooster call",
     "prompt": "Photorealistic 16:9 cinematic film still, thatched village rooftop against dramatic pre-dawn sky glowing orange and violet, rooster crowing on stone wall, awakening energy."},
    {"filename": "61-madiyinmai/18-n18_fishermen_launching_catamaran.jpg",
     "title": "Kural 605: Fishermen pushing log catamaran through surf",
     "prompt": "Photorealistic 16:9 cinematic film still, sandy beach at dawn, team of muscular Tamil fishermen waist-deep in foaming surf launching heavy wooden log boat into morning waves."},
    {"filename": "61-madiyinmai/19-n19_bustling_seaside_catch_market.jpg",
     "title": "Kural 605: Vibrant morning fish market on shore",
     "prompt": "Photorealistic 16:9 cinematic film still, sunlit coastal market, woven baskets brimming with shimmering silver fish, brisk joyful trade between fishermen and buyers."},
    {"filename": "61-madiyinmai/20-n20_brisk_morning_activity_village.jpg",
     "title": "Kural 605: Village street alive with early morning purpose",
     "prompt": "Photorealistic 16:9 cinematic film still, paved village avenue at sunrise, women drawing white rice-flour kolams, milkmen walking cattle, brisk healthy industry."},

    # Kural 606: Even kings of wide empires lose if sluggish
    {"filename": "61-madiyinmai/21-n21_king_working_late_by_lamp.jpg",
     "title": "Kural 606: King examining petitions late into the night",
     "prompt": "Photorealistic 16:9 cinematic film still, quiet palace study, an unwearied king seated with scholars reading state papers by heavy oil lamp, refusing idle slumber."},
    {"filename": "61-madiyinmai/22-n22_inspecting_cavalry_at_dawn.jpg",
     "title": "Kural 606: Commander inspecting cavalry lines before sunrise",
     "prompt": "Photorealistic 16:9 cinematic film still, misty military camp at first light, commander on horseback inspecting alert cavalrymen grooming horses, discipline and readiness."},
    {"filename": "61-madiyinmai/23-n23_dispatching_fast_messengers.jpg",
     "title": "Kural 606: Royal courier leaping onto swift horse",
     "prompt": "Photorealistic 16:9 cinematic action shot, palace gate, athletic royal messenger grasping leather satchel and springing onto galloping steed, urgent dispatch without delay."},
    {"filename": "61-madiyinmai/24-n24_monarch_visiting_public_works.jpg",
     "title": "Kural 606: King on foot inspecting canal construction",
     "prompt": "Photorealistic 16:9 cinematic film still, muddy riverbank, the king standing directly with stone masons and workers inspecting newly placed foundation blocks."},

    # Kural 607: Slothful receive reproaches; active earn honor
    {"filename": "61-madiyinmai/25-n25_master_weaver_correcting_apprentice.jpg",
     "title": "Kural 607: Master weaver teaching student unflagging care",
     "prompt": "Photorealistic 16:9 cinematic film still, wooden handloom workshop, senior weaver guiding hands of young apprentice to fix broken thread, instilling diligence."},
    {"filename": "61-madiyinmai/26-n26_bustling_handloom_hall.jpg",
     "title": "Kural 607: Dozen looms clicking in synchronous rhythm",
     "prompt": "Photorealistic 16:9 cinematic wide shot, spacious artisan weaving shed filled with natural sunlight, dozens of wooden looms moving in brisk harmonious motion."},
    {"filename": "61-madiyinmai/27-n27_inspecting_finished_golden_silk.jpg",
     "title": "Kural 607: Quality inspection of exquisite silk sari",
     "prompt": "Photorealistic 16:9 cinematic film still, merchants holding up lengths of brilliant crimson and gold-brocaded silk fabric, catching sunlight, triumph of industry."},
    {"filename": "61-madiyinmai/28-n28_merchant_guild_assembly.jpg",
     "title": "Kural 607: Trade guild honoring most hardworking member",
     "prompt": "Photorealistic 16:9 cinematic film still, stone guildhall, respected merchant leaders garlanding an energetic young trader for exemplary enterprise and honesty."},

    # Kural 608: Sloth makes an ancient family servant to enemies
    {"filename": "61-madiyinmai/29-n29_stonemasons_lifting_massive_beam.jpg",
     "title": "Kural 608: United stonemasons hoisting monolithic temple lintel",
     "prompt": "Photorealistic 16:9 cinematic dynamic shot, temple construction site, team of muscular Tamil stonecutters using wooden levers, rollers, and ropes to heave a 10-ton granite beam into place."},
    {"filename": "61-madiyinmai/30-n30_carving_towering_gopuram.jpg",
     "title": "Kural 608: Sculptors working on high wooden scaffolding",
     "prompt": "Photorealistic 16:9 cinematic film still, rising temple gopuram wrapped in bamboo scaffolding, artisans at great height chiseling intricate celestial figures against blue sky."},
    {"filename": "61-madiyinmai/31-n31_tireless_cooperation_in_labor.jpg",
     "title": "Kural 608: Team of workers passing clay bricks hand to hand",
     "prompt": "Photorealistic 16:9 cinematic film still, building rampart, long human chain of smiling energetic workers passing sun-baked bricks rhythmically in morning light."},
    {"filename": "61-madiyinmai/32-n32_magnificent_temple_rising.jpg",
     "title": "Kural 608: Majestic granite vimana tower nearing completion",
     "prompt": "Photorealistic 16:9 cinematic sweeping wide shot, towering granite temple tower gleaming in midday sun, testament to years of unceasing united human labor."},

    # Kural 609: Sloth discarded restores lost hereditary glory
    {"filename": "61-madiyinmai/33-n33_merchant_ships_returning_port.jpg",
     "title": "Kural 609: High-masted trading ships entering harbour laden with wealth",
     "prompt": "Photorealistic 16:9 cinematic wide shot, ancient seaport of Kaveripumpattinam, tall wooden merchant ships with billowing white sails sailing into calm stone wharves, rich cargo."},
    {"filename": "61-madiyinmai/34-n34_unloading_precious_cargo.jpg",
     "title": "Kural 609: Sailors unloading chests of silk, gems, and camphor",
     "prompt": "Photorealistic 16:9 cinematic film still, busy dockside, sturdy sailors hauling heavy brass-bound chests and aromatic spice crates ashore, bustling prosperous harbor."},
    {"filename": "61-madiyinmai/35-n35_rebuilding_ancestral_estate.jpg",
     "title": "Kural 609: Carpenters and masons renovating ancient family manor",
     "prompt": "Photorealistic 16:9 cinematic film still, grand traditional courtyarded home being renovated with fresh carved teak pillars and new terracotta roof tiles, rebirth of glory."},
    {"filename": "61-madiyinmai/36-n36_family_reunion_in_abundance.jpg",
     "title": "Kural 609: Joyful family gathering on renovated porch",
     "prompt": "Photorealistic 16:9 cinematic film still, sunlit veranda, three generations of an upright family seated together on carved benches, laughing and celebrating restored fortunes."},

    # Kural 610: The energetic person who conquers sloth steps over the world
    {"filename": "61-madiyinmai/37-n37_heroic_stride_at_dawn.jpg",
     "title": "Kural 610: Energetic leader walking purposefully at dawn",
     "prompt": "Photorealistic 16:9 cinematic film still, mountain trail, an athletic ancient Tamil leader or industrious pioneer striding forward with unwavering confidence into morning light."},
    {"filename": "61-madiyinmai/38-n38_standing_on_mountain_ridge.jpg",
     "title": "Kural 610: Overlooking endless cultivated green plains",
     "prompt": "Photorealistic 16:9 cinematic sweeping shot, panoramic view from high rocky ridge, a solitary visionary standing tall gazing at thousands of flourishing green farms and sparkling canals below."},
    {"filename": "61-madiyinmai/39-n39_sunrise_golden_glory.jpg",
     "title": "Kural 610: Brilliant morning sun breaking through clouds",
     "prompt": "Photorealistic 16:9 cinematic majestic landscape, golden sunrise rays bursting through mountain peaks, bathing ancient Tamil land in transcendent golden brilliance."},
    {"filename": "61-madiyinmai/40-n40_triumph_of_unceasing_exertion.jpg",
     "title": "Kural 610: Climax: The boundless victory of human diligence",
     "prompt": "Photorealistic 16:9 cinematic film still, thriving Sangam civilization with bustling cities, fertile fields, tranquil temples, and joyful hardworking citizens living in noble dignity."}
]

def build_notebook():
    total_images = len(CH54_PROMPTS) + len(CH57_PROMPTS) + len(CH61_PROMPTS)
    print(f"Total Thirukkural film shots to generate: {total_images} (Ch54: {len(CH54_PROMPTS)}, Ch57: {len(CH57_PROMPTS)}, Ch61: {len(CH61_PROMPTS)})")

    cells = []

    # Cell 0: Badge
    cells.append({
        "cell_type": "markdown",
        "metadata": {"id": "view-in-github"},
        "source": [
            '<a href="https://colab.research.google.com/github/shishyan/GuruKulaDesam/blob/main/colab_generate_gurukulam_artworks.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>\n'
        ]
    })

    # Cell 1: Intro Markdown
    cells.append({
        "cell_type": "markdown",
        "metadata": {"id": "intro_md"},
        "source": [
            "# 🎨 குரு குல தேசம் (Guru Kula Desam) — Master Film Visual Suite Generator\n",
            "### Dedicated GPU Colab Server for A100 GPU (40GB / 80GB VRAM)\n",
            "\n",
            "This notebook is optimized for **A100 GPU** to produce the entire remaining **136 cinematic artworks** across:\n",
            "- **Chapter 54 (*பொச்சாவாமை - Pochchaavaamai*)**: 46 verse-specific shots (6.94s pacing)\n",
            "- **Chapter 57 (*வெருவந்த செய்யாமை - Veruvantha Seyyaamai*)**: 50 verse-specific shots (6.83s pacing)\n",
            "- **Chapter 61 (*மடியின்மை - Madiyinmai*)**: 40 verse-specific shots (6.23s pacing)\n",
            "\n",
            "### Recommended Image Generator for A100: **FLUX.1-schnell** (Black Forest Labs)\n",
            "1. **State of the Art Quality**: 12-billion parameter flow-matching transformer — currently the #1 open model in the world.\n",
            "2. **Native 16:9 Widescreen**: Generates pristine `1280x720` cinematic film stills without cropping.\n",
            "3. **Speed on A100**: Only **4 steps (~1.5 to 2.5 seconds per 720p image)**. All 136 images complete in **~5 minutes**!\n",
            "4. **Alternative**: You can also switch `ENGINE = 'SDXL-Lightning'` for instant 4-step SDXL.\n",
            "\n",
            "👉 **How to Run**: Simply click **Runtime -> Run all** (or run cells Step 1 to Step 5 sequentially)."
        ]
    })

    # Cell 2: Step 1: Install packages
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"id": "step1_install"},
        "outputs": [],
        "source": [
            "# Step 1: Install high-performance generation libraries\n",
            "!pip install -q diffusers transformers accelerate safetensors sentencepiece protobuf torch torchvision\n",
            "\n",
            "import torch\n",
            "print('PyTorch Version:', torch.__version__)\n",
            "if torch.cuda.is_available():\n",
            "    device_name = torch.cuda.get_device_name(0)\n",
            "    vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9\n",
            "    print(f'✅ GPU Detected: {device_name} ({vram_gb:.2f} GB VRAM)')\n",
            "    if 'A100' in device_name:\n",
            "        print('🚀 Optimal A100 GPU active! Full bfloat16 FLUX.1 acceleration enabled.')\n",
            "else:\n",
            "    print('⚠️ WARNING: No GPU detected! Please go to Runtime -> Change runtime type -> Select A100 or T4 GPU.')\n"
        ]
    })

    # Cell 3: Step 2: Initialize Model Pipeline
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"id": "step2_load_pipeline"},
        "outputs": [],
        "source": [
            "# Step 2: Initialize Engine (FLUX.1-schnell or SDXL-Lightning)\n",
            "# Choose your preferred engine below:\n",
            "ENGINE = 'FLUX-schnell'  # Options: 'FLUX-schnell' (Best for A100, 4 steps) or 'SDXL-Lightning'\n",
            "\n",
            "import torch\n",
            "pipe = None\n",
            "\n",
            "if ENGINE == 'FLUX-schnell':\n",
            "    print('⏳ Loading FLUX.1-schnell (12B Flow Transformer in bfloat16)...')\n",
            "    from diffusers import FluxPipeline\n",
            "    pipe = FluxPipeline.from_pretrained(\n",
            "        'black-forest-labs/FLUX.1-schnell',\n",
            "        torch_dtype=torch.bfloat16\n",
            "    )\n",
            "    pipe.to('cuda')\n",
            "    print('✅ FLUX.1-schnell loaded and ready on A100 GPU!')\n",
            "else:\n",
            "    print('⏳ Loading SDXL-Lightning 4-step Pipeline...')\n",
            "    from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler\n",
            "    from huggingface_hub import hf_hub_download\n",
            "    from safetensors.torch import load_file\n",
            "\n",
            "    base = 'stabilityai/stable-diffusion-xl-base-1.0'\n",
            "    repo = 'ByteDance/SDXL-Lightning'\n",
            "    ckpt = 'sdxl_lightning_4step_unet.safetensors'\n",
            "    unet = UNet2DConditionModel.from_config(base, subfolder='unet').to('cuda', torch.float16)\n",
            "    unet.load_state_dict(load_file(hf_hub_download(repo, ckpt), device='cuda'))\n",
            "    pipe = StableDiffusionXLPipeline.from_pretrained(\n",
            "        base, unet=unet, torch_dtype=torch.float16, variant='fp16'\n",
            "    ).to('cuda')\n",
            "    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing='trailing')\n",
            "    print('✅ SDXL-Lightning loaded and ready!')\n"
        ]
    })

    # Cell 4: Step 3: Thirukkural Visual Generation (136 shots)
    tasks_json = json.dumps(CH54_PROMPTS + CH57_PROMPTS + CH61_PROMPTS, indent=4, ensure_ascii=False)
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"id": "step3_generate_all"},
        "outputs": [],
        "source": [
            f"# Step 3: Generate the Full 136-Shot Master Suite (Chapters 54, 57, 61)\n",
            "import os, time\n",
            "from PIL import Image\n",
            "\n",
            f"tasks = {tasks_json}\n",
            "\n",
            "base_out_dir = 'production/visuals/thirukkural'\n",
            "print(f'🚀 Starting batch generation of {len(tasks)} cinematic master artworks...')\n",
            "start_time = time.time()\n",
            "\n",
            "for idx, task in enumerate(tasks, 1):\n",
            "    out_path = os.path.join(base_out_dir, task['filename'])\n",
            "    os.makedirs(os.path.dirname(out_path), exist_ok=True)\n",
            "\n",
            "    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:\n",
            "        print(f'[{idx}/{len(tasks)}] Already exists, skipping: {task[\"filename\"]}')\n",
            "        continue\n",
            "\n",
            "    t0 = time.time()\n",
            "    prompt = task['prompt']\n",
            "    print(f'\\n[{idx}/{len(tasks)}] Generating: {task[\"title\"]} -> {task[\"filename\"]}')\n",
            "\n",
            "    if ENGINE == 'FLUX-schnell':\n",
            "        image = pipe(\n",
            "            prompt=prompt,\n",
            "            width=1280,\n",
            "            height=720,\n",
            "            num_inference_steps=4,\n",
            "            max_sequence_length=256\n",
            "        ).images[0]\n",
            "    else:\n",
            "        image = pipe(\n",
            "            prompt=prompt,\n",
            "            negative_prompt='modern elements, distorted limbs, blurry, text, watermark, bad anatomy, pink tint',\n",
            "            num_inference_steps=4,\n",
            "            guidance_scale=0.0,\n",
            "            width=1280,\n",
            "            height=720\n",
            "        ).images[0]\n",
            "\n",
            "    image.save(out_path, 'JPEG', quality=95)\n",
            "    elapsed = time.time() - t0\n",
            "    print(f'  ✅ Saved ({elapsed:.2f}s): {out_path}')\n",
            "\n",
            "total_elapsed = time.time() - start_time\n",
            "print(f'\\n🎉 All {len(tasks)} master film artworks generated successfully in {total_elapsed/60:.2f} minutes!')\n"
        ]
    })

    # Cell 5: Step 4: Zip and Download
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"id": "step4_zip_download"},
        "outputs": [],
        "source": [
            "# Step 4: Package Master Artworks into Zip and Download\n",
            "import os, zipfile\n",
            "from google.colab import files\n",
            "\n",
            "zip_filename = 'gurukuladesam_master_artworks.zip'\n",
            "print(f'📦 Packaging production visuals into {zip_filename}...')\n",
            "\n",
            "with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:\n",
            "    for root, dirs, filenames in os.walk('production/visuals/thirukkural'):\n",
            "        for fn in filenames:\n",
            "            if fn.endswith(('.jpg', '.png')):\n",
            "                full_path = os.path.join(root, fn)\n",
            "                arcname = os.path.relpath(full_path, '.')\n",
            "                zipf.write(full_path, arcname)\n",
            "\n",
            "size_mb = os.path.getsize(zip_filename) / (1024 * 1024)\n",
            "print(f'✅ Archive created: {zip_filename} ({size_mb:.2f} MB)')\n",
            "print('⬇ Triggering automatic download to your local machine...')\n",
            "files.download(zip_filename)\n"
        ]
    })

    nb = {
        "cells": cells,
        "metadata": {
            "colab": {
                "provenance": [],
                "toc_visible": True
            },
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            },
            "accelerator": "GPU"
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }

    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    print(f"Updated {NOTEBOOK_PATH} with {len(cells)} cells and all {total_images} shot prompts!")

if __name__ == "__main__":
    build_notebook()
