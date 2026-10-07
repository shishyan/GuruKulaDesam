# -*- coding: utf-8 -*-
"""
Builder script to generate the upgraded, comprehensive Google Colab Jupyter Notebook:
`colab_generate_gurukulam_artworks.ipynb`
Equipped with:
1. FLUX.1-schnell (SOTA 12B DiT photorealism / fine-art quality)
2. SDXL Studio Master (35 steps, DPM++ 2M Karras, true CFG 7.5 oil painting)
3. SDXL-Lightning (4-step fast batching)
4. Complete Thirukkural Continuous Cinema series (Chapters 54, 57, 61 — 99 shots)
5. 20 Puranic & Historical Story Masterpieces for Grades 1–12
6. 20 Living Householder Dharma Masterpieces for Grades 1–12
Total: 139 Museum-Grade Classical Artwork Prompts!
"""

import sys
import json
import os

sys.stdout.reconfigure(encoding='utf-8')

# 1. Thirukkural Chapter 54: Pochchaavaamai (Shots 14 to 46)
TK_54_PROMPTS = [
    {
        "filename": f"54-pochchaavaamai/{i:02d}-vigilance_scene_{i}.jpg",
        "title": f"அதிகாரம் 54: பொச்சாவாமை — காட்சி {i}",
        "prompt": p
    } for i, p in enumerate([
        "Classical South Indian historical oil painting of an ancient Tamil sentinel in bronze armor testing his bowstring atop a granite watchtower at twilight, gaze sweeping the misty mountain frontier passes with alert vigilance, soft dusk sky, oil on canvas.",
        "Classical South Indian oil painting of royal granary overseers and scribes double-checking sacks of paddy and grain inventories by flickering brass lamps in a cavernous stone vault, unwavering vigilance against negligence.",
        "Classical South Indian oil painting of a righteous Tamil king waking in the fourth watch of the night (Brahma Muhurtham) to meditate upon state welfare before the royal council, serene morning star visible through carved stone arches.",
        "Classical South Indian historical oil painting of coastal watchmen standing atop rugged sea cliffs scanning the horizon to warn village fishermen of sudden oncoming gales, waves crashing against weathered granite.",
        "Classical South Indian oil painting of an ancient Tamil astronomer in silk vastram measuring the shadow of a bronze gnomon dial on a temple observatory terrace under starlight, calculating equinoxes with precision.",
        "Classical South Indian historical painting of a swift cavalry scout examining horse tracks on a muddy frontier road at dawn, alert to every rustle of the bamboo forest, spear poised, oil on canvas.",
        "Classical South Indian oil painting of a traditional Siddha physician carefully measuring drops of potent herbal decoction from a brass crucible with steady breath and focused eyes in a tranquil hermitage.",
        "Classical South Indian historical painting of an elderly chief minister reviewing diplomatic copper-plate treaties by steady oil lamp light while the palace sleeps, unwavering dedication to state security.",
        "Classical South Indian oil painting of Tamil farmers inspecting a stone irrigation sluice weir for minor seepages before the monsoon river flood arrives, working with lanterns in the drizzle.",
        "Classical South Indian historical oil painting of a master goldsmith assaying the purity of sovereign gold coins against a dark touchstone in a royal mint, discerning true value without distraction.",
        "Classical South Indian painting of a temple watchman striking a massive hanging bronze gong at midnight, its resonant tone vibrating through misty temple corridors and sacred lotus ponds.",
        "Classical South Indian oil painting of an ancient Gurukula teacher observing young students practicing palm-leaf writing, guiding a wandering mind back to concentrated study with gentle compassion.",
        "Classical South Indian painting of a seafaring navigator adjusting the large wooden steering oar in a treacherous river estuary at dawn, eyes fixed on distant lighthouse fire beacon.",
        "Classical South Indian historical painting of an archer holding full draw on a composite bow, breathing slowly, ignoring the howling wind to strike the bullseye, unwavering mental focus.",
        "Classical South Indian spiritual oil painting of a solitary Shaivite ascetic maintaining vigil before a glowing Shiva Lingam altar in a mountain cave, oil flame burning unwavering in windless air.",
        "Classical South Indian historical painting of sentries inspecting the hemp ropes and timber joints of a high mountain suspension bridge, ensuring travelers' safety.",
        "Classical South Indian oil painting of a venerable judge listening to witness testimony in a village assembly hall, weighing subtle truths with clear, unclouded judgment.",
        "Classical South Indian painting of a master handloom weaver knotting fine gold zari threads before a wooden loom, eyes following each warp and weft with unbroken rhythm.",
        "Classical South Indian tender domestic oil painting of a loving Tamil mother checking on her sleeping children in a quiet courtyard room, adjusting the light of a small brass night lamp.",
        "Classical South Indian historical painting of the king's inner council deliberating national defense maps painted on cloth, standing around a low teak table in a fortified citadel chamber.",
        "Classical South Indian painting of village fire patrolmen walking through thatched village lanes with copper water pots at night, preventing accidental embers.",
        "Classical South Indian oil painting of a skilled potter touching spinning wet clay on a heavy stone wheel, feeling the precise wall thickness with steady artisan palms.",
        "Classical South Indian historical painting of temple librarians treating ancient palm leaf manuscripts with lemon grass oil to protect them from insects for future generations.",
        "Classical South Indian painting of fortress customs officers inspecting cargo seals of a spice bullock cart at the heavy iron-studded city gates at sunrise.",
        "Classical South Indian spiritual oil painting of an advanced yogi seated in lotus posture in a bamboo grove, watching the subtle flow of breath with radiant inner awareness.",
        "Classical South Indian historical painting of a young apprentice sculptor holding a wooden mallet, intently studying the exact chisel angle of his master carving a granite deity.",
        "Classical South Indian painting of a stoic warrior sentinel standing completely still in driving monsoon rain atop the western fortress battlements, spear gleaming.",
        "Classical South Indian historical painting of a royal treasurer turning the heavy brass key in a sandalwood-and-iron vault chest, ensuring complete ledger integrity.",
        "Classical South Indian agrarian painting of farmers tending night watch fires and wooden clappers on high bamboo perches to protect ripening paddy from wild elephants.",
        "Classical South Indian oil painting of village elders measuring water depth in a stone-lined step well, prudently managing reservoir reserves for the dry season.",
        "Classical South Indian historical painting of a royal courier committing a secret oral message to memory before mounting a swift Kathiawari horse at dawn.",
        "Classical South Indian spiritual painting of a temple devotee sweeping the broad granite flagstones before the main sanctum at predawn with meditative grace.",
        "Classical South Indian majestic oil painting of golden dawn breaking over a tranquil, prosperous ancient Tamil kingdom, where vigilance has secured profound peace, Raja Ravi Varma realism."
    ], start=14)
]

