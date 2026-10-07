# -*- coding: utf-8 -*-
"""
Batch 2 Prompt Definitions: Chapters 5, 8, 16, 25, 30, 31 (Total: 269 shots)
Option C: Essential Virtues & Compassion Suite
"""

import json
from pathlib import Path

# Chapter 5: இல்வாழ்க்கை (Ilvaazhkkai - Domestic Life / Grihastha Virtue) - 42 shots
CH05_PROMPTS = [
    # Kural 41: Supporting the three orders (students, ascetics, departed)
    ("05-ilvaazhkkai/01-n01_grihastha_morning_lamp.jpg", "Kural 41: Lighting the dawn lamp of the righteous household",
     "Photorealistic 16:9 cinematic film still, ancient Tamil courtyard home at dawn, a noble householder in a crisp white veshti lighting a tall seven-tiered brass kuthuvilakku lamp in the central open courtyard, jasmine flowers strewn around, soft morning light."),
    ("05-ilvaazhkkai/02-n02_welcoming_wandering_students.jpg", "Kural 41: Welcoming brahmacharis and young learners",
     "Photorealistic 16:9 cinematic film still, open pillared verandah of a village home, householder and his wife offering cool water from a brass kooja to young gurukulam students holding palm-leaf bundles, morning breeze rustling banana trees."),
    ("05-ilvaazhkkai/03-n03_serving_wandering_mendicants.jpg", "Kural 41: Offering alms to wandering ascetics",
     "Photorealistic 16:9 cinematic film still, a venerable householder respectfully placing steaming cooked rice and ghee into the wooden begging bowls of two wandering mendicants on a stone threshold, mango leaves tied at doorway."),
    ("05-ilvaazhkkai/04-n04_tending_elderly_kinsmen.jpg", "Kural 41: Caring for the departed and elderly sages",
     "Photorealistic 16:9 cinematic film still, peaceful veranda of an ancient courtyard home, householder gently draping a woven shawl over the shoulders of an elderly grandfather resting on a carved wooden cot, warm amber lantern glow."),

    # Kural 42: Helping the abandoned, poor, and dead
    ("05-ilvaazhkkai/05-n05_feeding_weary_travelers.jpg", "Kural 42: Feeding weary travelers under the tamarind grove",
     "Photorealistic 16:9 cinematic film still, shade of a giant flowering tamarind tree outside a village home, weary travelers seated on reed mats being served warm curd rice and sweet fruits on fresh green banana leaves, golden afternoon sun."),
    ("05-ilvaazhkkai/06-n06_giving_shelter_in_monsoon.jpg", "Kural 42: Giving sanctuary to the destitute during rain",
     "Photorealistic 16:9 cinematic film still, heavy tropical monsoon rain pouring from terracotta eaves into courtyard, a kind Tamil householder inviting a shivering family under the shelter of his tiled pavilion, warm oil lamp light on wet flagstones."),
    ("05-ilvaazhkkai/07-n07_distribution_of_grain.jpg", "Kural 42: Distributing surplus grain to the needy",
     "Photorealistic 16:9 cinematic film still, granary of an ancient Tamil village homestead, householder measuring golden unhusked paddy from a woven wicker granary into the cloth sacks of poor villagers, dust motes in sunbeams."),
    ("05-ilvaazhkkai/08-n08_comforting_lonely_elder.jpg", "Kural 42: Solacing a forlorn elder with dignity",
     "Photorealistic 16:9 cinematic film still, stone bench beside a blooming parijatha tree, householder sitting beside an old village poet listening with deep reverence to his tales, soft evening shadows."),

    # Kural 43: Fivefold duties (ancestors, gods, guests, kinsmen, self)
    ("05-ilvaazhkkai/09-n09_ancestral_libations_river.jpg", "Kural 43: Offering morning libations at the river",
     "Photorealistic 16:9 cinematic film still, householder standing waist-deep in the Kaveri river at dawn, offering water from his cupped palms to the rising sun and ancestors, ripples catching pink and gold dawn reflections."),
    ("05-ilvaazhkkai/10-n10_temple_flower_garlanding.jpg", "Kural 43: Floral offerings to the divine",
     "Photorealistic 16:9 cinematic film still, ancient stone mandapam altar, householder and his wife offering fresh lotus blooms and bilva leaves before a consecrated lingam, fragrance of burning camphor rising."),
    ("05-ilvaazhkkai/11-n11_honoring_visiting_kinsfolk.jpg", "Kural 43: Welcoming extended relatives with joy",
     "Photorealistic 16:9 cinematic film still, bustling pillared inner hall of a traditional home, relatives gathering around a festive feast, children laughing, brass platters heaped with savory dishes, joyful domestic warmth."),
    ("05-ilvaazhkkai/12-n12_communal_evening_prayer.jpg", "Kural 43: The fivefold harmony of the righteous home",
     "Photorealistic 16:9 cinematic film still, twilight in a tranquil village courtyard, the entire household gathered in quiet meditation around the central tulsi thara, sacred smoke of sambrani drifting into the starry night sky."),

    # Kural 44: Fear of dishonor and eating shared food
    ("05-ilvaazhkkai/13-n13_measuring_honest_produce.jpg", "Kural 44: Wealth acquired through clean and honest labor",
     "Photorealistic 16:9 cinematic film still, courtyard granary, householder using honest wooden marakkal grain measures with an open scale, surrounded by clean sacks of sesame and lentils, honest pride in his eyes."),
    ("05-ilvaazhkkai/14-n14_sharing_evening_meal.jpg", "Kural 44: Partaking of food only after guests are fed",
     "Photorealistic 16:9 cinematic film still, simple earthen dining room, householder and wife eating simple gruel with contentment after outside guests have eaten fully, serene peace on their faces."),
    ("05-ilvaazhkkai/15-n15_refusing_unjust_gain.jpg", "Kural 44: Turning away wrongful wealth",
     "Photorealistic 16:9 cinematic film still, a village home entryway, householder raising his hand in firm refusal to an emissary trying to offer an illicit bribe in a silk purse, upright posture of unyielding honor."),
    ("05-ilvaazhkkai/16-n16_everlasting_lineage_of_honor.jpg", "Kural 44: An untarnished heritage that endures generations",
     "Photorealistic 16:9 cinematic film still, lush green paddy fields backed by coconut palms and the sturdy stone walls of the ancestral homestead, children playing safely in the orchard, golden hour radiance."),

    # Kural 45: Love and virtue make domestic life fruitful
    ("05-ilvaazhkkai/17-n17_husband_wife_planting_tree.jpg", "Kural 45: Husband and wife planting a banyan sapling",
     "Photorealistic 16:9 cinematic film still, loving Tamil husband and wife together planting a sacred sapling in their garden, pouring water from a clay jug, tender smiles, soft sunlight filtering through betel leaves."),
    ("05-ilvaazhkkai/18-n18_mutual_respect_in_counsel.jpg", "Kural 45: Mutual consultation in domestic governance",
     "Photorealistic 16:9 cinematic film still, veranda at dusk, husband and wife reviewing palm-leaf family accounts together by the soft glow of a bronze lamp, mutual respect and shared harmony."),
    ("05-ilvaazhkkai/19-n19_cradle_under_jasmine_arbor.jpg", "Kural 45: Sweetness of domestic affection and progeny",
     "Photorealistic 16:9 cinematic film still, a carved wooden baby cradle rocking gently under an arbor blooming with white jasmine flowers, morning light dappling the clay floor."),
    ("05-ilvaazhkkai/20-n20_tender_care_of_infant.jpg", "Kural 45: Mother and father gazing upon their child",
     "Photorealistic 16:9 cinematic film still, intimate shot of Tamil parents looking down at their sleeping baby wrapped in soft cotton, profound peace and sacred devotion in their expressions."),

    # Kural 46: If domestic life has virtue, what does other asceticism achieve?
    ("05-ilvaazhkkai/21-n21_grihastha_meditating_at_home.jpg", "Kural 46: Spiritual enlightenment within the home",
     "Photorealistic 16:9 cinematic film still, householder seated in padmasana on a clean woven grass mat inside his quiet wooden veranda at dawn, peaceful meditative glow on his face, temple bell echoing in distance."),
    ("05-ilvaazhkkai/22-n22_ascetic_visiting_virtuous_home.jpg", "Kural 46: Forest ascetic admiring the householder's virtue",
     "Photorealistic 16:9 cinematic film still, a wandering saffron-clad sage standing at the garden gate looking upon the disciplined, loving household with deep admiration and folded palms."),
    ("05-ilvaazhkkai/23-n23_blooming_sacred_tulsi_thara.jpg", "Kural 46: Sacred altar at the heart of home",
     "Photorealistic 16:9 cinematic film still, carved terracotta tulsi altar in courtyard bathed in warm morning light, brass diya glowing, red hibiscus blossoms placed in veneration."),
    ("05-ilvaazhkkai/24-n24_pure_domestic_altar.jpg", "Kural 46: The household as a living sanctuary",
     "Photorealistic 16:9 cinematic film still, inner sanctum room of a traditional home, sandalwood paste, fresh jasmine, and a brass bell on a low stone pedestal, peaceful sacred stillness."),

    # Kural 47: Foremost among all seekers is the righteous householder
    ("05-ilvaazhkkai/25-n25_householder_guiding_villagers.jpg", "Kural 47: The householder as the pillar of society",
     "Photorealistic 16:9 cinematic film still, village square beneath a spreading banyan, the upright householder mediating a community discussion with calm wisdom, respected by all."),
    ("05-ilvaazhkkai/26-n26_sustaining_community_reservoir.jpg", "Kural 47: Maintaining the communal water tank",
     "Photorealistic 16:9 cinematic film still, householder working alongside farmers desilting and reinforcing the stone embankments of the village lotus tank, collective diligence in the morning sun."),
    ("05-ilvaazhkkai/27-n27_weaving_cloth_for_monks.jpg", "Kural 47: Weaving coarse cotton robes for hermits",
     "Photorealistic 16:9 cinematic film still, traditional wooden handloom in an open workshop, rhythmic weaving of unbleached cotton shawls intended as gifts for forest mendicants."),
    ("05-ilvaazhkkai/28-n28_harvesting_medicinal_herbs.jpg", "Kural 47: Harvesting healing herbs for the afflicted",
     "Photorealistic 16:9 cinematic film still, householder gathering neem and thulasi leaves into a woven basket in a sunlit herb garden to heal sick neighbors, compassionate smile."),

    # Kural 48: Helping others on virtue's path while walking it himself
    ("05-ilvaazhkkai/29-n29_teaching_children_values.jpg", "Kural 48: Instructing youth in virtue and dharma",
     "Photorealistic 16:9 cinematic film still, householder seated on a raised stone pyol teaching village children how to carve Tamil script onto palm leaves, patient guiding hand."),
    ("05-ilvaazhkkai/30-n30_supporting_pilgrims_road.jpg", "Kural 48: Maintaining a roadside rest-hall for pilgrims",
     "Photorealistic 16:9 cinematic film still, ancient stone mandapam by the highway where pilgrims rest in the heat of midday, large earthen pots filled with cool cardamom-scented water."),
    ("05-ilvaazhkkai/31-n31_reconciling_quarreling_neighbors.jpg", "Kural 48: Restoring peace among estranged neighbors",
     "Photorealistic 16:9 cinematic film still, rustic village lane, householder joining the hands of two formerly arguing farmers, soothing tensions with gentle upright words."),
    ("05-ilvaazhkkai/32-n32_lamp_lit_at_village_crossroads.jpg", "Kural 48: Lighting the way for midnight wayfarers",
     "Photorealistic 16:9 cinematic film still, householder placing an oil lamp into a carved stone niche at a rural crossroad as night falls, warm beacon guiding lone travelers."),

    # Kural 49: Domestic life rightly lived is supreme righteousness
    ("05-ilvaazhkkai/33-n33_bountiful_paddy_threshing.jpg", "Kural 49: The joyful threshing of righteous grain",
     "Photorealistic 16:9 cinematic film still, circular threshing floor in golden sunlight, bullocks treading golden grain stalks, family tossing chaff into the breeze, joyful abundance."),
    ("05-ilvaazhkkai/34-n34_distributing_first_harvest.jpg", "Kural 49: Sharing the first fruits of harvest with temples and the needy",
     "Photorealistic 16:9 cinematic film still, bullock cart laden with fresh sheaves of paddy arriving at the village temple gate, householder presenting baskets to the priest and gathered poor."),
    ("05-ilvaazhkkai/35-n35_clean_home_rangoli_threshold.jpg", "Kural 49: Graceful rice-flour kolam at sunrise",
     "Photorealistic 16:9 cinematic film still, high-angle view of a woman drawing intricate geometric white rice-flour kolam on red mud ground before the wooden doorway, birds pecking grain nearby."),
    ("05-ilvaazhkkai/36-n36_harmonious_evening_meal.jpg", "Kural 49: Peace and gratitude around the domestic board",
     "Photorealistic 16:9 cinematic film still, three generations seated together on reed mats enjoying a simple evening meal of steamed rice and dal, oil lamps casting a warm comforting amber glow."),

    # Kural 50: Living truly on earth, one is counted among gods in heaven
    ("05-ilvaazhkkai/37-n37_revered_elder_householder.jpg", "Kural 50: The venerated householder in the twilight of life",
     "Photorealistic 16:9 cinematic film still, aged householder with snow-white hair and serene luminous eyes, seated beneath an ancient peepal tree with village elders bowing in deep reverence."),
    ("05-ilvaazhkkai/38-n38_celestial_glow_over_courtyard.jpg", "Kural 50: Divine blessings falling upon the righteous home",
     "Photorealistic 16:9 cinematic film still, night sky filled with countless sparkling stars over the tiled roofs of the virtuous village homestead, gentle cool breeze swaying coconut palms."),
    ("05-ilvaazhkkai/39-n39_jasmine_petals_floating_water.jpg", "Kural 50: Purity that transcends the earthly realm",
     "Photorealistic 16:9 cinematic macro shot, fresh white jasmine petals and pink lotus petals floating gently on the crystal-clear water of a stone uruli bowl, reflection of golden morning sky."),
    ("05-ilvaazhkkai/40-n40_sunlit_homestead_orchard.jpg", "Kural 50: The flourishing earthly paradise of dharma",
     "Photorealistic 16:9 cinematic wide shot, sprawling Tamil countryside at golden hour, lush orchards of mango and jackfruit, thriving domestic cattle returning home, idyllic peace."),
    ("05-ilvaazhkkai/41-n41_householder_looking_at_horizon.jpg", "Kural 50: Fulfilled life gazing into the eternal horizon",
     "Photorealistic 16:9 cinematic shot, householder standing on a hillock overlooking his peaceful village at sunset, calm dignified silhouette against glowing clouds of orange and violet."),
    ("05-ilvaazhkkai/42-n42_eternal_temple_gateway_dusk.jpg", "Kural 50: The immortal glory of the domestic path",
     "Photorealistic 16:9 cinematic grand wide shot, ancient temple gopuram illuminated by hundreds of earthen oil lamps at dusk, peaceful pilgrims and families walking together in sacred communion.")
]

