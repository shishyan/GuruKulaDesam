# -*- coding: utf-8 -*-
"""
Build Comprehensive Google Colab Notebook with FLUX.1 + Indo-Realism LoRA & Juggernaut XL
Generates `colab_generate_gurukulam_artworks.ipynb` equipped with:
1. FLUX.1-schnell + Indo-Realism LoRA (prithivMLmods/Flux.1-Dev-Indo-Realism-LoRA)
2. Juggernaut-XL-v9 with Raja Ravi Varma fine-art negative and positive prompt anchors
3. Complete 150 Masterpiece Prompts:
   - 11 Core Grade 8-12 Bespoke Lessons (chaturs ashrama, agamas, body is temple, etc.)
   - 20 Puranic & Historical Story Masterpieces
   - 20 Householder Living Dharma Masterpieces
   - 99 Thirukkural Continuous Cinema shots for Chapters 54, 57, 61
4. Overwrite existing toggle and selective batch execution
5. Auto packaging to `gurukuladesam_artworks.zip` with instant browser download.
"""

import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# 1. Core Grade 8-12 Bespoke Curriculum Lessons (11 Artworks)
LESSON_PROMPTS = [
    {
        "filename": "grade8_chatur_ashrama.jpg",
        "title": "தரம் 8 பாடம் 4: சதுர் ஆசிரமங்கள் — இல்லற தர்மமே அனைத்திற்கும் மூலம்",
        "prompt": "Four Ashramas of Life (Chatur Ashrama) with the Householder (Grihastha) as the supreme generous foundation. At the carved wooden pillared thinnai porch of a heritage Tamil courtyard home, a noble, radiant Tamil householder husband and wife warmly offer hospitality and food (Annadhanam). The husband wears a pristine silk veshti with golden border, sacred thread, and tripundra vibhuti on his forehead. The wife wears a rich crimson and gold Kanchipuram silk saree with temple jewelry and jasmine flowers. They are serving food on fresh banana leaves to: a young Brahmachari student with a sacred thread holding a palm-leaf scripture, an elderly serene Vanaprastha hermit couple in earthy robes, and a wandering Sannyasi ascetic with a saffron robe, silver beard, and wooden staff (danda). On the red oxide floor are intricate white rice-flour kolam patterns and a gleaming brass kuthuvilakku oil lamp. Warm golden morning sunlight, lush green banana and coconut palms in background, sacred, dignified, and emotionally touching atmosphere."
    },
    {
        "filename": "grade9_saiva_agamas.jpg",
        "title": "தரம் 9 பாடம் 1: இருபத்தெட்டு சைவ ஆகமங்கள் & திருக்கோயில் வழிபாடு",
        "prompt": "Inside an ancient grand Chola granite temple sanctum (garbhagriha) with massive intricately sculpted stone pillars. Traditional Sivacharya temple priests with bare torsos, sacred yajnopavita thread, deep white dhotis with broad gold borders, prominent sacred tripundra vibhuti ash across foreheads and arms, and rudraksha malas, performing authentic Vedic-Agamic shodashopachara puja before a polished black stone Shiva Lingam. The Lingam is adorned with fresh green bilva leaves and vibrant red lotus garlands. Reverently held bronze Panchamukha Deepam (five-wicked arati lamp) casting brilliant warm golden illumination, tall brass kuthuvilakku floor lamps, fragrant rising swirls of sambrani incense smoke, sacred, mysterious, deeply devotional sanctum atmosphere."
    },
    {
        "filename": "grade9_body_is_temple.jpg",
        "title": "தரம் 9 பாடம் 2: உடலே ஆலயம் — திருமூலரின் 'உள்ளம் பெருங்கோயில் ஊனுடம்பு ஆலயம்'",
        "prompt": "Depicting Thirumoolar's Thirumandiram vision 'Ullam Perungoil Oonudambu Alayam' (The Body is a Living Temple). A serene, majestic Tamil yogi seated in steady Padmasana meditation under a sprawling sacred peepal tree on a tranquil riverbank at dawn. A subtle, luminous golden sacred geometry aura radiates through his physical form, revealing the mystical correspondence between the human body and the Hindu temple: his heart center glows as the sanctum sanctorum (garbhagriha) containing the divine flame of consciousness, and his spine aligns like the ascending temple vimana and gopuram tower. Three lines of holy white tripundra vibhuti and red tilak on his forehead, blissful meditative face, morning river mist, blooming pink lotus flowers floating on the water, spiritual transcendent serenity."
    },
    {
        "filename": "grade9_shaddarshanas_dialogue.jpg",
        "title": "தரம் 9 பாடம் 3: பாரதத்தின் ஷட்தர்சனங்கள் — மெய்யறிவு தத்துவ உரையாடல்",
        "prompt": "Set inside a magnificent ancient South Indian granite temple thousand-pillared mandapam with intricately sculpted Yali dragon-lion pillars. A dignified assembly of revered ancient Indian Vedic philosophers and rishis representing the Six Classical Darshanas (Shaddarshana) engaged in elevated, respectful philosophical discourse. They wear fine unstitched dhotis and angavastrams with sacred ash vibhuti and tilaks, holding inscribed palm-leaf manuscripts (olai chuvadi) and bronze styluses, gracefully gesturing with chinmudra and debate hands. Sunbeams stream through high carved granite pillars illuminating soft incense dust motes, with brass kamandalu water pots on the stone pavement. Dignified, timeless scholarly mastery and contemplative grandeur."
    },
    {
        "filename": "grade10_pati_pasu_pasam.jpg",
        "title": "தரம் 10 பாடம் 1: சைவ சித்தாந்த மும்முதற்பொருள்கள் — பதி, பசு, பாசம்",
        "prompt": "Classical Saiva Siddhanta philosophical masterpiece oil painting depicting Pati (God), Pasu (the Soul), and Pasam (the worldly bondage). In the celestial center, Lord Shiva in benevolent Sadashiva form radiates golden divine grace. In the foreground, an earnest human soul depicted as a devoted Tamil seeker in pure white dhoti with hands in anjali mudra looking upward in yearning. Between them, the three dark shadowy chains of Anava (egoism), Karma (action bondage), and Maya (illusion) dissolve and turn to golden dust under the piercing light of Shiva's grace, serene cosmic dawn."
    },
    {
        "filename": "grade10_temple_chariot_festival.jpg",
        "title": "தரம் 10 பாடம் 4: திருக்கோயில் தேர் திருவிழா — பக்திப் பெருவிழா",
        "prompt": "Spectacular classical South Indian historical oil painting of the grand Chola Temple Chariot Festival (Ther Thiruvizha). A towering, intricately carved multi-tiered wooden temple chariot with golden canopy and flying flags rumbles through the wide temple car street. Thousands of joyful devotees of all ages with vibhuti on foreheads united in purpose, pulling the colossal thick coir ropes. Musicians playing loud nadaswaram and thavil, flower petals raining from rooftops, glorious devotional ecstasy under bright blue skies."
    },
    {
        "filename": "grade11_nachiketas_yama.jpg",
        "title": "தரம் 11 பாடம் 2: கடோபநிடதம் — நசிகேதன் மற்றும் எமதர்மனின் ஆத்ம ஞான உரையாடல்",
        "prompt": "Solemn, sublime classical Indian oil painting of the Katha Upanishad dialogue. Young, pure-hearted boy Nachiketas with folded hands and luminous eyes, sitting on a deerskin before the regal, imposing yet profoundly wise Lord Yama (Dharmaraja) in his palace of cosmic order. Yama, seated with a lotus sceptre, imparts the sacred Brahma-Vidya knowledge of the eternal, immortal Atman. Sacred sacrificial fire (Nachiketa Agni) glowing between them, profound philosophical reverence, Raja Ravi Varma realism."
    },
    {
        "filename": "grade11_pancha_koshas.jpg",
        "title": "தரம் 11 பாடம் 4: தைத்திரீய உபநிடதம் — பஞ்ச கோசங்கள்",
        "prompt": "Classical Indian metaphysical oil painting visualizing the Pancha Koshas (Five Sheaths of Being) of the Taittiriya Upanishad. A noble Tamil seeker seated in silent meditation at sunrise, surrounded by five luminous translucent concentric layers of consciousness: the physical food body (Annamaya), vital breath (Pranamaya), mind and sensory organ (Manomaya), intuitive intellect (Vijnanamaya), and bliss sheath (Anandamaya), culminating in the radiant central spark of the immortal Self (Atman)."
    },
    {
        "filename": "grade12_jivanmukti_36tattvas.jpg",
        "title": "தரம் 12 பாடம் 1: ஜீவன்முக்தி & 36 தத்துவங்கள் கடத்தல்",
        "prompt": "Exquisite classical South Indian spiritual oil painting depicting Jivanmukti (liberation while living) and transcendence of the 36 Tattvas. An enlightened Tamil sage in simple unstitched white cloth resting serenely beside a clear Himalayan-Tamil river, gazing with boundless unconditional compassion. Around him, allegorical symbols of the 36 tattvas (elements, senses, mind, maya, vidya) rest in peaceful cosmic equilibrium, while wild deer and peacocks rest fearlessly at his feet."
    },
    {
        "filename": "grade12_thayumanavar_universal.jpg",
        "title": "தரம் 12 பாடம் 2: தாயுமானவ சுவாமிகள் — பராபரக் கண்ணி & சர்வ சமய சமரசம்",
        "prompt": "Soul-stirring classical Tamil oil painting of Saint Thayumanavar meditating upon the rock fort of Tiruchirappalli overlooking the lush green Kaveri river delta. Hands in Chinmudra, radiating the sublime vision of universal harmony ('எல்லாரும் இன்புற்றிருக்க நினைப்பதுவே'). A golden ray of divine light descends from the heavens onto the saint, uniting all sects and beings in boundless divine ecstasy, Raja Ravi Varma aesthetic."
    },
    {
        "filename": "grade12_grihastha_nirvana.jpg",
        "title": "தரம் 12 பாடம் 5: இல்லற தர்மமே அதிவேக முக்தி நெறி",
        "prompt": "Classical Tamil spiritual oil painting celebrating the supreme dignity of Householder Dharma as the direct expressway to Mukti. A mature, noble Tamil couple in traditional silk attire standing together in their sanctum home before the family deity lamp. Their grown children, disciples, and community members look to them with profound veneration. The couple radiates supreme spiritual peace and liberation (Jivanmukti) attained not by fleeing the world, but by fulfilling righteous family duty and universal compassion."
    }
]