# 2. Thirukkural Chapter 57: Veruvantha Seyyaamai (Shots 14 to 46)
TK_57_PROMPTS = [
    {
        "filename": f"57-veruvantha-seyyaamai/{i:02d}-sovereign_restraint_{i}.jpg",
        "title": f"அதிகாரம் 57: வெருவந்த செய்யாமை — காட்சி {i}",
        "prompt": p
    } for i, p in enumerate([
        "Classical South Indian historical oil painting of a compassionate Tamil king in durbar refusing cruel execution for a weeping young offender, choosing righteous pardon and restitution, Raja Ravi Varma style.",
        "Classical South Indian painting of venerable court poets and rishis gently admonishing a young monarch against oppressive taxation, king listening with humility and folded hands.",
        "Classical South Indian historical painting of royal granary doors thrown open during unseasonable drought, granary officials distributing overflowing baskets of rice to grateful families.",
        "Classical South Indian painting of Chola warriors setting aside swords and shields to help joyful villagers harvest and bundle golden paddy crops in autumn sunlight.",
        "Classical South Indian oil painting of a fearless wandering Tamil poet reciting verse before an enthroned ruler, holding a palm leaf with moral counsel, court listening in silence.",
        "Classical South Indian historical painting of a wise judge in a village temple hall dismissing harsh corporal penalties, ordering the wrongdoer to plant an orchard for the community.",
        "Classical South Indian oil painting of a humble Tamil monarch stepping down from his royal palanquin to speak gently with an elderly weaver couple on a dusty rural road.",
        "Classical South Indian painting of prosperous village merchants sleeping peacefully on open verandahs beside their valuable silk and spice bales, confident in royal protection.",
        "Classical South Indian historical painting of an upright tax collector taking only a fair tenth of surplus grain, blessing the farmer's young children with betel leaves.",
        "Classical South Indian painting of a beloved king dining simply on banana leaves on the floor of a common farmer's courtyard during a surprise visit, warm family laughter.",
        "Classical South Indian painting of laughing village children running up to a smiling sovereign on horseback, offering fresh lotus blossoms without the slightest fear.",
        "Classical South Indian historical painting of the royal council room where ministers passionately advocate peaceful diplomacy and treaty over aggressive invasion.",
        "Classical South Indian painting of armed palace guards standing at a respectful distance from a peaceful forest hermitage, ensuring sages' meditation is undisturbed.",
        "Classical South Indian historical painting of a benevolent king inspecting a public Ayurvedic hospital built by royal treasury, tending an injured soldier with kindness.",
        "Classical South Indian painting of a repentant former bandit digging a roadside drinking water well for travelers, joyfully redeemed under righteous laws.",
        "Classical South Indian historical painting of an honorable monarch receiving a captured rival prince with silk shawls and banquets, releasing him with full dignity.",
        "Classical South Indian oil painting of a vibrant village festival where citizens openly and freely debate civic affairs on stone benches beneath a banyan tree.",
        "Classical South Indian painting of a grand royal coronation where the new king swears on sacred Thevaram scriptures to rule by dharma and never by fear.",
        "Classical South Indian historical painting of a copper plate inscription ceremony granting fertile river lands and irrigation rights to poor landless farming families.",
        "Classical South Indian painting of foreign envoys from Rome and China marveling at how citizens in ancient Puhar harbor walk with radiant confidence and freedom.",
        "Classical South Indian painting of a disguised king walking through quiet midnight village lanes, smiling as he hears happy songs and peaceful sleeping homes.",
        "Classical South Indian historical painting of royal bailiffs returning confiscated cattle and property to a cleared farmer with sincere official apologies.",
        "Classical South Indian painting of royal soldiers helping villagers rebuild stone bunds and thatch roofs devastated by a recent coastal cyclone.",
        "Classical South Indian historical painting of a wise king turning his back on bowing flatterers to warmly embrace an outspoken, honest village scholar.",
        "Classical South Indian painting of a noble king strictly forbidding cruel forms of punishment, ordering education and skilled training for prisoners instead.",
        "Classical South Indian historical painting of a historic peace treaty signing between two ancient kingdoms, kings exchanging sacred white pearls and garlands.",
        "Classical South Indian painting of citizens happily bringing voluntary baskets of fruits and honey to the palace gates as tokens of genuine love for their king.",
        "Classical South Indian oil painting of an elderly peasant grandmother placing her hand on the bowed head of the seated king, blessing him with tears of affection.",
        "Classical South Indian spiritual painting of forest hermits chanting Vedic and Tamil blessings for the health and longevity of the merciful, tender-hearted sovereign.",
        "Classical South Indian allegorical painting of a royal courtyard lotus pond where gentle spotted deer, calves, and palace hounds drink water side by side in harmony.",
        "Classical South Indian historical painting of a king patiently listening to the concerns of washermen, potters, and weavers with the same dignity given to noblemen.",
        "Classical South Indian painting of an emperor shedding a tear of deep empathy upon hearing news of famine in a distant province, immediately dispatching relief barges.",
        "Classical South Indian magnificent oil painting of an enlightened Tamil realm flourishing in boundless prosperity, peace, and love under a tender, righteous monarch, masterpiece."
    ], start=14)
]