# Chapter 8: அன்புடைமை (Anbudaimai - Loving-Kindness / Affection) - 35 shots
CH08_PROMPTS = [
    # Kural 71: Can love be bolted shut? Tender tears reveal it
    ("08-anbudaimai/01-n01_tears_of_joy_mother_child.jpg", "Kural 71: Mother embracing returning child with tears of joy",
     "Photorealistic 16:9 cinematic close-up, an ancient Tamil mother weeping tears of overwhelming joy as she tightly embraces her young son returned from a long journey, tender morning light."),
    ("08-anbudaimai/02-n02_reunion_of_parted_friends.jpg", "Kural 71: Parted friends meeting after years",
     "Photorealistic 16:9 cinematic film still, two Tamil elders clasping each other's shoulders at a village gate, tears glistening in their eyes, sincere overwhelming affection, afternoon sun."),
    ("08-anbudaimai/03-n03_tender_care_of_injured_bird.jpg", "Kural 71: Loving hands sheltering a wounded dove",
     "Photorealistic 16:9 cinematic macro shot, weathered gentle hands cupping an injured white dove, applying cooling herbal paste to its wing, morning dew on leaves nearby."),
    ("08-anbudaimai/04-n04_weeping_for_another_sorrow.jpg", "Kural 71: Spontaneous tears of empathy for a stranger's grief",
     "Photorealistic 16:9 cinematic shot, village well at dusk, a compassionate woman gently comforting a grieving weeping widow with an embrace of profound heartfelt empathy."),

    # Kural 72: The loveless claim everything for themselves; the loving give even their bones
    ("08-anbudaimai/05-n05_miser_hoarding_in_darkness.jpg", "Kural 72: The unloving miser clutching wealth in shadows",
     "Photorealistic 16:9 cinematic film still, a harsh selfish merchant alone in a gloomy stone room counting copper coins with paranoid eyes, cold shadow and solitary isolation."),
    ("08-anbudaimai/06-n06_generous_giver_offering_all.jpg", "Kural 72: The loving soul sharing the last loaf of bread",
     "Photorealistic 16:9 cinematic film still, a poor Tamil laborer smiling warmly as he breaks his only millet flatbread in half to hand to a hungry stray child, golden dusty light."),
    ("08-anbudaimai/07-n07_heroic_sacrifice_saving_fellows.jpg", "Kural 72: Giving even one's body for another's life",
     "Photorealistic 16:9 cinematic dramatic shot, ancient storm on a turbulent river, a brave youth diving into swirling waters to rescue a drowning villager, selfless courage."),

    # Kural 73: Love binds the soul to human fellowship
    ("08-anbudaimai/08-n08_circle_of_friends_under_tree.jpg", "Kural 73: Deep communion of affectionate fellowship",
     "Photorealistic 16:9 cinematic film still, Sangam-era village pavilion, a circle of men and women of different trades laughing and sharing stories under a spreading peepal tree at sunset."),
    ("08-anbudaimai/09-n09_shared_labor_in_paddy_field.jpg", "Kural 73: Joyful shared labor rooted in mutual fondness",
     "Photorealistic 16:9 cinematic film still, line of Tamil women transplanting emerald green paddy seedlings in a flooded field, singing folk songs together in bright morning sunlight."),
    ("08-anbudaimai/10-n10_elders_sharing_pan_and_laughter.jpg", "Kural 73: Sweet companionship in old age",
     "Photorealistic 16:9 cinematic shot, two elderly friends sitting on a granite temple step sharing betel leaves, their crinkled faces beaming with decades of loyal affection."),

    # Kural 74: Love begets yearning, and yearning begets boundless friendship
    ("08-anbudaimai/11-n11_pacing_veranda_awaiting_friend.jpg", "Kural 74: Yearning heart watching the distant road",
     "Photorealistic 16:9 cinematic film still, a thoughtful Tamil woman standing on a wooden veranda looking toward a dusty highway winding over hills at twilight, waiting for a loved one."),
    ("08-anbudaimai/12-n12_warm_embrace_of_companions.jpg", "Kural 74: Boundless friendship blooming from sincere affection",
     "Photorealistic 16:9 cinematic film still, open green meadow with distant hills, two travelling scholars walking arm-in-arm, animatedly discussing poetry, evening breeze in their robes."),
    ("08-anbudaimai/13-n13_gift_of_fresh_lotus_garland.jpg", "Kural 74: Offering a fragrant garland to an esteemed companion",
     "Photorealistic 16:9 cinematic shot, hands presenting a freshly woven garland of pink lotus and fragrant vetiver roots, token of pure unselfish devotion, soft lamp light."),

    # Kural 75: Earthly joy and heavenly bliss are both fruits of love
    ("08-anbudaimai/14-n14_playful_family_under_mango_boughs.jpg", "Kural 75: Bliss of affectionate family life on earth",
     "Photorealistic 16:9 cinematic wide shot, lush shady mango orchard, parents laughing as children chase peacocks on green grass, idyllic warmth and unforced happiness."),
    ("08-anbudaimai/15-n15_serene_transcendent_peace.jpg", "Kural 75: Heaven brought down to earth through love",
     "Photorealistic 16:9 cinematic film still, an ancient stone pond reflecting towering white gopuram at sunrise, sacred swans gliding calmly across still water, ethereal mist."),
    ("08-anbudaimai/16-n16_evening_cradle_lullaby.jpg", "Kural 75: Sacred lullaby sung in peaceful dusk",
     "Photorealistic 16:9 cinematic shot, dim cozy bedroom lit by a single wick, mother softly singing to soothe her resting child, profound contentment and timeless grace."),

    # Kural 76: Ignorant say love aids only virtue; it is also the shield against vice
    ("08-anbudaimai/17-n17_forgiving_reformed_thief.jpg", "Kural 76: Love disarming an aggressive assailant",
     "Photorealistic 16:9 cinematic film still, rustic village path at dusk, an unarmed gentle sage responding to an angry youth with calm eyes and an open palm, the youth lowering his club in awe."),
    ("08-anbudaimai/18-n18_reconciling_feuding_tribes.jpg", "Kural 76: Loving diplomacy extinguishing ancient blood feuds",
     "Photorealistic 16:9 cinematic film still, torchlit courtyard, chieftain placing down weapons and embracing his rival leader, solemn peace treaty signed on palm leaf."),
    ("08-anbudaimai/19-n19_healing_a_bitter_heart.jpg", "Kural 76: Melting stubborn malice with unyielding warmth",
     "Photorealistic 16:9 cinematic medium shot, an elderly sister gently feeding her bitter ailing brother, his hard expression softening into grateful tears, warm interior light."),

    # Kural 77: The sun burns the boneless worm; virtue burns the unloving man
    ("08-anbudaimai/20-n20_boneless_worm_in_scorching_sun.jpg", "Kural 77: The boneless insect withering in desert heat",
     "Photorealistic 16:9 cinematic macro shot, dry cracked earth under a blazing noon sun, a tiny fragile earthworm shriveling on parched red soil, heat ripples in the air."),
    ("08-anbudaimai/21-n21_miserable_loneliness_of_unloving.jpg", "Kural 77: The cold misery of the unloving soul",
     "Photorealistic 16:9 cinematic film still, a harsh callous man sitting alone in a grand empty mansion, shadows closing around him while life and music thrive outside his locked gates."),
    ("08-anbudaimai/22-n22_withering_barren_desert_tree.jpg", "Kural 77: Parched leafless thorn tree in barren waste",
     "Photorealistic 16:9 cinematic wide shot, vast desolate salt desert under a stark blinding sky, a single twisted dead thorn tree casting a thin skeletal shadow."),

    # Kural 78: Life without love is like a dead withered sapling trying to bloom in stony desert
    ("08-anbudaimai/23-n23_dry_stump_in_rocky_ground.jpg", "Kural 78: Withered dry stump amidst arid boulders",
     "Photorealistic 16:9 cinematic shot, dry rocky hillside, a brittle dead tree branch snapping in dry wind, unable to produce green leaves or blossoms, desolate wasteland."),
    ("08-anbudaimai/24-n24_hopeless_striving_without_affection.jpg", "Kural 78: Fruitless exertion devoid of love",
     "Photorealistic 16:9 cinematic film still, a gloomy scholar surrounded by towering dry scrolls, his face hollow and lifeless, knowledge turned to ash without love."),
    ("08-anbudaimai/25-n25_contrast_of_lush_oasis.jpg", "Kural 78: The blossoming oasis fed by loving waters",
     "Photorealistic 16:9 cinematic shot, vibrant green oasis surrounded by desert, clear bubbling spring nourishing flourishing date palms and fragrant white flowers, refreshing cool breeze."),

    # Kural 79: External organs are useless if the inner heart lacks love
    ("08-anbudaimai/26-n26_handsome_exterior_cold_eyes.jpg", "Kural 79: Regal silks covering a lifeless cold heart",
     "Photorealistic 16:9 cinematic film still, a handsome aristocrat draped in ornate gold brocade and pearls, staring into a polished bronze mirror with eyes completely devoid of warmth."),
    ("08-anbudaimai/27-n27_humble_ragged_man_overflowing_love.jpg", "Kural 79: Poor beggar with radiant loving eyes",
     "Photorealistic 16:9 cinematic film still, an impoverished old man in patched coarse cloth, smiling with heavenly radiance as he gently strokes a scruffy village dog resting on his lap."),
    ("08-anbudaimai/28-n28_sculpting_the_hollow_statue.jpg", "Kural 79: A hollow stone statue compared to living feeling",
     "Photorealistic 16:9 cinematic shot, sculptor carving a polished marble idol, cold chisel striking lifeless stone, contrasting with a warm human hand reaching out in affection."),

    # Kural 80: The body with love is a living body; without it, merely bones clad in skin
    ("08-anbudaimai/29-n29_vibrant_living_pulse_of_love.jpg", "Kural 80: The radiant glow of a life inhabited by love",
     "Photorealistic 16:9 cinematic medium close-up, a Tamil woman radiating vitality and gentle beauty, laughing as she braids flowers into her daughter's hair, sunlight catching her smile."),
    ("08-anbudaimai/30-n30_hollow_skeleton_clad_in_skin.jpg", "Kural 80: Parable of the hollow walking skeleton",
     "Photorealistic 16:9 cinematic film still, a shadowy figure walking mechanically down a gloomy corridor, brooding and detached, mere bone and skin wandering in spiritual death."),
    ("08-anbudaimai/31-n31_child_running_into_open_arms.jpg", "Kural 80: Ecstatic rush of pure living love",
     "Photorealistic 16:9 cinematic wide shot, golden meadow filled with wildflowers, a little girl running with boundless joy toward her father who drops to his knees with open arms."),
    ("08-anbudaimai/32-n32_sacred_flame_of_the_loving_heart.jpg", "Kural 80: Eternal flame burning within the soul",
     "Photorealistic 16:9 cinematic macro shot, a pure flame in a polished bronze lamp resting upon carved granite, burning steadily without smoke, casting amber warmth over sacred carvings."),
    ("08-anbudaimai/33-n33_village_celebrating_in_unity.jpg", "Kural 80: Entire community flourishing in mutual love",
     "Photorealistic 16:9 cinematic wide vista, festival evening in a Tamil village, neighbors embracing, sharing sweets on palm leaves, temple lamps twinkling across the pond."),
    ("08-anbudaimai/34-n34_sunset_over_placid_lotus_lake.jpg", "Kural 80: Peace of a life anchored in universal affection",
     "Photorealistic 16:9 cinematic wide landscape, tranquil river valley at dusk, soft rose and gold reflections on water, peaceful heron flying low over blooming lotus pads."),
    ("08-anbudaimai/35-n35_morning_sunlight_illuminating_lovers.jpg", "Kural 80: Dawn of everlasting loving-kindness",
     "Photorealistic 16:9 cinematic majestic panoramic shot, golden sunrise breaking over ancient hills, illuminating temples, homes, and rivers in an embrace of warm celestial light.")
]

