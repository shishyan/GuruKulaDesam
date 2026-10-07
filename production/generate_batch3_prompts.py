# -*- coding: utf-8 -*-
"""
Batch 3 Prompt Definitions: Chapters 39, 40, 42, 44, 45, 46 (Total: 268 shots)
Option A: Statecraft & Political Wisdom Suite
"""

import json
from pathlib import Path

# Chapter 39: இறைமாட்சி (Iraimaatchi - Sovereign Majesty / Royal Excellence) - 37 shots
# Kurals 381 to 390
CH39_PROMPTS = [
    # Kural 381: Sixfold limbs of state (army, people, wealth, ministers, allies, fortress)
    ("39-iraimaatchi/01-n01_six_limbs_of_sovereignty.jpg", "Kural 381: The six pillars of sovereign majesty",
     "Photorealistic 16:9 cinematic film still, majestic ancient Tamil royal court, a crowned Chola monarch enthroned on a carved granite lion throne, flanked by ministers, treasury overseers, commanders, and allied envoys, warm sunlight streaming between tall granite pillars."),
    ("39-iraimaatchi/02-n02_mighty_army_disciplined_ranks.jpg", "Kural 381: Disciplined ranks of the royal army (Padai)",
     "Photorealistic 16:9 cinematic wide shot, vast open training field outside fortress walls, thousands of ancient Tamil infantry with bronze-tipped spears and wicker shields marching in perfect unison at dawn, dust glowing golden."),
    ("39-iraimaatchi/03-n03_thriving_citizenry_in_homeland.jpg", "Kural 381: Prosperous and contented citizens (Kudi)",
     "Photorealistic 16:9 cinematic film still, bustling village market and smiling families trading fresh produce, weavers at looms, children playing safely, peaceful domestic flourishing."),
    ("39-iraimaatchi/04-n04_abundant_treasury_granaries.jpg", "Kural 381: Bountiful state treasury and granaries (Koozh)",
     "Photorealistic 16:9 cinematic shot, massive royal stone storehouse with towering stacks of golden grain sacks and sealed clay jars of fragrant sesame oil and honey, treasury guards in background."),

    # Kural 382: Four virtues of a king (courage, liberality, wisdom, enterprise)
    ("39-iraimaatchi/05-n05_lion_hearted_courage_in_battle.jpg", "Kural 382: Lion-hearted courage in defending the realm",
     "Photorealistic 16:9 cinematic film still, high rampart during distant siege, the crowned monarch standing fearless with hand resting on the hilt of his curved iron sword, banner fluttering in storm wind."),
    ("39-iraimaatchi/06-n06_generous_liberality_to_poets.jpg", "Kural 382: Royal bounty showered upon poets and the destitute",
     "Photorealistic 16:9 cinematic film still, open audience pavilion, monarch placing a garland of pure gold flowers and a fine silk shawl over the shoulders of a humble Sangam bard holding a wooden yazh harp."),
    ("39-iraimaatchi/07-n07_penetrating_wisdom_in_counsel.jpg", "Kural 382: Penetrating wisdom deliberating state decrees",
     "Photorealistic 16:9 cinematic film still, royal library by night, monarch reviewing palm-leaf treatises under the warm illumination of a tall multi-tiered bronze lamp with wise elder scholars."),
    ("39-iraimaatchi/08-n08_unceasing_enterprise_at_dawn.jpg", "Kural 382: Unfailing energy rising before the sun",
     "Photorealistic 16:9 cinematic wide shot, palace balcony at dawn, monarch already active, dispatching fast royal messengers on swift horseback to frontier outposts, morning mist over city."),

    # Kural 383: Three essentials (vigilance, learning, daring resolve)
    ("39-iraimaatchi/09-n09_night_vigil_over_the_realm.jpg", "Kural 383: Untiring vigilance keeping watch over sleeping kingdom",
     "Photorealistic 16:9 cinematic film still, palace watchtower terrace at midnight, monarch standing silent under starry sky, gazing out over thousands of peaceful torchlit homes below."),
    ("39-iraimaatchi/10-n10_deep_study_of_ethical_treatises.jpg", "Kural 383: Lifelong dedication to sacred learning",
     "Photorealistic 16:9 cinematic shot, monarch seated in quiet stone alcove, carefully tracing ancient Tamil Brahmi characters on an oiled palm leaf with an iron stylus, scholar mentor seated nearby."),
    ("39-iraimaatchi/11-n11_daring_resolve_in_crisis.jpg", "Kural 383: Decisive daring in times of national trial",
     "Photorealistic 16:9 cinematic dramatic shot, war council room, monarch decisively placing the royal emblem seal upon a treaty scroll, bold resolute posture, ministers nodding in admiration."),

    # Kural 384: Never swerving from virtue, repressing vice, maintaining royal honor
    ("39-iraimaatchi/12-n12_unswerving_path_of_righteousness.jpg", "Kural 384: Walking the unwavering path of dharma",
     "Photorealistic 16:9 cinematic wide shot, royal temple path lined with carved granite pillars, monarch walking barefoot with folded palms toward the sacred sanctum, humble piety."),
    ("39-iraimaatchi/13-n13_impartial_curbing_of_injustice.jpg", "Kural 384: Firm suppression of wrongdoing and oppression",
     "Photorealistic 16:9 cinematic film still, royal judgment courtyard, monarch ordering corrupt bailiffs to return extorted grain to poor farmers, stern unbending justice."),
    ("39-iraimaatchi/14-n14_spotless_reputation_of_the_crown.jpg", "Kural 384: Royal dignity that knows no blemish",
     "Photorealistic 16:9 cinematic portrait, close-up of the noble monarch with serene upright expression, golden crown adorned with pearl strings, eyes reflecting integrity and selfless duty."),

    # Kural 385: Able to acquire wealth, store it safely, guard it, and distribute it wisely
    ("39-iraimaatchi/15-n15_fostering_oceanic_commerce.jpg", "Kural 385: Expanding legitimate state revenues through maritime trade",
     "Photorealistic 16:9 cinematic wide shot, bustling ancient port of Poompuhar, wooden merchant ships unloading silk, horses, and spices, royal customs officers measuring grain and gold."),
    ("39-iraimaatchi/16-n16_secure_state_treasury_vaults.jpg", "Kural 385: Secure preservation of accumulated wealth",
     "Photorealistic 16:9 cinematic film still, deep subterranean stone vault, heavy iron-banded timber chests storing bullion and gemstones, guarded by steadfast sentries with oil lamps."),
    ("39-iraimaatchi/17-n17_protecting_resources_from_predators.jpg", "Kural 385: Guarding national wealth from waste and theft",
     "Photorealistic 16:9 cinematic shot, royal auditor comparing village revenue tallies on palm-leaf rolls, verifying wax seals on grain storehouses with meticulous vigilance."),
    ("39-iraimaatchi/18-n18_wise_expenditure_on_public_works.jpg", "Kural 385: Generous allocation for monumental dams and reservoirs",
     "Photorealistic 16:9 cinematic wide shot, construction of a massive stone check-dam across a roaring river, royal overseers paying silver coins to stonecutters and laborers."),

    # Kural 386: Accessible to all, free from harsh speech; world praises such a sovereign
    ("39-iraimaatchi/19-n19_accessible_audience_to_humble_peasant.jpg", "Kural 386: The king easily accessible to the poorest subject",
     "Photorealistic 16:9 cinematic film still, open garden pavilion, monarch leaning down warmly from his seat to listen directly to an old village woman presenting a grievance, guards standing respectfully back."),
    ("39-iraimaatchi/20-n20_gentle_speech_in_royal_decrees.jpg", "Kural 386: Sweet and dignified royal speech without arrogance",
     "Photorealistic 16:9 cinematic shot, court hall, monarch smiling gently as he announces tax remissions during a dry season, courtiers and citizens beaming with relief."),
    ("39-iraimaatchi/21-n21_world_praising_the_gracious_ruler.jpg", "Kural 386: Universal reverence singing the king's benevolence",
     "Photorealistic 16:9 cinematic wide vista, crowded festival street, citizens waving palm leaves and showering fragrant red blossoms as the royal chariot passes peacefully."),

    # Kural 387: One who gives graciously, protects justly, and speaks kindly rules the entire earth
    ("39-iraimaatchi/22-n22_nourishing_the_famine_stricken.jpg", "Kural 387: Distributing free porridge during seasonal distress",
     "Photorealistic 16:9 cinematic film still, public rest-house, royal officers ladling hot spiced kanji rice porridge into earthen bowls for traveling refugees, monarch inspecting in person."),
    ("39-iraimaatchi/23-n23_shield_of_justice_over_the_weak.jpg", "Kural 387: The protective shield of impartial law",
     "Photorealistic 16:9 cinematic shot, village square, royal magistrate planting the copper plate of royal protection at a village boundary, guaranteeing peace to all residents."),
    ("39-iraimaatchi/24-n24_sovereign_reigning_over_hearts.jpg", "Kural 387: Ruling not by fear, but by the love of the people",
     "Photorealistic 16:9 cinematic portrait, monarch walking through a town street without armed escort, children running up to offer ripe guavas, absolute mutual trust."),

    # Kural 388: One who administers justice strictly according to law is honored as a god among men
    ("39-iraimaatchi/25-n25_golden_scepter_of_upright_rule.jpg", "Kural 388: The straight golden scepter of unbending justice (Sengol)",
     "Photorealistic 16:9 cinematic close-up, monarch's hands holding an ornate golden sengol scepter topped with the sacred bull emblem, bathed in pure morning altar light."),
    ("39-iraimaatchi/26-n26_impartial_verdict_without_favor.jpg", "Kural 388: Delivering justice even against royal kinsmen",
     "Photorealistic 16:9 cinematic film still, supreme court hall, monarch ordering restitution against a wealthy noble who infringed on poor farmers' pasture lands, majesty of law."),
    ("39-iraimaatchi/27-n27_the_divine_stature_of_the_just_king.jpg", "Kural 388: The righteous king venerated like divine providence",
     "Photorealistic 16:9 cinematic grand wide shot, ancient stone temple courtyard at dusk, oil lamps illuminating the monarch standing alongside temple priests and commoners in sacred unity."),

    # Kural 389: The king who bears with the bitter counsel of frank ministers will never fall
    ("39-iraimaatchi/28-n28_patient_hearing_of_bold_counsel.jpg", "Kural 389: Patiently enduring the blunt criticism of an upright minister",
     "Photorealistic 16:9 cinematic film still, private council chamber, a venerable white-bearded minister speaking stern truth to the monarch, the king listening with bowed head and humble reflection."),
    ("39-iraimaatchi/29-n29_honoring_the_fearless_poet.jpg", "Kural 389: Rewarding the poet who dared to reprimand royal error",
     "Photorealistic 16:9 cinematic film still, court terrace, monarch smiling with deep gratitude as he presents a gold coffer to a fearless Tamil poet who spoke unvarnished truth."),
    ("39-iraimaatchi/30-n30_unassailable_dynasty_guided_by_truth.jpg", "Kural 389: An unshakeable realm protected by honest guidance",
     "Photorealistic 16:9 cinematic wide shot, towering granite fortress citadel rising above fertile green river plains at golden hour, glorious enduring strength."),

    # Kural 390: The king who possesses generosity, compassion, justice, and care for subjects is the light among monarchs
    ("39-iraimaatchi/31-n31_fourfold_luster_of_the_ideal_king.jpg", "Kural 390: Generosity, compassion, justice, and ceaseless care",
     "Photorealistic 16:9 cinematic symbolic shot, royal courtyard at sunset, four ceremonial bronze lamps burning bright around the royal throne, glowing in evening mist."),
    ("39-iraimaatchi/32-n32_cradling_the_welfare_of_all_beings.jpg", "Kural 390: Extending royal care to cattle, wildlife, and forests",
     "Photorealistic 16:9 cinematic wide shot, monarch visiting a royal botanical reserve, touching the trunk of a great banyan tree while deer and peacocks wander fearlessly nearby."),
    ("39-iraimaatchi/33-n33_the_beacon_lamp_among_world_rulers.jpg", "Kural 390: A beacon of righteous majesty shining across nations",
     "Photorealistic 16:9 cinematic grand wide shot, high coastal palace terrace overlooking the ocean at sunset, foreign embassies paying homage to the renowned righteous king."),
    ("39-iraimaatchi/34-n34_monumental_irrigation_canal_opening.jpg", "Kural 390: Directing water into thousand dried village fields",
     "Photorealistic 16:9 cinematic wide shot, massive stone sluice gate being raised, sparkling Kaveri river water surging through canals into green parched fields, farmers cheering."),
    ("39-iraimaatchi/35-n35_evening_peace_over_the_realm.jpg", "Kural 390: Tranquil harmony reigning across all seven provinces",
     "Photorealistic 16:9 cinematic panoramic landscape, peaceful Tamil countryside at dusk, temple bells ringing, cattle returning home, smoke rising from village hearths."),
    ("39-iraimaatchi/36-n36_flourishing_arts_and_academy.jpg", "Kural 390: Golden age of Sangam literature under royal patron",
     "Photorealistic 16:9 cinematic film still, grand pillared hall filled with poets, scribes, musicians with harps and flutes, celebrating royal wisdom in golden light."),
    ("39-iraimaatchi/37-n37_eternal_glory_of_the_sengol.jpg", "Kural 390: The immortal glory of the righteous scepter",
     "Photorealistic 16:9 cinematic final shot, golden sengol resting on silk velvet before an ancient bronze Nataraja idol, glowing in steady lamplight, eternal majesty.")
]