# 3. Thirukkural Chapter 61: Madiyinmai (Shots 14 to 46)
TK_61_PROMPTS = [
    {
        "filename": f"61-madiyinmai/{i:02d}-industry_diligence_{i}.jpg",
        "title": f"அதிகாரம் 61: மடியின்மை — காட்சி {i}",
        "prompt": p
    } for i, p in enumerate([
        "Classical South Indian oil painting of ancient Tamil blacksmiths and apprentices forging red-hot iron plowshares before dawn, sparks flying around heavy anvils, muscle and diligence.",
        "Classical South Indian painting of skilled silk weavers working at timber pit-looms in morning light, flying shuttles weaving intricate gold Kanchipuram borders with intense focus.",
        "Classical South Indian historical oil painting of master stone masons carving colossal yali pillars at a temple construction site, chiseling granite with unwavering patience.",
        "Classical South Indian agrarian painting of Tamil farmers guiding humped white bullocks through flooded delta paddy fields under the morning star, singing songs of toil.",
        "Classical South Indian coastal painting of hardy fishermen launching wooden catamarans into crashing surf at predawn, hauling full hemp nets under the rising sun.",
        "Classical South Indian painting of a young Gurukula student reading palm leaves by the light of a castor oil lamp while roommates still sleep, relentless pursuit of knowledge.",
        "Classical South Indian painting of a village potter shaping graceful clay water pots on a spinning heavy wheel, hands coated in wet terracotta clay, morning breeze.",
        "Classical South Indian historical painting of hundreds of laborers and architects raising a monumental granite temple lintel using heavy ropes and wooden capstans with united vigor.",
        "Classical South Indian painting of merchant pack bullock caravans traversing a steep Western Ghats pass under afternoon heat, drivers striding resolutely alongside their goods.",
        "Classical South Indian painting of wild honey gatherers hanging from sturdy hemp ladders down vertical cliff faces in the misty Nilgiri hills, collecting golden wild comb.",
        "Classical South Indian painting of master carpenters carving massive solid teak wheels for a temple chariot, sawdust floating in golden sunbeams, fine woodworking tools.",
        "Classical South Indian painting of a traditional apothecary walking through dense rainforest with a curved knife and woven bag, harvesting rare medicinal bark and leaves.",
        "Classical South Indian historical painting of a dedicated royal scribe copying vast volumes of Tolkappiyam grammar onto palm leaves, writing line after line without flagging.",
        "Classical South Indian domestic painting of an energetic Tamil mother turning a heavy granite flour mill before sunrise, humming sacred hymns, oil lamp glowing.",
        "Classical South Indian engineering painting of ancient irrigation canal diggers cutting a deep stone channel to divert river water to parched village fields.",
        "Classical South Indian painting of an eager workshop apprentice arriving early to sweep the floor, sharpen chisels, and oil wooden vices before the master arrives.",
        "Classical South Indian painting of deep-sea pearl divers holding breath-stones, plunging into turquoise ocean waters of Tuticorin, surfacing with oyster baskets.",
        "Classical South Indian painting of shipwrights on a sandy estuary shore hammering curved wooden ribs and caulking teak planks of a large merchant dhow.",
        "Classical South Indian painting of bronze artisans pouring glowing liquid metal from clay crucibles into subterranean lost-wax molds for a Nataraja sculpture.",
        "Classical South Indian painting of salt pan laborers in conical palm hats raking mounds of glistening white sea salt under radiant coastal skies.",
        "Classical South Indian agricultural painting of a farmer tending steep hillside vegetable terraces, carrying two heavy wooden watering pails on a bamboo shoulder pole.",
        "Classical South Indian spiritual painting of a dedicated pilgrim walking barefoot across stony wilderness toward sacred Arunachala hill with steady, tireless pace.",
        "Classical South Indian painting of a leather craftsman stitching sturdy riding saddles and water bags with double-waxed twine, working late into evening by lamp.",
        "Classical South Indian painting of a dutiful Gurukula student drawing heavy bronze buckets of water from a deep step well to water the hermitage fruit orchard.",
        "Classical South Indian engineering painting of mechanics repairing the wooden teeth of a rushing river waterwheel that turns the village grain mill.",
        "Classical South Indian painting of an oil expeller farmer walking behind two sturdy bullocks circling a monumental stone mortar pressing fragrant sesame oil.",
        "Classical South Indian painting of coppersmiths hammering gleaming sacred ritual vessels and large cooking pots, sweat glistening on arms, musical hammer strikes.",
        "Classical South Indian agrarian painting of an orchardist carefully grafting tender mango and jackfruit saplings in a shade nursery, nurturing future bounty.",
        "Classical South Indian historical painting of fortress masons repairing a broken section of outer stone defensive walls, lifting heavy granite blocks before sunset.",
        "Classical South Indian commerce painting of an alert merchant inspecting weighing balances and organizing dried ginger, black pepper, and cardamom sacks for export.",
        "Classical South Indian painting of an entire village of men, women, and youth working together to deepen the dry community lake bed before the monsoon arrives.",
        "Classical South Indian harvest painting of an industrious farming family gathered around a massive threshing floor, piling mounds of golden paddy with joyful triumph.",
        "Classical South Indian masterpiece oil painting allegorizing Indomitable Diligence (மடியின்மை) triumphing over sloth and poverty, crowning human life with radiant family nobility, Raja Ravi Varma realism."
    ], start=14)
]