# Chapter 16: பொறையுடைமை (Poraiyudaimai - Forbearance / Forgiveness) - 62 shots
# Kural 151: Bearing with those who insult, like earth bearing those who dig into her (151-160)
CH16_PROMPTS = [
    # Kural 151: Earth bearing those who excavate her
    ("16-poraiyudaimai/01-n01_earth_bearing_diggers_plow.jpg", "Kural 151: Mother Earth enduring the sharp plow and pickaxe",
     "Photorealistic 16:9 cinematic film still, farmers digging deep irrigation trenches into rich dark soil with iron hoes, the fertile earth yielding cool water and green shoots without wrath, golden dawn."),
    ("16-poraiyudaimai/02-n02_quarrymen_hewing_mountain.jpg", "Kural 151: The mighty mountain enduring the chisel without complaint",
     "Photorealistic 16:9 cinematic film still, stone quarry on a rugged hill, masons cleaving massive granite blocks, the ancient silent mountain standing majestic and unmoving against the blue sky."),
    ("16-poraiyudaimai/03-n03_sage_hearing_harsh_abuse.jpg", "Kural 151: Noble sage calmly hearing the insults of an angry man",
     "Photorealistic 16:9 cinematic film still, ancient stone mandapam, an arrogant young man gesturing aggressively, while a serene Tamil sage listens with peaceful dignified eyes and steady breath."),
    ("16-poraiyudaimai/04-n04_deep_well_yielding_sweet_water.jpg", "Kural 151: The excavated well offering sweet water in return",
     "Photorealistic 16:9 cinematic film still, crystal-clear water gushing from a deep-cut stone stepwell, villagers lowering brass pots, returning bounty for being cut into."),
    ("16-poraiyudaimai/05-n05_serene_monk_under_banyan.jpg", "Kural 151: The unshakable calm of the patient soul",
     "Photorealistic 16:9 cinematic wide shot, vast ancient banyan tree with hanging aerial roots, an ascetic seated in deep meditation, breeze rustling leaves, majestic stillness."),
    ("16-poraiyudaimai/06-n06_fertile_delta_after_digging.jpg", "Kural 151: Endless green crops rising from cut furrows",
     "Photorealistic 16:9 cinematic landscape, vast fertile Kaveri river delta, freshly turned dark soil now blooming with tender green paddy shoots under gentle morning rain."),

    # Kural 152: Forgive always; but forgetting the offense is greater than forgiving
    ("16-poraiyudaimai/07-n07_releasing_written_grievance.jpg", "Kural 152: Burning the record of past slights",
     "Photorealistic 16:9 cinematic close-up, a wise man holding an old palm-leaf debt scroll over a sacred fire, watching the harsh words turn to glowing ash and floating sparks."),
    ("16-poraiyudaimai/08-n08_embracing_former_slanderer.jpg", "Kural 152: Welcoming the former enemy without memory of fault",
     "Photorealistic 16:9 cinematic film still, courtyard doorway, a gracious nobleman warmly embracing a man who had wronged him, showing no trace of suspicion, pure open-hearted grace."),
    ("16-poraiyudaimai/09-n09_writing_insult_on_sand_washed_by_wave.jpg", "Kural 152: Words written in sand washed away by the ocean",
     "Photorealistic 16:9 cinematic macro shot, ocean beach at sunset, foamy sea wave sweeping over harsh scrawls in wet sand, leaving a smooth pristine shore of untouched gold."),
    ("16-poraiyudaimai/10-n10_gentle_smile_erasing_past_pain.jpg", "Kural 152: The peace of a mind that has forgotten injury",
     "Photorealistic 16:9 cinematic portrait, elderly Tamil elder with kind wrinkled face looking up into morning sunlight, smile free from bitterness or lingering resentment."),
    ("16-poraiyudaimai/11-n11_flowing_river_carrying_debris.jpg", "Kural 152: River washing away fallen twigs and dirt",
     "Photorealistic 16:9 cinematic shot, fast-flowing mountain stream carrying away fallen dry branches, leaving clear sparkling pebble-strewn water sparkling in sunlight."),
    ("16-poraiyudaimai/12-n12_restored_friendship_temple_steps.jpg", "Kural 152: Joy of brotherhood renewed through total forgiveness",
     "Photorealistic 16:9 cinematic film still, temple steps at golden hour, two former rivals walking together in genuine cordiality, completely unburdened by past disputes."),

    # Kural 153: Poverty of poverty is turning away guests; strength of strength is bearing with fools
    ("16-poraiyudaimai/13-n13_patient_counselor_with_stubborn_fool.jpg", "Kural 153: Patient scholar listening calmly to an ignorant boaster",
     "Photorealistic 16:9 cinematic film still, royal library, a boisterous arrogant visitor speaking loudly while the master scholar listens with tranquil composed smile."),
    ("16-poraiyudaimai/14-n14_iron_pillar_withstanding_monsoon_gusts.jpg", "Kural 153: The granite pillar standing firm against harsh winds",
     "Photorealistic 16:9 cinematic wide shot, towering ancient stone pillar of a temple standing unshaken amidst swirling winds and dust, symbol of heroic endurance."),
    ("16-poraiyudaimai/15-n15_compassionate_guidance_of_errant_child.jpg", "Kural 153: Father gently correcting a misbehaving child",
     "Photorealistic 16:9 cinematic film still, sunlit veranda, patient father calmly kneeling before his weeping, headstrong boy, wiping his tears with loving understanding."),
    ("16-poraiyudaimai/16-n16_quiet_strength_in_village_assembly.jpg", "Kural 153: Supreme strength revealed in silence",
     "Photorealistic 16:9 cinematic film still, village council meeting, noisy disputes around, but the central respected elder remains serenely silent until passions cool."),
    ("16-poraiyudaimai/17-n17_deep_lake_absorbing_thrown_stone.jpg", "Kural 153: The deep lake swallowing a stone with calm ripples",
     "Photorealistic 16:9 cinematic shot, peaceful forest lake, a stone creating concentric gentle ripples on the glass-like water before returning to unbroken mirror stillness."),
    ("16-poraiyudaimai/18-n18_venerable_teacher_with_unruly_students.jpg", "Kural 153: Preceptor patiently repeating lessons for slow learners",
     "Photorealistic 16:9 cinematic film still, outdoor gurukulam, elderly teacher smiling patiently as he re-demonstrates astronomy calculations on sand board."),

    # Kural 154: If you desire greatness to endure, cultivate forbearance
    ("16-poraiyudaimai/19-n19_granite_temple_standing_centuries.jpg", "Kural 154: Granite monument weathering centuries",
     "Photorealistic 16:9 cinematic majestic wide shot, colossal Brihadisvara-style granite temple standing magnificent against evening sunset, eternal enduring grandeur."),
    ("16-poraiyudaimai/20-n20_monarch_granting_pardon_to_rebels.jpg", "Kural 154: King commuting sentence to pardon rebellious peasants",
     "Photorealistic 16:9 cinematic film still, grand audience hall, crowned Tamil monarch gesturing down to forgive kneeling frightened rebel farmers, winning their everlasting loyalty."),
    ("16-poraiyudaimai/21-n21_ancient_olive_tree_bearing_fruit.jpg", "Kural 154: Century-old tree flourishing through all seasons",
     "Photorealistic 16:9 cinematic shot, massive gnarled trunk of an ancient fruiting tree spreading broad green boughs laden with blossoms, sheltering birds and travelers."),
    ("16-poraiyudaimai/22-n22_scholar_inscribing_virtue_on_copper.jpg", "Kural 154: Inscribing the virtues of patient rulers on copper plates",
     "Photorealistic 16:9 cinematic macro shot, engraver using a sharp burin on a polished copper plate, carving Tamil script recording acts of sovereign mercy."),
    ("16-poraiyudaimai/23-n23_sunrise_over_timeless_hills.jpg", "Kural 154: Enduring dawn of an untarnished reputation",
     "Photorealistic 16:9 cinematic wide vista, dawn mist rising over ancient Western Ghats mountain ridges, golden sunlight spilling across untouched valleys."),
    ("16-poraiyudaimai/24-n24_noble_statue_unmoved_by_birds.jpg", "Kural 154: Silent dignity of true inner majesty",
     "Photorealistic 16:9 cinematic shot, carved stone dvarapala guardian statue in morning light, pigeons resting on its shoulder, serene strength without anger."),

    # Kural 155: Wise do not esteem the vengeful; they treasure the forgiving like gold
    ("16-poraiyudaimai/25-n25_goldsmith_testing_gold_touchstone.jpg", "Kural 155: Testing fine gold on the black touchstone",
     "Photorealistic 16:9 cinematic macro shot, Tamil goldsmith drawing a streak of pure gold across an urai-kal touchstone, examining the brilliant golden luster in lamp light."),
    ("16-poraiyudaimai/26-n26_hasty_wrathful_man_derided_by_crowd.jpg", "Kural 155: The vengeful hothead ignored by the wise",
     "Photorealistic 16:9 cinematic film still, village street, an angry man shouting and waving his fists, while respectable elders walk past without turning their heads."),
    ("16-poraiyudaimai/27-n27_casket_of_pure_gems_opened.jpg", "Kural 155: Treasuring the forgiving soul like precious jewels",
     "Photorealistic 16:9 cinematic shot, an ornate brass-bound sandalwood coffer opened to reveal glistening uncut rubies and pearls nestled in white velvet silk."),
    ("16-poraiyudaimai/28-n28_elders_honoring_the_patient_peacemaker.jpg", "Kural 155: Village elders seating the forgiving mediator in the seat of honor",
     "Photorealistic 16:9 cinematic film still, open village chavadi, elders ceremonially draping a white silk angavastram over the shoulders of a man who refused revenge."),
    ("16-poraiyudaimai/29-n29_pure_pearl_drawn_from_ocean.jpg", "Kural 155: Rare pearl formed by patient endurance within the shell",
     "Photorealistic 16:9 cinematic macro shot, open oyster shell resting on wet timber deck of a boat, revealing a flawless lustrous pearl glistening in the morning sun."),
    ("16-poraiyudaimai/30-n30_peaceful_haven_amidst_storm.jpg", "Kural 155: The patient soul as an unassailable fortress",
     "Photorealistic 16:9 cinematic wide shot, storm clouds gathering dark over sea, but a sturdy wooden lighthouse pavilion stands bright and warm with glowing lanterns."),

    # Kural 156: Joy of revenge lasts a single day; glory of forbearance lasts till end of time
    ("16-poraiyudaimai/31-n31_short_lived_hollow_triumph_of_spite.jpg", "Kural 156: The fleeting empty smirk of petty revenge",
     "Photorealistic 16:9 cinematic film still, shadowy alley, an angry youth looking down at a broken cart he vandalized, an expression of sudden emptiness and remorse on his face."),
    ("16-poraiyudaimai/32-n32_timeless_song_of_the_forgiving_hero.jpg", "Kural 156: Minstrels singing praises of a merciful king",
     "Photorealistic 16:9 cinematic film still, ancient royal court, wandering Panar bards strumming yazh harps, chanting verses celebrating the monarch's historic pardon."),
    ("16-poraiyudaimai/33-n33_memorial_hero_stone_with_palm_shade.jpg", "Kural 156: Ancient nadukal hero stone shaded by blooming flowers",
     "Photorealistic 16:9 cinematic shot, moss-covered hero stone carved with an upright chieftain, red kaner flowers resting at its base, golden late afternoon sun."),
    ("16-poraiyudaimai/34-n34_epigraph_recording_peace_treaty.jpg", "Kural 156: Everlasting inscription of peaceful reconciliation",
     "Photorealistic 16:9 cinematic close-up, granite wall of a thousand-year-old temple covered in sharp Tamil inscriptions detailing everlasting amnesty and peace."),
    ("16-poraiyudaimai/35-n35_starry_night_over_ancient_city.jpg", "Kural 156: Glory enduring like eternal constellations",
     "Photorealistic 16:9 cinematic majestic night shot, brilliant Milky Way arching across clear indigo sky above silhouettes of ancient temple gopurams and sleeping houses."),
    ("16-poraiyudaimai/36-n36_children_learning_of_magnanimity.jpg", "Kural 156: Storyteller recounting tales of great magnanimity to youth",
     "Photorealistic 16:9 cinematic film still, courtyard under lantern light, grandfather narrating ancient lore to wide-eyed grandchildren seated on woven mats."),

    # Kural 157: Though injured, do not retaliate with evil; return only good
    ("16-poraiyudaimai/37-n37_sandalwood_tree_perfuming_axe.jpg", "Kural 157: Sandalwood tree perfuming the axe that cuts it",
     "Photorealistic 16:9 cinematic shot, deep forest glade, fragrant chips of yellow sandalwood falling around the base of a cut tree, releasing rich sweet incense aroma."),
    ("16-poraiyudaimai/38-n38_physician_dressing_enemy_wounds.jpg", "Kural 157: Tamil physician tending to wounded enemy soldiers",
     "Photorealistic 16:9 cinematic film still, battlefield tent after truce, a skilled Tamil healer gently washing and bandaging the sword cut of a fallen adversary."),
    ("16-poraiyudaimai/39-n39_giving_sweet_water_to_the_insolent.jpg", "Kural 157: Offering cool palm juice to an insolent traveler",
     "Photorealistic 16:9 cinematic film still, village wayside booth, gracious woman handing a fresh earthen cup of sweet neera to a brash traveler who demanded it rudely."),
    ("16-poraiyudaimai/40-n40_returning_lost_cattle_to_rival.jpg", "Kural 157: Driving lost cows back to a neighbor who spoke ill",
     "Photorealistic 16:9 cinematic film still, green meadow, honest farmer leading straying calves safely back to the gate of an estranged envious neighbor."),
    ("16-poraiyudaimai/41-n41_planting_fruit_trees_on_border.jpg", "Kural 157: Planting fruiting trees along disputed boundaries",
     "Photorealistic 16:9 cinematic shot, boundary stone between two farms, householder planting sweet pomegranate sapling for both families to enjoy."),
    ("16-poraiyudaimai/42-n42_lighting_lamp_for_estranged_kin.jpg", "Kural 157: Placing an oil lamp outside to guide a straying brother home",
     "Photorealistic 16:9 cinematic shot, dark rainy night, gentle hands placing an oil lantern inside a brass protective lantern case on the front gate post."),

    # Kural 158: Overcome the insolent by patient forbearance; their own shame will defeat them
    ("16-poraiyudaimai/43-n43_insolent_man_hanging_head_in_shame.jpg", "Kural 158: The aggressor bowing his head in sudden burning shame",
     "Photorealistic 16:9 cinematic film still, village square, an arrogant aggressor suddenly dropping his eyes and hanging his head in humiliation before the calm dignity of the victim."),
    ("16-poraiyudaimai/44-n44_mirror_of_unbroken_peace.jpg", "Kural 158: Unbroken calm acting as a mirror to folly",
     "Photorealistic 16:9 cinematic portrait, serene Tamil scholar looking at an agitated interlocutor with boundless compassion, completely disarming his rage."),
    ("16-poraiyudaimai/45-n45_cool_snow_quenching_embers.jpg", "Kural 158: Cooling mist extinguishing scattered sparks",
     "Photorealistic 16:9 cinematic macro shot, glowing red charcoal embers being gently quenched by falling cool water drops, rising soft white steam."),
    ("16-poraiyudaimai/46-n46_aggressor_dropping_weapons.jpg", "Kural 158: Conquering hostility without raising a hand",
     "Photorealistic 16:9 cinematic film still, dusty road at sunset, a bandit letting his iron-tipped staff slip from his fingers, overwhelmed by an old saint's fearless calm."),
    ("16-poraiyudaimai/47-n47_reformed_offender_seeking_pardon.jpg", "Kural 158: Offender falling to his knees asking forgiveness",
     "Photorealistic 16:9 cinematic film still, pillared verandah, a humbled man bowing low touching the feet of the elder he wronged, receiving a gentle blessing hand."),
    ("16-poraiyudaimai/48-n48_crowd_murmuring_respect_for_patience.jpg", "Kural 158: Onlookers praising the steadfast dignity of the wronged",
     "Photorealistic 16:9 cinematic film still, bustling market street, onlookers nodding in deep respect at a merchant who quietly refused to engage in a brawl."),

    # Kural 159: Greater than ascetics who fast are those who bear the harsh words of others
    ("16-poraiyudaimai/49-n49_austere_ascetic_on_mountain_peak.jpg", "Kural 159: The mountain ascetic enduring harsh fasting",
     "Photorealistic 16:9 cinematic wide shot, solitary rocky mountain ledge at sunrise, an emaciated hermit sitting motionless in intense tapaskriya meditation."),
    ("16-poraiyudaimai/50-n50_humble_householder_absorbing_revilement.jpg", "Kural 159: The householder possessing even greater spiritual tapas",
     "Photorealistic 16:9 cinematic film still, busy village lane, a humble weaver smiling peacefully as an unruly cart driver berates him, inner tapas shining in his eyes."),
    ("16-poraiyudaimai/51-n51_scales_weighing_fasting_vs_forbearance.jpg", "Kural 159: The balance tipping in favor of forbearance",
     "Photorealistic 16:9 cinematic symbolic shot, ancient brass scales in a temple hall, sacred darbha grass on one side and a gentle white flower of patience heavily outweighing it."),
    ("16-poraiyudaimai/52-n52_pure_radiance_of_patient_soul.jpg", "Kural 159: Luminous serenity surpassing all mortifications",
     "Photorealistic 16:9 cinematic close-up, peaceful smiling face of an ordinary Tamil villager who harbors no grudge, eyes glowing with heavenly clarity."),
    ("16-poraiyudaimai/53-n53_monsoon_downpour_unmoved_lotus.jpg", "Kural 159: Lotus petal holding steadfast under heavy rain",
     "Photorealistic 16:9 cinematic macro shot, torrential rain pounding a pond, but a pristine pink lotus bloom stands proud and intact, beads of water rolling harmlessly off."),
    ("16-poraiyudaimai/54-n54_saintly_presence_calming_village.jpg", "Kural 159: A living master bringing peace to troubled hearts",
     "Photorealistic 16:9 cinematic wide shot, village under the twilight sky, villagers gathering peacefully around a beloved patient elder seated on a stone platform."),

    # Kural 160: Ascetics practice renunciation through hunger; forbearance renounces retaliation
    ("16-poraiyudaimai/55-n55_hermit_abstaining_from_food.jpg", "Kural 160: Ascetic practicing supreme fast in forest hermitage",
     "Photorealistic 16:9 cinematic shot, quiet bamboo hermitage, hermit meditating before a simple clay lamp, water pot beside him, sublime ascetic discipline."),
    ("16-poraiyudaimai/56-n56_hero_swallowing_his_own_anger.jpg", "Kural 160: The spiritual warrior conquering his own impulse of revenge",
     "Photorealistic 16:9 cinematic portrait, a strong warrior closing his eyes, taking a deep breath, and releasing his clenched fist, mastering himself completely."),
    ("16-poraiyudaimai/57-n57_cooling_stream_in_forest_sanctuary.jpg", "Kural 160: Cool crystal waters quenching all burning passion",
     "Photorealistic 16:9 cinematic landscape, pristine forest river cascading gently over smooth river stones, wild ferns and moss glowing in soft morning sunlight."),
    ("16-poraiyudaimai/58-n58_sacred_bull_calmly_resting.jpg", "Kural 160: The majestic temple bull resting in tranquil majesty",
     "Photorealistic 16:9 cinematic shot, magnificent white Kangeyam temple bull with adorned horns lying peacefully in temple courtyard, birds resting on its back."),
    ("16-poraiyudaimai/59-n59_open_heavens_above_patient_earth.jpg", "Kural 160: Vast endless sky embracing the patient earth",
     "Photorealistic 16:9 cinematic grand vista, endless green plains under an immense canopy of soft cumulus clouds and golden afternoon light, boundless freedom."),
    ("16-poraiyudaimai/60-n60_community_celebrating_in_reconciliation.jpg", "Kural 160: Universal harmony born of mutual forbearance",
     "Photorealistic 16:9 cinematic film still, wide shot of an ancient Tamil town square at dusk, families strolling, merchants chatting, children playing, total peaceful security."),
    ("16-poraiyudaimai/61-n61_temple_gopuram_against_setting_sun.jpg", "Kural 160: Enduring monument of patience reaching the heavens",
     "Photorealistic 16:9 cinematic wide shot, towering granite temple gopuram silhouetted against a breathtaking crimson and gold sunset, sacred flags fluttering."),
    ("16-poraiyudaimai/62-n62_eternal_flame_in_granite_sanctum.jpg", "Kural 160: The inextinguishable light of forbearance",
     "Photorealistic 16:9 cinematic close-up, single golden flame burning steadily in a deep granite niche inside an ancient temple corridor, defying darkness and drafts.")
]