# Chapter 40: கல்வி (Kalvi - Sacred Learning / Education) - 59 shots
# Kurals 391 to 400
CH40_PROMPTS = [
    # Kural 391: Learn thoroughly without flaw; then live according to what you have learned
    ("40-kalvi/01-n01_mastering_the_palm_leaf_scroll.jpg", "Kural 391: Deep, rigorous study of sacred texts",
     "Photorealistic 16:9 cinematic film still, ancient gurukulam library, a focused young Tamil scholar diligently reading bound palm-leaf manuscripts by morning light, iron stylus in hand."),
    ("40-kalvi/02-n02_scrutinizing_every_verse_for_truth.jpg", "Kural 391: Flawless comprehension through deep examination",
     "Photorealistic 16:9 cinematic close-up, wrinkled hands of an old guru guiding a student's stylus across etched palmyra leaves, tracing intricate Tamil script with precision."),
    ("40-kalvi/03-n03_walking_the_talk_of_wisdom.jpg", "Kural 391: Embodying learned virtue in daily conduct",
     "Photorealistic 16:9 cinematic film still, village street, an educated youth bowing respectfully to an impoverished elderly worker, translating philosophical learning into living humility."),
    ("40-kalvi/04-n04_dawn_recitation_at_temple_pond.jpg", "Kural 391: Morning chanting of learned verses",
     "Photorealistic 16:9 cinematic wide shot, granite steps of a temple lotus pond at dawn, young students chanting grammar and ethics verses, morning mist swirling on water."),
    ("40-kalvi/05-n05_applying_geometry_in_architecture.jpg", "Kural 391: Applying sacred science to build enduring temples",
     "Photorealistic 16:9 cinematic film still, construction site of a stone temple, an educated architect checking plumb lines and carved stone angles using bronze compasses and cords."),
    ("40-kalvi/06-n06_disciplined_mind_mastering_impulses.jpg", "Kural 391: The calm self-restraint born of true education",
     "Photorealistic 16:9 cinematic portrait, young scholar with serene alert eyes, undisturbed by surrounding market clamor, seated on a stone bench in deep reflection."),

    # Kural 392: Letters and numbers are the two living eyes of mankind
    ("40-kalvi/07-n07_letters_and_numbers_sacred_eyes.jpg", "Kural 392: Letters (En) and Numbers (Ezhuthu) as the twin eyes",
     "Photorealistic 16:9 cinematic macro shot, carved stone slate with ancient Tamil vowels and arithmetic numerical symbols illuminated by a ray of pure morning sunlight."),
    ("40-kalvi/08-n08_teaching_arithmetic_on_sand_board.jpg", "Kural 392: Tracing calculations on a smooth sand bed",
     "Photorealistic 16:9 cinematic film still, shaded outdoor school beneath a banyan tree, teacher using a reed pointer to guide children tracing astronomical calculations in white sand."),
    ("40-kalvi/09-n09_celestial_charts_and_astronomy.jpg", "Kural 392: Mapping the stars through mathematics",
     "Photorealistic 16:9 cinematic shot, night terrace of an ancient observatory, scholars measuring planetary alignments using armillary spheres and shadow sticks under brilliant Milky Way."),
    ("40-kalvi/10-n10_poet_composing_flawless_meter.jpg", "Kural 392: Mastery of linguistic poetics and meter",
     "Photorealistic 16:9 cinematic film still, quiet pavilion, poet chanting metered Venba couplets, beating the rhythm with fingers on palm, eyes glowing with creative inspiration."),
    ("40-kalvi/11-n11_the_blindness_of_the_unlearned.jpg", "Kural 392: The tragic darkness of illiteracy",
     "Photorealistic 16:9 cinematic dramatic shot, shadowy alleyway, a confused man clutching an unreadable royal notice scroll, bewildered in a world of written law."),
    ("40-kalvi/12-n12_illumination_of_the_intellectual_eye.jpg", "Kural 392: The opening of inner vision through knowledge",
     "Photorealistic 16:9 cinematic portrait, student's face suddenly lighting up with joyous understanding as a mathematical concept clicks, eyes shining with discovery."),

    # Kural 393: The learned have true eyes; the unlearned have two sores upon their face
    ("40-kalvi/13-n13_radiant_vision_of_the_learned.jpg", "Kural 393: The radiant, perceptive gaze of the scholar",
     "Photorealistic 16:9 cinematic close-up, sharp, luminous eyes of a mature Tamil philosopher looking directly into the lens, reflecting deep insight and boundless clarity."),
    ("40-kalvi/14-n14_hollow_sight_of_superficial_eyes.jpg", "Kural 393: Sight without understanding is mere blindness",
     "Photorealistic 16:9 cinematic film still, noisy carnival crowd, people distracted by superficial illusions while ignoring timeless truths carved on temple stones nearby."),
    ("40-kalvi/15-n15_seeing_the_hidden_truth_of_nature.jpg", "Kural 393: Discerning the botanical laws in a medicinal leaf",
     "Photorealistic 16:9 cinematic macro shot, a Siddha scholar holding up a translucent green herbal leaf against sunlight, examining vein structures and healing properties."),
    ("40-kalvi/16-n16_reading_the_tides_for_voyage.jpg", "Kural 393: Marine navigator reading ocean swells and wind patterns",
     "Photorealistic 16:9 cinematic film still, prow of a Sangam trading ship, seasoned captain studying coastal currents and cloud formations to guide the fleet safely."),

    # Kural 394: The nature of learning is to delight at meeting and leave with yearning for more
    ("40-kalvi/17-n17_joyous_meeting_of_intellectual_peers.jpg", "Kural 394: Intellectual communion among great minds",
     "Photorealistic 16:9 cinematic film still, breezy courtyard of a temple academy, scholars from different kingdoms embracing warmly, eager to exchange new manuscripts."),
    ("40-kalvi/18-n18_philosophical_debate_in_mandapam.jpg", "Kural 394: Rigorous and courteous academic debate",
     "Photorealistic 16:9 cinematic film still, pillared mandapam, two scholars sitting cross-legged presenting logical arguments with hand gestures, listening to each other with deep respect."),
    ("40-kalvi/19-n19_reluctance_to_part_at_nightfall.jpg", "Kural 394: Yearning lingering after parting of minds",
     "Photorealistic 16:9 cinematic film still, academy gate at twilight, scholars still lingering in animated conversation, reluctant to bring their inspiring dialogue to an end."),
    ("40-kalvi/20-n20_writing_letters_to_distant_scholars.jpg", "Kural 394: Sustaining intellectual fellowship across distances",
     "Photorealistic 16:9 cinematic shot, scholar in his study tying a thin cord around rolled palm leaves addressed to an academy in another city, warm oil lamp light."),

    # Kural 395: As the needy stand before the rich, the humble stand before the wise to learn
    ("40-kalvi/21-n21_humble_prince_standing_before_guru.jpg", "Kural 395: Crown prince bowing humbly to receive instruction",
     "Photorealistic 16:9 cinematic film still, rustic hermitage veranda, a young crowned prince in simple cotton standing with folded hands before an impoverished hermit teacher."),
    ("40-kalvi/22-n22_the_dignity_of_intellectual_humility.jpg", "Kural 395: Humility as the true prerequisite for knowledge",
     "Photorealistic 16:9 cinematic shot, eager young apprentice kneeling to sweep the dust of the academy floor, demonstrating sincerity and respect for learning."),
    ("40-kalvi/23-n23_the_worthless_pride_of_ignorance.jpg", "Kural 395: Arrogant ignorance that refuses to ask questions",
     "Photorealistic 16:9 cinematic film still, an arrogant nobleman turning his back on scholars, strutting away with puffed chest into hollow self-satisfied darkness."),
    ("40-kalvi/24-n24_elevation_of_the_diligent_student.jpg", "Kural 395: The humble seeker rising to the seat of wisdom",
     "Photorealistic 16:9 cinematic film still, years later, the once-humble student now seated on the raised teacher's platform, instructing new generations with gentle authority."),

    # Kural 396: As a sand-well yields water the deeper you dig, wisdom flows the more you learn
    ("40-kalvi/25-n25_digging_the_sand_spring_at_river.jpg", "Kural 396: Digging deep into sandy riverbed to find sweet water",
     "Photorealistic 16:9 cinematic film still, wide dry sandy Kaveri riverbed, villagers scooping out golden sand, crystal-clear sweet spring water instantly bubbling up to fill the hollow."),
    ("40-kalvi/26-n26_unrolling_ever_deeper_scrolls.jpg", "Kural 396: Unrolling deeper layers of timeless knowledge",
     "Photorealistic 16:9 cinematic close-up, hands untying silk ribbons of a deeply ancient palm-leaf bundle, revealing pristine hidden verses that spark revelation."),
    ("40-kalvi/27-n27_the_inexhaustible_fountain_of_mind.jpg", "Kural 396: Inexhaustible intellectual fountain within the soul",
     "Photorealistic 16:9 cinematic symbolic shot, clear mountain spring bubbling through mossy stones into a reflective pool, representing ceaseless inner wisdom."),
    ("40-kalvi/28-n28_student_drinking_deeply_from_treatises.jpg", "Kural 396: Quenching the thirst of the mind with knowledge",
     "Photorealistic 16:9 cinematic shot, night academy, student drinking cool water from an earthen pitcher between intense hours of studying ancient grammar scrolls."),

    # Kural 397: How can anyone remain unlearned when all lands become a scholar's homeland?
    ("40-kalvi/29-n29_scholar_welcomed_in_foreign_court.jpg", "Kural 397: Tamil scholar received with royal honors abroad",
     "Photorealistic 16:9 cinematic film still, grand audience hall of a neighboring realm, foreign monarch rising from his throne to welcome a traveling Tamil philosopher."),
    ("40-kalvi/30-n30_citizen_of_the_entire_world.jpg", "Kural 397: The scholar at home in every city under heaven",
     "Photorealistic 16:9 cinematic wide shot, ancient crossroads city gate, traveling scholar carrying book bag, local townsfolk smiling and bowing in universal kinship."),
    ("40-kalvi/31-n31_universal_language_of_truth.jpg", "Kural 397: Wisdom breaking through all regional barriers",
     "Photorealistic 16:9 cinematic film still, port town caravanserai, scholars of diverse cultures and robes gathered around a stone table comparing star charts peacefully."),
    ("40-kalvi/32-n32_the_tragedy_of_unwillingness_to_learn.jpg", "Kural 397: Parable of the willful recluse stuck in ignorance",
     "Photorealistic 16:9 cinematic shot, lone narrow room, a man staring idly at bare walls, refusing the vast illuminated world outside his window."),

    # Kural 398: Learning acquired in a single life serves a soul through seven reincarnations
    ("40-kalvi/33-n33_the_eternal_seed_of_knowledge.jpg", "Kural 398: Knowledge planted like an immortal banyan seed",
     "Photorealistic 16:9 cinematic macro shot, a tiny banyan fig seed resting in the open palm of a sage, sunlight revealing its capacity to yield a forest over ages."),
    ("40-kalvi/34-n34_child_prodigy_displaying_past_wisdom.jpg", "Kural 398: Instinctive genius carrying wisdom from past lives",
     "Photorealistic 16:9 cinematic film still, sunlit veranda, a young seven-year-old child effortlessly answering complex logical riddles posed by amazed elders."),
    ("40-kalvi/35-n35_river_flowing_into_immortal_sea.jpg", "Kural 398: The stream of consciousness flowing across lifetimes",
     "Photorealistic 16:9 cinematic wide vista, vast river winding through golden plains to meet the boundless ocean at sunset, symbol of eternal soul journey."),
    ("40-kalvi/36-n36_inscribing_wisdom_on_granite_for_posterity.jpg", "Kural 398: Preserving sacred knowledge across millennia",
     "Photorealistic 16:9 cinematic shot, master sculptor chiseling ethical verses into a monolithic granite pillar so future generations may inherit the light."),

    # Kural 399: Seeing that learning delights the world, the wise desire it all the more
    ("40-kalvi/37-n37_world_delighting_in_master_poet.jpg", "Kural 399: The populace rejoicing in the wisdom of the poet",
     "Photorealistic 16:9 cinematic wide shot, town hall gathering, crowd listening in enraptured silence as a scholar recites moral poems, faces glowing with delight."),
    ("40-kalvi/38-n38_scholars_deepening_their_inquiries.jpg", "Kural 399: The wise constantly hungry for deeper research",
     "Photorealistic 16:9 cinematic film still, evening academy, grey-haired senior professors gathering around a newly excavated stone inscription with magnifying crystals."),
    ("40-kalvi/39-n39_multiplying_libraries_and_schools.jpg", "Kural 399: Founding new seats of learning across towns",
     "Photorealistic 16:9 cinematic wide shot, newly constructed stone school building beside a sacred lotus pond, carpenters putting final touches on wooden book racks."),
    ("40-kalvi/40-n40_unquenchable_thirst_for_understanding.jpg", "Kural 399: Burning love for truth that grows with age",
     "Photorealistic 16:9 cinematic portrait, elderly scholar with silver beard reading by oil lamp at night, smile of youthful wonder on his face."),

    # Kural 400: Learning is the true imperishable wealth; other earthly riches are mere dross
    ("40-kalvi/41-n41_imperishable_treasure_of_the_mind.jpg", "Kural 400: Knowledge as the indestructible wealth",
     "Photorealistic 16:9 cinematic symbolic shot, an open palm-leaf book surrounded by gold and diamonds, but only the written words glow with divine uncreated light."),
    ("40-kalvi/42-n42_rust_and_fire_destroying_material_goods.jpg", "Kural 400: Material riches rotting while wisdom endures",
     "Photorealistic 16:9 cinematic film still, ruined storehouse where iron implements rust and silver coins are tarnished black, while stone library shelves remain pristine."),
    ("40-kalvi/43-n43_thieves_unable_to_steal_learning.jpg", "Kural 400: The wealth that no thief can take",
     "Photorealistic 16:9 cinematic shot, dark highway, highwaymen searching a traveling scholar's cart finding only coarse cloth and manuscripts, while the scholar smiles fearlessly."),
    ("40-kalvi/44-n44_sharing_knowledge_multiplies_it.jpg", "Kural 400: The unique wealth that increases when shared",
     "Photorealistic 16:9 cinematic film still, guru lighting five small clay lamps from his single large flame, each student's lamp burning equally bright without diminishing the master's flame."),
    ("40-kalvi/45-n45_the_illumined_temple_of_learning.jpg", "Kural 400: Grand Sangam university standing timeless",
     "Photorealistic 16:9 cinematic majestic wide shot, grand university campus of Nalanda/Madurai style with stone cloisters, gardens, lecture pavilions under golden sunrise."),
    ("40-kalvi/46-n46_astronomical_tower_measuring_solstice.jpg", "Kural 400: Astronomical tower measuring the summer solstice",
     "Photorealistic 16:9 cinematic shot, stone sundial tower, shadow falling precisely along marked bronze scale at noon, master astrologer noting calculations on slate."),
    ("40-kalvi/47-n47_physicians_preparing_herbal_extracts.jpg", "Kural 400: Applied medical science healing diseases",
     "Photorealistic 16:9 cinematic film still, Ayurvedic laboratory, copper distillation apparatus extracting fragrant medicinal oils from rare roots, apprentices assisting master."),
    ("40-kalvi/48-n48_young_girl_inscribing_verses.jpg", "Kural 400: Universal education for women and girls in Sangam era",
     "Photorealistic 16:9 cinematic shot, sunlit domestic veranda, young Tamil girl wearing jasmine flowers practicing writing poetry with iron stylus on green palm leaf."),
    ("40-kalvi/49-n49_royal_patron_subsidizing_academy.jpg", "Kural 400: King allocating vast village revenues to education",
     "Photorealistic 16:9 cinematic film still, assembly hall, monarch handing over a signed copper-plate charter granting land endowments to free gurukulam schools."),
    ("40-kalvi/50-n50_mastery_over_mechanical_arts.jpg", "Kural 400: Science of metallurgy, waterworks, and weaving",
     "Photorealistic 16:9 cinematic film still, bronze foundry, master metallurgist measuring proportions of copper, tin, and zinc to cast sacred Panchaloha idols."),
    ("40-kalvi/51-n51_preservation_of_ancient_epics.jpg", "Kural 400: Scribes copying fading manuscripts to ensure continuity",
     "Photorealistic 16:9 cinematic shot, rows of scribes in library scriptorium copying weathered scrolls onto fresh palm leaves treated with lemongrass oil."),
    ("40-kalvi/52-n52_debate_under_the_sacred_peepal.jpg", "Kural 400: Open-air philosophy seminar under village tree",
     "Photorealistic 16:9 cinematic wide shot, village community seated in circle under massive peepal tree, discussing ethics and justice with traveling teachers at dusk."),
    ("40-kalvi/53-n53_the_clarity_of_scientific_thought.jpg", "Kural 400: Banishing superstitious dread through clear reason",
     "Photorealistic 16:9 cinematic film still, teacher explaining solar eclipse to villagers using two wooden spheres and an oil lamp, replacing fear with wonder."),
    ("40-kalvi/54-n54_children_chanting_multiplication_tables.jpg", "Kural 400: Joyful rhythmic chanting of mathematics",
     "Photorealistic 16:9 cinematic film still, sunny classroom verandah, group of seven-year-olds clapping hands and smiling as they recite traditional multiplication tables in Tamil."),
    ("40-kalvi/55-n55_the_torch_of_enlightenment.jpg", "Kural 400: Passing the torch of wisdom down generations",
     "Photorealistic 16:9 cinematic dramatic shot, aging teacher handing a polished iron stylus to his brightest young disciple at graduation ceremony, golden sunset."),
    ("40-kalvi/56-n56_flourishing_civilization_rooted_in_mind.jpg", "Kural 400: High civilization flourishing through learned minds",
     "Photorealistic 16:9 cinematic grand wide shot, ancient Tamil capital city with orderly avenues, majestic stone libraries, clean waterways, and dignified citizens."),
    ("40-kalvi/57-n57_the_universal_teacher_thiruvalluvar.jpg", "Kural 400: Thiruvalluvar seated under the banyan tree",
     "Photorealistic 16:9 cinematic wide shot, Thiruvalluvar in pristine white unbleached robes seated in meditation under a giant flowering banyan, palm leaves beside him."),
    ("40-kalvi/58-n58_the_temple_gopuram_reaching_the_stars.jpg", "Kural 400: Monument of sacred knowledge ascending to heaven",
     "Photorealistic 16:9 cinematic wide shot, towering stone gopuram crowned with constellations under midnight sky, symbol of the human intellect reaching the cosmos."),
    ("40-kalvi/59-n59_golden_dawn_of_eternal_education.jpg", "Kural 400: The eternal sunrise of knowledge dispelling all night",
     "Photorealistic 16:9 cinematic breathtaking panorama, golden sunrise breaking over mountain ranges, casting glorious warm radiance over sacred libraries and peaceful towns.")
]