# 2. Thirukkural Chapter 54: Pochchaavaamai (Shots 14 to 46)
TK_54_PROMPTS = [
    {
        "filename": f"54-pochchaavaamai/{i:02d}-vigilance_shot_{i}.jpg",
        "title": f"அதிகாரம் 54: பொச்சாவாமை — காட்சி {i}",
        "prompt": p
    } for i, p in enumerate([
        "Classical South Indian historical oil painting of royal Tamil sentinels standing motionless on high stone battlement at midnight, holding bronze spears under moonlit skies, unwavering alertness.",
        "Classical South Indian painting of a dedicated village elder inspecting irrigation earthen dykes before torrential monsoon rains, holding a brass oil lamp, protective vigilance.",
        "Classical South Indian palace scene where an experienced prime minister gently reviews confidential royal seals with an attentive young prince by flickering lamp light.",
        "Classical South Indian painting of a diligent Tamil temple treasury keeper weighing sacred gold ornaments with precision scales, surrounded by stone granite carvings.",
        "Classical South Indian coastal scene where lighthouse keepers faithfully tend the colossal copper oil beacon atop sea cliffs, guiding fishing catamarans safely home.",
        "Classical South Indian historical painting of a Tamil merchant caravan leader scanning the forest pass from horseback while guards check wheel pins and harness ropes.",
        "Classical South Indian temple courtyard where an elderly Sivacharya meticulously counts sacred bilva leaves and fresh holy water vessels for the midnight puja.",
        "Classical South Indian domestic oil painting of a noble mother softly checking sleeping children and latching heavy teak doors before placing the night lamp in the niche.",
        "Classical South Indian agricultural painting of farmers building sturdy raised watchtowers in golden paddy fields, vigilant against wandering wild elephants at dusk.",
        "Classical South Indian martial academy scene where young Tamil warriors practice Silambam bamboo staff maneuvers under the keen watchful eye of an ancient master.",
        "Classical South Indian historical painting of a royal scribe double-checking copper plate inscriptions with a sharp iron stylus before the king applies the royal seal.",
        "Classical South Indian forest hermitage where young Brahmachari disciples keep the sacred Vedic sacrificial fire burning through torrential winds with careful shields.",
        "Classical South Indian painting of an Ayurvedic physician inspecting medicinal herbal brews over charcoal embers, measuring dried roots with meticulous focus.",
        "Classical South Indian palace armory where master armorers inspect tempered iron broadswords and leather shields, hanging them in impeccable order on granite walls.",
        "Classical South Indian village council scene beneath a banyan tree where righteous elders listen attentively to boundary dispute witnesses without missing a word.",
        "Classical South Indian maritime painting of a Tamil navigator using an ancient quadrant and star map to guide a great teak trading ship through dark starry waters.",
        "Classical South Indian painting of a royal messenger delivering urgent border scrolls to a sovereign who immediately sets aside feasting to read with serious resolve.",
        "Classical South Indian historical painting of a vigilant queen mother managing state granary ledgers during drought, ensuring no grain sack is wasted.",
        "Classical South Indian painting of fortress gatekeepers verifying tokens and identities of travelers before drawing the heavy iron portcullis at twilight.",
        "Classical South Indian monastery scene where scholars in white veshti proofread palm-leaf Thevaram manuscripts word by word against ancient master leaves.",
        "Classical South Indian market scene where weights-and-measures inspectors test bronze balances of spice traders in bustling ancient Madurai bazaar.",
        "Classical South Indian painting of a stone mason measuring the plumb-line of a towering temple gopuram pillar, checking symmetry with total concentration.",
        "Classical South Indian royal garden scene where vigilant guards discreetly scan the perimeter while the king consults quietly with foreign ambassadors.",
        "Classical South Indian painting of a vigilant herd-boy counting each humped cow and calf as they pass through the wooden cattle pen into the village.",
        "Classical South Indian mountain outpost painting of scouts signaling across misty peaks using polished bronze mirrors reflecting sunlight.",
        "Classical South Indian painting of an upright judge carefully examining sealed evidence packets before rendering judgment in the village sabha.",
        "Classical South Indian painting of a dedicated apprentice goldsmith watching the melting point of gold alloy in a clay crucible without blinking.",
        "Classical South Indian historical painting of royal treasurers locking the triple-keyed vault of temple jewels under the watchful eyes of three different overseers.",
        "Classical South Indian painting of a young Tamil prince resisting sleep to finish studying the Arthashastra and Thirukkural by an oil lamp.",
        "Classical South Indian painting of river lock operators lowering heavy wooden sluice gates as floodwaters surge down the Kaveri river delta.",
        "Classical South Indian painting of temple night-watchmen holding flaming torches as they patrol the sacred praharams of a grand granite temple complex.",
        "Classical South Indian historical painting of a monarch holding dawn audience, sharp-eyed and energetic while lazy courtiers stifle yawns in the background.",
        "Classical South Indian majestic oil painting of golden dawn breaking over a tranquil, prosperous ancient Tamil kingdom, where vigilance has secured profound peace, Raja Ravi Varma realism."
    ], start=14)
]