# Chapter 25: அருளுடைமை (Aruludaimai - Universal Compassion / Grace) - 37 shots
CH25_PROMPTS = [
    # Kural 241: Wealth of grace is the supreme wealth; material wealth exists even for the base
    ("25-aruludaimai/01-n01_gold_coins_scattered_ground.jpg", "Kural 241: Material wealth held by the unworthy",
     "Photorealistic 16:9 cinematic film still, heavy bronze chest overflowing with dull copper and gold coins lying on flagstones, while a callous rich man looks on with cold anxious eyes."),
    ("25-aruludaimai/02-n02_compassionate_hands_cradling_fawn.jpg", "Kural 241: The priceless wealth of universal mercy",
     "Photorealistic 16:9 cinematic film still, gentle hands of a forest sage in unbleached cotton cradling a trembling newborn spotted deer, morning sun rays piercing forest canopy."),
    ("25-aruludaimai/03-n03_radiant_smile_of_saintly_soul.jpg", "Kural 241: Inward treasure of grace shining on human face",
     "Photorealistic 16:9 cinematic portrait, elderly Tamil saint with eyes shining with unconditional love, surrounded by blooming thulasi and gentle forest breeze, golden hour."),
    ("25-aruludaimai/04-n04_sharing_wealth_with_humble_creatures.jpg", "Kural 241: Scattering grains for birds at dawn",
     "Photorealistic 16:9 cinematic film still, courtyard flagstones, compassionate woman scattering handfuls of golden grain, surrounded by dozens of descending sparrows and doves."),

    # Kural 242: Seek by worthy ways and cleave to grace; even in doubt, grace is the only ally
    ("25-aruludaimai/05-n05_walking_the_righteous_forest_path.jpg", "Kural 242: Walking the narrow forest path of virtue",
     "Photorealistic 16:9 cinematic wide shot, tranquil ancient trail through bamboo groves, a solitary seeker in simple robes walking barefoot with mindful steps, dappled sunlight."),
    ("25-aruludaimai/06-n06_saving_fallen_insects_from_water.jpg", "Kural 242: Rescuing tiny drowning insects from a lotus pond",
     "Photorealistic 16:9 cinematic macro shot, a gentle wooden leaf used to lift a struggling golden honeybee out of clear pond water onto a dry floating lotus leaf."),
    ("25-aruludaimai/07-n07_monk_clearing_thorns_from_public_road.jpg", "Kural 242: Removing sharp thorns from the path of others",
     "Photorealistic 16:9 cinematic shot, dusty rural lane, a traveling monk bending down to carefully pick up thorny acacia twigs so that barefoot pilgrims may walk unharmed."),
    ("25-aruludaimai/08-n08_guiding_lantern_in_misty_night.jpg", "Kural 242: Grace as an infallible beacon in times of perplexity",
     "Photorealistic 16:9 cinematic film still, dark misty riverside, a warm brass lantern held aloft cutting through swirling fog, illuminating the safe ford across the river."),

    # Kural 243: The kingdom of heaven does not belong to those without grace
    ("25-aruludaimai/09-n09_celestial_heavens_closed_to_the_callous.jpg", "Kural 243: The gates of light barred against cruelty",
     "Photorealistic 16:9 cinematic atmospheric shot, dark storm clouds veiling the stars, a cold stone doorway closed tight, symbol of spiritual exclusion for the heartless."),
    ("25-aruludaimai/10-n10_radiant_temple_welcoming_compassionate.jpg", "Kural 243: The luminous abode of universal grace",
     "Photorealistic 16:9 cinematic grand wide shot, sunlit golden temple mandapam glowing with ethereal light, white swans, blooming lotuses, and radiant peaceful atmosphere."),
    ("25-aruludaimai/11-n11_feeding_stray_animals_in_rain.jpg", "Kural 243: Mercy extended to homeless creatures",
     "Photorealistic 16:9 cinematic film still, under a thatched eaves during rain, a young boy lovingly placing a leaf plate of cooked food before a shivering stray dog, gentle smile."),

    # Kural 244: Those who protect all beings will never see fearful realms
    ("25-aruludaimai/12-n12_guardian_of_forest_wildlife.jpg", "Kural 244: Forest warden coexisting with wild elephants",
     "Photorealistic 16:9 cinematic film still, dense misty jungle, wild herd of majestic elephants peacefully grazing near an ancient stone hermitage, unalarmed by the resident sage."),
    ("25-aruludaimai/13-n13_sheltering_nesting_birds.jpg", "Kural 244: Protecting bird nests in temple eaves",
     "Photorealistic 16:9 cinematic shot, carved wooden rafters of an ancient shrine, mother swallow feeding her chirping chicks safely, protected from harm by worshippers."),
    ("25-aruludaimai/14-n14_fearless_sleep_under_the_stars.jpg", "Kural 244: The fearless tranquility of the compassionate soul",
     "Photorealistic 16:9 cinematic film still, open stone platform beside an ancient banyan, a peaceful hermit sleeping peacefully under a sky full of stars, completely free of anxiety."),
    ("25-aruludaimai/15-n15_animals_drinking_at_peaceful_pool.jpg", "Kural 244: Forest pool where tiger and deer drink together",
     "Photorealistic 16:9 cinematic wide shot, serene forest watering hole at sunset, various wild creatures drinking quietly side by side in harmony, golden reflections on still water."),

    # Kural 245: The broad earth witness that grief visits not those whose souls are full of grace
    ("25-aruludaimai/16-n16_bountiful_earth_yielding_fruits.jpg", "Kural 245: The grateful earth blessing the merciful",
     "Photorealistic 16:9 cinematic wide vista, rolling green hills of Tamil countryside bursting with ripe jackfruit, bananas, and coconut palms under a bright blue sky."),
    ("25-aruludaimai/17-n17_free_from_grief_in_old_age.jpg", "Kural 245: A peaceful conscience free from all sorrow",
     "Photorealistic 16:9 cinematic portrait, serene elderly woman in unbleached cotton saree holding prayer beads, her face unblemished by bitter regrets or lingering guilt."),
    ("25-aruludaimai/18-n18_healer_curing_sick_village_cow.jpg", "Kural 245: Gentle healer bandaging the leg of a calf",
     "Photorealistic 16:9 cinematic film still, rustic village cattle pen, gentle cowherd applying cooling turmeric and neem poultice to a limping calf, affection in every movement."),

    # Kural 246: Those who abandon grace and act cruelly forget their own true self
    ("25-aruludaimai/19-n19_cruel_hunter_snaring_beasts.jpg", "Kural 246: The tragic blindness of cruelty",
     "Photorealistic 16:9 cinematic film still, dark tangled jungle at twilight, a grim hunter hiding behind thorny bushes with a heavy net, trapped in his own cycle of fear and violence."),
    ("25-aruludaimai/20-n20_haunted_sleepless_night_of_oppressor.jpg", "Kural 246: The torment of an unmerciful heart",
     "Photorealistic 16:9 cinematic film still, shadowy chamber, a harsh tax collector tossing restlessly on a silk bed, haunted by the cries of those he dispossessed."),
    ("25-aruludaimai/21-n21_freeing_caged_birds_into_sky.jpg", "Kural 246: Opening the cage door to the open sky",
     "Photorealistic 16:9 cinematic shot, temple terrace, hands opening the wicker door of a cage, green parakeets bursting into joyous flight against a vibrant blue morning sky."),

    # Kural 247: As this world belongs not to the penniless, the other belongs not to the unmerciful
    ("25-aruludaimai/22-n22_penniless_man_turned_from_market.jpg", "Kural 247: The penniless turned away from earthly commerce",
     "Photorealistic 16:9 cinematic film still, bustling ancient bazaar, a man with empty pockets unable to purchase goods, illustrating the necessity of the currency of grace."),
    ("25-aruludaimai/23-n23_the_spiritual_currency_of_grace.jpg", "Kural 247: The spiritual passport to heavenly liberation",
     "Photorealistic 16:9 cinematic symbolic shot, radiant warm light streaming through carved stone temple columns, illuminating lotus flowers and fragrant sandalwood offerings."),
    ("25-aruludaimai/24-n24_monk_sharing_water_with_thirsting_dog.jpg", "Kural 247: Pouring precious water for a parched animal",
     "Photorealistic 16:9 cinematic film still, dusty roadside in scorching heat, a traveling monk pouring the last cup of cool water from his brass kamandalam for a thirsty dog."),

    # Kural 248: The impoverished can regain wealth; those who lose grace are utterly bankrupt
    ("25-aruludaimai/25-n25_bankrupt_merchant_rebuilding_enterprise.jpg", "Kural 248: Ruined merchant recovering prosperity through diligent labor",
     "Photorealistic 16:9 cinematic film still, harbour dockside, an energetic merchant reviewing new timber manifests, rising again from poverty through honest labor."),
    ("25-aruludaimai/26-n26_hollow_ruin_of_a_callous_tyrant.jpg", "Kural 248: Irrecoverable ruin of the heart that lost mercy",
     "Photorealistic 16:9 cinematic wide shot, abandoned fortress crumbling on a barren hill, dry wind howling through empty arched windows, desolate ruin."),
    ("25-aruludaimai/27-n27_restoring_fading_plant_with_water.jpg", "Kural 248: Reviving a drooping jasmine vine with fresh water",
     "Photorealistic 16:9 cinematic macro shot, dry drooping flower vine springing back to life as crystal droplets of water are poured gently onto its parched roots."),

    # Kural 249: Can one without grace perform virtue? As well can a blind man see in darkness
    ("25-aruludaimai/28-n28_blind_man_stumbling_in_the_dark.jpg", "Kural 249: Attempting virtue without love is like stumbling in darkness",
     "Photorealistic 16:9 cinematic film still, shadowy rocky cavern, a blindfolded figure grasping blindly at shadows, unable to find the illuminated exit."),
    ("25-aruludaimai/29-n29_lamp_of_grace_illuminating_all_dharma.jpg", "Kural 249: Grace as the essential flame that gives life to all virtues",
     "Photorealistic 16:9 cinematic shot, ornate seven-wick brass oil lamp burning brightly, casting warm golden illumination over sacred manuscripts and fresh blossoms."),
    ("25-aruludaimai/30-n30_mechanical_ritual_without_heart.jpg", "Kural 249: Hollow ritual lacking genuine compassion",
     "Photorealistic 16:9 cinematic film still, priest performing fire offerings mechanically with distracted indifferent eyes, smoke billowing without inner warmth."),
    ("25-aruludaimai/31-n31_child_hugging_mother_pure_grace.jpg", "Kural 249: Pure spontaneous warmth transcending all rules",
     "Photorealistic 16:9 cinematic shot, little girl spontaneously embracing a weeping village elder, offering a wild yellow flower, pure instinctive compassion."),

    # Kural 250: When tempted to oppress the weak, remember how you tremble before the mighty
    ("25-aruludaimai/32-n32_bully_oppressing_fragile_peasant.jpg", "Kural 250: Cruel official lording over a helpless farmer",
     "Photorealistic 16:9 cinematic film still, village street, an arrogant bailiff intimidating a frail elderly peasant, holding a heavy stick threatingly."),
    ("25-aruludaimai/33-n33_the_same_bully_trembling_before_king.jpg", "Kural 250: The same oppressor cowering before the royal throne",
     "Photorealistic 16:9 cinematic film still, grand palace audience hall, the arrogant bailiff trembling prostrate on polished granite before the stern gaze of the king."),
    ("25-aruludaimai/34-n34_releasing_the_weak_with_mercy.jpg", "Kural 250: Remembering one's own vulnerability and staying one's hand",
     "Photorealistic 16:9 cinematic film still, warrior lowering his sword, remembering mercy, and offering his hand to help up a fallen defeated opponent."),
    ("25-aruludaimai/35-n35_sanctuary_of_grace_for_all_beings.jpg", "Kural 250: Universal sanctuary where none fear the strong",
     "Photorealistic 16:9 cinematic wide shot, sacred grove surrounding an ancient granite temple, deer, peacocks, cattle, and humans resting together in peace."),
    ("25-aruludaimai/36-n36_sunset_glow_over_river_ferry.jpg", "Kural 250: The gentle ferryman carrying all across the flood",
     "Photorealistic 16:9 cinematic wide shot, wide calm river at sunset, wooden ferryboat carrying villagers, monks, and stray animals safely to the opposite shore."),
    ("25-aruludaimai/37-n37_golden_dawn_of_universal_compassion.jpg", "Kural 250: The boundless ocean of universal divine grace",
     "Photorealistic 16:9 cinematic panoramic sunrise, golden light reflecting across calm ocean waves, distant sailing ships, gulls soaring freely in warm morning air.")
]