# Chapter 42: கேள்வி (Kelvi - Listening / Wisdom of the Elders) - 41 shots
# Kurals 411 to 420
CH42_PROMPTS = [
    # Kural 411: Wealth of the ear is the supreme wealth; it is the foremost of all riches
    ("42-kelvi/01-n01_listening_to_the_elder_sage.jpg", "Kural 411: Attentive ear receiving sacred instruction",
     "Photorealistic 16:9 cinematic close-up, a young seeker leaning forward with rapt attention and cupped ear, listening to the soft profound words of a venerable white-haired rishi."),
    ("42-kelvi/02-n02_treasure_of_sound_vs_treasure_of_gold.jpg", "Kural 411: The wealth of listening outshining gold coffers",
     "Photorealistic 16:9 cinematic film still, royal court, a prince turning his gaze away from chests of pearls to focus entirely on the spoken counsel of a visiting philosopher."),
    ("42-kelvi/03-n03_pure_melody_of_the_yazh_harp.jpg", "Kural 411: Sweet spiritual words nourishing the ear",
     "Photorealistic 16:9 cinematic shot, evening portico, minstrel softly plucking strings of ancient Yazh harp while singing ethical verses, listeners transfixed in stillness."),
    ("42-kelvi/04-n04_the_sanctuary_of_focused_hearing.jpg", "Kural 411: Total silence in the audience of the master",
     "Photorealistic 16:9 cinematic wide shot, ancient stone hall, hundreds of citizens seated in pin-drop silence, hanging on every syllable of a discourse on justice."),

    # Kural 412: When there is no food for the ear, give a little food to the stomach
    ("42-kelvi/05-n05_prioritizing_ear_over_belly.jpg", "Kural 412: Spiritual hunger taking precedence over bodily appetite",
     "Photorealistic 16:9 cinematic film still, dining hall, students leaving steaming food platters untouched to listen eagerly to a sage who just began expounding a verse."),
    ("42-kelvi/06-n06_simple_meal_after_feast_of_wisdom.jpg", "Kural 412: Partaking of simple sustenance after intellectual feast",
     "Photorealistic 16:9 cinematic film still, peaceful veranda at dusk, householder eating simple curd rice with a smile of deep contentment after hours of listening to sacred poetry."),
    ("42-kelvi/07-n07_fasting_for_wisdom.jpg", "Kural 412: The body quieted so the ear may absorb truth",
     "Photorealistic 16:9 cinematic shot, quiet temple corner, a young disciple sipping cool water while absorbing the deep oral transmission of astronomy from his teacher."),
    ("42-kelvi/08-n08_the_supreme_satisfaction_of_listening.jpg", "Kural 412: Inner fullness that transcends physical food",
     "Photorealistic 16:9 cinematic portrait, elderly villager with serene glowing face, his heart satisfied by an afternoon of hearing the Mahabharata recited under village tree."),

    # Kural 413: Those who feed on wisdom through the ear are equal to gods who partake of heavenly offerings
    ("42-kelvi/09-n09_godlike_stature_of_the_wise_listener.jpg", "Kural 413: Listeners elevated to divine fellowship",
     "Photorealistic 16:9 cinematic symbolic shot, golden sunrise light illuminating scholars seated in circle, their silhouettes glowing with ethereal divine dignity."),
    ("42-kelvi/10-n10_celestial_nectar_of_spoken_dharma.jpg", "Kural 413: Spoken wisdom as divine amrita (nectar)",
     "Photorealistic 16:9 cinematic macro shot, carved stone chalice catching sparkling morning dew droplets under a blooming parijatha tree, sacred nectar of truth."),
    ("42-kelvi/11-n11_sacrificial_fires_yielding_to_wise_speech.jpg", "Kural 413: Wise speech surpassing the smoke of ritual altars",
     "Photorealistic 16:9 cinematic film still, temple courtyard, sacred homam fire dying down to fragrant ash while all priests gather to listen to an elder expounding ethics."),
    ("42-kelvi/12-n12_transcendent_peace_in_the_auditory_sanctum.jpg", "Kural 413: The sublime stillness of the illumined mind",
     "Photorealistic 16:9 cinematic shot, deep granite corridor of an ancient temple, echoes of sacred chants creating a timeless sanctuary of spiritual listening."),

    # Kural 414: Even if unlearned, let a man listen; it will be a staff to lean on in weakness
    ("42-kelvi/13-n13_the_sturdy_walking_staff_on_steep_hill.jpg", "Kural 414: A sturdy wooden staff supporting the traveler on rocky slopes",
     "Photorealistic 16:9 cinematic shot, steep rocky mountain trail, weathered hand grasping a polished bamboo walking staff firmly, stepping safely across loose gravel."),
    ("42-kelvi/14-n14_unlettered_farmer_guided_by_proverbs.jpg", "Kural 414: Unlettered farmer guided through adversity by remembered words",
     "Photorealistic 16:9 cinematic film still, rustic village hut, an illiterate farmer calmly solving a dispute by quoting the wise counsel he heard at the temple last season."),
    ("42-kelvi/15-n15_listening_compensating_for_illiteracy.jpg", "Kural 414: Oral transmission uplifting the unlettered",
     "Photorealistic 16:9 cinematic film still, village square, humble blacksmith listening intently to a bard reciting ancient heroic poems, his eyes shining with moral courage."),
    ("42-kelvi/16-n16_the_reliable_compass_in_confusion.jpg", "Kural 414: Remembered words serving as an unwavering compass",
     "Photorealistic 16:9 cinematic dramatic shot, dense foggy forest at dusk, traveler pausing, recalling the elder's directional advice, and confidently choosing the safe path."),

    # Kural 415: Words from the lips of the virtuous are like a firm staff on slippery ground
    ("42-kelvi/17-n17_slippery_muddy_path_in_monsoon.jpg", "Kural 415: Firm footing on slippery clay ground",
     "Photorealistic 16:9 cinematic film still, slippery red clay path during heavy monsoon rain, traveler planting his wooden staff deep into the soil to prevent a treacherous fall."),
    ("42-kelvi/18-n18_counsel_saving_youth_from_moral_pitfall.jpg", "Kural 415: Elder's timely warning preventing a young man's ruin",
     "Photorealistic 16:9 cinematic film still, evening tavern threshold, an elderly uncle gently gripping the arm of an impulsive nephew, speaking words that pull him back from folly."),
    ("42-kelvi/19-n19_golden_speech_of_the_virtuous.jpg", "Kural 415: Pure words distilled from a lifetime of righteousness",
     "Photorealistic 16:9 cinematic portrait, dignified elderly Tamil grandmother speaking soothing ethical proverbs to grandchildren gathered at her knee by lamplight."),
    ("42-kelvi/20-n20_anchor_holding_ship_in_surge.jpg", "Kural 415: Heavy iron anchor gripping seabed in swirling currents",
     "Photorealistic 16:9 cinematic dramatic shot, harbor bay, thick hemp rope and iron anchor keeping wooden sailing vessel completely steady against turbulent waves."),

    # Kural 416: Hear even a little of noble things; it will yield immense greatness
    ("42-kelvi/21-n21_single_drop_of_rain_in_pearl_oyster.jpg", "Kural 416: A single drop yielding a priceless lustrous pearl",
     "Photorealistic 16:9 cinematic macro shot, open oyster shell resting on coastal rock, a single crystal drop of rain falling into its heart, glistening in morning sun."),
    ("42-kelvi/22-n22_a_single_wise_sentence_changing_a_life.jpg", "Kural 416: A brief proverb transforming a bandit into a saint",
     "Photorealistic 16:9 cinematic film still, forest trail, fierce bandit dropping his weapon in sudden spiritual awakening after hearing a lone sentence from a wandering monk."),
    ("42-kelvi/23-n23_tiny_spark_lighting_grand_citadel.jpg", "Kural 416: A minute spark of wisdom illuminating the entire realm",
     "Photorealistic 16:9 cinematic wide shot, dusk falling over ancient city, single flame touching the peak beacon of the temple tower, inspiring thousands below."),
    ("42-kelvi/24-n24_treasuring_a_small_verse.jpg", "Kural 416: Inscribing a single treasured couplet on a ring",
     "Photorealistic 16:9 cinematic close-up, goldsmith carving a tiny ethical Tamil phrase onto the bezel of a royal gold signet ring under magnifying crystal."),

    # Kural 417: Those who have listened with deep inquiry never utter foolish words even in error
    ("42-kelvi/25-n25_measured_deliberate_speech_in_debate.jpg", "Kural 417: Guarded, deliberate speech that never slips into folly",
     "Photorealistic 16:9 cinematic film still, royal council, seasoned diplomat pausing thoughtfully before delivering an answer of flawless precision and dignified tact."),
    ("42-kelvi/26-n26_filtering_water_through_fine_cloth.jpg", "Kural 417: Pure speech filtered through extensive listening",
     "Photorealistic 16:9 cinematic macro shot, pure mountain water passing through a clean woven cotton filter into a polished brass pitcher, crystal clear without grit."),
    ("42-kelvi/27-n27_the_chastened_intellect_free_from_vanity.jpg", "Kural 417: Mind disciplined by listening to diverse masters",
     "Photorealistic 16:9 cinematic portrait, scholar with serene smile and tranquil brow, free from the brash impulse to boast or speak unconsidered opinions."),
    ("42-kelvi/28-n28_deep_lake_that_never_overflows_its_banks.jpg", "Kural 417: The deep reservoir that absorbs heavy rains without flooding",
     "Photorealistic 16:9 cinematic landscape, vast tranquil irrigation tank bordered by ancient stone sluices, holding torrential rains with effortless stability."),

    # Kural 418: An ear that has not been pierced by wise instruction is deaf, though it can hear
    ("42-kelvi/29-n29_hollow_ear_unpierced_by_wisdom.jpg", "Kural 418: The tragic deafness of the self-absorbed ear",
     "Photorealistic 16:9 cinematic dramatic portrait, a distracted man covering his ears amidst a room full of wise counsel, trapped in his own chaotic delusions."),
    ("42-kelvi/30-n30_carved_stone_ear_of_temple_statue.jpg", "Kural 418: Like a stone statue having ears that perceive nothing",
     "Photorealistic 16:9 cinematic close-up, carved granite dvarapala statue, intricate stone ear that feels no music or wisdom, contrasting with living sensitive ear."),
    ("42-kelvi/31-n31_piercing_the_ear_with_sacred_verses.jpg", "Kural 418: Sacred rite of awakening the auditory consciousness",
     "Photorealistic 16:9 cinematic film still, temple ceremony, guru whispering the sacred mantra into the right ear of a young seeker bathed in fragrant sandalwood paste."),
    ("42-kelvi/32-n32_the_ear_as_a_consecrated_shrine.jpg", "Kural 418: The ear consecrated as a temple of truth",
     "Photorealistic 16:9 cinematic close-up, warm golden sunlight illuminating a listening child's face, pure joy and understanding radiating from his expression."),

    # Kural 419: It is hard for those who have not heard wisdom to speak humbly before an assembly
    ("42-kelvi/33-n33_brash_fool_humiliated_in_learned_assembly.jpg", "Kural 419: The arrogant speaker stammering before wise assembly",
     "Photorealistic 16:9 cinematic film still, grand Sangam assembly hall, an arrogant uneducated speaker stammering with dry throat before the penetrating gaze of master scholars."),
    ("42-kelvi/34-n34_humble_scholar_speaking_with_grace.jpg", "Kural 419: The graceful, modest speech of the well-listened",
     "Photorealistic 16:9 cinematic film still, academy podium, a humble scholar bowing respectfully before addressing the elders, speaking words of gentle profundity."),
    ("42-kelvi/35-n35_untested_vessel_cracking_under_heat.jpg", "Kural 419: The unbaked clay pot collapsing in the kiln",
     "Photorealistic 16:9 cinematic shot, pottery kiln, a brittle unbaked vessel crumbling into dust when exposed to intense heat, parable of superficial speech."),
    ("42-kelvi/36-n36_silence_as_the_greatest_eloquence.jpg", "Kural 419: The wise knowing when to listen rather than speak",
     "Photorealistic 16:9 cinematic film still, council chamber, respected elder maintaining solemn thoughtful silence while others debate, waiting for the exact moment of wisdom."),

    # Kural 420: Those who know only taste of tongue and not of ear, what matters if they live or die?
    ("42-kelvi/40-n40_glutton_feasting_in_ignorance.jpg", "Kural 420: The glutton obsessed only with physical palate",
     "Photorealistic 16:9 cinematic film still, banquet table with heaps of rich meat and wine, a bloated man stuffing his face in oblivious sensual indulgence while neglecting his mind."),
    ("42-kelvi/38-n38_the_higher_hunger_for_immortal_sound.jpg", "Kural 420: The refined palate that craves philosophical truth",
     "Photorealistic 16:9 cinematic film still, simple stone courtyard, seeker sitting in rapt attention as an elder chants the Upanishads, savoring the syllables like divine ambrosia."),
    ("42-kelvi/39-n39_cattle_grazing_grass_unaware_of_stars.jpg", "Kural 420: Like animals living only for the belly",
     "Photorealistic 16:9 cinematic shot, herd of cows grazing pasture with heads down in grass, while the glorious starry night sky arches above them unnoticed."),
    ("42-kelvi/37-n37_the_immortal_life_of_the_discerning_listener.jpg", "Kural 420: Eternal vitality of the soul nourished by hearing",
     "Photorealistic 16:9 cinematic majestic wide shot, sunset over ancient temple pond, scholars gathered in contemplation, peaceful ripples reflecting eternal golden heavens."),
    ("42-kelvi/41-n41_dawn_over_the_academy_of_listening.jpg", "Kural 420: The glorious dawn of the listening soul",
     "Photorealistic 16:9 cinematic panoramic sunrise, golden light illuminating stone academies, forest hermitages, and peaceful villages where wisdom is spoken and heard.")
]