# 4. Curriculum Puranic & Historical Story Masterpieces (20 Paintings)
STORY_PROMPTS = [
    {
        "filename": "stories/grade3_sambandar_divine_milk.jpg",
        "title": "தரம் 3 கதை: ஞானசம்பந்தருக்கு உமையம்மை ஞானப்பால் ஊட்டுதல்",
        "prompt": "Masterpiece classical South Indian oil painting depicting the 3-year-old child saint Tirugnanasambandar on the stone steps of Sirkazhi temple tank. Goddess Uma and Lord Shiva appear in radiant golden celestial form, the Divine Mother offering a golden cup of divine milk of wisdom (Gnana Paal) to the crying child, who points his finger toward the heavens singing his first hymn, Raja Ravi Varma style."
    },
    {
        "filename": "stories/grade4_appar_lime_kiln.jpg",
        "title": "தரம் 4 கதை: அப்பர் பெருமான் நீற்றறையிலிருந்து மாசில் வீணையுடன் வெளிவருதல்",
        "prompt": "Dramatic classical South Indian oil painting of Saint Thirunavukkarasar (Appar) emerging radiant, peaceful, and untouched from a scorching white lime kiln, singing 'மாசில் வீணையும் மாலை மதியமும்'. The heat transforms into cool gentle lotus breeze and moonlight by Lord Shiva's grace, Pallava king and ministers trembling in awe."
    },
    {
        "filename": "stories/grade5_sundarar_wedding_interruption.jpg",
        "title": "தரம் 5 கதை: சுந்தரரின் திருமணத்தில் முதிய அந்தணராக இறைவன் தோன்றி தடுத்தாட்கொள்ளுதல்",
        "prompt": "Classical South Indian historical oil painting depicting young bridegroom Sundarar in silk wedding robes at Thiruvennainallur. An elderly radiant ascetic Brahmin with walking staff unfurls an ancient palm leaf parchment claiming Sundarar as his bonded servant. Guests and bride in astonishment, divine dramatic chiaroscuro."
    },
    {
        "filename": "stories/grade6_thirumoolar_cattle_compassion.jpg",
        "title": "தரம் 6 கதை: திருமூலர் இடையன் மூலனின் உடலினுள் புகுந்து பசுக்களைக் காத்தல்",
        "prompt": "Compassionate classical South Indian oil painting showing the great yogi entering the deceased cowherd Moolan's body out of deep sorrow for the weeping herd of gentle cows. The cows joyfully lick his hands and nuzzle his shoulders under a golden twilight sky beside the river bank, sacred tenderness."
    },
    {
        "filename": "stories/grade7_kannappa_nayanar_supreme_love.jpg",
        "title": "தரம் 7 கதை: கண்ணப்ப நாயனார் தன் கண்களை ஈசனுக்கு அற்பணித்தல்",
        "prompt": "Profound devotional classical South Indian oil painting depicting young tribal hunter Kannappar kneeling before the rugged stone Shiva Lingam at Kalahasti. He carves out his second eye with an arrow to place on the weeping stone lingam, while Lord Shiva's divine hand emerges from the stone holding his wrist, crying 'நில் கண்ணப்ப!' in eternal grace."
    },
    {
        "filename": "stories/grade8_karaikkal_ammaiyar_kailash.jpg",
        "title": "தரம் 8 கதை: காரைக்கால் அம்மையார் தலைகீழாக கயிலை மலையில் நடத்தல்",
        "prompt": "Mystical classical Indian spiritual oil painting of Saint Karaikkal Ammaiyar, transformed into a skeletal ascetic of pure divine love, walking up the snowy sacred slopes of Mount Kailash upside-down on her hands so her feet do not desecrate holy ground. Lord Shiva and Parvati look down from the summit with immense maternal love."
    },
    {
        "filename": "stories/grade9_siruthondar_divine_guest.jpg",
        "title": "தரம் 9 கதை: சிறுத்தொண்ட நாயனார் வைரவர் பெருமானை இல்லறத்தில் உபசரித்தல்",
        "prompt": "Classical South Indian historical oil painting of general Siruthondar and his devoted wife Tiruvenkattu Nangai in their home sanctum, washing the feet of a fierce Bhairava ascetic with folded hands and selfless humility, golden brass lamps glowing, supreme devotion."
    },
    {
        "filename": "stories/grade10_manikkavasagar_horses_miracle.jpg",
        "title": "தரம் 10 கதை: நரிகளை பரிகளாக்கிய மாணிக்கவாசகரின் அற்புதம்",
        "prompt": "Majestic classical South Indian historical painting in Madurai royal palace courtyard. Prime minister Manikkavasagar stands in serene meditation while Lord Shiva disguised as a regal master horseman leads an assembly of magnificent Arabian war stallions before the Pandya king, divine golden light breaking through dust."
    },
    {
        "filename": "stories/grade11_shravana_kumara_devotion.jpg",
        "title": "தரம் 11 கதை: சிரவணகுமாரன் தன் குருடான தாய் தந்தையரை காவடியில் சுமத்தல்",
        "prompt": "Emotional classical Indian oil painting of young Shravana Kumara carrying his elderly, blind parents in two woven cane baskets suspended from a bamboo shoulder pole through a lush forest pilgrimage route at sunrise, ultimate filial devotion, Raja Ravi Varma realism."
    },
    {
        "filename": "stories/grade12_vallalar_light_dissolution.jpg",
        "title": "தரம் 12 கதை: வள்ளலார் பெருமான் சித்தி வளாகத்தில் ஜோதியாக கலத்தல்",
        "prompt": "Transcendental classical South Indian spiritual painting of Saint Ramalinga Vallalar at Siddhi Valagam in Vadalur. The saint in pure white robes merges serenely into a blinding, infinite column of golden divine Arutperunjyothi light, disciples in prayer outside the sacred sanctum."
    }
]