# Chapter 30: வாய்மை (Vaaimai - Truthfulness) - 41 shots
CH30_PROMPTS = [
    # Kural 291: Truthfulness is speech devoid of every taint of harmfulness
    ("30-vaaimai/01-n01_unblemished_speech_of_the_sage.jpg", "Kural 291: Pure speech that wounds no living soul",
     "Photorealistic 16:9 cinematic film still, serene Tamil philosopher seated under an ancient portico, speaking with gentle dignity to attentive seekers, soft morning light."),
    ("30-vaaimai/02-n02_crystal_water_flowing_over_white_stones.jpg", "Kural 291: Truth flowing clear and harmless like mountain spring",
     "Photorealistic 16:9 cinematic macro shot, crystal-clear water flowing over smooth white river pebbles, pristine transparency without a single speck of silt."),
    ("30-vaaimai/03-n03_refusing_to_speak_cruel_truths.jpg", "Kural 291: Choosing harmless silence over destructive bluntness",
     "Photorealistic 16:9 cinematic film still, royal council chamber, a thoughtful minister closing his lips thoughtfully, refusing to utter gossip that would destroy an innocent life."),
    ("30-vaaimai/04-n04_honeyed_pure_words_comforting_grief.jpg", "Kural 291: Healing words grounded in pure truth",
     "Photorealistic 16:9 cinematic film still, rustic veranda, gentle physician speaking words of calm reassuring truth to an anxious mother, bringing peace to her heart."),

    # Kural 292: Even falsehood is reckoned as truth if it brings unblemished good to others
    ("30-vaaimai/05-n05_saving_fleeing_innocent_from_bandits.jpg", "Kural 292: Diverting ruthless pursuers to save an innocent life",
     "Photorealistic 16:9 cinematic film still, crossroad in ancient forest, an upright traveler calmly pointing pursuers away from the hidden grove where frightened refugees hide."),
    ("30-vaaimai/06-n06_reconciling_quarreling_brothers_with_kindness.jpg", "Kural 292: Healing a family breach with benevolent tact",
     "Photorealistic 16:9 cinematic film still, village courtyard, a wise grandfather telling estranged brothers of each other's secret enduring affection, uniting their hands."),
    ("30-vaaimai/07-n07_shielding_the_helpless_orphan.jpg", "Kural 292: Protecting a helpless orphan from cruel oppressors",
     "Photorealistic 16:9 cinematic film still, rustic doorway, a courageous woman sheltering a frightened child behind her saree, answering ruthless bailiffs with fearless calm."),
    ("30-vaaimai/08-n08_the_supreme_motive_of_spotless_good.jpg", "Kural 292: Spotless benevolence as the true essence of truth",
     "Photorealistic 16:9 cinematic symbolic shot, ancient brass weighing balance, words of mercy balancing perfectly with the radiant light of truth."),

    # Kural 293: Let no one speak what his conscience knows to be false; his conscience will burn him
    ("30-vaaimai/09-n09_guilty_witness_tormented_by_conscience.jpg", "Kural 293: Torment of a man who bore false witness",
     "Photorealistic 16:9 cinematic film still, dark room at midnight, a false witness clutching his head in anguish beside a dying candle, burning with inner shame."),
    ("30-vaaimai/10-n10_pure_unflinching_gaze_of_honest_man.jpg", "Kural 293: The fearless, unclouded gaze of an honest witness",
     "Photorealistic 16:9 cinematic portrait, an ancient Tamil farmer in village court looking directly into the judge's eyes with crystal clear, unwavering integrity."),
    ("30-vaaimai/11-n11_fire_burning_within_the_breast.jpg", "Kural 293: The inner fire of conscience consuming falsehood",
     "Photorealistic 16:9 cinematic dramatic close-up, a glowing ember burning brightly in dark volcanic rock, symbol of the unquenchable flame of moral conscience."),
    ("30-vaaimai/12-n12_confessing_fault_and_finding_peace.jpg", "Kural 293: Confessing the truth and reclaiming inner freedom",
     "Photorealistic 16:9 cinematic film still, temple steps at sunrise, a young man bowing before village elders, speaking the honest truth, weight lifting from his soul."),

    # Kural 294: One who lives true to his own conscience reigns in the hearts of all the world
    ("30-vaaimai/13-n13_revered_magistrate_enthroned_in_hearts.jpg", "Kural 294: The truthful judge beloved by the entire populace",
     "Photorealistic 16:9 cinematic film still, village square under a sacred neem tree, an upright magistrate seated on a granite platform, citizens gazing upon him with absolute trust."),
    ("30-vaaimai/14-n14_merchant_trusted_without_written_bonds.jpg", "Kural 294: The merchant whose spoken word is gold",
     "Photorealistic 16:9 cinematic film still, spice market, trading partners shaking hands over a deal without parchment or seals, relying solely on the merchant's pure word."),
    ("30-vaaimai/15-n15_universal_love_for_the_truthful.jpg", "Kural 294: Children and elders gathering warmly around the truthful man",
     "Photorealistic 16:9 cinematic film still, sunlit village lane, the honest schoolmaster walking amidst laughing children and bowing farmers, beloved by every soul."),
    ("30-vaaimai/16-n16_radiance_of_unbroken_integrity.jpg", "Kural 294: Light of integrity shining like the midday sun",
     "Photorealistic 16:9 cinematic portrait, elderly Tamil scholar standing on temple platform, serene dignity and spotless integrity radiating from his peaceful face."),

    # Kural 295: Greater than penance and charity combined is truthfulness lived in the heart
    ("30-vaaimai/17-n17_scales_comparing_penance_and_truth.jpg", "Kural 295: Truthfulness outweighing thousand austerities",
     "Photorealistic 16:9 cinematic symbolic shot, grand stone temple sanctum, brass balance with golden coins and ascetic beads on one pan, and the simple lotus of truth outbalancing both."),
    ("30-vaaimai/18-n18_hermit_meditating_on_snowy_peak.jpg", "Kural 295: Austere tapas on Himalayan crags",
     "Photorealistic 16:9 cinematic wide shot, breathtaking snow-covered mountain peak, solitary ascetic sitting in padmasana amidst swirling white mist."),
    ("30-vaaimai/19-n19_simple_truthful_artisan_at_his_loom.jpg", "Kural 295: Simple weaver living flawless truth at his handloom",
     "Photorealistic 16:9 cinematic film still, sunlit village workshop, honest weaver crafting fine white cotton cloth with meticulous care, inner holiness surpassing hermits."),
    ("30-vaaimai/20-n20_giving_alms_with_ostentation.jpg", "Kural 295: Charity without truth is a hollow shell",
     "Photorealistic 16:9 cinematic film still, wealthy patron tossing coins to a crowd for applause, contrasted with the quiet, unpraised integrity of the truthful man."),

    # Kural 296: Truthfulness yields all glory without effort; it brings every other virtue in its train
    ("30-vaaimai/21-n21_spontaneous_flowering_of_virtues.jpg", "Kural 296: All virtues following truth like attendants of a queen",
     "Photorealistic 16:9 cinematic artistic wide shot, lush royal botanical garden in full bloom, countless fragrant flowers blooming along a stone pathway of pure white marble."),
    ("30-vaaimai/22-n22_effortless_esteem_of_the_truthful.jpg", "Kural 296: The effortless honour awarded to the honest",
     "Photorealistic 16:9 cinematic film still, grand council of Sangam scholars, poet of unwavering truth invited to take the primary seat without having to seek it."),
    ("30-vaaimai/23-n23_unshakable_reputation_like_granite_pillar.jpg", "Kural 296: Reputation standing firm as an eternal pillar",
     "Photorealistic 16:9 cinematic shot, monolithic granite pillar of Mahabalipuram carved with sacred lions, standing tall against ocean spray and centuries."),
    ("30-vaaimai/24-n24_pure_white_pearl_without_blemish.jpg", "Kural 296: Spotless pearl reflecting pure daylight",
     "Photorealistic 16:9 cinematic macro shot, single enormous flawless white pearl resting on a dark velvet cloth, reflecting clear sky and morning sun without imperfection."),

    # Kural 297: If one cleaves to truthfulness, there is no need for any other austerity
    ("30-vaaimai/25-n25_seeker_laying_aside_ascetic_staff.jpg", "Kural 297: Laying aside external rituals in favor of pure truth",
     "Photorealistic 16:9 cinematic film still, temple corridor, an enlightened disciple placing down his ascetic waterpot and staff, walking forward with simple unadorned truth."),
    ("30-vaaimai/26-n26_the_sacred_fire_within_the_heart.jpg", "Kural 297: The inward flame of truth replacing sacrificial fires",
     "Photorealistic 16:9 cinematic close-up, glowing embers of a sacred homam hearth fading into peaceful grey ash, while a devotee meditates in stillness."),
    ("30-vaaimai/27-n27_walking_unharmed_through_briars.jpg", "Kural 297: Walking safely through life protected by truth alone",
     "Photorealistic 16:9 cinematic shot, barefoot traveler walking calmly along a stony thorny path without stumbling, golden sunset illuminating his path."),
    ("30-vaaimai/28-n28_pure_mountain_stream_mirroring_heavens.jpg", "Kural 297: Unbroken reflection of truth in still water",
     "Photorealistic 16:9 cinematic landscape, pristine alpine lake reflecting snow-capped peaks and azure sky with glassy perfection, silence and peace."),

    # Kural 298: Water cleanses external body; truth cleanses inward soul
    ("30-vaaimai/29-n29_ritual_bathing_in_sacred_river.jpg", "Kural 298: Washing the body in the holy Kaveri waters",
     "Photorealistic 16:9 cinematic film still, river ghat at sunrise, pilgrims bathing in flowing river waters, pouring water over heads with brass chembu pots."),
    ("30-vaaimai/30-n30_truth_purifying_the_inner_sanctum.jpg", "Kural 298: Truth cleansing the hidden recesses of the heart",
     "Photorealistic 16:9 cinematic portrait, devotee with eyes closed in meditation, a soft golden inner light appearing to illuminate his chest and face, radiant purity."),
    ("30-vaaimai/31-n31_polishing_bronze_mirror_to_clarity.jpg", "Kural 298: Polishing away the grime of deceit",
     "Photorealistic 16:9 cinematic close-up, craftsman polishing an ancient Aranmula metal mirror, wiping away grey paste to reveal a blindingly bright, undistorted reflection."),
    ("30-vaaimai/32-n32_clear_spring_washing_away_mud.jpg", "Kural 298: Fresh gushing spring clearing turbid mud",
     "Photorealistic 16:9 cinematic macro shot, fresh subterranean spring bubbling up through white sand, instantly carrying away cloudy sediment to leave pure drinking water."),

    # Kural 299: All lamps are not lamps; the lamp of truth untainted by falsehood is the only true light
    ("30-vaaimai/33-n33_thousands_of_temple_oil_lamps.jpg", "Kural 299: Rows of clay lamps glittering along temple walls",
     "Photorealistic 16:9 cinematic wide shot, Karthigai Deepam festival night, thousands of flickering terracotta agal vilakku lamps illuminating the granite steps of a temple tank."),
    ("30-vaaimai/34-n34_the_single_eternal_lamp_of_truth.jpg", "Kural 299: The solitary flame of truth outshining all earthly lights",
     "Photorealistic 16:9 cinematic close-up, a single steady brass oil lamp in a dark stone sanctum, its clear luminous flame casting long warm shadows across ancient inscriptions."),
    ("30-vaaimai/35-n35_morning_sun_dispelling_all_shadows.jpg", "Kural 299: The sun of truth rising over the world",
     "Photorealistic 16:9 cinematic grand wide shot, brilliant golden sunrise breaking through dark clouds over ancient Tamil city, banishing all darkness and fog."),
    ("30-vaaimai/36-n36_lantern_guiding_traveler_through_marsh.jpg", "Kural 299: The reliable lantern that never blows out in the wind",
     "Photorealistic 16:9 cinematic film still, night traveler walking safely along a narrow embankment between deep marshes, guided by an oil lantern with an unbroken steady flame."),

    # Kural 300: Of all great truths we have scrutinized, nothing surpasses truthfulness
    ("30-vaaimai/37-n37_scholars_examining_ancient_scrolls.jpg", "Kural 300: Sages scrutinizing all sacred philosophical treatises",
     "Photorealistic 16:9 cinematic film still, grand stone academy library, venerable grey-bearded Tamil philosophers unrolling tied palm-leaf texts under tall arches, nodding in agreement."),
    ("30-vaaimai/38-n38_poet_carving_the_final_conclusion.jpg", "Kural 300: Inscribing the supreme truth with iron stylus",
     "Photorealistic 16:9 cinematic close-up, iron stylus etching clear Tamil Brahmi characters onto a golden-brown dried palmyra leaf, recording the supremacy of truth."),
    ("30-vaaimai/39-n39_summit_of_the_sacred_mountain.jpg", "Kural 300: The highest summit of moral attainment",
     "Photorealistic 16:9 cinematic majestic wide shot, highest granite peak of Arunachala at dawn, bathed in pure golden sunlight above rolling seas of white morning clouds."),
    ("30-vaaimai/40-n40_universal_assembly_honoring_truth.jpg", "Kural 300: Mankind uniting under the banner of spotless truth",
     "Photorealistic 16:9 cinematic film still, panoramic view of a massive festival concourse outside a temple gopuram, diverse citizens moving together in peace and mutual trust."),
    ("30-vaaimai/41-n41_golden_horizon_of_eternal_truth.jpg", "Kural 300: The eternal, unfading light of truth across the ages",
     "Photorealistic 16:9 cinematic cinematic final wide shot, vast calm ocean meeting a glowing golden sunset horizon, calm water reflecting an infinite sky of peace.")
]