# Chapter 44: குற்றங்கடிதல் (Kutrangadithal - Guarding against Faults) - 36 shots
# Kurals 431 to 440
CH44_PROMPTS = [
    # Kural 431: Pride, careless anger, and lust are faults that destroy a king
    ("44-kutrangadithal/01-n01_pride_wrath_lust_destroyers.jpg", "Kural 431: The three deadly vices that topple crowns",
     "Photorealistic 16:9 cinematic film still, shadowy royal bedchamber, an arrogant prince scowling with clenched fists and averted eyes, surrounded by fallen goblets and neglected state documents."),
    ("44-kutrangadithal/02-n02_sober_reflection_before_the_mirror.jpg", "Kural 431: King examining his conscience in bronze mirror",
     "Photorealistic 16:9 cinematic close-up, monarch gazing into a polished bronze mirror by oil-lamp glow, inspecting not his regal jewelry but his inner thoughts, searching for pride."),
    ("44-kutrangadithal/03-n03_striking_down_the_inner_arrogance.jpg", "Kural 431: Uprooting inner ego before it harms the state",
     "Photorealistic 16:9 cinematic film still, quiet prayer hall, monarch bowing his head upon a stone step before the divine, surrendering ego and imperial vanity in deep humility."),
    ("44-kutrangadithal/04-n04_the_shipwreck_of_unchecked_passions.jpg", "Kural 431: Parable of the flagship shattered on reefs of wrath",
     "Photorealistic 16:9 cinematic dramatic wide shot, tempestuous sea, a magnificent war galley with snapped mast crashing against jagged black rocks in foaming stormy waves."),

    # Kural 432: Avarice, vain pride, and vulgar merriment are defects of majesty
    ("44-kutrangadithal/05-n05_miserly_king_counting_coins.jpg", "Kural 432: The stain of royal parsimony",
     "Photorealistic 16:9 cinematic film still, gloomy stone vault, a king secretly hoarding gold coins in locked coffers instead of funding irrigation reservoirs during drought."),
    ("44-kutrangadithal/06-n06_frivolous_revelry_during_crisis.jpg", "Kural 432: Vulgar frivolity while the nation struggles",
     "Photorealistic 16:9 cinematic film still, festive hall with dancers and jesters, while through the archway poor peasants huddle in the cold night outside the gates."),
    ("44-kutrangadithal/07-n07_dignified_sobriety_of_true_majesty.jpg", "Kural 432: Noble sobriety and moral gravity",
     "Photorealistic 16:9 cinematic portrait, upright Tamil king seated in dignified posture, adorned with simple pearls, radiating solemn duty and sober responsibility."),
    ("44-kutrangadithal/08-n08_guarding_the_purity_of_the_throne.jpg", "Kural 432: Banishing sycophants and shallow flatterers",
     "Photorealistic 16:9 cinematic film still, audience chamber, monarch signaling royal guards to escort obsequious, flattering courtiers away from the council table."),

    # Kural 433: Though a fault be small as a millet seed, to the wise it appears huge as a palm tree
    ("44-kutrangadithal/09-n09_millet_seed_and_towering_palm.jpg", "Kural 433: The tiny millet seed compared to colossal palmyra palm",
     "Photorealistic 16:9 cinematic macro shot, a single tiny golden tinai millet seed resting beside a towering palmyra palm tree rising majestically against morning sky."),
    ("44-kutrangadithal/10-n10_scrutinizing_the_smallest_oversight.jpg", "Kural 433: Detecting the slightest deviation from justice",
     "Photorealistic 16:9 cinematic film still, royal treasury desk, minister holding a balance scale that tilts by a single grain weight, refusing to overlook even the minutest error."),
    ("44-kutrangadithal/11-n11_a_single_drop_of_ink_on_silk.jpg", "Kural 433: A speck of black ink spoiling pure white silk",
     "Photorealistic 16:9 cinematic close-up, pristine unbleached white silk shawl draped on carved teakwood, a single black ink spot starkly visible, symbol of conspicuous fault."),
    ("44-kutrangadithal/12-n12_vigilant_self_correction_of_the_sage.jpg", "Kural 433: Instant repentance and correction of a small slip",
     "Photorealistic 16:9 cinematic portrait, thoughtful scholar pausing in middle of speech, acknowledging a slight factual inaccuracy, and immediately correcting it with grace."),

    # Kural 434: Guard against faults as your greatest enemy; faults will consume your glory
    ("44-kutrangadithal/13-n13_guarding_against_internal_faults.jpg", "Kural 434: The unseen internal enemy deadlier than foreign armies",
     "Photorealistic 16:9 cinematic film still, inner fortress citadel, monarch inspecting guards and defenses, but pausing to examine his own motives and moral discipline."),
    ("44-kutrangadithal/14-n14_termite_eating_the_royal_throne.jpg", "Kural 434: Termites hollowing out the carved wooden throne",
     "Photorealistic 16:9 cinematic macro close-up, intricate carved teak throne leg showing subtle hollow sawdust trails, insidious decay from within."),
    ("44-kutrangadithal/15-n15_vigilant_sentry_at_the_inner_gate.jpg", "Kural 434: Sentry guarding the inner sanctum of character",
     "Photorealistic 16:9 cinematic shot, ancient arched doorway lit by torches, disciplined guard standing impassive with spear, symbol of vigilance over consciousness."),
    ("44-kutrangadithal/16-n16_radiant_glory_preserved_by_purity.jpg", "Kural 434: Untarnished crown shining across decades",
     "Photorealistic 16:9 cinematic portrait, aging monarch with clear unclouded eyes, beloved by all subjects because his sixty-year reign has remained spotless."),

    # Kural 435: One who does not foresee faults before they happen is consumed like a haycock before fire
    ("44-kutrangadithal/17-n17_haystack_bursting_into_flame.jpg", "Kural 435: The dry haystack consumed instantly by a flying spark",
     "Photorealistic 16:9 cinematic dramatic shot, dry harvest field at dusk, a massive stack of dry paddy straw suddenly engulfed in fierce orange flames from a single windblown ember."),
    ("44-kutrangadithal/18-n18_careless_king_surprised_by_ruin.jpg", "Kural 435: The negligent ruler shocked by sudden rebellion",
     "Photorealistic 16:9 cinematic film still, palace balcony, careless king waking up to see smoke rising from outer suburbs, caught unprepared by ignored grievances."),
    ("44-kutrangadithal/19-n19_preemptive_clearing_of_dry_brush.jpg", "Kural 435: Clearing dry brush before summer winds blow",
     "Photorealistic 16:9 cinematic film still, edge of village homestead, careful farmers clearing away dead grass and wetting the perimeter to prevent wildfire spread."),
    ("44-kutrangadithal/20-n20_foresight_securing_the_fortress.jpg", "Kural 435: Foresight storing water and grain before drought",
     "Photorealistic 16:9 cinematic wide shot, vast underground stone cisterns being filled with monsoon runoff, wise king securing the fortress years ahead of scarcity."),

    # Kural 436: If a man removes his own faults before examining others, what evil can touch him?
    ("44-kutrangadithal/21-n21_cleansing_one_own_faults_first.jpg", "Kural 436: Correcting oneself before judging neighbors",
     "Photorealistic 16:9 cinematic film still, village assembly, elder looking into his own palm in deep contemplation before pronouncing judgment on a disputed boundary."),
    ("44-kutrangadithal/22-n22_the_unimpeachable_magistrate.jpg", "Kural 436: The judge whose spotless life silences all critics",
     "Photorealistic 16:9 cinematic film still, courtroom steps, upright magistrate walking past crowd, even the convicted acknowledging his absolute moral purity and fairness."),
    ("44-kutrangadithal/23-n23_washing_the_linen_clean.jpg", "Kural 436: Washing one's own cloth before inspecting others",
     "Photorealistic 16:9 cinematic shot, riverbank, washerman scrubbing white cotton cloth clean on granite stone in running river, clear water washing away all stains."),
    ("44-kutrangadithal/24-n24_invulnerability_of_the_faultless.jpg", "Kural 436: The invulnerable shield of spotless character",
     "Photorealistic 16:9 cinematic portrait, noble Tamil householder standing calm in morning breeze, no slander or malice able to find a foothold against his integrity."),

    # Kural 437: Wealth hoarded by one who neglects dharma is lost without leaving a trace
    ("44-kutrangadithal/25-n25_hoarded_gold_lost_to_flood.jpg", "Kural 437: Ill-gotten wealth washed away by rushing floodwaters",
     "Photorealistic 16:9 cinematic dramatic shot, turbulent brown river overflowing its banks, sweeping away a wealthy miser's wooden coffer, coins scattering into muddy silt."),
    ("44-kutrangadithal/26-n26_empty_vault_of_the_unrighteous.jpg", "Kural 437: The hollow emptiness of corrupt gains",
     "Photorealistic 16:9 cinematic film still, abandoned cellar, broken open stone chests covered in dust and cobwebs, no trace left of ill-acquired riches."),
    ("44-kutrangadithal/27-n27_enduring_abundance_of_virtuous_wealth.jpg", "Kural 437: Righteous wealth nourishing generations",
     "Photorealistic 16:9 cinematic wide shot, fertile family orchard thriving with mango and coconut, cattle well fed, children playing peacefully under ancestral boughs."),
    ("44-kutrangadithal/28-n28_distributing_wealth_to_avert_decay.jpg", "Kural 437: Purifying wealth by spending it on the public good",
     "Photorealistic 16:9 cinematic film still, village square, wealthy merchant dedicating a newly dug stone drinking well to the community, pouring water freely for all."),

    # Kural 438: The greed of the grasping miser is the greatest of all human faults
    ("44-kutrangadithal/29-n29_miser_clutching_purse_in_starvation.jpg", "Kural 438: The tragic sickness of insatiable greed",
     "Photorealistic 16:9 cinematic film still, dim room, an emaciated rich man clutching a heavy leather purse to his chest while shivering alone in rags, enslaved by gold."),
    ("44-kutrangadithal/30-n30_generous_hands_open_like_clouds.jpg", "Kural 438: Open hands raining bounty like monsoon clouds",
     "Photorealistic 16:9 cinematic close-up, open noble hands pouring silver coins and grain into outstretched palms of the needy, pure joyous liberation from greed."),
    ("44-kutrangadithal/31-n31_overflowing_river_refreshing_lands.jpg", "Kural 438: Unstinting flow of generosity refreshing the dry earth",
     "Photorealistic 16:9 cinematic wide shot, sparkling river spilling over low stone weirs into a network of green farm channels, life springing up on all banks."),
    ("44-kutrangadithal/32-n32_freedom_from_the_chain_of_covetousness.jpg", "Kural 438: The peaceful contentment of a non-possessive soul",
     "Photorealistic 16:9 cinematic portrait, smiling Tamil sage walking along a mountain ridge at sunset with empty hands, rich in inner peace and boundless freedom."),

    # Kural 439: Never indulge in self-praise; never do deeds that yield no good
    ("44-kutrangadithal/33-n33_humble_silence_regarding_achievements.jpg", "Kural 439: Silent modesty regarding one's own great deeds",
     "Photorealistic 16:9 cinematic film still, royal court, victorious commander refusing to boast of his conquest, directing all praise to his brave soldiers and just cause."),
    ("44-kutrangadithal/34-n34_turning_away_from_futile_enterprises.jpg", "Kural 439: Abandoning vain and destructive projects",
     "Photorealistic 16:9 cinematic film still, council table, king rolling up architectural plans for an extravagant palace monument, redirecting state funds to border granaries."),
    ("44-kutrangadithal/35-n35_quiet_work_of_true_greatness.jpg", "Kural 439: Quiet greatness working without trumpet or drum",
     "Photorealistic 16:9 cinematic film still, artisan village, master weaver quietly finishing a masterpiece of gold-threaded silk without shouting for attention."),
    ("44-kutrangadithal/36-n36_eternal_monument_of_faultless_rule.jpg", "Kural 439: The everlasting kingdom founded on constant vigilance",
     "Photorealistic 16:9 cinematic grand wide shot, panoramic view of ancient Tamilakam at sunrise, magnificent stone temples, bustling ports, green delta, eternal dharma.")
]