# 3. Thirukkural Chapter 57: Veruvantha Seyyaamai (Shots 14 to 46)
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

# 4. Thirukkural Chapter 61: Madiyinmai (Shots 14 to 46)
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
        "Classical South Indian painting of an agile coconut harvester climbing towering palm trees before the heat of day, tossing ripe coconuts into soft sand below.",
        "Classical South Indian painting of a traditional cartwright bending steamed acacia timber to form indestructible wagon wheels, working intently by the forge fire.",
        "Classical South Indian painting of diligent washermen and women boiling, rinsing, and beating white cottons on river stones at dawn, clean fabrics drying on grass.",
        "Classical South Indian painting of a dedicated temple garland maker stringing fresh jasmine, tulasi, and lotus blossoms into ten-foot garlands before the morning bell.",
        "Classical South Indian historical painting of an old guru looking with boundless pride at his diligent student who has surpassed him in grammar, astronomy, and righteousness.",
        "Classical South Indian magnificent panoramic oil painting of a bustling, prosperous Tamil agricultural and trading town where honest toil has brought joy to every home, masterpiece."
    ], start=14)
]

# 5. Curriculum Puranic & Historical Story Masterpieces (20 Paintings)
STORY_PROMPTS = [
    {
        "filename": "stories/grade3_sambandar_divine_milk.jpg",
        "title": "தரம் 3 கதை: ஞானசம்பந்தருக்கு உமையம்மை ஞானப்பால் ஊட்டுதல்",
        "prompt": "Masterpiece classical South Indian oil painting depicting the 3-year-old child saint Tirugnanasambandar wearing silver anklets and sacred thread on the stone steps of Sirkazhi temple tank. Goddess Uma Parvati and Lord Shiva appear in radiant golden celestial form on the sacred bull Nandi. The Divine Mother Uma tenderly offers a gleaming golden cup filled with divine milk of wisdom (Gnana Paal) to the crying child, who points his tiny finger toward the temple vimanam singing his first hymn 'Thodudaiya Seviyan'. Traditional Raja Ravi Varma realism, sacred emotional tenderness."
    },
    {
        "filename": "stories/grade4_appar_lime_kiln.jpg",
        "title": "தரம் 4 கதை: அப்பர் பெருமான் நீற்றறையிலிருந்து மாசில் வீணையுடன் வெளிவருதல்",
        "prompt": "Dramatic classical South Indian oil painting of Saint Thirunavukkarasar (Appar) emerging radiant, peaceful, and completely untouched from a scorching white lime kiln, singing 'மாசில் வீணையும் மாலை மதியமும்'. Holy white tripundra vibhuti and rudraksha on his body, gentle smile, holding a brass hoe (uzhavarappadai). The deadly heat transforms into a cool breeze and sweet moonlight by Lord Shiva's grace. Astonished Pallava king and royal guards drop their weapons in awe."
    },
    {
        "filename": "stories/grade5_sundarar_wedding_interruption.jpg",
        "title": "தரம் 5 கதை: சுந்தரரின் திருமணத்தில் முதிய அந்தணராக இறைவன் தோன்றி தடுத்தாட்கொள்ளுதல்",
        "prompt": "Classical South Indian historical oil painting in a grand, lavishly decorated Tamil wedding pandal with fresh banana trunks, hanging jasmine toranams, and sacrificial fire. The youthful, handsome bridegroom Sundarar in royal silk attire and gold jewelry turns in astonishment as an elderly, majestic ascetic Brahmin with flowing white beard, sacred thread, and tripundra vibhuti strides into the pavilion holding an ancient, rolled palm-leaf legal deed (olai chuvadi) claiming Sundarar as his bonded servant. Wedding guests in dramatic shock, divine theatrical chiaroscuro lighting."
    },
    {
        "filename": "stories/grade6_thirumoolar_cattle_compassion.jpg",
        "title": "தரம் 6 கதை: திருமூலர் இடையன் மூலனின் உடலினுள் புகுந்து பசுக்களைக் காத்தல்",
        "prompt": "Compassionate classical South Indian oil painting showing the great yogi Sundaranatha entering the deceased cowherd Moolan's body out of deep sorrow for the weeping herd of gentle native humped cows. The cows joyfully crowd around him, licking his hands and nuzzling his chest with tears of relief beside the green river bank under a golden twilight sky. Sacred tenderness, Raja Ravi Varma style."
    },
    {
        "filename": "stories/grade7_kannappa_nayanar_supreme_love.jpg",
        "title": "தரம் 7 கதை: கண்ணப்ப நாயனார் தன் கண்களை ஈசனுக்கு அற்பணித்தல்",
        "prompt": "Devotional classical South Indian oil painting depicting the young forest hunter Thinnan (Kannappar) kneeling with supreme love before the rugged granite Shiva Lingam at Kalahasti hill. He points a sharp hunting arrow toward his remaining eye to gouge it out for the bleeding stone lingam, while the divine glowing hand of Lord Shiva miraculously emerges from the solid stone Lingam firmly grasping his wrist, crying 'Stop, Kannappa!' in eternal divine love."
    },
    {
        "filename": "stories/grade8_karaikkal_ammaiyar_kailash.jpg",
        "title": "தரம் 8 கதை: காரைக்கால் அம்மையார் தலைகீழாக கயிலை மலையில் நடத்தல்",
        "prompt": "Mystical classical Indian spiritual oil painting of Saint Karaikkal Ammaiyar, transformed into a skeletal ascetic form of pure divine love, ascending the snowy sacred slopes of Mount Kailash upside-down on her hands so her feet do not desecrate holy ground. At the celestial summit, Lord Shiva and Parvati look down with boundless maternal love, Shiva welcoming her with the word 'Ammaye' (My Mother)."
    },
    {
        "filename": "stories/grade9_siruthondar_divine_guest.jpg",
        "title": "தரம் 9 கதை: சிறுத்தொண்ட நாயனார் வைரவர் பெருமானை இல்லறத்தில் உபசரித்தல்",
        "prompt": "Classical South Indian historical oil painting of general Siruthondar and his devoted wife Tiruvenkattu Nangai in the sanctum courtyard of their home, washing the sacred feet of a fierce, radiant Bhairava ascetic with folded hands and selfless humility. Golden brass lamps glowing, banana leaf feast prepared, supreme fidelity to the guest."
    },
    {
        "filename": "stories/grade10_manikkavasagar_horses_miracle.jpg",
        "title": "தரம் 10 கதை: நரிகளை பரிகளாக்கிய மாணிக்கவாசகரின் அற்புதம்",
        "prompt": "Majestic classical South Indian historical painting in Madurai royal palace courtyard. Prime minister Manikkavasagar stands in serene prayer with tripundra vibhuti, while Lord Shiva disguised as a regal master horseman in royal turban leads a cavalry of magnificent noble war stallions before the awe-struck Pandya king Arimardhana, divine golden morning light breaking through the dust."
    },
    {
        "filename": "stories/grade11_shravana_kumara_devotion.jpg",
        "title": "தரம் 11 கதை: சிரவணகுமாரன் தன் குருடான தாய் தந்தையரை காவடியில் சுமத்தல்",
        "prompt": "Emotional classical Indian oil painting of young Shravana Kumara carrying his elderly, blind parents in two woven cane baskets suspended from a sturdy bamboo shoulder pole (kavadi) along a lush riverbank pilgrimage route at sunrise. His devoted, loving expression as he steps gently, parents smiling with gratitude, golden mist, ultimate filial duty, Raja Ravi Varma realism."
    },
    {
        "filename": "stories/grade12_vallalar_light_dissolution.jpg",
        "title": "தரம் 12 கதை: வள்ளலார் பெருமான் சித்தி வளாகத்தில் ஜோதியாக கலத்தல்",
        "prompt": "Transcendental classical South Indian spiritual painting of Saint Ramalinga Vallalar at Siddhi Valagam in Vadalur. The saint clad in simple white cotton merges serenely into an infinite, blinding column of golden-white divine Arutperunjyothi light, disciples outside the closed doors in tearful veneration, radiating universal love."
    },
    {
        "filename": "stories/grade3_avvaiyar_athiyaman_amla.jpg",
        "title": "தரம் 3 கதை: அதியமான் ஔவையாருக்கு நெல்லிக்கனி நல்குதல்",
        "prompt": "Classical Tamil historical oil painting depicting noble king Athiyaman in his royal hill court at Tagadur humbly presenting the rare, immortal black gooseberry (Amla) to the venerable elderly Tamil poetess Avvaiyar. The king smiles with reverence, preferring the poet's life for Tamil literature over his own mortality. Avvaiyar holding her walking staff with touched heart."
    },
    {
        "filename": "stories/grade4_nandanar_nandi_miracle.jpg",
        "title": "தரம் 4 கதை: திருப்புன்கூரில் நந்தனாருக்காக நந்தி விலகிய அற்புதம்",
        "prompt": "Classical South Indian temple painting at Thirupunkur. Devoted saint Nandanar standing outside the temple entrance with tears of devotion, unable to see the Shiva Lingam because the massive stone Nandi bull blocks the view. Miraculously, the colossal granite Nandi leans aside by Lord Shiva's command, granting full darshan to the ecstatic saint."
    },
    {
        "filename": "stories/grade5_markandeya_yama_victory.jpg",
        "title": "தரம் 5 கதை: மார்க்கண்டேயன் சிவலிங்கத்தை கட்டித் தழுவி மரணத்தை வெல்லுதல்",
        "prompt": "Dynamic, heroic classical Indian oil painting of sixteen-year-old Markandeya tightly embracing the stone Shiva Lingam with devotion. Fierce Lord Yama on his black buffalo casts the death noose, but Lord Shiva erupts from the Lingam as Kalasamhara Murti with trident, kicking Yama away and bestowing eternal life upon the youthful sage."
    },
    {
        "filename": "stories/grade6_rajaraja_chola_temple_dedication.jpg",
        "title": "தரம் 6 கதை: முதலாம் ராஜராஜ சோழன் தஞ்சை பெரிய கோயிலை அர்ப்பணித்தல்",
        "prompt": "Epic classical Chola historical oil painting of Emperor Rajaraja Chola and his sister Kundavai standing before the colossal 216-foot granite vimanam of the Thanjavur Brihadisvara Temple during the consecration ceremony. Golden kalasam atop the vimanam, royal elephants, thousands of Sivacharyas chanting, monumental granite grandeur."
    },
    {
        "filename": "stories/grade7_sekkizhar_periyapuranam_recital.jpg",
        "title": "தரம் 7 கதை: சேக்கிழார் பெருமான் தில்லை நடராஜர் சந்நிதியில் பெரியபுராணம் அரங்கேற்றுதல்",
        "prompt": "Regal classical South Indian oil painting depicting Chief Minister Sekkizhar presenting the sacred palm-leaf Periyapuranam in the Thousand Pillared Hall of Chidambaram Nataraja Temple before King Kulothunga Chola and the assembly of Dikshitars, Lord Nataraja's golden sabha in background, intense devotional splendor."
    },
    {
        "filename": "stories/grade8_pattinathar_renunciation.jpg",
        "title": "தரம் 8 கதை: பட்டினத்தார் காதற்ற ஊசியும் வாராது காண் எனும் ஞானம் பெறுதல்",
        "prompt": "Dramatic classical Tamil oil painting of the billionaire merchant Pattinathar of Kaveripoompattinam holding a rusted, eyeless needle with a small note from his son 'even an eyeless needle will not accompany you at death'. A wave of supreme spiritual renunciation sweeps his face; he casts off his ruby necklaces and silk robes into the dust, walking forth as a free wandering sage."
    },
    {
        "filename": "stories/grade9_sambandar_madurai_debate.jpg",
        "title": "தரம் 9 கதை: மதுரையில் திருஞானசம்பந்தர் அனல்வாதம் மற்றும் புனல்வாதம் வெல்லுதல்",
        "prompt": "Historical classical South Indian oil painting on the banks of the Vaigai river in Madurai. Child prodigy Saint Sambandar standing serenely before Queen Mangayarkkarasi and King Nedumaran. His inscribed palm leaf swims upstream against the rushing river waters in victorious miracle, while ministers marvel at divine truth."
    },
    {
        "filename": "stories/grade10_arunagirinathar_murugan_grace.jpg",
        "title": "தரம் 10 கதை: அருணகிரிநாதரை முருகன் தன் வேல் கொண்டு ஆட்கொள்ளுதல்",
        "prompt": "Sublime devotional classical Tamil painting at the towering granite gopuram of Tiruvannamalai temple. Arunagirinathar throws himself down from the high stone tower in despair, but Lord Murugan with radiant golden Vel appears in mid-air, catching him in his divine arms and inscribing the sacred Pranava mantra Om on his tongue with the golden spear tip."
    },
    {
        "filename": "stories/grade11_harischandra_truth_triumph.jpg",
        "title": "தரம் 11 கதை: அரிச்சந்திரன் மயானத்தில் வாய்மை தவறாத மாண்பு",
        "prompt": "Soulful classical Indian oil painting in the nocturnal cremation grounds of Kashi. King Harischandra, working as a humble cemetery guard in torn loincloth, firmly refuses to cremate his dead son without the required tax from his weeping wife Chandramati, upholding absolute truth. Gods shower golden celestial flowers as his test concludes in triumph."
    },
    {
        "filename": "stories/grade12_nachiketas_return_enlightened.jpg",
        "title": "தரம் 12 கதை: நசிகேதன் ஆத்ம ஞானம் பெற்று பூமிக்கு மீளுதல்",
        "prompt": "Glorious classical Indian painting depicting young Nachiketas returning to his father sage Vajasravasa's hermitage. The boy's face radiates supreme, calm Atma-Jnana (self-realization) like a rising sun. His repentant father runs to embrace him with tears of joy, cattle, deer, and birds rejoicing at the return of the enlightened youth."
    }
]