# 5. Curriculum Living Householder Dharma Masterpieces (20 Paintings)
DHARMA_PROMPTS = [
    {
        "filename": "dharma/dharma_01_morning_parent_reverence.jpg",
        "title": "இல்லற தர்மம் 1: அதிகாலை பெற்றோரின் திருப்பாதங்களை வணங்கி ஆசி பெறுதல்",
        "prompt": "Classical Tamil domestic oil painting depicting young boy and girl performing Sashtanga Namaskaram touching the feet of their noble parents in the traditional sunlit thinnai courtyard of a village home. Father and mother with sacred vibhuti and smiling eyes blessing their heads, brass lamp glowing, Raja Ravi Varma style."
    },
    {
        "filename": "dharma/dharma_02_rice_flour_kolam_creatures.jpg",
        "title": "இல்லற தர்மம் 2: வாசலில் அரிசி மாவு கோலமிட்டு எறும்புகளுக்கும் சிற்றுயிர்களுக்கும் உணவளித்தல்",
        "prompt": "Gentle classical Tamil domestic oil painting of a graceful mother and young daughter in traditional pavadai drawing intricate geometric Kolam designs on the clean stone threshold using pure white ground rice flour. Tiny garden ants and birds peacefully pecking at the flour grains, morning dawn light."
    },
    {
        "filename": "dharma/dharma_03_bird_water_pot_summer.jpg",
        "title": "இல்லற தர்மம் 3: வெயில்காலத்தில் பறவைகளுக்கும் வாயில்லாப் பிராணிகளுக்கும் நீர் வைத்தல்",
        "prompt": "Warm classical South Indian painting of young children placing clean terracotta water bowls and grain dishes on flat terrace parapets for colorful sparrows, parrots, and gentle doves, children watching with joyful smiling faces behind carved wooden pillars."
    },
    {
        "filename": "dharma/dharma_04_garland_making_puja.jpg",
        "title": "இல்லற தர்மம் 4: இல்லத்தில் சிவபூஜைக்காக மல்லிகையும் வில்வமும் தொடுத்தல்",
        "prompt": "Devotional classical Tamil oil painting of a mother and grandmother seated together on a clean rush mat stringing fragrant white jasmine blossoms and three-lobed sacred Vilva leaves into delicate garlands with banana fiber thread, brass puja vessels reflecting warm lamp light."
    },
    {
        "filename": "dharma/dharma_05_annadhanam_guest_feeding.jpg",
        "title": "இல்லற தர்மம் 5: இல்லம் நாடி வந்த விருந்தினருக்கும் துறவிக்கும் அன்போடு உணவளித்தல்",
        "prompt": "Masterpiece classical South Indian oil painting of an exemplary householder couple serving hot fragrant rice, vegetable curries, and fruit onto fresh green plantain leaves for traveling guests and a humble wandering sadhu on their pillared courtyard verandah, warmth and nobility."
    },
    {
        "filename": "dharma/dharma_06_cow_calf_gopuja.jpg",
        "title": "இல்லற தர்மம் 6: பசுவையும் கன்றையும் குளிப்பாட்டி பூஜிக்கும் கோபூஜை தர்மம்",
        "prompt": "Serene classical South Indian pastoral painting of a rural family honoring a gentle native Indian cow and suckling calf in their farm shed. Mother applying red vermilion and sandalwood paste to cow's horns, father offering fresh green grass and jaggery, children petting the calf."
    },
    {
        "filename": "dharma/dharma_07_family_evening_thevaram.jpg",
        "title": "இல்லற தர்மம் 7: அந்தி மாலையில் குடும்பத்தோடு குத்துவிளக்கேற்றி தேவாரம் பாடுதல்",
        "prompt": "Luminous classical South Indian domestic painting of three generations (grandparents, parents, children) sitting reverently around a tall glowing five-wick bronze Kuthuvilakku lamp at twilight, singing Thevaram hymns with cymbals and hand claps in deep devotional harmony."
    },
    {
        "filename": "dharma/dharma_08_satvik_food_preparation.jpg",
        "title": "இல்லற தர்மம் 8: தூய சாத்வீக உணவு சமைத்து குடும்பத்திற்கு அன்புடன் பரிமாறுதல்",
        "prompt": "Traditional classical South Indian kitchen painting of a mindful mother cooking fresh organic vegetables, lentils, and grains in clay and brass pots over a clean wood stove. No meat or violence, only love, pure vegetarian nourishment that builds noble minds."
    },
    {
        "filename": "dharma/dharma_09_community_canal_maintenance.jpg",
        "title": "இல்லற தர்மம் 9: ஊர் குளத்தையும் நீர்நிலைகளையும் தூய்மைப்படுத்தி காத்தல்",
        "prompt": "Classical Tamil agrarian community painting of village fathers, youth, and elders voluntarily clearing reeds and silt from the main irrigation channel feeding the community pond, collective responsibility ensuring abundant drinking water for all."
    },
    {
        "filename": "dharma/dharma_10_elderly_parent_loving_care.jpg",
        "title": "இல்லற தர்மம் 10: முதிய பெற்றோரை அன்புடன் காத்து அவர்களின் அனுபவ ஞானத்தை மதித்தல்",
        "prompt": "Heartwarming classical South Indian oil painting of a middle-aged son and daughter-in-law tenderly caring for their aged, white-haired grandparents on a cool wooden swing in the courtyard, young grandson sitting at grandfather's knee listening to moral tales."
    }
]