# Chapter 45: பெரியாரைத் துணைக்கோடல் (Periyaaraith Thunaikkodal - Seeking the Fellowship of Sages) - 42 shots
# Kurals 441 to 450
CH45_PROMPTS = [
    # Kural 441: Seek the friendship of men of mature wisdom and virtue
    ("45-periyaaraith-thunaikkodal/01-n01_monarch_inviting_venerable_sages.jpg", "Kural 441: King extending royal invitation to venerated philosophers",
     "Photorealistic 16:9 cinematic film still, ancient palace audience pavilion, crowned Tamil monarch bowing with folded hands to welcome grey-bearded forest hermits into his court."),
    ("45-periyaaraith-thunaikkodal/02-n02_royal_chariot_visiting_hermitage.jpg", "Kural 441: Royal chariot journeying to deep forest ashram",
     "Photorealistic 16:9 cinematic wide shot, sunlit clearing in dense teak forest, king stepping down from golden chariot without weapons to greet a solitary meditating sage."),
    ("45-periyaaraith-thunaikkodal/03-n03_council_of_seasoned_elders.jpg", "Kural 441: Surrounding the throne with men of ripe experience",
     "Photorealistic 16:9 cinematic film still, council room, monarch seated at table surrounded by veteran grey-haired ministers examining national irrigation maps on cloth."),
    ("45-periyaaraith-thunaikkodal/04-n04_deep_reverence_for_moral_integrity.jpg", "Kural 441: Valuing spotless character above political cunning",
     "Photorealistic 16:9 cinematic shot, palace terrace, young king attentively listening to an upright village elder, learning the real struggles of the agrarian poor."),

    # Kural 442: Cherish the great and win their friendship through devoted service
    ("45-periyaaraith-thunaikkodal/05-n05_serving_the_sages_with_reverence.jpg", "Kural 442: Serving the needs of the great with filial devotion",
     "Photorealistic 16:9 cinematic film still, monastery courtyard, young prince washing the dust from the feet of an old traveling philosopher with cool water from a brass kooja."),
    ("45-periyaaraith-thunaikkodal/06-n06_offering_sanctuary_to_scholars.jpg", "Kural 442: Building peaceful retreats for contemplative masters",
     "Photorealistic 16:9 cinematic wide shot, serene stone hermitage pavilion beside a mountain waterfall, monks and scholars walking quietly in garden paths."),
    ("45-periyaaraith-thunaikkodal/07-n07_winning_the_hearts_of_the_wise.jpg", "Kural 442: Earning the loyalty of upright counselors",
     "Photorealistic 16:9 cinematic shot, king presenting a humble gift of fresh Bilva leaves and sandalwood paste to a revered rishi, receiving a warm hand of blessing."),
    ("45-periyaaraith-thunaikkodal/08-n08_the_supreme_acquisition_of_state.jpg", "Kural 442: Gaining the friendship of sages as the highest conquest",
     "Photorealistic 16:9 cinematic film still, audience hall, monarch placing the lead chair beside his throne for the chief philosopher, affirming wisdom above power."),

    # Kural 443: To live in fellowship with men greater than oneself is the highest virtue
    ("45-periyaaraith-thunaikkodal/09-n09_walking_with_those_who_surpass_you.jpg", "Kural 443: Walking in the shadow of morally superior mentors",
     "Photorealistic 16:9 cinematic film still, shady temple cloisters at dawn, young king walking half a step behind his venerable preceptor, listening with humble reverence."),
    ("45-periyaaraith-thunaikkodal/10-n10_elevating_the_soul_through_company.jpg", "Kural 443: Upward pull of elevated companionship",
     "Photorealistic 16:9 cinematic portrait, young nobleman looking at a serene sage with deep aspiration in his eyes, feeling petty ambitions dissolve in holy presence."),
    ("45-periyaaraith-thunaikkodal/11-n11_the_mirror_of_higher_ideals.jpg", "Kural 443: Companions who constantly remind you of perfection",
     "Photorealistic 16:9 cinematic shot, gurukulam veranda, group of earnest students surrounding a luminous master, their faces reflecting noble resolve and moral beauty."),
    ("45-periyaaraith-thunaikkodal/12-n12_rising_above_mediocrity.jpg", "Kural 443: Transcending narrow self-interest in the presence of greatness",
     "Photorealistic 16:9 cinematic film still, public assembly, young prince rising to speak, influenced by the presence of his guru, choosing selfless justice over dynasty pride."),

    # Kural 444: When you have counselors who can rebuke your faults, who can conquer you?
    ("45-periyaaraith-thunaikkodal/13-n13_fearless_minister_rebuking_the_king.jpg", "Kural 444: The upright minister delivering sharp moral correction",
     "Photorealistic 16:9 cinematic film still, private council chamber, fearless grey-haired minister standing tall, pointing finger at royal decrees, rebuking an unjust tax."),
    ("45-periyaaraith-thunaikkodal/14-n14_king_thanking_his_critic.jpg", "Kural 444: King bowing in gratitude to the mentor who corrected him",
     "Photorealistic 16:9 cinematic film still, throne room, monarch stepping down from dais to clasp the hands of the counselor who stopped him from committing injustice."),
    ("45-periyaaraith-thunaikkodal/15-n15_invincible_fortress_of_honest_counsel.jpg", "Kural 444: An unassailable kingdom protected by honest critics",
     "Photorealistic 16:9 cinematic wide shot, colossal granite fortress on a mountain ridge under sunny skies, flags fluttering, symbol of invincibility built on truth."),
    ("45-periyaaraith-thunaikkodal/16-n16_foes_powerless_against_corrected_realm.jpg", "Kural 444: Enemies finding no chink in the nation's moral armor",
     "Photorealistic 16:9 cinematic film still, enemy spies peering through binoculars at a frontier town, finding absolute administrative harmony and no discord to exploit."),

    # Kural 445: The king who has no guide to reprove him will perish though he has no foes
    ("45-periyaaraith-thunaikkodal/17-n17_self_destruction_of_the_unguided_king.jpg", "Kural 445: The tragic fall of the monarch who silenced his critics",
     "Photorealistic 16:9 cinematic dramatic shot, dim ruined palace corridor, lone tyrant wandering paranoid and solitary among cold marble pillars, ruined by his own unchecked pride."),
    ("45-periyaaraith-thunaikkodal/18-n18_court_of_flatterers_leading_to_abyss.jpg", "Kural 445: Flatterers nodding smilingly while kingdom slides to ruin",
     "Photorealistic 16:9 cinematic film still, decadent court, obsequious sycophants applauding foolish royal decrees while empty granaries are hidden behind curtains."),
    ("45-periyaaraith-thunaikkodal/19-n19_ship_without_rudder_in_storm.jpg", "Kural 445: Parable of the rudderless ship drifting into rocky reefs",
     "Photorealistic 16:9 cinematic dramatic shot, stormy dark ocean, wooden ship without steering rudder spinning helpless in surging waves toward jagged shoreline rocks."),
    ("45-periyaaraith-thunaikkodal/20-n20_silencing_the_voice_of_conscience.jpg", "Kural 445: The lonely cemetery of unguided dynasties",
     "Photorealistic 16:9 cinematic shot, overgrown ancient ruins of a forgotten citadel, cracked throne half-buried in dry soil and briars, solemn cautionary vista."),

    # Kural 446: Without capital there is no gain; without the support of the wise there is no stability
    ("45-periyaaraith-thunaikkodal/21-n21_merchant_investing_sound_capital.jpg", "Kural 446: Merchant needing capital to conduct profitable commerce",
     "Photorealistic 16:9 cinematic film still, port warehouse, merchant laying out bags of silver seed capital on desk before launching trading fleet to foreign harbors."),
    ("45-periyaaraith-thunaikkodal/22-n22_the_spiritual_capital_of_wise_counselors.jpg", "Kural 446: Sage counselors as the irreplaceable capital of state",
     "Photorealistic 16:9 cinematic film still, throne room, king consulting five elder sages, comparing their collective moral wisdom to foundation stones of the palace."),
    ("45-periyaaraith-thunaikkodal/23-n23_building_on_shifting_sand.jpg", "Kural 446: The instability of a regime without moral advisors",
     "Photorealistic 16:9 cinematic shot, sandy riverbank, a stone wall cracking and toppling into water because its base was laid on mud without granite pilings."),
    ("45-periyaaraith-thunaikkodal/24-n24_rock_solid_pillars_of_the_realm.jpg", "Kural 446: Granite columns holding up the temple roof for a thousand years",
     "Photorealistic 16:9 cinematic wide shot, thousand-pillar mandapam of a monumental temple, massive granite pillars standing straight and unshakable in morning light."),

    # Kural 447: Severing the friendship of the wise is ten times worse than incurring the wrath of foes
    ("45-periyaaraith-thunaikkodal/25-n25_banishing_the_upright_sage_in_anger.jpg", "Kural 447: The calamitous mistake of alienating a righteous counselor",
     "Photorealistic 16:9 cinematic film still, palace gate at dusk, a venerable sage walking away with his walking staff and water pot, while the foolish young king looks on with proud defiance."),
    ("45-periyaaraith-thunaikkodal/26-n26_the_calamity_of_losing_spiritual_shield.jpg", "Kural 447: The loss of divine protection when sages depart",
     "Photorealistic 16:9 cinematic dramatic shot, dark gathering storm clouds over the citadel towers, cold ominous wind blowing fallen autumn leaves across empty courtyard."),
    ("45-periyaaraith-thunaikkodal/27-n27_reconciliation_before_disaster_strikes.jpg", "Kural 447: King running barefoot to bring back the departed sage",
     "Photorealistic 16:9 cinematic film still, dusty highway outside city walls, king kneeling on the road before the departing hermit, begging him to return and guide the realm."),
    ("45-periyaaraith-thunaikkodal/28-n28_harmony_restored_in_the_palace.jpg", "Kural 447: Rejoicing of the citizenry when the sage re-enters the gate",
     "Photorealistic 16:9 cinematic wide shot, palace gates, citizens and elders cheering with joy as the beloved sage walks back inside beside the repentant monarch."),

    # Kural 448: If you secure the alliance of men of power and wisdom, what enemies can prevail?
    ("45-periyaaraith-thunaikkodal/29-n29_coalition_of_righteous_rulers_and_sages.jpg", "Kural 448: Sovereign alliance of righteous monarchs and saints",
     "Photorealistic 16:9 cinematic film still, grand diplomatic pavilion, multiple crowned kings seated alongside forest rishis, signing everlasting peace treaty on palm leaf."),
    ("45-periyaaraith-thunaikkodal/30-n30_impregnable_shield_of_collective_virtue.jpg", "Kural 448: Total security against foreign conspiracies",
     "Photorealistic 16:9 cinematic wide shot, serene border frontier, peaceful farmers harvesting paddy without a single garrison needed, protected by moral prestige."),
    ("45-periyaaraith-thunaikkodal/31-n31_dissolving_threats_without_bloodshed.jpg", "Kural 448: Disarming hostile neighbors through wise diplomacy",
     "Photorealistic 16:9 cinematic film still, open pavilion on border, elder sage speaking to invading general, convincing him with reason and justice to turn his army home in peace."),
    ("45-periyaaraith-thunaikkodal/32-n32_the_calm_majesty_of_the_allied_throne.jpg", "Kural 448: Sovereign seated in tranquil majesty amidst wise friends",
     "Photorealistic 16:9 cinematic portrait, monarch seated on granite bench in temple garden, surrounded by poets, astronomers, and healers, radiant with serene confidence."),

    # Kural 449: Make the friendship of those who foresee future events and guide you safely
    ("45-periyaaraith-thunaikkodal/33-n33_astronomers_reading_the_monsoon_signs.jpg", "Kural 449: Sages reading environmental signs to avert famine",
     "Photorealistic 16:9 cinematic film still, palace observatory, astronomers showing the king alignments of planets and wind shifts, advising early granary preparation."),
    ("45-periyaaraith-thunaikkodal/34-n34_navigating_future_perils_with_wisdom.jpg", "Kural 449: Navigating the hidden shoals of upcoming decades",
     "Photorealistic 16:9 cinematic film still, council hall, elder statesman unrolling long historical scrolls, warning the prince of cyclical political crises based on century-old records."),
    ("45-periyaaraith-thunaikkodal/35-n35_the_beacon_fire_on_high_cape.jpg", "Kural 449: The lighthouse guiding fleets past submerged reefs",
     "Photorealistic 16:9 cinematic shot, coastal cliff at dusk, high stone lighthouse tower with burning brazier illuminating dangerous coral reefs for incoming merchant ships."),
    ("45-periyaaraith-thunaikkodal/36-n36_safe_voyage_through_turbulent_times.jpg", "Kural 449: The nation sailing safely through generational storms",
     "Photorealistic 16:9 cinematic majestic wide shot, Sangam trading fleet sailing smoothly under calm sunset sky, guided by seasoned navigators."),

    # Kural 450: The greatest blessing for a ruler is to win the heart and alliance of the great
    ("45-periyaaraith-thunaikkodal/37-n37_supreme_blessing_of_the_royal_house.jpg", "Kural 450: The crowning blessing of a prosperous dynasty",
     "Photorealistic 16:9 cinematic grand wide shot, magnificent temple coronation hall, elders and sages showering golden consecrated flowers over the crowned monarch."),
    ("45-periyaaraith-thunaikkodal/38-n38_generational_lineage_of_wise_kings.jpg", "Kural 450: Father, son, and grandson educated at the feet of sages",
     "Photorealistic 16:9 cinematic film still, family pavilion, three generations of royal princes seated on reed mats around an elder master, learning statecraft together."),
    ("45-periyaaraith-thunaikkodal/39-n39_universal_harmony_born_of_holy_counsel.jpg", "Kural 450: Peace descending upon every village, field, and town",
     "Photorealistic 16:9 cinematic panoramic landscape, vast view of green Kaveri river valley at golden hour, temple spires gleaming in sunlight, total idyllic peace."),
    ("45-periyaaraith-thunaikkodal/40-n40_sages_blessing_the_sleeping_capital.jpg", "Kural 450: Sages meditating on the hill overlooking the capital",
     "Photorealistic 16:9 cinematic majestic night shot, hilltop shrine overlooking glowing torchlit capital city below, hermit raising hand in silent universal blessing."),
    ("45-periyaaraith-thunaikkodal/41-n41_sacred_lotus_blossoming_in_clear_pool.jpg", "Kural 450: The pure bloom of righteous fellowship",
     "Photorealistic 16:9 cinematic macro shot, pristine pink lotus opening its petals in clear spring water, droplets catching morning sun, symbol of awakened consciousness."),
    ("45-periyaaraith-thunaikkodal/42-n42_golden_dawn_of_eternal_fellowship.jpg", "Kural 450: The immortal alliance of truth, majesty, and wisdom",
     "Photorealistic 16:9 cinematic final shot, breathtaking sunrise over Western Ghats, golden rays bathing ancient stone temples and peaceful homelands in everlasting glory.")
]