# Chapter 31: வெகுளாமை (Vegulaamai - Restraint from Anger) - 52 shots
CH31_PROMPTS = [
    # Kural 301: Restrain anger where it has power to strike; where powerless, what matters anger?
    ("31-vegulaamai/01-n01_monarch_holding_back_wrath.jpg", "Kural 301: King staying his hand against a helpless prisoner",
     "Photorealistic 16:9 cinematic film still, ancient palace judgment hall, crowned monarch closing his eyes and signaling royal guards to lower their drawn swords, sparing a kneeling offender."),
    ("31-vegulaamai/02-n02_master_withholding_rebuke_to_servant.jpg", "Kural 301: Wealthy master restraining anger toward a clumsy servant",
     "Photorealistic 16:9 cinematic film still, dining hall, a trembling servant has dropped a ceramic jar, the master takes a deep breath and smiles with forgiving reassurance."),
    ("31-vegulaamai/03-n03_futile_fury_against_mighty_fortress.jpg", "Kural 301: The pointlessness of anger where one is powerless",
     "Photorealistic 16:9 cinematic film still, lone figure shouting fruitlessly at the base of colossal granite fortress walls, dust blowing in the wind, depicting impotent rage."),
    ("31-vegulaamai/04-n04_deep_breath_of_self_command.jpg", "Kural 301: The calm mastery of staying one's own strike",
     "Photorealistic 16:9 cinematic portrait, a powerful Tamil warrior lowering his raised fist, his tense jaw relaxing into serene self-discipline, morning mist around him."),
    ("31-vegulaamai/05-n05_sovereign_peace_in_council.jpg", "Kural 301: Supreme ruler mastering irritation during heated debate",
     "Photorealistic 16:9 cinematic film still, council of war, heated ministers shouting, while the wise commander remains completely still, hand resting lightly on his armrest."),

    # Kural 302: Anger against the powerless is evil; against the powerful it is impossible and futile
    ("31-vegulaamai/06-n06_protecting_the_vulnerable_child.jpg", "Kural 302: Refusing to vent frustration upon a frightened child",
     "Photorealistic 16:9 cinematic film still, village courtyard, a weary artisan putting down his mallet, kneeling down to comfort his weeping child instead of scolding, warm twilight."),
    ("31-vegulaamai/07-n07_raging_against_a_storm_wind.jpg", "Kural 302: Like striking a granite mountain with bare hands",
     "Photorealistic 16:9 cinematic wide shot, sea cliff during a gale, massive waves crashing against ancient black basalt rocks, unyielding against the fury of the ocean."),
    ("31-vegulaamai/08-n08_quelling_the_bully_instinct.jpg", "Kural 302: Uprooting petty dominance over the weak",
     "Photorealistic 16:9 cinematic film still, market stalls, a merchant stepping in between an angry bully and a meek porter, calmly settling the dispute with fairness."),
    ("31-vegulaamai/09-n09_serenity_amidst_adversity.jpg", "Kural 302: Noble equanimity in face of insurmountable obstacles",
     "Photorealistic 16:9 cinematic film still, ruined field after storm, farmer looking at fallen stalks not with rage, but with calm determination to replant in morning light."),
    ("31-vegulaamai/10-n10_gentle_handling_of_young_beast.jpg", "Kural 302: Patient training of an unruly young bullock",
     "Photorealistic 16:9 cinematic film still, cattle pen, kind farmer gently stroking the head of a frightened young ox, soothing its panic with soft words and sweet grass."),

    # Kural 303: Forget anger against everyone; from anger spring countless evils
    ("31-vegulaamai/11-n11_forest_fire_ignited_by_single_spark.jpg", "Kural 303: A single spark of wrath engulfing an entire forest",
     "Photorealistic 16:9 cinematic wide shot, dry bamboo forest at dusk, wind whipping small embers into an expanding wall of blazing fire and billowing black smoke."),
    ("31-vegulaamai/12-n12_shattered_friendship_from_angry_word.jpg", "Kural 303: Bitter regret after hasty angry accusation",
     "Photorealistic 16:9 cinematic film still, stone veranda, two close friends turned away from each other in stony silence, broken clay pot on the floor between them."),
    ("31-vegulaamai/13-n13_letting_go_of_the_burning_coal.jpg", "Kural 303: Dropping the burning coal of resentment",
     "Photorealistic 16:9 cinematic macro close-up, a human hand letting go of a glowing charcoal briquette, letting it fall onto wet stone where it hisses out in harmless steam."),
    ("31-vegulaamai/14-n14_clearing_storm_clouds_at_sunset.jpg", "Kural 303: Anger dissipating like evening rainclouds",
     "Photorealistic 16:9 cinematic wide landscape, violent storm clouds breaking apart over a serene river valley, revealing peaceful glowing lavender and golden twilight sky."),
    ("31-vegulaamai/15-n15_brother_reconciling_with_brother.jpg", "Kural 303: Banishment of anger bringing instant peace",
     "Photorealistic 16:9 cinematic film still, courtyard under neem tree, two brothers clasping forearms, smiles returning as anger melts away into mutual forgiveness."),

    # Kural 304: Is there an enemy greater than anger, which destroys joy and peace of mind?
    ("31-vegulaamai/16-n16_wrath_distorting_handsome_face.jpg", "Kural 304: Fury disfiguring a noble countenance",
     "Photorealistic 16:9 cinematic dramatic portrait, intense chiaroscuro lighting on a man gripped by sudden rage, clenched jaw, wild eyes, inner poison destroying his beauty."),
    ("31-vegulaamai/17-n17_smiling_peace_of_the_tranquil_sage.jpg", "Kural 304: The sublime beauty of unruffled peace",
     "Photorealistic 16:9 cinematic portrait, serene Tamil sage with relaxed brow and kind gentle eyes, radiating profound happiness and contentment in morning light."),
    ("31-vegulaamai/18-n18_ruined_banquet_hall_after_brawl.jpg", "Kural 304: Joy murdered by an outburst of temper",
     "Photorealistic 16:9 cinematic film still, festive hall with overturned wooden tables, spilt wine, scattered garlands, and silent empty gloom after an angry dispute."),
    ("31-vegulaamai/19-n19_tranquil_pond_reflecting_lotus.jpg", "Kural 304: Joy restored to the unruffled soul",
     "Photorealistic 16:9 cinematic shot, mirror-smooth water of a temple pond reflecting pink blooming lotus flowers and morning sky without a single ripple of agitation."),
    ("31-vegulaamai/20-n20_peaceful_sleep_free_from_vengeance.jpg", "Kural 304: Sweet untroubled sleep of the anger-free",
     "Photorealistic 16:9 cinematic film still, simple bedroom, householder sleeping peacefully with a relaxed smile, cool night breeze stirring linen curtains."),

    # Kural 305: Guard yourself against anger; unguarding it will destroy yourself
    ("31-vegulaamai/21-n21_warrior_guarding_his_own_heart.jpg", "Kural 305: Vigilance over one's own rising temper",
     "Photorealistic 16:9 cinematic film still, stone fortress battlements, a veteran warrior pausing, closing his eyes, and breathing deeply to master his rising temper."),
    ("31-vegulaamai/22-n22_wildfire_consuming_the_tree_that_sparked_it.jpg", "Kural 305: The fire consuming its own source",
     "Photorealistic 16:9 cinematic dramatic shot, dry hollow tree trunk burning furiously from within, flames leaping out of knot-holes, self-destruction of wrath."),
    ("31-vegulaamai/23-n23_cool_water_poured_over_steaming_head.jpg", "Kural 305: Pouring cool water to quench internal heat",
     "Photorealistic 16:9 cinematic shot, riverbank at noon, a man pouring a brass vessel of cool river water over his head, water droplets flying in golden sunlight."),
    ("31-vegulaamai/24-n24_stout_shield_deflecting_fiery_darts.jpg", "Kural 305: Shield of forbearance protecting the soul",
     "Photorealistic 16:9 cinematic close-up, a polished bronze shield effortlessly deflecting flaming sparks, standing undamaged and gleaming."),
    ("31-vegulaamai/25-n25_restful_sanctuary_of_the_disciplined.jpg", "Kural 305: The invulnerable peace of the self-guarded",
     "Photorealistic 16:9 cinematic wide shot, quiet monastery courtyard surrounded by carved granite pillars, monk sweeping dry leaves in rhythmic meditative peace."),

    # Kural 306: The fire of anger consumes not only you, but your kin and heritage
    ("31-vegulaamai/26-n26_conflagration_sweeping_ancient_homestead.jpg", "Kural 306: Fire consuming the ancestral home",
     "Photorealistic 16:9 cinematic wide shot, tragic silhouette of a burning wooden hall against night sky, family standing weeping in distance, parable of destructive anger."),
    ("31-vegulaamai/27-n27_tears_of_family_caught_in_feud.jpg", "Kural 306: Kinfolk mourning the consequences of a hothead's wrath",
     "Photorealistic 16:9 cinematic film still, dim courtyard, mother and children weeping together as the father is led away in chains after an angry brawl."),
    ("31-vegulaamai/28-n28_prosperous_dynasty_in_harmony.jpg", "Kural 306: Preservation of lineage through peaceful restraint",
     "Photorealistic 16:9 cinematic wide shot, thriving Tamil homestead with multiple generations laughing, harvesting grain together, cattle thriving, golden sunlight."),
    ("31-vegulaamai/29-n29_smoldering_ruins_of_quarrelsome_clan.jpg", "Kural 306: Ash and silence where rage once ruled",
     "Photorealistic 16:9 cinematic shot, overgrown ruined stone courtyard, blackened hearth stones with weed growing through cracks, solemn cautionary landscape."),
    ("31-vegulaamai/30-n30_tender_reunion_of_family_clan.jpg", "Kural 306: Loving protection of kin through sweet patience",
     "Photorealistic 16:9 cinematic film still, festival feast, large extended family dining happily together on plantain leaves, absolute trust and domestic bliss."),

    # Kural 307: Striking the ground with one's hand hurts only oneself; so does anger fail of target
    ("31-vegulaamai/31-n31_striking_the_hard_ground_in_fury.jpg", "Kural 307: Striking the stone floor with bare fist in futile rage",
     "Photorealistic 16:9 cinematic close-up, an angry man striking the unyielding granite floor with his clenched fist, bruising his knuckles while the earth remains unmoved."),
    ("31-vegulaamai/32-n32_calm_target_unscathed_by_wrath.jpg", "Kural 307: The serene target untouched by another's scream",
     "Photorealistic 16:9 cinematic film still, temple steps, a peaceful saint smiling gently while a passerby rants, the saint's robe fluttering gently in the breeze."),
    ("31-vegulaamai/33-n33_throwing_dust_against_the_wind.jpg", "Kural 307: Throwing dust against the wind, blowing back into one's eyes",
     "Photorealistic 16:9 cinematic dramatic shot, sandy road, an angry traveler hurling red dust into the wind, only for the gust to blow it directly back into his own face."),
    ("31-vegulaamai/34-n34_the_immovable_rock_amidst_breaker.jpg", "Kural 307: The rock that breaks the surging wave",
     "Photorealistic 16:9 cinematic shot, ocean shore, towering black rock standing majestic while frothing white waves crash harmlessly and shatter into foam."),
    ("31-vegulaamai/35-n35_soothing_the_bruised_hand_with_balm.jpg", "Kural 307: Learning the bitter lesson of self-inflicted pain",
     "Photorealistic 16:9 cinematic film still, veranda, a humbled youth sheepishly applying herbal oil to his bruised hand, smiling ruefully at his own past foolish anger."),

    # Kural 308: Though one causes you injury as painful as burning fire, refrain from wrath
    ("31-vegulaamai/36-n36_walking_through_flames_of_provocation.jpg", "Kural 308: Enduring searing provocation like heat of a furnace",
     "Photorealistic 16:9 cinematic dramatic shot, blacksmith forge, glowing molten metal being hammered, sparks flying, symbolizing intense fiery provocation."),
    ("31-vegulaamai/37-n37_gentle_response_to_a_searing_insult.jpg", "Kural 308: Returning gentle cool words to burning accusations",
     "Photorealistic 16:9 cinematic film still, village council, an elder listening to venomous words with calm eyes, then responding in soft melodious tones that disarm all."),
    ("31-vegulaamai/38-n38_soothing_sandalwood_paste_on_burns.jpg", "Kural 308: Applying cool sandalwood to soothe burns",
     "Photorealistic 16:9 cinematic macro close-up, fingers applying fragrant white sandalwood paste onto scorched skin, instant relief and fragrant steam."),
    ("31-vegulaamai/39-n39_green_shoots_rising_after_fire.jpg", "Kural 308: Tender green shoots sprouting from scorched grass",
     "Photorealistic 16:9 cinematic macro shot, charred earth after brushfire, delicate emerald-green blades of grass and tiny yellow flowers pushing up into sunshine."),
    ("31-vegulaamai/40-n40_unshaken_majesty_in_the_face_of_harm.jpg", "Kural 308: Divine fortitude standing calm amidst betrayal",
     "Photorealistic 16:9 cinematic portrait, dignified Tamil leader looking forward with steadfast resolve and forgiveness after being wronged by trusted allies."),

    # Kural 309: If a man harbored no anger in his heart, whatever he wishes will be instantly his
    ("31-vegulaamai/41-n41_ascetic_whose_word_comes_to_pass.jpg", "Kural 309: The sage whose blessings instantly manifest",
     "Photorealistic 16:9 cinematic film still, forest hermitage at sunrise, an anger-free rishi raising his palm in gentle blessing, golden light bathing a kneeling farmer."),
    ("31-vegulaamai/42-n42_nature_cooperating_with_the_gentle.jpg", "Kural 309: Wild creatures eating from the hands of the peaceful",
     "Photorealistic 16:9 cinematic shot, sunlit clearing, colorful songbirds, squirrels, and wild hares gathered fearlessly around an elder sitting quietly on a mossy log."),
    ("31-vegulaamai/43-n43_effortless_abundance_of_the_peaceful_home.jpg", "Kural 309: All desires fulfilled in the anger-free household",
     "Photorealistic 16:9 cinematic wide shot, prosperous rural homestead, granaries overflowing with golden grain, cows giving milk, children healthy and laughing."),
    ("31-vegulaamai/44-n44_crystal_clear_waters_yielding_gems.jpg", "Kural 309: Ocean depths opening up treasures to the pure",
     "Photorealistic 16:9 cinematic shot, shallow turquoise coastal waters, shimmering pearls and colorful shells resting visible on sparkling white sand."),
    ("31-vegulaamai/45-n45_the_magnetic_power_of_unbroken_calm.jpg", "Kural 309: Crowds naturally drawn to the aura of the peaceful",
     "Photorealistic 16:9 cinematic film still, ancient stone mandapam, townsfolk gathered in eager reverence around a tranquil master whose presence brings instant solace."),
    ("31-vegulaamai/46-n46_golden_harvest_under_peaceful_skies.jpg", "Kural 309: Heaven smiling on the land that knows no wrath",
     "Photorealistic 16:9 cinematic wide vista, vast panoramic view of ripe golden paddy fields under a rainbow arching across gentle blue and white skies."),

    # Kural 310: Those who give way to anger are like the dead; those who conquer it have conquered death
    ("31-vegulaamai/47-n47_the_walking_dead_consumed_by_wrath.jpg", "Kural 310: The bitter living death of the chronically enraged",
     "Photorealistic 16:9 cinematic film still, dim narrow street, a haggard man pacing with clenched fists and hollow haunted eyes, living in self-made purgatory."),
    ("31-vegulaamai/48-n48_immortal_radiance_of_the_anger_conqueror.jpg", "Kural 310: The radiant immortality of the conqueror of wrath",
     "Photorealistic 16:9 cinematic portrait, glowing face of an enlightened Tamil sage sitting in morning light, eyes reflecting the infinite sky, beyond death."),
    ("31-vegulaamai/49-n49_triumph_over_the_snakes_of_passion.jpg", "Kural 310: Conquering the poisonous serpents of wrath",
     "Photorealistic 16:9 cinematic symbolic shot, carved granite temple frieze depicting a peaceful sage serenely resting upon a coiled serpent whose fangs are harmless."),
    ("31-vegulaamai/50-n50_cool_rain_quenching_the_great_drought.jpg", "Kural 310: Life-giving rain terminating the scorching heat",
     "Photorealistic 16:9 cinematic wide shot, dark parched fields suddenly bathed in a refreshing monsoon downpour, farmers lifting their hands to heaven in ecstasy."),
    ("31-vegulaamai/51-n51_monumental_temple_chariot_rolling.jpg", "Kural 310: Grand celebration of virtue rolling forward",
     "Photorealistic 16:9 cinematic grand wide shot, massive intricately carved wooden temple chariot being pulled by thousands of joyful devotees along a festival street."),
    ("31-vegulaamai/52-n52_eternal_dawn_over_peaceful_tamilakam.jpg", "Kural 310: The eternal golden dawn of peace and righteousness",
     "Photorealistic 16:9 cinematic breathtaking panorama, golden sunrise illuminating the sacred temples, rivers, palm groves, and hills of ancient Tamilakam in timeless splendor.")
]

ALL_CHAPTERS = {
    5: {"name": "05-ilvaazhkkai", "prompts": CH05_PROMPTS, "count": len(CH05_PROMPTS)},
    8: {"name": "08-anbudaimai", "prompts": CH08_PROMPTS, "count": len(CH08_PROMPTS)},
    16: {"name": "16-poraiyudaimai", "prompts": CH16_PROMPTS, "count": len(CH16_PROMPTS)},
    25: {"name": "25-aruludaimai", "prompts": CH25_PROMPTS, "count": len(CH25_PROMPTS)},
    30: {"name": "30-vaaimai", "prompts": CH30_PROMPTS, "count": len(CH30_PROMPTS)},
    31: {"name": "31-vegulaamai", "prompts": CH31_PROMPTS, "count": len(CH31_PROMPTS)},
}

if __name__ == "__main__":
    total = sum(c["count"] for c in ALL_CHAPTERS.values())
    print(f"Total Batch 2 Prompts defined: {total}")
    for ch, data in ALL_CHAPTERS.items():
        print(f"  Chapter {ch} ({data['name']}): {data['count']} prompts")