# 6. Curriculum Living Householder Dharma Masterpieces (20 Paintings)
DHARMA_PROMPTS = [
    {
        "filename": "dharma/dharma_01_morning_parent_reverence.jpg",
        "title": "இல்லற தர்மம் 1: அதிகாலை பெற்றோரின் திருப்பாதங்களை வணங்கி ஆசி பெறுதல்",
        "prompt": "Classical Tamil domestic oil painting depicting young boy and girl performing Sashtanga Namaskaram touching the feet of their noble parents in the traditional sunlit thinnai courtyard of a village home. Father and mother with sacred vibhuti and smiling eyes blessing their heads, brass lamp glowing, Raja Ravi Varma style."
    },
    {
        "filename": "dharma/dharma_02_kolam_courtyard_sanctity.jpg",
        "title": "இல்லற தர்மம் 2: அதிகாலை வாசலில் அரிசி மாவு கோலமிட்டு அன்னதானம் செய்தல்",
        "prompt": "Serene dawn oil painting of a traditional Tamil mother in silk saree drawing intricate geometric white rice-flour Kolam on the freshly swept red earth outside the wooden carved threshold of her home. Sparrows and little squirrels happily pecking at the edible rice flour patterns, brass water vessel nearby, sacred peace."
    },
    {
        "filename": "dharma/dharma_03_pancha_maha_yajna_offering.jpg",
        "title": "இல்லற தர்மம் 3: இல்லறத்தான் இயற்றும் பஞ்ச மகா யாகங்கள்",
        "prompt": "Magnificent classical South Indian painting depicting the five noble sacrifices of a Tamil householder: feeding a wandering guest (Manushya Yajna), offering water to a sacred cow (Bhuta Yajna), studying scriptures with children (Brahma Yajna), offering water to ancestors (Pitru Yajna), and morning fire oblations (Deva Yajna)."
    },
    {
        "filename": "dharma/dharma_04_feeding_hungry_guest.jpg",
        "title": "இல்லற தர்மம் 4: பசித்த விருந்தினருக்கு முகம் மலர்ந்து உணவளித்தல்",
        "prompt": "Heartwarming classical Tamil oil painting of a noble householder couple serving a steaming hot feast on fresh green plantain leaves to unexpected weary travelers and pilgrims in their veranda. The wife pours fragrant sambar with a smiling, hospitable face, husband offering cool water from a brass kooja."
    },
    {
        "filename": "dharma/dharma_05_sandhyavandanam_riverbank.jpg",
        "title": "இல்லற தர்மம் 5: அந்தி சந்தி வந்தனம் & காயத்ரி ஜெபம்",
        "prompt": "Atmospheric classical South Indian oil painting of an upright householder father teaching his young son the sacred Sandhyavandanam Gayatri meditation at sunrise on the stone ghats of Kaveri river, offering sacred water arghyam toward the rising golden sun with pure devotion."
    },
    {
        "filename": "dharma/dharma_06_cow_veneration_kamadhenu.jpg",
        "title": "இல்லற தர்மம் 6: பசுவை கோமாதாவாக போற்றி வணங்குதல்",
        "prompt": "Charming classical Tamil domestic painting of a grandmother and little granddaughter applying sacred red kumkum and turmeric to the forehead of a gentle native Gir cow and her frisky calf, offering fresh green grass and jaggery in the sunlit backyard garden."
    },
    {
        "filename": "dharma/dharma_07_joint_family_evening_thevaram.jpg",
        "title": "இல்லற தர்மம் 7: மாலை விளக்கேற்றி கூட்டுப் பிரார்த்தனை செய்தல்",
        "prompt": "Warm, golden-lit classical Tamil interior oil painting of three generations of a joint family gathered in the central prayer room. Tall brass kuthuvilakku lamps glowing, children and elders singing Thevaram and Thiruppugazh hymns together with brass cymbals and hand claps."
    },
    {
        "filename": "dharma/dharma_08_elder_care_veneration.jpg",
        "title": "இல்லற தர்மம் 8: முதியோரை அன்போடு அரவணைத்துப் பேணுதல்",
        "prompt": "Touching classical South Indian domestic painting of an adult son gently applying soothing herbal oil to the tired feet of his elderly, resting father on a woven coir cot, while his wife brings a warm cup of herbal milk with deep affection and filial reverence."
    },
    {
        "filename": "dharma/dharma_09_guru_dakshina_reverence.jpg",
        "title": "இல்லற தர்மம் 9: வித்யாபியாசம் முடித்த சீடன் குரு தட்சிணை சமர்ப்பித்தல்",
        "prompt": "Reverent classical South Indian hermitage painting of a graduating young scholar bowing low before his venerable Guru under an ashram banyan tree, offering a silver tray with betel leaves, fresh fruits, and silk cloth as Guru Dakshina with tears of profound gratitude."
    },
    {
        "filename": "dharma/dharma_10_truthful_merchant_dharma.jpg",
        "title": "இல்லற தர்மம் 10: வாணிகத்தில் நேர்மையும் தூய அறமும்",
        "prompt": "Classical Tamil historical oil painting in a Madurai spice and grain bazaar. An honest Tamil merchant weighing peppercorns on brass balance scales, carefully ensuring the balance tilts slightly in favor of the customer, smiling with integrity, adhering to Thirukkural trade ethics."
    },
    {
        "filename": "dharma/dharma_11_ahimsa_protecting_creatures.jpg",
        "title": "இல்லற தர்மம் 11: அனைத்து உயிர்களிடத்தும் கொள்ளும் கொல்லாமை அறம்",
        "prompt": "Gentle classical South Indian garden painting of a Tamil householder farmer carefully placing a fallen bird chick back into its tree nest, while his little children scatter broken grains of rice for wild peacocks, squirrels, and pigeons feeding peacefully around their feet."
    },
    {
        "filename": "dharma/dharma_12_mutual_respect_spouses.jpg",
        "title": "இல்லற தர்மம் 12: கணவன் மனைவி இடையே நிலவும் சமத்துவ அன்பு",
        "prompt": "Dignified classical Tamil oil painting of a noble householder husband and wife consulting together in their library room over household ledgers and charitable plans, mutual respect and shared spiritual equality radiating from their serene expressions."
    },
    {
        "filename": "dharma/dharma_13_temple_service_uzhavaram.jpg",
        "title": "இல்லற தர்மம் 13: திருக்கோயில் திருப்பணியில் குடும்பத்தோடு ஈடுபடுதல்",
        "prompt": "Classical Tamil devotional painting of an entire village family joyfully performing temple cleaning service (uzhavaram) in an ancient granite temple courtyard: father weeding stone pavement crevices, mother sweeping, children washing brass oil lamps."
    },
    {
        "filename": "dharma/dharma_14_charity_annadhanam_festival.jpg",
        "title": "இல்லற தர்மம் 14: திருவிழா நாட்களில் ஊருக்கே அன்னதானம் வழங்கல்",
        "prompt": "Vibrant classical South Indian festival painting of a large community Annadhanam hall during a temple festival. Noble householders rolling up their sleeves to serve piping hot sweet pongal, rice, and vadai to hundreds of seated villagers and pilgrims of all castes."
    },
    {
        "filename": "dharma/dharma_15_planting_shade_trees.jpg",
        "title": "இல்லற தர்மம் 15: வழிப்போக்கர்களுக்காக நிழல் தரும் மரங்களை நடுதல்",
        "prompt": "Classical South Indian rural oil painting of a householder father and his two teenage sons planting sturdy banyan and neem saplings along a dusty pilgrim highway, building protective thorn fences and watering them from clay pots for future generations."
    },
    {
        "filename": "dharma/dharma_16_water_charity_thanneer_panthal.jpg",
        "title": "இல்லற தர்மம் 16: கோடைக்காலத்தில் தண்ணீர் பந்தல் அமைத்து தாகம் தீர்த்தல்",
        "prompt": "Sunny classical South Indian summer painting of a thatched roadside water shed (Thanneer Panthal). A kind-hearted householder girl pouring cool water from a fragrant vetiver-wrapped clay pot into the cupped hands of a weary traveling pilgrim."
    },
    {
        "filename": "dharma/dharma_17_learning_scriptures_olai_chuvadi.jpg",
        "title": "இல்லற தர்மம் 17: நாள்தோறும் திருமுறை & திருக்குறள் ஓதுதல்",
        "prompt": "Classical Tamil domestic painting of a father holding an inscribed palm-leaf manuscript (olai chuvadi) on the open courtyard thinnai, chanting verses of Thirukkural and Thevaram to his eager young children listening attentively in evening twilight."
    },
    {
        "filename": "dharma/dharma_18_forgiveness_resolving_dispute.jpg",
        "title": "இல்லற தர்மம் 18: இன்சொல்லும் பொறுமையும் கொண்டு பகையை வெல்லுதல்",
        "prompt": "Nobly composed classical South Indian painting of a calm, dignified Tamil householder embracing an angry neighbor who has come to quarrel, disarming hostility with gentle words, a cool cup of buttermilk, and genuine forgiving patience."
    },
    {
        "filename": "dharma/dharma_19_frugal_noble_living.jpg",
        "title": "இல்லற தர்மம் 19: ஆடம்பரமின்றி எளிய தூய வாழ்வு வாழ்தல்",
        "prompt": "Sublime classical Tamil interior oil painting of a prosperous yet thoroughly simple household. Spotless clay and stone surfaces, hand-spun unbleached cotton clothes, a healthy simple vegetarian meal, living with total contentment and zero ostentation."
    },
    {
        "filename": "dharma/dharma_20_peaceful_fulfillment_old_age.jpg",
        "title": "இல்லற தர்மம் 20: அறநெறி வாழ்ந்து நிறைவடைந்த முதியோரின் சாந்தம்",
        "prompt": "Heart-soothing classical South Indian painting of an elderly venerable Tamil couple seated on their garden porch at sunset. Surrounded by loving grandchildren playing, their work in the world completed in righteousness, eyes glowing with supreme inner peace and liberation."
    }
]