# Chapter 46: சிற்றினஞ்சேராமை (Sitrinanjeraamai - Avoiding Base Fellowship) - 53 shots
# Kurals 451 to 460
CH46_PROMPTS = [
    # Kural 451: The noble fear base fellowship; the ignoble embrace it as their own kin
    ("46-sitrinanjeraamai/01-n01_noble_soul_turning_from_base_crowd.jpg", "Kural 451: The noble man turning aside from vulgar company",
     "Photorealistic 16:9 cinematic film still, busy town street, a dignified scholar in clean white dhoti consciously veering his path away from a rowdy gambling den of brawling drunkards."),
    ("46-sitrinanjeraamai/02-n02_the_base_embracing_corrupt_companions.jpg", "Kural 451: The base rushing eagerly into corrupt fellowship",
     "Photorealistic 16:9 cinematic film still, dim shadowy tavern alley, conspiratorial men whispering over ill-gotten loot, laughing coarsely in moral depravity."),
    ("46-sitrinanjeraamai/03-n03_swan_avoiding_muddy_puddle.jpg", "Kural 451: The royal swan flying above turbid ditches to pure lotus lake",
     "Photorealistic 16:9 cinematic wide shot, graceful white swan soaring high in clear blue sky, turning away from stagnant muddy swamp toward a glistening crystal lake."),
    ("46-sitrinanjeraamai/04-n04_guarding_the_sanctity_of_the_home.jpg", "Kural 451: Protecting the domestic threshold from corrupting elements",
     "Photorealistic 16:9 cinematic film still, courtyard entrance, householder firmly refusing entry to deceitful flatterers, keeping his domestic sanctuary pure."),
    ("46-sitrinanjeraamai/05-n05_instinctive_dread_of_dishonor.jpg", "Kural 451: Natural dread of moral contamination",
     "Photorealistic 16:9 cinematic portrait, young student stepping back with immediate aversion when invited to join an immoral plot, pure conscience shining in his eyes."),

    # Kural 452: As water changes its nature according to the soil, man takes the character of his companions
    ("46-sitrinanjeraamai/06-n06_pure_rain_falling_on_red_soil.jpg", "Kural 452: Pure rainwater turning red as it touches red clay soil",
     "Photorealistic 16:9 cinematic macro shot, crystal-clear falling raindrops striking dry red clay earth, instantly transforming into dark crimson mud as they blend."),
    ("46-sitrinanjeraamai/07-n07_water_flowing_through_white_sand.jpg", "Kural 452: Water remaining pure and crystal when flowing over white sand",
     "Photorealistic 16:9 cinematic macro shot, clear stream rushing over bed of pure white quartz pebbles, remaining limpid, sparkling, and sweet to taste."),
    ("46-sitrinanjeraamai/08-n08_water_stagnating_in_alkaline_mire.jpg", "Kural 452: Fresh water turning bitter and foul in alkaline salt marsh",
     "Photorealistic 16:9 cinematic shot, bleak salt flat, clear rainwater pooling into grey saline crust, turning brackish and toxic, unable to sustain green life."),
    ("46-sitrinanjeraamai/09-n09_youth_absorbing_manners_of_friends.jpg", "Kural 452: Young man adopting the speech and demeanor of his circle",
     "Photorealistic 16:9 cinematic film still, market portico, an impressionable youth sitting with crude companions, beginning to mirror their slouch and cynical sneer."),
    ("46-sitrinanjeraamai/10-n10_disciple_absorbing_radiance_of_guru.jpg", "Kural 452: Disciple becoming luminous in the aura of the master",
     "Photorealistic 16:9 cinematic portrait, young student sitting at the feet of a saintly guru, his countenance gradually taking on the master's serene peaceful glow."),

    # Kural 453: The mind is shaped by intellect; but character is shaped by company
    ("46-sitrinanjeraamai/11-n11_brilliant_intellect_corrupted_by_vile_friends.jpg", "Kural 453: Sharp intellect misdirected into crime by bad company",
     "Photorealistic 16:9 cinematic film still, midnight study, an educated scholar drawing maps of royal treasury vaults for a gang of thieves, genius perverted by vile associates."),
    ("46-sitrinanjeraamai/12-n12_simple_soul_ennobled_by_good_company.jpg", "Kural 453: Humble artisan rising to sainthood in good company",
     "Photorealistic 16:9 cinematic film still, temple corridor, simple potter listening to chanting saints, his simple heart blossoming into exalted moral devotion."),
    ("46-sitrinanjeraamai/13-n13_iron_bar_smelted_with_gold.jpg", "Kural 453: Base metal taking on luster when alloyed with gold",
     "Photorealistic 16:9 cinematic macro shot, goldsmith's crucible glowing in furnace fire, molten metals blending together, taking on golden luster."),
    ("46-sitrinanjeraamai/14-n14_fragrant_jasmine_perfuming_dry_thread.jpg", "Kural 453: Plain coarse cotton thread made fragrant by jasmine blooms",
     "Photorealistic 16:9 cinematic close-up, garland maker weaving white jasmine blossoms onto simple brown thread, the thread absorbing the rich divine aroma."),
    ("46-sitrinanjeraamai/15-n15_sculptor_shaping_rough_granite.jpg", "Kural 453: Constant companionship shaping the soul like a chisel",
     "Photorealistic 16:9 cinematic shot, sculpture workshop, master artisan's steady hand guiding apprentice's hammer, carving divine form from rough unhewn rock."),

    # Kural 454: Wisdom seems born within the mind; but it is nurtured by the company you keep
    ("46-sitrinanjeraamai/16-n16_the_silent_soil_nourishing_the_tree.jpg", "Kural 454: The fertile soil that gives life to the majestic banyan",
     "Photorealistic 16:9 cinematic wide shot, immense banyan tree spreading hundreds of aerial roots into rich dark humus soil, nurtured by the unseen earth below."),
    ("46-sitrinanjeraamai/17-n17_igniting_lamp_from_living_torch.jpg", "Kural 454: Intellectual spark leaping from living master to student",
     "Photorealistic 16:9 cinematic close-up, tip of a flaming temple torch touching the cotton wick of an unlit bronze lamp, instantly bringing it to bright life."),
    ("46-sitrinanjeraamai/18-n18_dialogue_sharpening_philosophical_insight.jpg", "Kural 454: Ideas sharpened like swords against whetstones of friends",
     "Photorealistic 16:9 cinematic film still, courtyard mandapam, two scholars leaning forward across a low table, sharpening their philosophical definitions through intense dialogue."),
    ("46-sitrinanjeraamai/19-n19_withering_of_mind_in_isolated_folly.jpg", "Kural 454: Intellectual decay when trapped among the ignorant",
     "Photorealistic 16:9 cinematic film still, lonely room, intelligent youth staring down at uninspired papers, his vocabulary and passion dulled by years among vulgar peers."),
    ("46-sitrinanjeraamai/20-n20_blooming_orchard_sheltered_from_gale.jpg", "Kural 454: Tender saplings flourishing behind windbreak trees",
     "Photorealistic 16:9 cinematic landscape, lush young fruit orchard thriving in calm sunshine behind a protective wall of tall bamboo and cedar trees."),

    # Kural 455: Purity of mind and purity of action depend upon the purity of companionship
    ("46-sitrinanjeraamai/21-n21_washing_hands_in_sacred_spring.jpg", "Kural 455: Washing hands in pristine holy waters before ceremony",
     "Photorealistic 16:9 cinematic close-up, cupped hands dipping into crystal-clear spring water in a stone basin, drops splashing clean in morning light."),
    ("46-sitrinanjeraamai/22-n22_the_pure_circle_of_truth_seekers.jpg", "Kural 455: Spotless fellowship keeping actions upright",
     "Photorealistic 16:9 cinematic film still, shaded temple veranda, group of white-robed seekers meditating together in unbroken silence, mutual support in virtue."),
    ("46-sitrinanjeraamai/23-n23_avoiding_the_contagion_of_dishonesty.jpg", "Kural 455: Walking away from corrupt commercial collusion",
     "Photorealistic 16:9 cinematic film still, spice warehouse, honest merchant stepping away from a group of traders plotting to fix grain prices, keeping his ledger pure."),
    ("46-sitrinanjeraamai/24-n24_pure_milk_untouched_by_sour_curd.jpg", "Kural 455: Fresh sweet milk protected from a drop of sour curd",
     "Photorealistic 16:9 cinematic macro shot, polished brass bowl filled with pure fresh frothing milk, clean and untainted by souring agents."),
    ("46-sitrinanjeraamai/25-n25_radiant_whiteness_of_conch_shell.jpg", "Kural 455: Natural purity of a conch shell formed in deep ocean",
     "Photorealistic 16:9 cinematic macro close-up, sacred white Valampuri conch shell resting on red silk altar cloth, flawless spiral glistening in sunlight."),

    # Kural 456: The pure in heart leave good progeny; the pure in company leave flawless deeds
    ("46-sitrinanjeraamai/26-n26_virtuous_children_carrying_ancestral_honor.jpg", "Kural 456: Noble children continuing the legacy of an upright home",
     "Photorealistic 16:9 cinematic film still, courtyard home, healthy smiling children helping their father water the garden, inheriting good lineage."),
    ("46-sitrinanjeraamai/27-n27_flawless_public_works_completed_by_good_team.jpg", "Kural 456: Great public works achieved through harmonious companions",
     "Photorealistic 16:9 cinematic wide shot, completed stone reservoir embankment, master builders standing together admiring the calm lake holding life for fifty villages."),
    ("46-sitrinanjeraamai/28-n28_lasting_poetry_born_of_pure_circle.jpg", "Kural 456: Sangam anthologies compiled by spotless poet guilds",
     "Photorealistic 16:9 cinematic film still, royal archive hall, scholars placing tied bundles of peer-reviewed palm-leaf poems into carved cedar chests."),
    ("46-sitrinanjeraamai/29-n29_the_lasting_monument_of_righteous_collaboration.jpg", "Kural 456: Granite temple carved by guild of devoted sculptors",
     "Photorealistic 16:9 cinematic wide shot, towering granite temple sanctum glowing at golden hour, master artisans standing back with folded palms in shared achievement."),
    ("46-sitrinanjeraamai/30-n30_peaceful_departure_leaving_pure_memory.jpg", "Kural 456: Peaceful legacy of a life shared with noble friends",
     "Photorealistic 16:9 cinematic wide vista, peaceful village cemetery shaded by flowering neem trees at dusk, memory of a righteous citizen honored by all."),

    # Kural 457: Goodness of mind yields wealth; goodness of company yields everlasting glory
    ("46-sitrinanjeraamai/31-n31_peaceful_mind_bringing_inner_treasure.jpg", "Kural 457: Inward contentment as true wealth of the soul",
     "Photorealistic 16:9 cinematic portrait, Tamil householder smiling peacefully in simple cotton robes, rich in contentment, seated by home oil lamp."),
    ("46-sitrinanjeraamai/32-n32_everlasting_glory_bestowed_by_noble_peers.jpg", "Kural 457: Renown that echoes through centuries among the wise",
     "Photorealistic 16:9 cinematic film still, Sangam academy podium, bards singing verses that commemorate the heroic friendship of Pari and Kapilar."),
    ("46-sitrinanjeraamai/33-n33_sculpting_the_memorial_hero_stone.jpg", "Kural 457: Hero stone inscribed with deeds of noble companionship",
     "Photorealistic 16:9 cinematic shot, village boundary, masons finishing a carved hero stone depicting two loyal comrades standing shoulder to shoulder in battle."),
    ("46-sitrinanjeraamai/34-n34_timeless_constellations_over_the_plains.jpg", "Kural 457: Glory shining like constellations in the night sky",
     "Photorealistic 16:9 cinematic majestic night shot, brilliant stars of Orion and Pleiades shining over silhouettes of ancient Tamil temples and hills."),

    # Kural 458: Though men possess natural goodness of mind, good company strengthens it to perfection
    ("46-sitrinanjeraamai/35-n35_polishing_the_rough_diamond.jpg", "Kural 458: Rough diamond cut and polished by master lapidary",
     "Photorealistic 16:9 cinematic macro close-up, diamond cutting wheel spinning with oil and diamond dust, transforming an uncut pebble into a blazing brilliant jewel."),
    ("46-sitrinanjeraamai/36-n36_gentle_sapling_staked_against_the_wind.jpg", "Kural 458: Staking a fragile fruit sapling with strong bamboo support",
     "Photorealistic 16:9 cinematic shot, garden orchard, young gardener tying a slender mango sapling to a sturdy bamboo pole, ensuring it grows straight and tall."),
    ("46-sitrinanjeraamai/37-n37_noble_nature_refined_by_sages.jpg", "Kural 458: Naturally virtuous prince perfected by the council of saints",
     "Photorealistic 16:9 cinematic film still, terrace garden, young prince listening with rapt attention to an elder sage, his rough edges smoothed into royal grace."),
    ("46-sitrinanjeraamai/38-n38_pure_gold_refined_in_the_crucible.jpg", "Kural 458: Refining gold to highest purity in charcoal forge",
     "Photorealistic 16:9 cinematic close-up, goldsmith using a clay blowpipe on glowing charcoal hearth, watching gold burn away the last dross to shine with pristine yellow luster."),

    # Kural 459: Goodness of mind secures heaven; but good company preserves it from slipping
    ("46-sitrinanjeraamai/39-n39_firm_hand_holding_brother_on_ledge.jpg", "Kural 459: Comrade gripping brother's hand on precarious cliff edge",
     "Photorealistic 16:9 cinematic dramatic shot, high mountain precipice, strong warrior arm gripping the wrist of his slipping companion, pulling him safely back to solid rock."),
    ("46-sitrinanjeraamai/40-n40_safe_haven_inside_the_sanctuary_walls.jpg", "Kural 459: Finding shelter within the fortress of the good",
     "Photorealistic 16:9 cinematic wide shot, torrential storm outside massive stone temple cloisters, but inside seekers walk peacefully in dry, sheltered serenity."),
    ("46-sitrinanjeraamai/41-n41_maintaining_spiritual_balance.jpg", "Kural 459: Daily association keeping the soul aligned with heaven",
     "Photorealistic 16:9 cinematic film still, dawn courtyard, three elderly monks sitting together in meditation, their synchronized breathing maintaining unbroken peace."),
    ("46-sitrinanjeraamai/42-n42_the_strait_gate_to_celestial_realms.jpg", "Kural 459: Ascending the sacred stairway of moral fellowship",
     "Photorealistic 16:9 cinematic wide shot, long stone stairway ascending sacred mountain at sunrise, pilgrims walking together supporting each other's steps."),

    # Kural 460: There is no greater help than good company; there is no greater ruin than base fellowship
    ("46-sitrinanjeraamai/43-n43_the_twin_paths_diverging_at_crossroad.jpg", "Kural 460: The two roads diverging at the ancient boundary stone",
     "Photorealistic 16:9 cinematic wide shot, rural crossroad at dawn, one path leading up to a sunlit temple hill, the other winding down into a dark thorny marshland."),
    ("46-sitrinanjeraamai/44-n44_rescued_from_the_quicksand_of_vice.jpg", "Kural 460: True friends pulling a companion out of treacherous mire",
     "Photorealistic 16:9 cinematic dramatic shot, marshy river edge, two strong friends extending a wooden branch to haul a sinking companion out of dangerous mud."),
    ("46-sitrinanjeraamai/45-n45_the_poisonous_snake_in_the_sleeping_chamber.jpg", "Kural 460: The deadly hidden peril of corrupt companions",
     "Photorealistic 16:9 cinematic dramatic close-up, coiled black cobra slithering silently near a silk bed in moonlit chamber, symbol of treacherous base associates."),
    ("46-sitrinanjeraamai/46-n46_healing_balm_of_true_brotherhood.jpg", "Kural 460: The soothing solace of upright loyal companions",
     "Photorealistic 16:9 cinematic film still, veranda at dusk, friends gathering around an injured comrade, tending his wounds with herbal oil and comforting smiles."),
    ("46-sitrinanjeraamai/47-n47_banishing_corrupt_courtiers_from_court.jpg", "Kural 460: Sovereign purging the court of corrupt parasites",
     "Photorealistic 16:9 cinematic film still, palace gate, royal guards shutting heavy bronze-studded doors against banished corrupt intriguers, securing the realm."),
    ("46-sitrinanjeraamai/48-n48_gathering_the_pure_council.jpg", "Kural 460: Assembly of righteous, truthful, and loyal advisors",
     "Photorealistic 16:9 cinematic film still, sunlit council table, monarch smiling as he looks upon his circle of honest counselors, absolute peace and strength."),
    ("46-sitrinanjeraamai/49-n49_harvest_flourishing_in_weeded_field.jpg", "Kural 460: Bumper crop thriving after thorough weeding",
     "Photorealistic 16:9 cinematic wide shot, boundless green paddy field completely cleared of choking weeds, stalks heavy with golden grain swaying in morning breeze."),
    ("46-sitrinanjeraamai/50-n50_the_clear_stream_flowing_to_ocean.jpg", "Kural 460: Pure stream joining the ocean without losing sweetness",
     "Photorealistic 16:9 cinematic landscape, clear river delta meeting turquoise ocean waters, sea birds gliding, clean horizon bathed in morning sunlight."),
    ("46-sitrinanjeraamai/51-n51_the_sacred_flame_fed_by_pure_ghee.jpg", "Kural 460: Feeding the holy fire only with pure clarified butter",
     "Photorealistic 16:9 cinematic close-up, priest pouring golden melted ghee into the sacred fire altar, flame leaping up golden and smokeless toward the temple ceiling."),
    ("46-sitrinanjeraamai/52-n52_the_prosperous_homeland_of_righteous_fellowship.jpg", "Kural 460: A nation flourishing in the fellowship of the good",
     "Photorealistic 16:9 cinematic panoramic vista, ancient Tamil capital city from high hill, stone gopurams gleaming in late afternoon sun, peaceful people walking the avenues."),
    ("46-sitrinanjeraamai/53-n53_the_eternal_dawn_of_wisdom.jpg", "Kural 460: Immortal golden sunrise over Tamilakam",
     "Photorealistic 16:9 cinematic final shot, breathtaking golden sunrise breaking over mountain ranges, casting celestial radiance over sacred temples, libraries, and peaceful lands.")
]

ALL_BATCH3_CHAPTERS = {
    39: {"name": "39-iraimaatchi", "prompts": CH39_PROMPTS, "count": len(CH39_PROMPTS)},
    40: {"name": "40-kalvi", "prompts": CH40_PROMPTS, "count": len(CH40_PROMPTS)},
    42: {"name": "42-kelvi", "prompts": CH42_PROMPTS, "count": len(CH42_PROMPTS)},
    44: {"name": "44-kutrangadithal", "prompts": CH44_PROMPTS, "count": len(CH44_PROMPTS)},
    45: {"name": "45-periyaaraith-thunaikkodal", "prompts": CH45_PROMPTS, "count": len(CH45_PROMPTS)},
    46: {"name": "46-sitrinanjeraamai", "prompts": CH46_PROMPTS, "count": len(CH46_PROMPTS)},
}

if __name__ == "__main__":
    total = sum(c["count"] for c in ALL_BATCH3_CHAPTERS.values())
    print(f"Total Batch 3 Prompts defined: {total}")
    for ch, data in ALL_BATCH3_CHAPTERS.items():
        print(f"  Chapter {ch} ({data['name']}): {data['count']} prompts")