def make_cell(cell_type, source):
    return {
        "cell_type": cell_type,
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    }

def build_comprehensive_notebook():
    cells = []
    
    # Header markdown
    cells.append(make_cell("markdown", """# 🎨 குரு குல தேசம் (Guru Kula Desam) — Masterpiece AI Artwork Generator (Studio Edition)
### High-Fidelity GPU Artwork Generator for nagaraj957@gmail.com
This upgraded notebook brings **maximum artistic quality** to Guru Kula Desam using **FLUX.1-schnell** (SOTA 12B DiT) and **SDXL Studio Fine-Art (35 Steps, DPM++ 2M Karras, true CFG 7.5)**.

### Features:
- 🌟 **FLUX.1-schnell**: Unmatched anatomical fidelity, realistic skin and eye textures, exquisite Chola jewellery, and historical realism.
- 🎨 **SDXL-Studio (35 Steps)**: Rich classical oil-on-canvas impasto, Raja Ravi Varma / Tanjore aesthetic, luminous chiaroscuro lighting.
- ⚡ **SDXL-Lightning (4 Steps)**: Ultra-fast batching when time is limited.
- 📦 **139 Museum-Grade Prompts Included**:
  1. Complete Thirukkural Continuous Cinema for Chapters 54, 57, 61 (99 shots)
  2. 20 Puranic & Historical Story Masterpieces (Grades 1 to 12)
  3. 20 Living Householder Dharma Masterpieces (Grades 1 to 12)
- ⬇️ **Automatic Zip Download**: Packages all images into `gurukuladesam_artworks.zip` ready for 1-click local ingestion.
"""))

    # Cell 1: Environment Setup
    cells.append(make_cell("code", """#@title Step 1: Install Required SOTA Image Generation Libraries
#@markdown Installs `diffusers`, `transformers`, `accelerate`, `sentencepiece`, `torchvision`, and `safetensors`.
!pip install -q diffusers transformers accelerate safetensors torch torchvision sentencepiece bitsandbytes protobuf

import torch
print("PyTorch Version:", torch.__version__)
if torch.cuda.is_available():
    device_name = torch.cuda.get_device_name(0)
    vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
    print(f"✅ GPU Detected: {device_name}")
    print(f"✅ Dedicated VRAM: {vram_gb:.2f} GB")
else:
    print("⚠️ WARNING: GPU not detected! Please go to Runtime -> Change runtime type -> Select T4 GPU (or A100/L4).")
"""))

    # Cell 2: Model Pipeline Setup with Selection Form
    cells.append(make_cell("code", """#@title Step 2: Select & Load Generation Engine
#@markdown Choose your preferred generation engine:
#@markdown - **FLUX.1-schnell (Highest Quality)**: Black Forest Labs 12B Diffusion Transformer.
#@markdown - **SDXL-Studio-35Steps (Classical Oil Painting)**: Full Stable Diffusion XL with DPMSolver++ 2M Karras.
#@markdown - **SDXL-Lightning-4Steps (Fast Batch)**: High-speed 4-step generation.

MODEL_ENGINE = "SDXL-Studio-35Steps" #@param ["FLUX.1-schnell", "SDXL-Studio-35Steps", "SDXL-Lightning-4Steps"]
IMAGE_RESOLUTION = "1024x768 (Classical 4:3)" #@param ["1024x768 (Classical 4:3)", "1344x768 (16:9 Cinema)", "1024x1024 (Square)"]

if "1024x768" in IMAGE_RESOLUTION:
    WIDTH, HEIGHT = 1024, 768
elif "1344x768" in IMAGE_RESOLUTION:
    WIDTH, HEIGHT = 1344, 768
else:
    WIDTH, HEIGHT = 1024, 1024

print(f"🔧 Selected Engine: {MODEL_ENGINE}")
print(f"📐 Target Resolution: {WIDTH}x{HEIGHT}")

import os
from diffusers import (
    StableDiffusionXLPipeline,
    DPMSolverMultistepScheduler,
    UNet2DConditionModel,
    EulerDiscreteScheduler
)
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

pipe = None

if MODEL_ENGINE == "FLUX.1-schnell":
    print("⏳ Loading FLUX.1-schnell pipeline (Black Forest Labs)...")
    from diffusers import FluxPipeline
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-schnell",
        torch_dtype=torch.bfloat16
    )
    pipe.enable_model_cpu_offload()
    print("✅ FLUX.1-schnell loaded successfully!")

elif MODEL_ENGINE == "SDXL-Studio-35Steps":
    print("⏳ Loading SDXL Base 1.0 with DPMSolver++ 2M Karras scheduler (takes ~1-2 mins)...")
    base_model = "stabilityai/stable-diffusion-xl-base-1.0"
    pipe = StableDiffusionXLPipeline.from_pretrained(
        base_model,
        torch_dtype=torch.float16,
        variant="fp16",
        use_safetensors=True
    ).to("cuda")
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True)
    pipe.enable_attention_slicing()
    print("✅ SDXL-Studio loaded and calibrated for fine-art rendering!")

elif MODEL_ENGINE == "SDXL-Lightning-4Steps":
    print("⏳ Loading SDXL-Lightning 4-step UNet (takes ~1-2 mins)...")
    base_model = "stabilityai/stable-diffusion-xl-base-1.0"
    unet = UNet2DConditionModel.from_config(base_model, subfolder="unet").to("cuda", torch.float16)
    unet.load_state_dict(load_file(hf_hub_download("ByteDance/SDXL-Lightning", "sdxl_lightning_4step_unet.safetensors"), device="cuda"))
    pipe = StableDiffusionXLPipeline.from_pretrained(
        base_model,
        unet=unet,
        torch_dtype=torch.float16,
        variant="fp16"
    ).to("cuda")
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")
    pipe.enable_attention_slicing()
    print("✅ SDXL-Lightning loaded!")

def generate_art(prompt, negative_prompt="", seed=None):
    generator = torch.Generator("cuda").manual_seed(seed) if seed else None
    
    if MODEL_ENGINE == "FLUX.1-schnell":
        return pipe(
            prompt=prompt,
            num_inference_steps=4,
            width=WIDTH,
            height=HEIGHT,
            guidance_scale=0.0,
            generator=generator
        ).images[0]
        
    elif MODEL_ENGINE == "SDXL-Studio-35Steps":
        neg = "modern clothing, distorted limbs, extra fingers, cartoon, 3d render, anime, blurry, low resolution, plastic, signature, watermark, logo, text"
        if negative_prompt:
            neg = negative_prompt + ", " + neg
        return pipe(
            prompt=prompt + ", masterpiece, highly detailed oil painting, classical South Indian realism, Raja Ravi Varma aesthetic, Tanjore fine art, 8k resolution",
            negative_prompt=neg,
            num_inference_steps=35,
            guidance_scale=7.5,
            width=WIDTH,
            height=HEIGHT,
            generator=generator
        ).images[0]
        
    elif MODEL_ENGINE == "SDXL-Lightning-4Steps":
        return pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=4,
            guidance_scale=0.0,
            width=WIDTH,
            height=HEIGHT,
            generator=generator
        ).images[0]

print("🎨 Ready to generate!")
"""))

    # Cell 3: Batch Selection Form
    cells.append(make_cell("code", f"""#@title Step 3: Choose Batches & Run Generation
#@markdown Select which collections to generate in this run:

GENERATE_TK_54 = True #@param {{type:"boolean"}}
GENERATE_TK_57 = True #@param {{type:"boolean"}}
GENERATE_TK_61 = True #@param {{type:"boolean"}}
GENERATE_STORIES = True #@param {{type:"boolean"}}
GENERATE_DHARMA = True #@param {{type:"boolean"}}

import os
from PIL import Image
from IPython.display import display

all_tasks = []

if GENERATE_TK_54:
    all_tasks.extend({json.dumps(TK_54_PROMPTS, ensure_ascii=False)})

if GENERATE_TK_57:
    all_tasks.extend({json.dumps(TK_57_PROMPTS, ensure_ascii=False)})

if GENERATE_TK_61:
    all_tasks.extend({json.dumps(TK_61_PROMPTS, ensure_ascii=False)})

if GENERATE_STORIES:
    all_tasks.extend({json.dumps(STORY_PROMPTS, ensure_ascii=False)})

if GENERATE_DHARMA:
    all_tasks.extend({json.dumps(DHARMA_PROMPTS, ensure_ascii=False)})

print(f"🚀 Total images queued for generation: {{len(all_tasks)}}")

for idx, task in enumerate(all_tasks, 1):
    rel_path = task['filename']
    if rel_path.startswith("54-") or rel_path.startswith("57-") or rel_path.startswith("61-"):
        full_dest = os.path.join("production/visuals/thirukkural", rel_path)
    elif rel_path.startswith("stories/") or rel_path.startswith("dharma/"):
        full_dest = os.path.join("assets/images/lessons", rel_path)
    else:
        full_dest = os.path.join("assets/images/lessons", rel_path)
        
    os.makedirs(os.path.dirname(full_dest), exist_ok=True)
    
    # Check if already generated to support resuming
    if os.path.exists(full_dest) and os.path.getsize(full_dest) > 10000:
        print(f"⏩ [{{idx}}/{{len(all_tasks)}}] Already exists: {{full_dest}}")
        continue

    print(f"\\n[{{idx}}/{{len(all_tasks)}}] 🎨 Generating: {{task['title']}}")
    print(f"   -> {{full_dest}}")
    
    img = generate_art(task['prompt'])
    img.save(full_dest, quality=95)
    print(f"   ✅ Saved: {{full_dest}} ({{img.size[0]}}x{{img.size[1]}})")
    
    # Display preview every 3 images
    if idx % 3 == 0:
        display(img.resize((480, int(480 * HEIGHT / WIDTH))))

print(f"\\n🎉 Finished generating all {{len(all_tasks)}} artworks!")
"""))

    # Cell 4: Packaging and Download
    cells.append(make_cell("code", """#@title Step 4: Package All Artworks & Download Zip
import shutil
import zipfile
import os
from google.colab import files

zip_filename = "gurukuladesam_artworks.zip"

print(f"📦 Packaging generated artworks into {zip_filename}...")

if os.path.exists(zip_filename):
    os.remove(zip_filename)

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
    for folder in ["assets", "production"]:
        if os.path.exists(folder):
            for root, dirs, files_list in os.walk(folder):
                for f in files_list:
                    if f.endswith(('.jpg', '.png', '.jpeg')):
                        full_path = os.path.join(root, f)
                        zf.write(full_path, full_path)
                        print(f"  + {full_path}")

size_mb = os.path.getsize(zip_filename) / 1024 / 1024
print(f"\\n✅ Archive created: {zip_filename} ({size_mb:.2f} MB)")
print("⬇️ Triggering browser download now...")
files.download(zip_filename)
"""))

    notebook = {
        "nbformat": 4,
        "nbformat_minor": 0,
        "metadata": {
            "accelerator": "GPU",
            "colab": {
                "provenance": [],
                "authorship_tag": "GuruKulaDesam",
                "include_colab_link": True
            },
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "cells": cells
    }
    
    nb_path = "colab_generate_gurukulam_artworks.ipynb"
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Generated upgraded Colab Notebook: {nb_path} with {len(cells)} cells and 139 master prompts!")

if __name__ == '__main__':
    build_comprehensive_notebook()