def make_cell(cell_type, source_code):
    return {
        "cell_type": cell_type,
        "metadata": {},
        "source": [line + "\n" for line in source_code.strip().split("\n")]
    }

def build_comprehensive_notebook():
    cells = []
    
    # Header markdown
    cells.append(make_cell("markdown", """# 🎨 குரு குல தேசம் (Guru Kula Desam) — SOTA Artwork Generator (Indo-Realism Edition)
### High-Fidelity GPU Artwork Generator for `nagaraj957@gmail.com`
This upgraded studio notebook brings **maximum cultural authenticity and anatomical perfection** using:
1. 🌟 **`FLUX.1-schnell` + `Indo-Realism LoRA`** (`prithivMLmods/Flux.1-Dev-Indo-Realism-LoRA`):
   - Eliminates deformed hands, plastic skin, and fake orientalist fantasy.
   - Enforces authentic South Indian Tamil heritage, *Tripundra Vibhuti*, *Rudraksha*, *Kanchipuram* silk weaves, and sacred Chola granite architecture.
2. 🏛️ **`Juggernaut-XL-v9` (RunDiffusion)**: Premier classical oil-painting model with negative prompts against foreign fantasy or Tibetan robes.
3. ⚡ **`SDXL-Lightning-4Steps`**: Fast preview mode.

---

### 📦 150 Masterpiece Prompts Included:
- **11 Core Grade 8-12 Bespoke Lessons** (Chatur Ashramas, 28 Agamas, Body is Temple, Six Darshanas, Pati-Pasu-Pasam, Chariot Festival, Nachiketas, Pancha Koshas, Jivanmukti, Thayumanavar, Grihastha Nirvana)
- **20 Puranic & Historical Story Masterpieces** (Sambandar, Appar, Sundarar, Thirumoolar, Kannappar, Karaikkal Ammaiyar, Siruthondar, Manikkavasagar, Shravana Kumara, Vallalar, etc.)
- **20 Living Householder Dharma Masterpieces** (Morning parent reverence, Kolam courtyard charity, Pancha Maha Yajnas, joint family prayer, guest feeding, etc.)
- **99 Thirukkural Continuous Cinema Shots** (Chapters 54, 57, 61 — 33 dedicated shots each)
"""))

    # Cell 1: Environment Setup
    cells.append(make_cell("code", """#@title Step 1: Install SOTA Diffusion & LoRA Libraries
#@markdown Installs `diffusers`, `transformers`, `accelerate`, `safetensors`, `torch`, `sentencepiece`, `peft`, and `bitsandbytes`.
!pip install -q diffusers transformers accelerate safetensors torch torchvision sentencepiece bitsandbytes protobuf peft huggingface_hub

import torch
print("PyTorch Version:", torch.__version__)
if torch.cuda.is_available():
    device_name = torch.cuda.get_device_name(0)
    vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
    print(f"✅ GPU Active: {device_name}")
    print(f"✅ Dedicated VRAM: {vram_gb:.2f} GB")
else:
    print("⚠️ WARNING: GPU not detected! Go to Runtime -> Change runtime type -> Select T4 GPU (or A100/L4).")
"""))

    # Cell 2: Model Pipeline Setup with LoRA Loading
    cells.append(make_cell("code", """#@title Step 2: Select & Load Generation Engine with Indian LoRA
#@markdown Choose your preferred generation engine:
#@markdown - **FLUX.1-schnell + Indo-Realism LoRA (Recommended #1)**: 12B DiT with specialized Indian cultural & anatomical LoRA.
#@markdown - **Juggernaut-XL-v9 (Studio Indian Realism)**: Premier fine-art SDXL fine-tune with negative prompt filtering.
#@markdown - **SDXL-Lightning-4Steps (Fast Batch)**: High-speed 4-step generation for quick checks.

MODEL_ENGINE = "FLUX.1-schnell + Indo-Realism LoRA (Recommended)" #@param ["FLUX.1-schnell + Indo-Realism LoRA (Recommended)", "Juggernaut-XL-v9 (Studio Indian Realism)", "SDXL-Lightning-4Steps (Fast Batch)"]
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
import torch
from diffusers import (
    StableDiffusionXLPipeline,
    DPMSolverMultistepScheduler,
    UNet2DConditionModel,
    EulerDiscreteScheduler
)

pipe = None

if "FLUX.1-schnell" in MODEL_ENGINE:
    print("⏳ Loading FLUX.1-schnell (Black Forest Labs 12B DiT)...")
    from diffusers import FluxPipeline
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-schnell",
        torch_dtype=torch.bfloat16
    )
    print("⏳ Attaching Indo-Realism LoRA (prithivMLmods/Flux.1-Dev-Indo-Realism-LoRA)...")
    try:
        pipe.load_lora_weights("prithivMLmods/Flux.1-Dev-Indo-Realism-LoRA", weight_name="indo-realism.safetensors")
        print("✅ Indo-Realism LoRA attached successfully!")
    except Exception as e:
        print(f"⚠️ LoRA attach note: {e}")
    pipe.enable_model_cpu_offload()
    print("✅ FLUX.1-schnell + Indo-Realism ready!")

elif "Juggernaut-XL-v9" in MODEL_ENGINE:
    print("⏳ Loading Juggernaut-XL-v9 photorealistic fine-art model...")
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "RunDiffusion/Juggernaut-XL-v9",
        torch_dtype=torch.float16,
        variant="fp16"
    ).to("cuda")
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True)
    pipe.enable_attention_slicing()
    print("✅ Juggernaut-XL-v9 loaded and calibrated!")

elif "SDXL-Lightning" in MODEL_ENGINE:
    print("⏳ Loading SDXL-Lightning 4-step UNet...")
    from huggingface_hub import hf_hub_download
    from safetensors.torch import load_file
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

def generate_art(prompt, seed=None):
    generator = torch.Generator("cuda").manual_seed(seed) if seed else None
    
    if "FLUX.1" in MODEL_ENGINE:
        # Inject Indo-Realism trigger word and classical South Indian sacred art tokens
        full_prompt = (
            "indo-realism, classical South Indian oil painting masterpiece in the style of Raja Ravi Varma and Thanjavur fine art, "
            + prompt
            + ", authentic South Indian facial features, sacred tripundra vibhuti on forehead, rudraksha malas, traditional silk veshti and Kanchipuram saree, ancient Dravidian granite temple architecture, perfectly formed anatomical hands, 8k resolution, cinematic golden hour lighting"
        )
        return pipe(
            prompt=full_prompt,
            num_inference_steps=6,
            width=WIDTH,
            height=HEIGHT,
            guidance_scale=1.5,
            generator=generator
        ).images[0]
        
    elif "Juggernaut-XL" in MODEL_ENGINE:
        neg = "malformed hands, distorted fingers, extra fingers, missing fingers, deformed anatomy, plastic skin, 3d render, anime, cartoon, western clothing, modern clothing, buddhist monk robes, conical hats, orientalist fantasy, blurry, low resolution, signature, watermark"
        full_prompt = (
            "masterpiece, classical South Indian oil painting, Raja Ravi Varma realism, Tanjore fine art, "
            + prompt
            + ", authentic Tamil heritage, sacred tripundra vibhuti, rudraksha, authentic silk veshti, granite temple, 8k resolution"
        )
        return pipe(
            prompt=full_prompt,
            negative_prompt=neg,
            num_inference_steps=35,
            guidance_scale=7.5,
            width=WIDTH,
            height=HEIGHT,
            generator=generator
        ).images[0]
        
    elif "SDXL-Lightning" in MODEL_ENGINE:
        return pipe(
            prompt=prompt,
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

OVERWRITE_EXISTING = True #@param {{type:"boolean"}}
GENERATE_LESSONS = True #@param {{type:"boolean"}}
GENERATE_STORIES = True #@param {{type:"boolean"}}
GENERATE_DHARMA = True #@param {{type:"boolean"}}
GENERATE_TK_54 = True #@param {{type:"boolean"}}
GENERATE_TK_57 = True #@param {{type:"boolean"}}
GENERATE_TK_61 = True #@param {{type:"boolean"}}

import os
from PIL import Image
from IPython.display import display

all_tasks = []

if GENERATE_LESSONS:
    all_tasks.extend({json.dumps(LESSON_PROMPTS, ensure_ascii=False)})

if GENERATE_STORIES:
    all_tasks.extend({json.dumps(STORY_PROMPTS, ensure_ascii=False)})

if GENERATE_DHARMA:
    all_tasks.extend({json.dumps(DHARMA_PROMPTS, ensure_ascii=False)})

if GENERATE_TK_54:
    all_tasks.extend({json.dumps(TK_54_PROMPTS, ensure_ascii=False)})

if GENERATE_TK_57:
    all_tasks.extend({json.dumps(TK_57_PROMPTS, ensure_ascii=False)})

if GENERATE_TK_61:
    all_tasks.extend({json.dumps(TK_61_PROMPTS, ensure_ascii=False)})

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
    
    if not OVERWRITE_EXISTING and os.path.exists(full_dest) and os.path.getsize(full_dest) > 10000:
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
        
    print(f"✅ Generated upgraded Colab Notebook: {nb_path} with {len(cells)} cells and 150 master prompts!")

if __name__ == '__main__':
    build_comprehensive_notebook()
