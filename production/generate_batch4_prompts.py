# -*- coding: utf-8 -*-
"""
Batch 4 Master Art Prompts Generator: Dynamic Enterprise & Heroic Action Suite
Chapters:
  - 60: ஊக்கமுடைமை (Ookkamudaimai - Energy & Determination) -> 50 shots
  - 62: ஆள்வினையுடைமை (Aalvinaiyudaimai - Industrious Enterprise) -> 47 shots
  - 65: சொல்வன்மை (Solvanmai - Eloquent & Powerful Speech) -> 54 shots
  - 66: வினைத்தூய்மை (Vinaithooymai - Purity of Action) -> 44 shots
  - 67: வினைத்திட்பம் (Vinaithitpam - Resolute Action & Will) -> 49 shots
  - 74: நாடு (Naadu - The Prosperous Realm) -> 35 shots
Total: 279 unique cinematic shots
"""

import sys
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

# -------------------------------------------------------------
# CHAPTER 60: ஊக்கமுடைமை (Ookkamudaimai) - 50 SHOTS
# -------------------------------------------------------------
CH60_PROMPTS = [
    # Kural 591: Possessing energy is true possession; wealth without energy vanishes
    ("60-ookkamudaimai/01-n01_flame_of_determination_in_warrior_eyes.jpg", "Kural 591: Inner energy as the supreme true wealth",
     "Photorealistic 16:9 cinematic close-up, Sangam Tamil commander with piercing determined eyes lit by glowing bronze torch flame at night, bronze chestplate, unyielding focus."),
    ("60-ookkamudaimai/02-n02_youth_facing_roaring_ocean_gale.jpg", "Kural 591: Fearless youth standing steadfast against stormy winds",
     "Photorealistic 16:9 cinematic shot, rocky coastal promontory of ancient Poompuhar at dusk, athletic young Tamil navigator standing tall against ocean spray and stormy wind."),
    ("60-ookkamudaimai/03-n03_fleeting_gold_slipping_like_sand.jpg", "Kural 591: Transience of wealth without sustained effort",
     "Photorealistic 16:9 cinematic macro shot, hands opening as gold coins and fine river sand slip through trembling fingers on marble palace floor, dramatic side lighting."),
    ("60-ookkamudaimai/04-n04_steady_granite_pillar_standing_unshaken.jpg", "Kural 591: Enduring strength of resolute character",
     "Photorealistic 16:9 cinematic architectural shot, massive hand-carved monolithic granite pillar in ancient temple corridor standing solid as storm shadows flicker."),
    ("60-ookkamudaimai/05-n05_artisan_striking_iron_anvil_sparks.jpg", "Kural 591: Relentless vigor in the blacksmith forge",
     "Photorealistic 16:9 cinematic dynamic action shot, ancient Tamil armorer swinging heavy iron hammer on red-hot sword blade, brilliant golden sparks cascading over charcoal forge."),

    # Kural 592: Energy of mind is true property; material wealth leaves soon
    ("60-ookkamudaimai/06-n06_sage_walking_unarmed_through_mountain_pass.jpg", "Kural 592: Fearless composure of the spiritually resolute",
     "Photorealistic 16:9 cinematic wide shot, mist-shrouded Western Ghats gorge, serene solitary Tamil wandering seeker in saffron veshti walking confidently past craggy boulders at dawn."),
    ("60-ookkamudaimai/07-n07_empty_treasury_vault_reclaimed_by_vigor.jpg", "Kural 592: Overcoming poverty through boundless inner drive",
     "Photorealistic 16:9 cinematic film still, sunbeam piercing into dark stone vault where a determined young merchant rolls up his sleeves to rebuild his commerce from scratch."),
    ("60-ookkamudaimai/08-n08_charioteer_taming_wild_steeds.jpg", "Kural 592: Mind mastering turbulent impulses",
     "Photorealistic 16:9 cinematic dramatic shot, sandy riverbed, veteran Tamil charioteer firmly gripping leather reins of four rearing black stallions, morning dust catching sunrise."),
    ("60-ookkamudaimai/09-n09_weaver_operating_intricate_wooden_loom.jpg", "Kural 592: Diligence creating enduring beauty",
     "Photorealistic 16:9 cinematic medium shot, Kanchipuram weaver throwing polished wooden shuttle through golden silk warp threads, rhythmic concentration in morning veranda."),
    ("60-ookkamudaimai/10-n10_beacon_fire_blazing_on_hilltop.jpg", "Kural 592: Unquenchable fire of enterprise",
     "Photorealistic 16:9 cinematic night shot, giant bonfire blazing inside stone watchtower brazier atop granite ridge, sending crimson embers into starry Tamil sky."),

    # Kural 593: Those with tireless enthusiasm never lament saying 'we are lost'
    ("60-ookkamudaimai/11-n11_mariners_rebuilding_broken_mast_at_sea.jpg", "Kural 593: Never despairing amid disaster",
     "Photorealistic 16:9 cinematic dramatic scene, wooden trading vessel deck at sea after storm, crew working urgently together with hemp ropes and adzes to raise a new timber mast."),
    ("60-ookkamudaimai/12-n12_farmer_plowing_after_drought_rain.jpg", "Kural 593: Renewed vigor when hope returns",
     "Photorealistic 16:9 cinematic shot, red soil field under heavy rain clouds, resilient Tamil farmer with white bullocks cutting deep dark furrows with wooden plow, joyful perseverance."),
    ("60-ookkamudaimai/13-n13_caravan_crossing_arid_scrubland.jpg", "Kural 593: Steadfast endurance across harsh landscapes",
     "Photorealistic 16:9 cinematic wide landscape, long line of bullock carts and merchant guards marching steadily across heat-hazed Deccan plateau beneath expansive afternoon sky."),
    ("60-ookkamudaimai/14-n14_scholar_copying_manuscript_by_oil_lamp.jpg", "Kural 593: Tireless intellect preserving wisdom",
     "Photorealistic 16:9 cinematic close-up, weathered Sangam scholar holding iron stylus, etching precise Tamil Brahmi characters onto dried palmyra leaf by warm terracotta lamp."),
    ("60-ookkamudaimai/15-n15_young_apprentice_hewing_granite_block.jpg", "Kural 593: Patient effort shaping the impossible",
     "Photorealistic 16:9 cinematic medium shot, temple stone-carving courtyard, young apprentice chipping away granite flakes with chisel and mallet under banyan shade."),

    # Kural 594: Fortune itself seeks out the man of unflagging resolve
    ("60-ookkamudaimai/16-n16_goddess_lakshmi_aura_over_industrious_hall.jpg", "Kural 594: Prosperity greeting the door of the energetic",
     "Photorealistic 16:9 cinematic ethereal shot, open teak palace gates at dawn, golden light illuminating brass kolam vessels and blooming lotus garlands as trade caravans arrive."),
    ("60-ookkamudaimai/17-n17_dockworkers_unloading_wealth_of_ships.jpg", "Kural 594: Influx of global trade to industrious harbors",
     "Photorealistic 16:9 cinematic panoramic view, ancient port of Muziris, hundreds of sailors and laborers unloading amphorae, gold ingots, and aromatic spices along wooden docks."),
    ("60-ookkamudaimai/18-n18_bountiful_storehouses_of_grain.jpg", "Kural 594: Fruitful abundance following relentless labor",
     "Photorealistic 16:9 cinematic interior, vaulted stone granary overflowing with golden paddy grains, village elders inspecting quality with warm smiles of fulfillment."),
    ("60-ookkamudaimai/19-n19_river_canal_cleared_by_volunteer_citizens.jpg", "Kural 594: Collective energy revitalizing the kingdom",
     "Photorealistic 16:9 cinematic wide shot, dozens of village youths working knee-deep in mud, clearing ancient stone irrigation sluice, fresh water gushing forward."),
    ("60-ookkamudaimai/20-n20_monarch_crowning_industrious_pioneer.jpg", "Kural 594: State honoring civic enterprise",
     "Photorealistic 16:9 cinematic royal court, Tamil king in ceremonial pearl necklace honoring a pioneering irrigation master with an inscribed copper plate and silk turban."),

    # Kural 595: Water lily stalk grows with water depth; man rises with greatness of soul
    ("60-ookkamudaimai/21-n21_blooming_lotus_rising_above_deep_pond.jpg", "Kural 595: Lotus flower soaring above deep waters",
     "Photorealistic 16:9 cinematic poetic macro shot, deep sacred temple tank, immaculate pink lotus bloom rising tall on slender green stem above mirror-still deep water at sunrise."),
    ("60-ookkamudaimai/22-n22_water_lily_pads_floating_in_monsoon_swell.jpg", "Kural 595: Adaptation to rising challenges",
     "Photorealistic 16:9 cinematic high-angle shot, raindrops creating concentric ripples around floating round lily leaves and vibrant purple water flowers in village pond."),
    ("60-ookkamudaimai/23-n23_swimmer_surfacing_with_radiant_breath.jpg", "Kural 595: Rising triumphant from the depths",
     "Photorealistic 16:9 cinematic underwater-to-surface transition, pearl diver breaking through turquoise ocean surface, taking a triumphant deep breath under golden morning sun."),
    ("60-ookkamudaimai/24-n24_eagle_soaring_on_mountain_updraft.jpg", "Kural 595: Elevation matched to inner vision",
     "Photorealistic 16:9 cinematic majestic nature shot, brahminy kite with broad rust-red wings riding powerful thermals above misty emerald peaks of the Western Ghats."),
    ("60-ookkamudaimai/25-n25_young_scholar_standing_among_elder_masters.jpg", "Kural 595: Lofty mind rising naturally to high stature",
     "Photorealistic 16:9 cinematic scene, Madurai Sangam academy terrace, brilliant young philosopher debating respectfully among venerable grey-bearded masters, serene confidence."),

    # Kural 596: Let your aspirations always be lofty; even if thwarted, dignity remains
    ("60-ookkamudaimai/26-n26_architect_sketching_monumental_temple_gopuram.jpg", "Kural 596: Conceiving grand architectural dreams",
     "Photorealistic 16:9 cinematic medium shot, master architect holding a charcoal stylus over a large vellum scroll, drafting plans for a towering stone tower, visionary eyes."),
    ("60-ookkamudaimai/27-n27_sculptor_gazing_at_unhewn_cliff_face.jpg", "Kural 596: Seeing the god within the wild stone",
     "Photorealistic 16:9 cinematic wide shot, coastal granite cliff of Mamallapuram at dawn, master sculptor standing before blank cliff wall, visualizing grand chariot shrines."),
    ("60-ookkamudaimai/28-n28_warrior_aiming_at_distant_mountain_target.jpg", "Kural 596: Setting sights upon the highest mark",
     "Photorealistic 16:9 cinematic shot, archery ground on grassy plateau, young warrior drawing bowstring back to cheek, aiming toward far flag fluttering on mountain peak."),
    ("60-ookkamudaimai/29-n29_astronomer_calculating_planetary_courses.jpg", "Kural 596: Reaching for cosmic heights of understanding",
     "Photorealistic 16:9 cinematic night shot, open palace observatory terrace, ancient astronomer using brass armillary ring and water clock to chart planetary alignments."),
    ("60-ookkamudaimai/30-n30_monarch_surveying_broad_realm_from_summit.jpg", "Kural 596: Vision encompassing the welfare of all",
     "Photorealistic 16:9 cinematic panoramic vista, Tamil monarch in crimson silk standing atop fortress summit overlooking vast green river valley dotted with villages and temples."),

    # Kural 597: Elephant pierced with arrows stands firm; brave man yields not to adversity
    ("60-ookkamudaimai/31-n31_tusker_bearing_battle_scars_standing_immovable.jpg", "Kural 597: War elephant standing resolute despite wounds",
     "Photorealistic 16:9 cinematic dramatic shot, massive royal bull elephant with ornamental bronze headplate, standing unshaken amid dust and falling monsoon rain, regal composure."),
    ("60-ookkamudaimai/32-n32_shield_wall_holding_against_barrage.jpg", "Kural 597: Unbroken shield wall of steadfast soldiers",
     "Photorealistic 16:9 cinematic intense scene, Sangam infantry locking heavy hide-and-bronze shields together, standing shoulder to shoulder against incoming volley of arrows."),
    ("60-ookkamudaimai/33-n33_veteran_commander_calming_his_troops.jpg", "Kural 597: Leadership in the crucible of trial",
     "Photorealistic 16:9 cinematic medium shot, scarred veteran commander raising his bronze sword with calm authority, rallying battle-weary comrades with fearless gaze."),
    ("60-ookkamudaimai/34-n34_monolithic_sea_rock_breaking_turbulent_waves.jpg", "Kural 597: Sea rock shattering the fury of storms",
     "Photorealistic 16:9 cinematic seascape, dark granite headland at Kanyakumari enduring thunderous turquoise ocean waves breaking into white foam, immovable permanence."),
    ("60-ookkamudaimai/35-n35_wounded_patriot_nursing_his_comrade.jpg", "Kural 597: Heroic fortitude caring for others",
     "Photorealistic 16:9 cinematic tender warrior scene, under canvas tent at dusk, wounded soldier bandaging comrade's shoulder with herbal salve, smiles of mutual brotherly courage."),

    # Kural 598: Without hearty energy, one cannot attain the glory of great bounty
    ("60-ookkamudaimai/36-n36_philanthropist_distributing_rice_to_pilgrims.jpg", "Kural 598: Generosity made possible through active enterprise",
     "Photorealistic 16:9 cinematic wide shot, temple choultry hall, benevolent merchant ladle-serving fragrant hot pongal rice to long line of tired pilgrims and travelers."),
    ("60-ookkamudaimai/37-n37_caravan_leader_opening_free_water_wells.jpg", "Kural 598: Creating life-saving civic infrastructure",
     "Photorealistic 16:9 cinematic outdoor shot, thirsty roadside grove in arid plains, caravan master unveiling a stone well with wooden pulley, cold fresh water pouring into clay pots."),
    ("60-ookkamudaimai/38-n38_noble_patron_gifting_bronze_lamp_to_temple.jpg", "Kural 598: Devotional endowment from honest industry",
     "Photorealistic 16:9 cinematic interior, pillared mandapam glowing with thousands of clay lamps, donor presenting a towering five-tier bronze Deepalakshmi lamp to priests."),
    ("60-ookkamudaimai/39-n39_shipwright_donating_vessel_for_famine_relief.jpg", "Kural 598: Mobilizing grand resources for public good",
     "Photorealistic 16:9 cinematic harbor view, shipbuilders launching new double-masted vessel loaded with rice bags into calm river mouth, cheering townspeople."),
    ("60-ookkamudaimai/40-n40_patron_honoring_visiting_bards_with_gold.jpg", "Kural 598: Magnanimous reward for poets and artists",
     "Photorealistic 16:9 cinematic audience scene, Chola chieftain adorning visiting female bard with golden lotus pendant, admiring assembly applauding the sacred arts."),

    # Kural 599: Elephant with sharp tusks flees when tiger roars; size yields to zeal
    ("60-ookkamudaimai/41-n41_bengal_tiger_prowling_bamboo_jungle.jpg", "Kural 599: Fiery spirit of the royal tiger",
     "Photorealistic 16:9 cinematic wildlife shot, sun-dappled Western Ghats bamboo grove, magnificent Royal Bengal tiger with blazing eyes and muscular stride radiating pure courage."),
    ("60-ookkamudaimai/42-n42_wild_tusker_pausing_in_dense_thicket.jpg", "Kural 599: Huge bulk acknowledging dynamic courage",
     "Photorealistic 16:9 cinematic medium-wide shot, massive wild elephant standing back among twisted jungle vines, ears flared in caution at distant predator roar."),
    ("60-ookkamudaimai/43-n43_small_scouting_boat_outmaneuvering_gale.jpg", "Kural 599: Agility and spirit surpassing raw mass",
     "Photorealistic 16:9 cinematic marine shot, slender Tamil catamaran riding crest of towering ocean swell with fearless paddle strokes, slipping through storm safely."),
    ("60-ookkamudaimai/44-n44_swift_panther_leaping_granite_ravine.jpg", "Kural 599: Daring leap of decisive vigor",
     "Photorealistic 16:9 cinematic action shot, golden hour mountain pass, sleek black panther leaping gracefully across deep rocky fissure, airborne silhouette against sunset."),
    ("60-ookkamudaimai/45-n45_slender_swordsman_disarming_heavy_opponent.jpg", "Kural 599: Skill and zealous focus conquering brute force",
     "Photorealistic 16:9 cinematic martial duel, martial arts kalaripayattu sand arena, agile young fighter with urumi whip-sword deftly stepping inside heavy club swing."),

    # Kural 600: Energy is a man's true strength; without it, he is but a tree in human form
    ("60-ookkamudaimai/46-n46_lifeless_dry_log_beside_living_sprout.jpg", "Kural 600: Contrast between inertia and vibrant life",
     "Photorealistic 16:9 cinematic nature metaphor, parched dry fallen tree trunk lying on mossy forest floor, right beside a vibrant green seedling bursting through loam into sunlight."),
    ("60-ookkamudaimai/47-n47_sluggish_idlers_lounging_under_shade.jpg", "Kural 600: The dull emptiness of indolent existence",
     "Photorealistic 16:9 cinematic scene, village square at midday, listless men lounging against dusty temple wall, eyes vacant as vibrant life and commerce bustle past them."),
    ("60-ookkamudaimai/48-n48_dynamic_runners_carrying_royal_scrolls.jpg", "Kural 600: Swift messengers driven by purposeful energy",
     "Photorealistic 16:9 cinematic dynamic action shot, two athletic Tamil courier runners with brass batons sprinting across sunlit red-dirt country trail with effortless endurance."),
    ("60-ookkamudaimai/49-n49_banyan_tree_sending_prop_roots_into_earth.jpg", "Kural 600: Boundless vitality anchoring into the world",
     "Photorealistic 16:9 cinematic grand nature shot, centuries-old giant banyan tree sending hundreds of sturdy prop roots into earth, lush green canopy humming with birds at dawn."),
    ("60-ookkamudaimai/50-n50_triumphant_hero_welcoming_the_dawn.jpg", "Kural 600: Sovereign glory of the purposeful spirit",
     "Photorealistic 16:9 cinematic final shot, warrior-philosopher standing on cliff edge at dawn, arms open to golden rising sun, wind whipping silk dhoti, absolute vitality.")
]

# -------------------------------------------------------------
# CHAPTER 62: ஆள்வினையுடைமை (Aalvinaiyudaimai) - 47 SHOTS
# -------------------------------------------------------------
CH62_PROMPTS = [
    # Kural 611: Do not faint at difficulty; sustained effort yields greatness
    ("62-aalvinaiyudaimai/01-n01_mason_carving_steps_up_mountain_cliff.jpg", "Kural 611: Patiently hewing stairway into bare rock",
     "Photorealistic 16:9 cinematic wide shot, steep mountain precipice, determined ancient Tamil mason with iron chisel and mallet cutting footholds into vertical granite wall."),
    ("62-aalvinaiyudaimai/02-n02_farmer_digging_irrigation_trench_in_hardpan.jpg", "Kural 621: Breaking sun-baked clay with relentless pickaxe",
     "Photorealistic 16:9 cinematic shot, parched delta field, muscular farmer swinging heavy bronze-tipped adze into cracked dry soil, sweat glistening under midday sun."),
    ("62-aalvinaiyudaimai/03-n03_scholar_deciphering_faded_inscriptions.jpg", "Kural 611: Untiring scholarly perseverance",
     "Photorealistic 16:9 cinematic close-up, ancient epigraphist gently brushing moss off weathered granite temple inscription, tracing faint Brahmi letters with fingertips."),
    ("62-aalvinaiyudaimai/04-n04_potter_kneading_stiff_river_clay.jpg", "Kural 611: Transforming rough elements through labor",
     "Photorealistic 16:9 cinematic medium shot, potter's workshop, artisan kneading thick grey alluvial clay with bare feet and strong hands on granite slab, morning sunlight."),
    ("62-aalvinaiyudaimai/05-n05_pearl_divers_preparing_ropes_at_dawn.jpg", "Kural 611: Venturing into dangerous depths without fear",
     "Photorealistic 16:9 cinematic morning shot, wooden catamaran rocking on calm swells off Tuticorin coast, divers tying stone dive-weights and nose-clips before plunging."),

    # Kural 612: Beware of leaving tasks unfinished; world cares not for half-done work
    ("62-aalvinaiyudaimai/06-n06_half_built_temple_covered_in_vines.jpg", "Kural 612: Tragedy of the abandoned endeavor",
     "Photorealistic 16:9 cinematic moody shot, overgrown jungle clearing, half-erected stone mandapam with exposed pillars choked by creeping jungle vines and wild briers."),
    ("62-aalvinaiyudaimai/07-n07_carpenter_placing_final_keystone_in_hull.jpg", "Kural 612: Seeing the work through to completion",
     "Photorealistic 16:9 cinematic workshop shot, shipwright driving the final teak peg into the sternpost of a seafaring dhow, smiling in quiet fulfillment."),
    ("62-aalvinaiyudaimai/08-n08_weaver_tying_off_golden_border_fringe.jpg", "Kural 612: Finishing the masterpiece with pristine care",
     "Photorealistic 16:9 cinematic macro shot, weaver's delicate fingers tying intricate golden tassels at the border of a completed royal silk saree."),
    ("62-aalvinaiyudaimai/09-n09_dam_builders_securing_last_sluice_gate.jpg", "Kural 612: Sealing the fortress against disaster",
     "Photorealistic 16:9 cinematic dramatic shot, granite check-dam on Kaveri river, engineers securing heavy wooden sluice gate with bronze chains as river water rises."),
    ("62-aalvinaiyudaimai/10-n10_monarch_signing_completed_treaty_scroll.jpg", "Kural 612: Concluding diplomatic accords with precision",
     "Photorealistic 16:9 cinematic courtly scene, king stamping royal tiger seal into hot red lacquer on tied palm-leaf treaty scroll, completing years of diplomacy."),

    # Kural 613: The noble desire to help others thrives only on manly effort
    ("62-aalvinaiyudaimai/11-n11_village_headman_distributing_seed_grain.jpg", "Kural 613: Philanthropy founded on prosperous industry",
     "Photorealistic 16:9 cinematic outdoor scene, village granary courtyard, generous elder distributing woven sacks of prime seed grain to neighboring smallholders after drought."),
    ("62-aalvinaiyudaimai/12-n12_communal_well_digging_by_village_youth.jpg", "Kural 613: Collective labor building communal oasis",
     "Photorealistic 16:9 cinematic wide shot, village outskirts, young men and women passing wicker baskets of earth up from deep stone-lined well excavation, joyful teamwork."),
    ("62-aalvinaiyudaimai/13-n13_hospital_apothecary_grinding_medicines.jpg", "Kural 613: Active care relieving the sick",
     "Photorealistic 16:9 cinematic interior, ancient Ayurvedic clinic, dedicated healer grinding dried herbs and roots in massive stone mortar, shelves lined with earthen medicine jars."),
    ("62-aalvinaiyudaimai/14-n14_merchant_funding_resthouse_for_travelers.jpg", "Kural 613: Turning commercial profit into civic blessings",
     "Photorealistic 16:9 cinematic architectural view, highway resthouse (chathiram) under banyan trees, weary wayfarers washing feet and resting with water jugs."),
    ("62-aalvinaiyudaimai/15-n15_orchardist_planting_mango_groves_for_posterity.jpg", "Kural 613: Planting trees whose shade one may never see",
     "Photorealistic 16:9 cinematic golden hour shot, elderly farmer carefully placing green mango sapling into moist earth, young grandson holding water pitcher nearby."),

    # Kural 614: Like an eunuch with a sword is the bounty of an idle man
    ("62-aalvinaiyudaimai/16-n16_rusty_sword_abandoned_in_thorny_bush.jpg", "Kural 614: Uselessness of unapplied potential",
     "Photorealistic 16:9 cinematic symbolic shot, ornate royal sword with jeweled hilt left rusting among dry thorns and cobwebs, devoid of warrior's hand."),
    ("62-aalvinaiyudaimai/17-n17_sharp_plowshare_buried_under_weeds.jpg", "Kural 614: Unused tools bringing no harvest",
     "Photorealistic 16:9 cinematic macro-low angle, heavy iron plowshare overgrown with noxious weeds in neglected field, symbol of wasted capability."),
    ("62-aalvinaiyudaimai/18-n18_idle_man_daydreaming_while_sun_sets.jpg", "Kural 614: Futile wishing without exertion",
     "Photorealistic 16:9 cinematic film still, dusty veranda, man sitting idly gazing at sunset with empty hands, while across the lane industrious neighbors pack goods."),
    ("62-aalvinaiyudaimai/19-n19_master_craftsman_wielding_tools_with_precision.jpg", "Kural 614: True mastery through practiced application",
     "Photorealistic 16:9 cinematic close-up, woodcarver's steady veins and muscular hands guiding fine gouge along teak temple door panel, curling shavings falling."),
    ("62-aalvinaiyudaimai/20-n20_sailor_hoisting_canvas_to_catch_wind.jpg", "Kural 614: Harnessing nature through resolute action",
     "Photorealistic 16:9 cinematic action shot, dhow bowsprit, seasoned sailor hauling thick rope with total bodily commitment, catching the seasonal monsoon breeze."),

    # Kural 615: He who delights in labor not in pleasure lifts up his kinsmen
    ("62-aalvinaiyudaimai/21-n21_blacksmith_working_through_the_night.jpg", "Kural 615: Toiling while the world sleeps",
     "Photorealistic 16:9 cinematic night shot, stone smithy, blacksmith hammering glowing steel under oil lamp glow, sweat pouring down bare muscular back, devoted duty."),
    ("62-aalvinaiyudaimai/22-n22_mother_tending_loom_by_flickering_lamp.jpg", "Kural 615: Maternal sacrifice uplifting the lineage",
     "Photorealistic 16:9 cinematic tender scene, humble village cottage, mother weaving late into night by clay lamp while her young children sleep peacefully on woven mats."),
    ("62-aalvinaiyudaimai/23-n23_young_merchant_carrying_wares_at_dawn.jpg", "Kural 615: Rejecting luxury for honorable toil",
     "Photorealistic 16:9 cinematic morning shot, dew-covered village road, young merchant carrying balanced wicker hampers of brassware on shoulder pole, marching with proud smile."),
    ("62-aalvinaiyudaimai/24-n24_family_prospering_around_harvest_hearth.jpg", "Kural 615: Sweet fruit of sustained domestic labor",
     "Photorealistic 16:9 cinematic warm interior, extended family dining together on brass plates in clean courtyard, smiling grandmother serving fresh ghee and steaming rice."),
    ("62-aalvinaiyudaimai/25-n25_restored_ancestral_estate_standing_proud.jpg", "Kural 615: Diligent son rebuilding ancestral heritage",
     "Photorealistic 16:9 cinematic wide shot, newly plastered and tiled Tamil courtyard house with carved wooden pillars and brass lamps, symbol of resurrected family dignity."),

    # Kural 616: Effort yields wealth; lack of effort brings destitution
    ("62-aalvinaiyudaimai/26-n26_flourishing_bazaar_teeming_with_commerce.jpg", "Kural 616: Wealth blossoming from collective industry",
     "Photorealistic 16:9 cinematic panoramic view, Madurai textile bazaar, stacks of madder-dyed cotton, spices, and copper vessels, thriving merchants and buyers."),
    ("62-aalvinaiyudaimai/27-n27_abandoned_hearth_covered_in_ash.jpg", "Kural 616: The cold desolation of sloth",
     "Photorealistic 16:9 cinematic somber shot, ruined village hut, cold hearth covered in windblown grey ashes and spiderwebs, broken clay pot on floor."),
    ("62-aalvinaiyudaimai/28-n28_caravan_returning_laden_with_silk_and_gold.jpg", "Kural 616: Fruitful harvest of adventurous trade",
     "Photorealistic 16:9 cinematic golden hour shot, caravan of camels and pack bullocks crossing city gates, saddlebags bulging with silk bolts and brass caskets."),
    ("62-aalvinaiyudaimai/29-n29_cobbler_crafting_durable_leather_sandals.jpg", "Kural 616: Dignity and earning in every honest craft",
     "Photorealistic 16:9 cinematic close-up, street artisan stitching thick leather soles with waxed hemp thread, worn hands showing years of honorable independent labor."),
    ("62-aalvinaiyudaimai/30-n30_granary_floor_swept_clean_of_paddy.jpg", "Kural 616: The reward of meticulous seasonal harvest",
     "Photorealistic 16:9 cinematic sunny outdoor shot, village threshing floor, oxen treading golden stalks while laborers winnow chaff into the wind, golden grain piling high."),

    # Kural 617: In effort resides Lakshmi; in sloth resides elder sister Jyeshtha
    ("62-aalvinaiyudaimai/31-n31_lamp_lit_courtyard_with_fresh_kolam.jpg", "Kural 617: Sanctity and fortune entering clean industrious home",
     "Photorealistic 16:9 cinematic dawn shot, traditional home entrance swept clean, intricate rice-flour kolam pattern on cow-dung washed doorstep, brass oil lamp flickering warmly."),
    ("62-aalvinaiyudaimai/32-n32_dusty_cluttered_threshold_with_broken_shutters.jpg", "Kural 617: Neglect inviting ruin and decay",
     "Photorealistic 16:9 cinematic moody shot, neglected house entrance, peeling wooden shutters hanging loose on hinges, dead leaves blowing across unwashed threshold."),
    ("62-aalvinaiyudaimai/33-n33_prosperous_merchant_inspecting_gemstones.jpg", "Kural 617: Golden touch of unwavering enterprise",
     "Photorealistic 16:9 cinematic close-up, merchant sitting on white mattress, examining deep red rubies and emeralds against morning window light, peaceful contentment."),
    ("62-aalvinaiyudaimai/34-n34_weaver_family_singing_at_the_looms.jpg", "Kural 617: Joyful labor sanctifying the home",
     "Photorealistic 16:9 cinematic medium-wide shot, airy loom shed, father, mother, and elder son each at separate looms, synchronized rhythmic weaving and singing."),
    ("62-aalvinaiyudaimai/35-n35_clean_village_granary_guarded_by_faithful_mastiff.jpg", "Kural 617: Preserving the fruits of honest toil",
     "Photorealistic 16:9 cinematic peaceful evening scene, stone granary courtyard, sleek Kombai hound lying vigilantly near sealed grain baskets under twilight sky."),

    # Kural 618: Unfavorable fate is no disgrace; lack of manly effort is real shame
    ("62-aalvinaiyudaimai/36-n36_one_legged_carpenter_hewing_temple_chariot_wheel.jpg", "Kural 618: Physical handicap overcome by indomitable will",
     "Photorealistic 16:9 cinematic inspiring portrait, veteran artisan with wooden peg-leg sitting steadily on wooden bench, carving intricate spokes of massive chariot wheel with chisel."),
    ("62-aalvinaiyudaimai/37-n37_blind_bard_tuning_ancient_yazh_harp.jpg", "Kural 618: Transcending limitation through devoted practice",
     "Photorealistic 16:9 cinematic close-up, elderly blind Tamil musician with serene face, sensitive fingers plucking the gut strings of a magnificent carved yazh harp, pure devotion."),
    ("62-aalvinaiyudaimai/38-n38_parched_land_blooming_with_hand_carried_water.jpg", "Kural 618: Defying cruel weather with human toil",
     "Photorealistic 16:9 cinematic shot, arid hillside terrace, green vegetable patches thriving because farmer has carried hundreds of clay water pots up from distant stream."),
    ("62-aalvinaiyudaimai/39-n39_shipwrecked_survivor_crafting_fire_on_shore.jpg", "Kural 618: Immediate enterprise upon surviving catastrophe",
     "Photorealistic 16:9 cinematic coastal scene, sea survivor on wild rocky shore spinning wooden fire drill between palms, creating smoke and flame, uncrushed spirit."),
    ("62-aalvinaiyudaimai/40-n40_warrior_training_swordplay_in_pouring_rain.jpg", "Kural 618: Relentless discipline regardless of conditions",
     "Photorealistic 16:9 cinematic action shot, muddy courtyard in driving monsoon rain, lone warrior practicing sword forms with blazing intensity, water spraying with every slash."),

    # Kural 619: Though fate deny success, labor itself yields wages equal to bodily toil
    ("62-aalvinaiyudaimai/41-n41_deep_well_digger_sweating_in_rocky_ground.jpg", "Kural 619: Bodily labor carving its own sacred worth",
     "Photorealistic 16:9 cinematic subterranean shot, deep inside rock-cut well shaft, digger's muscular shoulders glistening with sweat and rock dust as hammer strikes chisel."),
    ("62-aalvinaiyudaimai/42-n42_student_memorizing_grammatical_sutras.jpg", "Kural 619: Mental sweat building immortal capacity",
     "Photorealistic 16:9 cinematic intimate scene, stone veranda, young student reciting ancient Tolkappiyam verses, finger following palm leaf text, inner illumination."),
    ("62-aalvinaiyudaimai/43-n43_goldsmith_smelting_in_dimly_lit_forge.jpg", "Kural 619: Exacting care in the crucible of toil",
     "Photorealistic 16:9 cinematic close-up, glowing crucible holding molten copper and gold, artisan's weathered face reflected in liquid metal radiance, intense patience."),
    ("62-aalvinaiyudaimai/44-n44_mariner_rowing_against_counter_current.jpg", "Kural 619: Muscular struggle yielding inner steel",
     "Photorealistic 16:9 cinematic dynamic shot, wooden rowboat in river rapids, oarsman pulling with every sinew against white water, veins bulging on forearms."),

    # Kural 620: Those who strive with unyielding effort will conquer even stubborn fate
    ("62-aalvinaiyudaimai/45-n45_massive_stone_dam_diverting_turbulent_river.jpg", "Kural 620: Human engineering overcoming nature's decree",
     "Photorealistic 16:9 cinematic panoramic view, Grand Anicut (Kallanai), ancient stone barrage parting raging floodwaters safely into canal networks, triumph of human labor."),
    ("62-aalvinaiyudaimai/46-n46_barren_desert_transformed_into_green_paddy.jpg", "Kural 620: Defeating harsh destiny through tireless agriculture",
     "Photorealistic 16:9 cinematic sweeping landscape, boundary between arid rocky wasteland and lush emerald-green irrigated paddy fields stretching to horizon."),
    ("62-aalvinaiyudaimai/47-n47_monarch_and_plowman_standing_as_equals_at_dawn.jpg", "Kural 620: The supreme dignity of human effort conqueror of fate",
     "Photorealistic 16:9 cinematic final shot, golden sunrise over Tamilakam, king and humble farmer standing side by side overlooking prosperous realm, shared pride in honest toil.")
]

# -------------------------------------------------------------
# CHAPTER 65: சொல்வன்மை (Solvanmai) - 54 SHOTS
# -------------------------------------------------------------
CH65_PROMPTS = [
    # Kural 641: Power of speech is the supreme asset; other assets pale before it
    ("65-solvanmai/01-n01_orator_standing_before_grand_royal_council.jpg", "Kural 641: Eloquent orator holding court spellbound",
     "Photorealistic 16:9 cinematic wide shot, pillared council hall of Madurai palace, charismatic Tamil orator in white silk standing before king and ministers, arm raised in impassioned speech."),
    ("65-solvanmai/02-n02_listening_courtiers_captivated_by_speech.jpg", "Kural 641: Audience enthralled by golden eloquence",
     "Photorealistic 16:9 cinematic medium shot, audience of veteran ministers and scholars leaning forward with wide eyes and parted lips, completely entranced by speech."),
    ("65-solvanmai/03-n03_nectar_flowing_from_conch_vessel.jpg", "Kural 641: Speech sweet as divine amrita",
     "Photorealistic 16:9 cinematic poetic macro shot, carved ceremonial conch pouring clear honey into polished brass bowl, warm sunlight catching translucent drops."),
    ("65-solvanmai/04-n04_poet_reciting_verse_in_temple_mandapam.jpg", "Kural 641: Vocal power commanding spiritual reverence",
     "Photorealistic 16:9 cinematic shot, stone mandapam with carved pillars, Sangam poet reciting rhythmically, hands gesturing gracefully, temple lamps flickering."),
    ("65-solvanmai/05-n05_youth_advocating_peace_between_hostile_clans.jpg", "Kural 641: Words that disarm hatred and war",
     "Photorealistic 16:9 cinematic dramatic shot, border outpost, young Tamil diplomat with bare chest and flower garland speaking calmly between two armed chieftains who lower their spears."),

    # Kural 642: Speech brings both wealth and ruin; guard your words with care
    ("65-solvanmai/06-n06_sharp_double_edged_dagger_on_silk.jpg", "Kural 642: Words cut keener than steel blades",
     "Photorealistic 16:9 cinematic close-up, gleaming Damascus-steel Tamil dagger resting on crimson silk cushion, blade reflecting razor-sharp edge in oil-lamp flame."),
    ("65-solvanmai/07-n07_monarch_granting_estates_to_wise_counselor.jpg", "Kural 642: Right speech rewarded with prosperity and honor",
     "Photorealistic 16:9 cinematic court scene, king presenting inscribed copper plate grant and golden bracelet to an eloquent minister whose advice saved the realm."),
    ("65-solvanmai/08-n08_rash_courtier_lowering_head_in_disgrace.jpg", "Kural 642: The catastrophic cost of careless speech",
     "Photorealistic 16:9 cinematic dramatic scene, throne room, disgraced courtier with head bowed in shame as guards escort him away following a reckless offensive remark."),
    ("65-solvanmai/09-n09_honey_and_poison_pots_side_by_side.jpg", "Kural 642: The dual potential of the spoken tongue",
     "Photorealistic 16:9 cinematic still life, antique terracotta jar overflowing with golden honey next to a black clay phial of potent serpent antidote, symbolic illumination."),
    ("65-solvanmai/10-n10_sage_sitting_in_vow_of_measured_speech.jpg", "Kural 642: Restraint and mindfulness in every syllable",
     "Photorealistic 16:9 cinematic serene portrait, forest hermitage, venerable sage seated on deer skin, eyes closed in contemplation, radiating profound verbal self-mastery."),

    # Kural 643: Good speech binds friends and converts even adversaries
    ("65-solvanmai/11-n11_two_kings_embracing_in_peaceful_treaty.jpg", "Kural 643: Diplomatic speech uniting rival monarchs",
     "Photorealistic 16:9 cinematic royal scene, tent pavilion on border river, Chera and Chola kings in royal silks embracing warmly as counselors exchange treaty scrolls."),
    ("65-solvanmai/12-n12_hostile_chieftain_softening_expression_at_council.jpg", "Kural 643: Words melting hardened animosity",
     "Photorealistic 16:9 cinematic close-up, rugged mountain chieftain's stern furrowed brow relaxing into an appreciative smile while listening to respectful embassy."),
    ("65-solvanmai/13-n13_circles_of_villagers_listening_under_banyan.jpg", "Kural 643: Communal harmony forged through sweet speech",
     "Photorealistic 16:9 cinematic wide shot, ancient village banyan tree at sunset, dozens of villagers sitting peacefully in circles as headman speaks calming guidance."),
    ("65-solvanmai/14-n14_ambassador_speaking_with_gracious_humility.jpg", "Kural 643: Tact and grace opening stubborn gates",
     "Photorealistic 16:9 cinematic medium shot, foreign audience hall, Tamil ambassador bowing gracefully with palms joined, face illuminated with genuine goodwill."),
    ("65-solvanmai/15-n15_shared_meal_of_reconciled_neighbors.jpg", "Kural 643: Fellowship restored through healing conversation",
     "Photorealistic 16:9 cinematic intimate scene, garden veranda, two former rivals eating together from banana leaves, sharing laughter over steaming food."),

    # Kural 644: Assess the nature of the assembly and speak with tailored wisdom
    ("65-solvanmai/16-n16_scholar_addressing_gathering_of_philosophers.jpg", "Kural 644: Speaking subtle metaphysics to learned sages",
     "Photorealistic 16:9 cinematic intellectual scene, temple library surrounded by palm-leaf scroll cabinets, scholar debating complex epistemology with austere sages."),
    ("65-solvanmai/17-n17_leader_addressing_village_farmers_in_simple_tongue.jpg", "Kural 644: Speaking practical clarity to hardworking folk",
     "Photorealistic 16:9 cinematic rural scene, harvest festival, administrator standing on wooden cart speaking in straightforward, earthy metaphors to cheering farmers."),
    ("65-solvanmai/18-n18_envoy_speaking_ceremonial_protocol_in_imperial_court.jpg", "Kural 644: Masterful command of high courtly etiquette",
     "Photorealistic 16:9 cinematic majestic view, towering stone throne room, envoy delivering ornate metered verse tribute with flawless Sangam high Tamil grammar."),
    ("65-solvanmai/19-n19_teacher_explaining_astronomy_to_eager_youth.jpg", "Kural 644: Adapting profound knowledge to budding minds",
     "Photorealistic 16:9 cinematic educational shot, starry night courtyard, teacher pointing at constellations with wooden wand, young students gazing with wonder."),
    ("65-solvanmai/20-n20_judge_announcing_unambiguous_verdict.jpg", "Kural 644: Lucid precision leaving no room for dispute",
     "Photorealistic 16:9 cinematic courtroom shot, seated magistrate on granite bench holding iron stylus, reading impartial verdict with crystal clarity to quiet hall."),

    # Kural 645: Utter only words that no other word can surpass or refute
    ("65-solvanmai/21-n21_irrefutable_argument_silencing_the_sophist.jpg", "Kural 645: Unassailable truth crushing hollow rhetoric",
     "Photorealistic 16:9 cinematic intellectual duel, academy debating arena, confident scholar delivering decisive argument while rival sits speechless in defeated awe."),
    ("65-solvanmai/22-n22_solid_granite_anchor_holding_in_current.jpg", "Kural 645: Words immovable as sunken stone anchors",
     "Photorealistic 16:9 cinematic marine metaphor, massive hand-cut granite anchor stone resting immovable on riverbed as clear waters surge past."),
    ("65-solvanmai/23-n23_pure_gold_hallmark_stamped_on_ingot.jpg", "Kural 645: Authenticity stamped beyond doubt",
     "Photorealistic 16:9 cinematic macro shot, heavy gold bar stamped with royal tiger emblem, flawless surface catching light, hallmark of unchallengeable truth."),
    ("65-solvanmai/24-n24_monarch_nodding_in_unanimous_assent.jpg", "Kural 645: Sovereign accepting conclusive counsel",
     "Photorealistic 16:9 cinematic close-up, king smiling in deep admiration, nodding approvingly at minister whose concise words solved a national crisis."),
    ("65-solvanmai/25-n25_written_decree_inscribed_on_copper_plates.jpg", "Kural 645: Immortal words preserved for millennia",
     "Photorealistic 16:9 cinematic close-up, bundle of copper plates tied with heavy bronze ring and royal seal, finely incised Tamil script enduring forever."),

    # Kural 646: Deliver your ideas attractively; absorb the best from others
    ("65-solvanmai/26-n26_poet_weaving_words_like_fresh_jasmine_garland.jpg", "Kural 646: Speech arranged with fragrant elegance",
     "Photorealistic 16:9 cinematic artistic shot, poet's hands arranging pure white jasmine blossoms and fragrant maruvam herbs into an exquisite ceremonial garland."),
    ("65-solvanmai/27-n27_scholar_listening_intently_with_palm_leaf_open.jpg", "Kural 646: Keen listener absorbing another's wisdom",
     "Photorealistic 16:9 cinematic medium shot, open-air mandapam, seasoned scholar listening with tilted head and focused warmth to a traveling guest lecturer."),
    ("65-solvanmai/28-n28_master_bard_singing_to_the_strum_of_yazh.jpg", "Kural 646: Blending eloquence with melodic beauty",
     "Photorealistic 16:9 cinematic film still, courtyard under neem blossoms, Panar bard singing stirring epic poem while plucking wooden yazh harp strings."),
    ("65-solvanmai/29-n29_two_scholars_in_joyous_mutual_enlightenment.jpg", "Kural 646: Dialogue that enriches both speakers",
     "Photorealistic 16:9 cinematic sunny scene, temple steps, two philosophers smiling warmly as they exchange complementary perspectives over open scrolls."),
    ("65-solvanmai/30-n30_silver_flute_producing_enchanting_melody.jpg", "Kural 646: The irresistible harmony of persuasive speech",
     "Photorealistic 16:9 cinematic poetic shot, musician's fingers dancing over bamboo flute stops in evening courtyard, soft breeze rustling palm leaves."),

    # Kural 647: No foe can defeat the eloquent man who is vigilant and skilled in debate
    ("65-solvanmai/31-n31_invincible_champion_standing_at_academy_dais.jpg", "Kural 647: Unconquerable intellect in the arena of logic",
     "Photorealistic 16:9 cinematic wide shot, Sangam hall, scholar with serene smile standing victorious at center of forum, rival debaters applauding with respect."),
    ("65-solvanmai/32-n32_impregnable_stone_fortress_on_high_crag.jpg", "Kural 647: Mind fortified with comprehensive learning",
     "Photorealistic 16:9 cinematic landscape, mighty granite hill-fortress with towering ramparts standing majestic against stormy skies, unassailable defenses."),
    ("65-solvanmai/33-n33_diplomat_outwitting_treacherous_negotiator.jpg", "Kural 647: Vigilance turning the tables on deception",
     "Photorealistic 16:9 cinematic dramatic close-up, sharp-eyed Tamil ambassador calmly pointing out hidden clause in rival court's scroll, disarming deceit."),
    ("65-solvanmai/34-n34_warrior_deflecting_javelin_with_bronze_buckler.jpg", "Kural 647: Deft parry of aggressive rhetoric",
     "Photorealistic 16:9 cinematic action metaphor, athletic warrior cleanly deflecting heavy iron spear with circular bronze shield, sparkling impact."),
    ("65-solvanmai/35-n35_laurel_wreath_of_victory_placed_on_orator.jpg", "Kural 647: Crowning the master of assemblies",
     "Photorealistic 16:9 cinematic ceremonial shot, elder scholars crowning eloquent victor with a wreath of golden vetchi and kurunji flowers, hall in celebration."),

    # Kural 648: The world swiftly heeds the counsel of one who speaks with sweet lucidity
    ("65-solvanmai/36-n36_crowd_of_citizens_nodding_in_peaceful_consensus.jpg", "Kural 648: Populace gladly embracing wise guidance",
     "Photorealistic 16:9 cinematic wide shot, town market square, hundreds of citizens raising hands in joyful agreement with the benevolent elder magistrate."),
    ("65-solvanmai/37-n37_clear_mountain_stream_quenching_thirsty_travelers.jpg", "Kural 648: Refreshing clarity of pure communication",
     "Photorealistic 16:9 cinematic nature shot, crystal-clear mountain spring bubbling over polished grey pebbles, thirsty pilgrims drinking with cupped hands."),
    ("65-solvanmai/38-n38_monarch_implementing_reforms_after_minister_speech.jpg", "Kural 648: Words that immediately inspire state action",
     "Photorealistic 16:9 cinematic court scene, king rising from carved sandalwood throne, commanding royal scribes to write new irrigation edicts immediately."),
    ("65-solvanmai/39-n39_mother_soothing_crying_child_with_soft_lullaby.jpg", "Kural 648: The miraculous soothing power of tender words",
     "Photorealistic 16:9 cinematic intimate tender scene, sunlit veranda, mother holding infant to chest, whispering gentle song, child drifting into peaceful sleep."),
    ("65-solvanmai/40-n40_village_elders_resolving_land_dispute_amicably.jpg", "Kural 648: Sweet mediation healing long-standing discord",
     "Photorealistic 16:9 cinematic outdoor scene, under village tamarind tree, two farming families embracing and sharing betel leaves after elder's gentle counsel."),

    # Kural 649: Those unable to express clearly in brief words love endless chatter
    ("65-solvanmai/41-n41_concise_gem_shining_beside_heap_of_gravel.jpg", "Kural 649: Brilliant brevity versus voluminous trivia",
     "Photorealistic 16:9 cinematic macro still life, single blazing cut sapphire resting beside a sprawling pile of rough grey pebbles on jeweler's velvet cloth."),
    ("65-solvanmai/42-n42_tedious_courtier_rambling_while_king_grows_weary.jpg", "Kural 649: Tedium of long-winded empty speech",
     "Photorealistic 16:9 cinematic dramatic court scene, verbose courtier talking endlessly from huge stack of scrolls while king rests cheek on hand in obvious boredom."),
    ("65-solvanmai/43-n43_single_drop_of_sandalwood_oil_scenting_hall.jpg", "Kural 649: Potent concentration of essence",
     "Photorealistic 16:9 cinematic close-up, single golden drop of pure sandalwood oil falling from glass rod onto warm bronze brazier, rich fragrant smoke rising."),
    ("65-solvanmai/44-n44_swift_arrow_hitting_bullseye_in_one_breath.jpg", "Kural 649: Direct delivery straight to the heart of the matter",
     "Photorealistic 16:9 cinematic action shot, target range, single red-fletched arrow embedded dead-center in wooden target ring, quiver empty, clean precision."),
    ("65-solvanmai/45-n45_sage_speaking_one_sentence_that_solves_riddle.jpg", "Kural 649: The lightning flash of concise revelation",
     "Photorealistic 16:9 cinematic close-up, serene sage uttering three quiet words, scholars around him suddenly lighting up with profound realization."),

    # Kural 650: He who cannot explain his learning to others is like a scentless flower
    ("65-solvanmai/46-n46_vibrant_silk_flower_lacking_any_fragrance.jpg", "Kural 650: Beautiful appearance devoid of living aroma",
     "Photorealistic 16:9 cinematic close-up, artificial bright paper flower sitting on stone ledge, bees flying past it to land on tiny fragrant wild thyme blossoms."),
    ("65-solvanmai/47-n47_learned_recluse_tongue_tied_before_the_assembly.jpg", "Kural 650: Tragic silence of uncommunicated scholarship",
     "Photorealistic 16:9 cinematic scene, academy podium, bookish scholar clutching palm leaves nervously, looking paralyzed before sea of expectant faces."),
    ("65-solvanmai/48-n48_blooming_champaka_flower_perfuming_entire_garden.jpg", "Kural 650: Learning shared generously in full radiance",
     "Photorealistic 16:9 cinematic macro nature shot, golden champaka flower blooming on leafy branch, radiating intoxicating sweet perfume through sunlit grove."),
    ("65-solvanmai/49-n49_teacher_surrounded_by_radiant_disciples.jpg", "Kural 650: Wisdom overflowing naturally into worthy minds",
     "Photorealistic 16:9 cinematic outdoor school, shade of sacred fig tree, master joyfully explaining verse to glowing young disciples who take notes with styluses."),
    ("65-solvanmai/50-n50_brazen_trumpet_echoing_across_mountain_valleys.jpg", "Kural 650: The resonance of truth carried far and wide",
     "Photorealistic 16:9 cinematic majestic shot, fortress parapet at dawn, royal herald sounding curved bronze horn, sound waves rippling across misty river valley."),

    # Grand climactic sequence for Chapter 65
    ("65-solvanmai/51-n51_the_triumph_of_the_sangam_bards.jpg", "Kural 641-650: Gathering of the supreme poetic masters",
     "Photorealistic 16:9 cinematic panoramic view, golden hall of the Madurai Sangam, poets and bards singing in harmonious choral verse, banners billowing."),
    ("65-solvanmai/52-n52_words_that_shape_destinies_of_nations.jpg", "Kural 641-650: Statesmanship guided by sublime speech",
     "Photorealistic 16:9 cinematic wide shot, royal dais overlooking grand assembly, prime minister delivering the state policy address to resounding ovation."),
    ("65-solvanmai/53-n53_the_eternal_song_of_the_tamil_tongue.jpg", "Kural 641-650: Sacred beauty of the ancient Tamil language",
     "Photorealistic 16:9 cinematic poetic composition, ornate bronze Nataraja surrounded by palm-leaf scriptures, jasmine blossoms, and glowing clay lamps at twilight."),
    ("65-solvanmai/54-n54_the_radiant_dawn_of_wisdom_and_speech.jpg", "Kural 641-650: Golden sunrise over the land of eloquence",
     "Photorealistic 16:9 cinematic final shot, breathtaking golden sunrise breaking over temple gopurams of Tamilakam, celestial rays illuminating the sacred land.")
]

# -------------------------------------------------------------
# CHAPTER 66: வினைத்தூய்மை (Vinaithooymai) - 44 SHOTS
# -------------------------------------------------------------
CH66_PROMPTS = [
    # Kural 651: Good companions bring honor; purity of action brings all blessings
    ("66-vinaithooymai/01-n01_spotless_white_lotus_in_crystal_stream.jpg", "Kural 651: Flawless purity of pristine action",
     "Photorealistic 16:9 cinematic macro nature shot, spotless white lotus bloom floating in crystal-clear flowing spring water, morning sunbeams sparkling on droplets."),
    ("66-vinaithooymai/02-n02_righteous_magistrate_returning_bribe.jpg", "Kural 651: Uncompromising integrity rejecting corrupt gifts",
     "Photorealistic 16:9 cinematic dramatic court shot, ancient Tamil magistrate firmly pushing away a velvet pouch of gold coins with solemn dignity, strict gaze."),
    ("66-vinaithooymai/03-n03_purifying_hands_in_sacred_temple_stream.jpg", "Kural 651: Cleansing mind and deed before holy duty",
     "Photorealistic 16:9 cinematic close-up, cupped brown hands scooping cool sacred river water at dawn, water spilling like liquid silver, brass prayer vessel nearby."),
    ("66-vinaithooymai/04-n04_clean_white_cotton_drying_in_sunlight.jpg", "Kural 651: Actions unblemished by dark deceit",
     "Photorealistic 16:9 cinematic outdoor shot, lines of freshly washed pure white khadi cotton dhotis billowing in clean sea breeze under bright morning sky."),
    ("66-vinaithooymai/05-n05_honest_merchant_using_true_balance_scales.jpg", "Kural 651: Scrupulous honesty in daily commerce",
     "Photorealistic 16:9 cinematic medium shot, spice merchant steadying bronze balance scale to exact equilibrium while customer watches with total trust."),

    # Kural 652: Shun actions that yield neither fame nor virtue
    ("66-vinaithooymai/06-n06_turning_back_from_the_darkened_alley.jpg", "Kural 652: Walking away from ignominious deeds",
     "Photorealistic 16:9 cinematic moody shot, cobblestone city lane at dusk, noble young citizen turning his back on shadowy gambling den, walking into warm lamplight."),
    ("66-vinaithooymai/07-n07_refusing_to_forge_royal_seal.jpg", "Kural 652: Scribe upholding moral truth over pressure",
     "Photorealistic 16:9 cinematic dramatic film still, dimly lit chamber, royal scribe throwing down bronze stylus, refusing corrupt nobleman's order to forge document."),
    ("66-vinaithooymai/08-n08_burning_tainted_gold_in_charcoal_furnace.jpg", "Kural 652: Rejecting illicit gain without hesitation",
     "Photorealistic 16:9 cinematic intense close-up, upright citizen casting dishonorably obtained coin into red-hot furnace, smoke rising, unpolluted conscience."),
    ("66-vinaithooymai/09-n09_clean_mountain_path_ascending_to_temple.jpg", "Kural 652: Choosing the steep and noble road",
     "Photorealistic 16:9 cinematic wide landscape, rugged mountain stairway ascending toward ancient sunlit hill shrine, flanked by wild blooming oleanders."),

    # Kural 653: Those who desire greatness must never commit base deeds
    ("66-vinaithooymai/10-n10_warrior_refusing_to_strike_fallen_foe.jpg", "Kural 653: Chivalry that transcends mere victory",
     "Photorealistic 16:9 cinematic dramatic battlefield shot, Sangam hero stepping back and lowering his bronze spear, offering hand to disarmed opponent in honorable combat."),
    ("66-vinaithooymai/11-n11_monarch_consulting_spiritual_conscience.jpg", "Kural 653: Sovereign measuring every decree by dharma",
     "Photorealistic 16:9 cinematic quiet royal scene, private prayer room, king sitting barefoot on reed mat before Shiva Lingam, meditating deeply before war council."),
    ("66-vinaithooymai/12-n12_architect_rejecting_flawed_granite_block.jpg", "Kural 653: Zero compromise on foundational integrity",
     "Photorealistic 16:9 cinematic courtyard shot, master builder marking a red cross on a cracked granite block, instructing quarrymen to fetch only sound stone."),
    ("66-vinaithooymai/13-n13_pure_gold_crucible_burning_away_dross.jpg", "Kural 653: Refining character to diamond perfection",
     "Photorealistic 16:9 cinematic macro close-up, molten gold bubbling in clay crucible, grey slag burning off to leave mirror-bright yellow surface, blazing heat."),

    # Kural 654: Even in deepest adversity, the wise commit no forbidden act
    ("66-vinaithooymai/14-n14_starving_family_sharing_last_honest_morsel.jpg", "Kural 654: Preserving honor through the pangs of famine",
     "Photorealistic 16:9 cinematic poignant scene, humble hut during drought, austere parents feeding their last small bowl of gruel to child with calm noble faces."),
    ("66-vinaithooymai/15-n15_ascetic_refusing_meat_in_wild_forest.jpg", "Kural 654: Inviolable principles despite mortal hunger",
     "Photorealistic 16:9 cinematic forest shot, holy hermit sitting beneath ancient banyan, gently feeding wild deer with forest berries, peaceful countenance."),
    ("66-vinaithooymai/16-n16_stranded_merchant_protecting_entrusted_cargo.jpg", "Kural 654: Sacred guardianship under dire conditions",
     "Photorealistic 16:9 cinematic coastal cliff shot, shipwreck survivor shivering in cold rain, carefully sheltering client's sealed treasure coffer under canvas."),
    ("66-vinaithooymai/17-n17_soldier_keeping_night_vigil_in_winter_frost.jpg", "Kural 654: Duty kept without slipping for a single second",
     "Photorealistic 16:9 cinematic night shot, frost-covered fortress wall, sentry standing rigid and alert with spear, breath puffing white in moonlight."),

    # Kural 655: Do not perform acts that bring regret; if done, repeat them never
    ("66-vinaithooymai/18-n18_penitent_prostrating_before_sacred_flame.jpg", "Kural 655: Genuine repentance purging past errors",
     "Photorealistic 16:9 cinematic devotional shot, stone temple sanctum, man prostrating full length on granite floor before blazing oil lamp, heartfelt humility."),
    ("66-vinaithooymai/19-n19_broken_arrow_snapped_in_renunciation.jpg", "Kural 655: Vow never to repeat a wrongful act",
     "Photorealistic 16:9 cinematic macro shot, warrior's strong hands deliberately snapping a poisoned hunting arrow in two over stone altar, firm resolve."),
    ("66-vinaithooymai/20-n20_cleansing_morning_bath_in_the_holy_river.jpg", "Kural 655: Spiritual rebirth in the waters of repentance",
     "Photorealistic 16:9 cinematic dawn shot, Kaveri river ghat, devotee submerging into glistening water, emerging with palms raised to the rising golden sun."),
    ("66-vinaithooymai/21-n21_writing_restitution_scroll_for_wronged_neighbor.jpg", "Kural 655: Immediate active repair of past wrongs",
     "Photorealistic 16:9 cinematic intimate scene, citizen writing deeds to transfer fertile land to a neighbor he had once cheated, tears of moral relief."),

    # Kural 656: Even to save one's starving mother, do not perform unrighteous deeds
    ("66-vinaithooymai/22-n22_elderly_mother_blessing_upright_son.jpg", "Kural 656: Mother who prefers honest hunger to sinful bread",
     "Photorealistic 16:9 cinematic poignant portrait, weathered old Tamil mother placing frail loving hand on son's head, smiling proudly at his unwavering dharma."),
    ("66-vinaithooymai/23-n23_son_gathering_wild_roots_with_dignity.jpg", "Kural 656: Honorable labor to sustain aged parents",
     "Photorealistic 16:9 cinematic outdoor shot, forest hillside, young man digging nutritious wild yams from rocky soil, determined to feed mother by honest sweat."),
    ("66-vinaithooymai/24-n24_pure_water_offered_in_polished_brass_cup.jpg", "Kural 656: Clean sustenance brings divine blessing",
     "Photorealistic 16:9 cinematic close-up, young man holding brass cup of clean water and simple millet bread to smiling mother on veranda."),
    ("66-vinaithooymai/25-n25_ancestral_hearth_burning_with_sacred_smoke.jpg", "Kural 656: Lineage kept untainted across generations",
     "Photorealistic 16:9 cinematic interior, humble village home, gentle dhoopam smoke rising from terracotta censer, peace and righteousness dwelling within."),

    # Kural 657: Poverty earned by righteous action is far nobler than wealth gained by sin
    ("66-vinaithooymai/26-n26_serene_scholar_in_simple_thatched_cottage.jpg", "Kural 657: Noble poverty illuminated by wisdom",
     "Photorealistic 16:9 cinematic warm interior, thatched cottage, scholar reading palm leaves in serene contentment, wearing coarse cotton, radiant aura of peace."),
    ("66-vinaithooymai/27-n27_corrupt_potentate_haunted_by_paranoia.jpg", "Kural 657: The torment of illicit luxury",
     "Photorealistic 16:9 cinematic dramatic night shot, luxurious silk-draped bedchamber, wealthy corrupt minister sitting upright in bed in terror, clutching dagger at shadows."),
    ("66-vinaithooymai/28-n28_honest_weaver_sleeping_peacefully_on_mat.jpg", "Kural 657: The priceless blessing of clear conscience",
     "Photorealistic 16:9 cinematic moonlight shot, humble veranda, weaver sleeping in deep untroubled repose with gentle smile, cool night breeze stirring curtains."),
    ("66-vinaithooymai/29-n29_golden_goblet_filled_with_poisoned_wine.jpg", "Kural 657: The deadly illusion of sinful riches",
     "Photorealistic 16:9 cinematic macro still life, ornate gem-encrusted golden goblet spilling dark wine onto cold marble floor, dead scorpion nearby."),

    # Kural 658: Deeds achieved through wrong means bring sorrow in the end
    ("66-vinaithooymai/30-n30_house_built_on_sand_crumbling_in_rain.jpg", "Kural 658: Collapse of wealth founded on deceit",
     "Photorealistic 16:9 cinematic dramatic scene, coastal bluff during squall, ornate mansion with cracked foundations sliding into raging ocean waves."),
    ("66-vinaithooymai/31-n31_usurper_cowering_as_truth_is_unveiled.jpg", "Kural 658: Inevitable downfall of the unjust ruler",
     "Photorealistic 16:9 cinematic throne room drama, fraudulent claimant to the throne trembling as royal judges produce the authentic copper land charters."),
    ("66-vinaithooymai/32-n32_counterfeit_coins_exposed_by_assayer_fire.jpg", "Kural 658: Fraud melting away under the test of truth",
     "Photorealistic 16:9 cinematic close-up, assayer's furnace, fake bronze coins turning to black dross while genuine gold stays pure and shining."),

    # Kural 659: Wealth acquired through tears departs with bitter weeping
    ("66-vinaithooymai/33-n33_extortionist_watching_treasury_burn.jpg", "Kural 659: Ill-gotten gains consumed by flames",
     "Photorealistic 16:9 cinematic dramatic shot, night courtyard, corrupt tax collector wailing on knees as lightning sets his hoarded storehouse ablaze."),
    ("66-vinaithooymai/34-n34_tears_of_the_oppressed_transforming_into_fire.jpg", "Kural 659: The cosmic law that balances tears with ruin",
     "Photorealistic 16:9 cinematic poetic composition, weeping village mother's tear drop falling onto dry earth, reflecting a rising celestial storm cloud."),
    ("66-vinaithooymai/35-n35_righteous_charity_returning_hundredfold.jpg", "Kural 659: Legitimate wealth multiplying in peace",
     "Photorealistic 16:9 cinematic joyful scene, honest merchant receiving overflowing bags of grain from farmers who eagerly trade with him year after year."),

    # Kural 660: Storing ill-gotten wealth is like pouring water into unbaked clay pot
    ("66-vinaithooymai/36-n36_water_dissolving_unbaked_earthen_pot.jpg", "Kural 660: Raw clay pot dissolving in water",
     "Photorealistic 16:9 cinematic macro shot, fresh unbaked clay pot dissolving into muddy sludge as water is poured in, water and vessel both destroyed."),
    ("66-vinaithooymai/37-n37_kiln_fired_terracotta_urn_holding_pure_water.jpg", "Kural 660: Well-tested integrity holding eternal blessings",
     "Photorealistic 16:9 cinematic close-up, kiln-fired red terracotta urn with polished surface holding crystal-clear cold well water without leaking a drop."),
    ("66-vinaithooymai/38-n38_granite_reservoir_enduring_across_centuries.jpg", "Kural 660: Actions built on dharma enduring forever",
     "Photorealistic 16:9 cinematic grand view, ancient stone irrigation tank (eri) holding immense body of sparkling water, stone steps solid as mountains."),
    ("66-vinaithooymai/39-n39_honest_craftsman_passing_tools_to_proud_son.jpg", "Kural 660: Pure legacy that survives generations",
     "Photorealistic 16:9 cinematic heartwarming portrait, workshop veranda, master carpenter placing his grandfather's bronze square into hands of his proud son."),

    # Grand climactic sequence for Chapter 66
    ("66-vinaithooymai/40-n40_the_radiance_of_unblemished_integrity.jpg", "Kural 651-660: The shining soul of absolute righteousness",
     "Photorealistic 16:9 cinematic majestic portrait, elderly Tamil statesman standing in pristine white garments on palace terrace, calm eyes reflecting pure honor."),
    ("66-vinaithooymai/41-n41_the_peaceful_kingdom_governed_by_purity.jpg", "Kural 651-660: Realm flourishing under upright administration",
     "Photorealistic 16:9 cinematic panoramic vista, bustling Tamil river city, clean streets, thriving markets, soaring temple gopurams gleaming in afternoon light."),
    ("66-vinaithooymai/42-n42_the_sacred_river_cleansing_the_realm.jpg", "Kural 651-660: Pure actions flowing like life-giving river",
     "Photorealistic 16:9 cinematic landscape, Kaveri delta river flowing wide and serene between emerald banks, reflecting golden sunset clouds."),
    ("66-vinaithooymai/43-n43_the_eternal_flame_of_truth_and_action.jpg", "Kural 651-660: Unquenchable lamp of righteous deeds",
     "Photorealistic 16:9 cinematic close-up, monumental bronze temple lamp burning with five golden wicks, perfectly still and luminous in sacred sanctum."),
    ("66-vinaithooymai/44-n44_the_immortal_dawn_of_dharma.jpg", "Kural 651-660: Golden dawn over the land of purity",
     "Photorealistic 16:9 cinematic final shot, celestial golden sunrise breaking over mountain ranges, casting glorious golden radiance across peaceful homeland.")
]

# -------------------------------------------------------------
# CHAPTER 67: வினைத்திட்பம் (Vinaithitpam) - 49 SHOTS
# -------------------------------------------------------------
CH67_PROMPTS = [
    # Kural 661: Resolute action is firmness of mind; all other qualities are secondary
    ("67-vinaithitpam/01-n01_warrior_clenched_fist_over_iron_hilt.jpg", "Kural 661: Unshakable resolve centered in the mind",
     "Photorealistic 16:9 cinematic macro close-up, warrior's sinewy hand firmly gripping carved horn hilt of heavy iron sword, bronze wristband, total composure."),
    ("67-vinaithitpam/02-n02_deep_mountain_roots_gripping_sheer_cliff.jpg", "Kural 661: Roots anchoring into living stone",
     "Photorealistic 16:9 cinematic nature shot, sheer granite precipice, ancient banyan roots gripping cracked stone fissures, unbudged by howling canyon winds."),
    ("67-vinaithitpam/03-n03_general_delivering_firm_command_at_dusk.jpg", "Kural 661: Decisive leadership executing strategy",
     "Photorealistic 16:9 cinematic dramatic scene, military command tent, veteran general pointing finger at strategic map on wooden table, commanders nodding in steel resolve."),
    ("67-vinaithitpam/04-n04_diver_plunging_into_churning_breakers.jpg", "Kural 661: Fearless plunge into the decisive moment",
     "Photorealistic 16:9 cinematic action shot, rock ledge, athletic diver leaping boldly into turbulent ocean foam, silhouette framed against stormy twilight."),
    ("67-vinaithitpam/05-n05_blacksmith_quenching_white_hot_blade.jpg", "Kural 661: Steel temper forged in trial",
     "Photorealistic 16:9 cinematic dramatic shot, smithy, armorer plunging glowing sword blade into water trough, clouds of white steam hissing upward."),

    # Kural 662: Two things to avoid: starting an unpromising deed, and fainting mid-way
    ("67-vinaithitpam/06-n06_scout_reconnoitering_enemy_terrain_carefully.jpg", "Kural 662: Thorough foresight before initiating action",
     "Photorealistic 16:9 cinematic stealth shot, dense jungle ridge, Tamil scout peering through foliage at fortified mountain pass, taking meticulous mental notes."),
    ("67-vinaithitpam/07-n07_monarch_canceling_hasty_campaign.jpg", "Kural 662: Wisdom to decline reckless ventures",
     "Photorealistic 16:9 cinematic council shot, king calmly waving hand to roll up an over-ambitious military map, choosing patience over rash adventure."),
    ("67-vinaithitpam/08-n08_climber_reaching_highest_ledge_without_pause.jpg", "Kural 662: Never halting halfway up the mountain",
     "Photorealistic 16:9 cinematic dramatic shot, high cliff face, climber's chalked hand grasping final rock ledge, pulling body upward to summit in sunrise."),
    ("67-vinaithitpam/09-n09_weaver_completing_epic_tapestry.jpg", "Kural 662: Sustaining concentration to the very last thread",
     "Photorealistic 16:9 cinematic wide shot, loom workshop, master artisan cutting finished twelve-yard silk tapestry from frame, standing back with proud gaze."),
    ("67-vinaithitpam/10-n10_bridge_builders_placing_central_arch_stone.jpg", "Kural 662: Triumph of perseverance completing public work",
     "Photorealistic 16:9 cinematic engineering shot, stone bridge over river gorge, masons guiding heavy keystone into place with hemp pulleys and wooden levers."),

    # Kural 663: Make your intention known only through its glorious completion
    ("67-vinaithitpam/11-n11_silent_craftsman_unveiling_magnificent_bronze_deity.jpg", "Kural 663: Let results speak, not boasting words",
     "Photorealistic 16:9 cinematic reveal shot, casting workshop, artisan pulling silk veil off newly cast towering bronze Nataraja, courtiers gasping in awe."),
    ("67-vinaithitpam/12-n12_silent_monarch_working_late_in_study.jpg", "Kural 663: Secret preparation outshining empty fanfare",
     "Photorealistic 16:9 cinematic intimate scene, private library, monarch drafting economic reforms alone by lamp, keeping grand plans secret until ready."),
    ("67-vinaithitpam/13-n13_caravan_arriving_unheralded_with_vital_grain.jpg", "Kural 663: Surprise relief arriving in the nick of time",
     "Photorealistic 16:9 cinematic wide shot, city gates at dawn, hundred grain carts rolling silently into famine-struck town, townspeople cheering in joyful disbelief."),
    ("67-vinaithitpam/14-n14_sculptor_unveiling_carved_temple_chariot.jpg", "Kural 663: Stunned admiration at finished masterpiece",
     "Photorealistic 16:9 cinematic sunny festival shot, massive carved wooden temple car revealed to thousands of pilgrims with raised hands and ringing bells."),
    ("67-vinaithitpam/15-n15_underwater_aqueduct_gushing_fresh_water.jpg", "Kural 663: Hidden labor emerging into triumphant blessing",
     "Photorealistic 16:9 cinematic dramatic shot, dry stone canal basin suddenly flooded with roaring fresh water as secret subterranean aqueduct is opened."),

    # Kural 664: Anyone can speak of deeds; rare is he who executes them to the finish
    ("67-vinaithitpam/16-n16_hollow_boaster_talking_with_wide_gestures.jpg", "Kural 664: The cheap ease of boastful talk",
     "Photorealistic 16:9 cinematic street shot, marketplace platform, loud man making theatrical gestures while quiet, seasoned laborers walk past ignoring him."),
    ("67-vinaithitpam/17-n17_silent_warrior_sharpening_spear_point.jpg", "Kural 664: Quiet focus of the true man of action",
     "Photorealistic 16:9 cinematic close-up, veteran soldier sitting on tree stump, smoothly running whetstone along bronze spearhead, quiet deadly concentration."),
    ("67-vinaithitpam/18-n18_mason_laying_thousands_of_granite_blocks.jpg", "Kural 664: Thousand unseen strokes achieving monumental glory",
     "Photorealistic 16:9 cinematic construction view, colossal temple foundation, lone mason mortaring granite block with steady rhythm, wall stretching into distance."),
    ("67-vinaithitpam/19-n19_sailor_navigating_by_lone_polestar.jpg", "Kural 664: Solitary execution through the long dark night",
     "Photorealistic 16:9 cinematic night sea shot, dhow tiller, weathered navigator holding helm steady under canopy of bright southern stars, unbroken alertness."),
    ("67-vinaithitpam/20-n20_farmer_threshing_grain_under_noon_heat.jpg", "Kural 664: Practical toil versus arm-chair theorizing",
     "Photorealistic 16:9 cinematic dusty golden shot, threshing circle, farmer driving bullocks in endless circles over wheat stalks, sun beating down, steadfast endurance."),

    # Kural 665: Execute actions in such a way that both thought and deed win public praise
    ("67-vinaithitpam/21-n21_architect_explaining_flawless_dam_design.jpg", "Kural 665: Brilliant concept executed with matching artistry",
     "Photorealistic 16:9 cinematic riverbank scene, engineer showing miniature clay model of river diversion to king, pointing to where granite works already stand firm."),
    ("67-vinaithitpam/22-n22_general_conducting_bloodless_siege_victory.jpg", "Kural 665: Humane mastery praised by friend and foe",
     "Photorealistic 16:9 cinematic fortress gates, general accepting fortress keys from besieged governor after negotiating surrender without shedding a single drop of blood."),
    ("67-vinaithitpam/23-n23_physician_performing_successful_delicate_surgery.jpg", "Kural 665: Flawless surgical skill saving royal heir",
     "Photorealistic 16:9 cinematic clinic interior, Siddha surgeon setting down bronze forceps and bandaging patient's arm with soothing herbal poultice, court in relief."),
    ("67-vinaithitpam/24-n24_diplomat_securing_all_treaty_objectives.jpg", "Kural 665: Total diplomatic success celebrated by kingdom",
     "Photorealistic 16:9 cinematic audience hall, envoy bowing before cheering assembly after securing safe trade routes and sovereign border independence."),
    ("67-vinaithitpam/25-n25_village_assembly_voting_unanimous_honor.jpg", "Kural 665: Universal acclaim for exemplary civic leadership",
     "Photorealistic 16:9 cinematic mandapam shot, hundreds of village elders holding palm leaf ballots aloft in unanimous acclaim of upright irrigation overseer."),

    # Kural 666: What is conceived will be achieved as conceived, if the mind remains steadfast
    ("67-vinaithitpam/26-n26_sculptor_blueprint_becoming_living_granite_shrine.jpg", "Kural 666: Vision materializing into immortal stone",
     "Photorealistic 16:9 cinematic double-focus shot, foreground palm-leaf sketch of temple tower aligning perfectly with towering completed granite gopuram in background."),
    ("67-vinaithitpam/27-n27_monarch_envisioning_canal_network_across_valley.jpg", "Kural 666: Grand statecraft realized through unshakable focus",
     "Photorealistic 16:9 cinematic panoramic view, king standing on hill overlooking vast valley where gleaming canal network now mirrors the exact lines sketched on his scroll."),
    ("67-vinaithitpam/28-n28_athlete_crossing_finish_line_after_exhausting_race.jpg", "Kural 666: The physical triumph born of mental conviction",
     "Photorealistic 16:9 cinematic action shot, sandy arena, young Tamil runner bursting through finish line ribbon, chest heaving, triumphant roar of mental mastery."),
    ("67-vinaithitpam/29-n29_scholar_completing_the_grand_encyclopedia.jpg", "Kural 666: Lifelong intellectual project brought to fruition",
     "Photorealistic 16:9 cinematic library scene, venerable scholar stacking the hundredth polished palm-leaf manuscript bundle on teak bookstand, tears of fulfillment."),
    ("67-vinaithitpam/30-n30_shipbuilder_watching_new_flagship_sail_to_sea.jpg", "Kural 666: Seeing the dream take flight upon the waters",
     "Photorealistic 16:9 cinematic coastal vista, master shipwright standing on dock watching magnificent triple-decked sailing ship glide effortlessly into open ocean."),

    # Kural 667: Do not despise a man for small stature; axletree is held by small linchpin
    ("67-vinaithitpam/31-n31_small_bronze_linchpin_holding_massive_chariot_wheel.jpg", "Kural 667: Small linchpin securing the colossal chariot",
     "Photorealistic 16:9 cinematic macro close-up, heavy wooden war chariot axle, a small forged bronze linchpin firmly holding a nine-foot wooden wheel in place."),
    ("67-vinaithitpam/32-n32_slight_frail_sage_reproving_giant_warrior.jpg", "Kural 667: Mighty spiritual authority in a diminutive frame",
     "Photorealistic 16:9 cinematic dramatic scene, temple steps, frail elderly ascetic holding wooden staff, looking sternly into eyes of a towering armored warrior who bows meekly."),
    ("67-vinaithitpam/33-n33_young_boy_leading_giant_war_elephant.jpg", "Kural 667: Tiny guide commanding immense physical power",
     "Photorealistic 16:9 cinematic heartwarming shot, riverbank, slender twelve-year-old mahout boy holding ear of massive six-ton tusker, gently steering him with soft word."),
    ("67-vinaithitpam/34-n34_slender_keystone_supporting_colossal_stone_vault.jpg", "Kural 667: Central small stone bearing the weight of domes",
     "Photorealistic 16:9 cinematic upward angle, magnificent temple ceiling, intricately carved central keystone locking dozens of giant radiating granite beams in eternal balance."),
    ("67-vinaithitpam/35-n35_small_flame_illuminating_vast_cavern.jpg", "Kural 667: Modest flame dispelling boundless darkness",
     "Photorealistic 16:9 cinematic cavern shot, massive subterranean stone hall, single small clay oil lamp banishing pitch darkness, casting warm golden glow across carved pillars."),

    # Kural 668: Act decisively without delay; what should be pondered, ponder without haste
    ("67-vinaithitpam/36-n36_warrior_drawing_sword_with_lightning_speed.jpg", "Kural 668: Instant execution once deliberation is done",
     "Photorealistic 16:9 cinematic dynamic action shot, warrior drawing curved bronze sword from wooden scabbard with blur of blinding speed, blade flashing in sunlight."),
    ("67-vinaithitpam/37-n37_monarch_pausing_in_quiet_council_before_order.jpg", "Kural 668: Patient deliberation before the stroke of action",
     "Photorealistic 16:9 cinematic moody court scene, king sitting motionless in deep thought beside hourglass, weighing consequences before giving the final signal."),
    ("67-vinaithitpam/38-n38_charioteer_leaping_across_broken_bridge.jpg", "Kural 668: Decisive split-second courage",
     "Photorealistic 16:9 cinematic dramatic scene, wooden chariot leaping across washed-out bridge gap, hooves kicking up river spray, absolute commitment."),
    ("67-vinaithitpam/39-n39_physician_administering_remedy_without_hesitation.jpg", "Kural 668: Rapid intervention in critical crisis",
     "Photorealistic 16:9 cinematic close-up, physician pouring herbal antidote into unconscious snakebite victim's mouth with steady, unhurried precision, saving a life."),
    ("67-vinaithitpam/40-n40_falcon_diving_from_sky_onto_target.jpg", "Kural 668: The unstoppable dive of resolute purpose",
     "Photorealistic 16:9 cinematic aerial shot, peregrine falcon folded into arrow-like dive across morning sky, striking down with razor focus and speed."),

    # Kural 669: Even at the cost of intense pain, perform resolute deeds that bring victory
    ("67-vinaithitpam/41-n41_warrior_bearing_battle_scars_standing_unyielding.jpg", "Kural 669: Enduring agonizing wounds to defend homeland",
     "Photorealistic 16:9 cinematic dramatic portrait, bloodied and bandaged Tamil commander leaning on spear, chest adorned with hero scars, standing victorious on rampart."),
    ("67-vinaithitpam/42-n42_firefighters_entering_burning_granary_to_save_grain.jpg", "Kural 669: Enduring burning heat for public welfare",
     "Photorealistic 16:9 cinematic intense scene, flaming storehouse, brave citizens hauling water buckets and dragging sacks of grain out through roaring smoke and sparks."),
    ("67-vinaithitpam/43-n43_deep_sea_diver_surfacing_with_bleeding_ears.jpg", "Kural 669: Physical trial rewarded with precious treasure",
     "Photorealistic 16:9 cinematic raw portrait, exhausted pearl diver pulling himself into boat, holding up a giant lustrous natural oyster pearl, face glowing with triumph."),
    ("67-vinaithitpam/44-n44_monarch_fasting_until_justice_is_served.jpg", "Kural 669: Royal self-mortification to uphold moral law",
     "Photorealistic 16:9 cinematic solemn court scene, king seated on stone floor in fasting vigil, refusing food and crown until wronged subject's innocence is proven."),

    # Kural 670: The world does not desire the counsel of those devoid of resolute action
    ("67-vinaithitpam/45-n45_assembly_turning_away_from_spineless_adviser.jpg", "Kural 670: Rejection of weak-willed advisors",
     "Photorealistic 16:9 cinematic dramatic court shot, royal ministers turning their backs in quiet disdain on a cowardly courtier who proposes surrender to invaders."),
    ("67-vinaithitpam/46-n46_resolute_champion_carried_on_shoulders_of_people.jpg", "Kural 670: World celebrating the man of iron execution",
     "Photorealistic 16:9 cinematic joyful outdoor shot, city avenue, crowds hoisting heroic engineer on their shoulders, throwing flower petals as new aqueduct opens."),
    ("67-vinaithitpam/47-n47_granite_pillar_supporting_celestial_roof.jpg", "Kural 670: Strength that bears the weight of the realm",
     "Photorealistic 16:9 cinematic architectural view, magnificent row of carved lion-pillars (yali) holding up the massive granite roof of ancient temple corridor."),
    ("67-vinaithitpam/48-n48_flame_burning_brightly_in_howling_wind.jpg", "Kural 670: Unquenchable resolution defying the storm",
     "Photorealistic 16:9 cinematic macro shot, heavy bronze oil lamp on fortress battlement, flame burning upright and unwavering against torrential rain and howling gales."),
    ("67-vinaithitpam/49-n49_the_immortal_citadel_of_resolute_action.jpg", "Kural 661-670: Supreme triumph of the iron will",
     "Photorealistic 16:9 cinematic final shot, breathtaking panoramic view of ancient Tamil fortress city bathed in triumphant golden sunrise, banners fluttering in dawn wind.")
]

# -------------------------------------------------------------
# CHAPTER 74: நாடு (Naadu) - 35 SHOTS
# -------------------------------------------------------------
CH74_PROMPTS = [
    # Kural 731: An ideal country has unflagging harvest, virtuous people, and wealth
    ("74-naadu/01-n01_boundless_golden_paddy_fields_swaying_in_breeze.jpg", "Kural 731: Endless golden paddy fields of Tamil delta",
     "Photorealistic 16:9 cinematic sweeping landscape, Kaveri river basin, golden waves of ripe rice stalks heavy with grain stretching to palm-fringed horizon at dawn."),
    ("74-naadu/02-n02_happy_peasant_family_harvesting_together.jpg", "Kural 731: Joyful domestic harmony in rural heartland",
     "Photorealistic 16:9 cinematic medium-wide shot, fertile field, smiling Tamil farmer, his wife in yellow saree, and children cutting golden stalks with curved sickles."),
    ("74-naadu/03-n03_bustling_river_port_overflowing_with_wealth.jpg", "Kural 731: Merchant ships and maritime abundance",
     "Photorealistic 16:9 cinematic harbor view, river port of Poompuhar, wooden ships with billowing white sails docking, quayside piled with jars, timber, and silk."),
    ("74-naadu/04-n04_peaceful_village_with_grazing_cows_and_ponds.jpg", "Kural 731: Pastoral serenity of the righteous realm",
     "Photorealistic 16:9 cinematic idyllic rural scene, whitewashed thatched houses, sleek hump-backed cows grazing beside lotus-filled pond under gentle morning mist."),

    # Kural 732: A land desired for vast resources, yielding abundance without destructive toil
    ("74-naadu/05-n05_lush_delta_canals_flowing_effortlessly.jpg", "Kural 732: Hydraulic bounty watering the landscape",
     "Photorealistic 16:9 cinematic high-angle shot, network of stone-lined irrigation canals branching off mighty river, feeding green emerald plots with gentle gradient."),
    ("74-naadu/06-n06_bountiful_fruit_orchards_heavy_with_mangoes.jpg", "Kural 732: Orchards dropping ripe jackfruit and mangoes",
     "Photorealistic 16:9 cinematic close-up orchard shot, branches laden with giant ripe jackfruit, golden mangoes, and clusters of tender coconuts in sunlit grove."),
    ("74-naadu/07-n07_mountain_slopes_covered_in_pepper_and_cardamom.jpg", "Kural 732: Hill country brimming with precious spices",
     "Photorealistic 16:9 cinematic landscape, misty slopes of the Annamalai hills, wild pepper vines climbing silver oak trees, cardamom bushes flowering in shade."),
    ("74-naadu/08-n08_fisherman_pulling_nets_heavy_with_silver_fish.jpg", "Kural 732: Coastal seas teeming with rich sea harvests",
     "Photorealistic 16:9 cinematic morning beach scene, catamaran fishermen pulling large woven hemp nets foaming with silver fish, waves sparkling in early light."),

    # Kural 733: A land that bears burdens and pays taxes gladly to a just king
    ("74-naadu/09-n09_citizens_joyfully_bringing_first_fruits_to_palace.jpg", "Kural 733: Citizens gladly presenting fair share of harvest",
     "Photorealistic 16:9 cinematic wide shot, palace courtyard, cheerful villagers and farmers bringing baskets of golden grain, honey pots, and fruits to royal granary."),
    ("74-naadu/10-n10_king_opening_royal_granaries_during_public_festival.jpg", "Kural 733: Mutual reciprocity between crown and people",
     "Photorealistic 16:9 cinematic royal scene, smiling king overseeing distribution of festival sweets and new clothes to townspeople from stone treasury portico."),
    ("74-naadu/11-n11_village_panchayat_administering_civic_funds.jpg", "Kural 733: Local self-governance managing prosperity",
     "Photorealistic 16:9 cinematic pillared mandapam shot, village elders reviewing accounts inscribed on palm leaves, allocating gold for temple pond repairs."),
    ("74-naadu/12-n12_communal_granaries_sealed_with_wax_stamps.jpg", "Kural 733: National food security stored in safety",
     "Photorealistic 16:9 cinematic interior, massive underground terracotta grain silos (kudhir), sealed with inscribed clay seals, ensuring eternal food buffer."),

    # Kural 734: Free from excessive famine, epidemics, and devastating enemies
    ("74-naadu/13-n13_healthy_children_playing_in_blooming_meadow.jpg", "Kural 734: Freedom from plague and sickness",
     "Photorealistic 16:9 cinematic sunny meadow, vigorous healthy children laughing and playing tag among yellow mustard blossoms, radiant vitality."),
    ("74-naadu/14-n14_granite_frontier_fortress_guarding_the_pass.jpg", "Kural 734: Impenetrable borders guarding against invasion",
     "Photorealistic 16:9 cinematic dramatic shot, mountain pass between craggy peaks, formidable stone gate with disciplined sentries watching road in total safety."),
    ("74-naadu/15-n15_physicians_preparing_herbal_remedies_in_peace.jpg", "Kural 734: State healthcare warding off epidemics",
     "Photorealistic 16:9 cinematic calm interior, Ayurvedic apothecary, doctors bottling pure neem and tulsi distillations, preventative care for the entire populace."),
    ("74-naadu/16-n16_shepherd_sleeping_peacefully_under_stars.jpg", "Kural 734: Absolute security allowing deep untroubled sleep",
     "Photorealistic 16:9 cinematic night shot, grassy meadow under brilliant starry sky, shepherd resting peacefully on woven blanket with sheep and dog sleeping quietly nearby."),

    # Kural 735: Free from factional strife, internal sedition, and marauding bandits
    ("74-naadu/17-n17_various_communities_feasting_together_at_festival.jpg", "Kural 735: Social harmony free from factional discord",
     "Photorealistic 16:9 cinematic vibrant celebration, long avenue outside temple, diverse communities seated together enjoying feast on fresh banana leaves in fellowship."),
    ("74-naadu/18-n18_unarmed_merchants_traveling_safely_at_night.jpg", "Kural 735: Highways completely free from highwaymen",
     "Photorealistic 16:9 cinematic moonlit highway, merchant cart with lanterns traveling through dark forest road without fear of bandits, royal patrols passing with friendly waves."),
    ("74-naadu/19-n19_court_of_justice_settling_grievances_with_mercy.jpg", "Kural 735: Swift justice resolving disputes before they fester",
     "Photorealistic 16:9 cinematic pillared pavilion, respected judge listening attentively to two neighbors, shaking hands and walking away smiling in reconciliation."),
    ("74-naadu/20-n20_temple_bells_tolling_in_unified_harmony.jpg", "Kural 735: Sacred unity across all sectors of society",
     "Photorealistic 16:9 cinematic twilight shot, grand temple gateway with bronze bells swinging, sound carrying across town, lighting lamps in unison."),

    # Kural 736: A country that suffers no ruin from foes, and recovers swiftly if touched
    ("74-naadu/21-n21_ancient_stonework_enduring_through_millennia.jpg", "Kural 736: Resilience that weathers every historical storm",
     "Photorealistic 16:9 cinematic wide shot, monumental monolithic temple chariot standing weathered yet completely intact against stormy coastal backdrop."),
    ("74-naadu/22-n22_citizens_swiftly_repairing_monsoon_breach.jpg", "Kural 736: Rapid collective restoration after floods",
     "Photorealistic 16:9 cinematic dynamic scene, riverbank after heavy rains, hundreds of villagers working in unison with sandbags and wicker hurdles to reinforce levee."),
    ("74-naadu/23-n23_market_reopening_with_vibrant_energy.jpg", "Kural 736: Economic rebirth after seasonal tribulations",
     "Photorealistic 16:9 cinematic sunny morning shot, city bazaar bustling with fresh vegetables, flowers, and brassware, people trading with joyful smiles."),
    ("74-naadu/24-n24_monarch_surveying_restored_provinces.jpg", "Kural 736: Benevolent governance healing every wound",
     "Photorealistic 16:9 cinematic wide vista, king on horseback riding through thriving countryside, waving warmly to cheering farmers working in green fields."),

    # Kural 737: Two waters, well-sited hills, rivers, and fortress make a land
    ("74-naadu/25-n25_twin_waters_surface_rain_and_subterranean_springs.jpg", "Kural 737: Abundance of rain and underground springs",
     "Photorealistic 16:9 cinematic nature composition, mountain stream cascading into stone reservoir while gentle monsoon rain creates silver ripples on water surface."),
    ("74-naadu/26-n26_majestic_mountain_ranges_sheltering_the_plains.jpg", "Kural 737: Protective mountain ramparts of Tamilakam",
     "Photorealistic 16:9 cinematic panoramic landscape, blue silhouettes of Western Ghats mountain ridges standing as natural fortress walls against western horizon."),
    ("74-naadu/27-n27_perennial_river_winding_through_emerald_valleys.jpg", "Kural 737: Life-giving perennial river",
     "Photorealistic 16:9 cinematic high-angle river vista, wide shimmering Kaveri river curving gracefully through lush paddy fields, palm groves, and temple towns."),
    ("74-naadu/28-n28_impregnable_stone_fortress_overlooking_the_delta.jpg", "Kural 737: Mighty stronghold securing the homeland",
     "Photorealistic 16:9 cinematic sunset view, colossal granite fortress standing proudly on solitary hill, battlements glowing orange in dying sunlight."),

    # Kural 738: Five ornaments of a realm: health, wealth, harvest, joy, and security
    ("74-naadu/29-n29_the_five_jewels_of_the_ideal_homeland.jpg", "Kural 738: Synthesis of health, wealth, harvest, joy, and defense",
     "Photorealistic 16:9 cinematic poetic montage composition, golden paddy sheaves, brass coins, smiling mother and child, blooming temple pond, and bronze shield."),
    ("74-naadu/30-n30_village_folk_singing_around_pongal_pot.jpg", "Kural 738: Joyous festival of gratitude and harvest",
     "Photorealistic 16:9 cinematic festive scene, decorated terracotta pot boiling over with sweet milk-rice pongal, joyous family shouting 'Pongalo Pongal!' in golden sun."),
    ("74-naadu/31-n31_thriving_weavers_crafting_golden_silks.jpg", "Kural 738: Commercial prosperity and artistic mastery",
     "Photorealistic 16:9 cinematic workshop view, weavers working vibrant zari gold patterns on crimson silk, master merchant inspecting sheen with satisfaction."),

    # Kural 739 & 740: A country that yields without begging; useless without a noble king
    ("74-naadu/32-n32_earth_yielding_spontaneous_bounty_unbidden.jpg", "Kural 739: Natural spontaneous generosity of the land",
     "Photorealistic 16:9 cinematic lush shot, wild fertile riverside where banana plants hang heavy with fruit, coconut palms bend with nuts, and lotus ponds thrive."),
    ("74-naadu/33-n33_righteous_monarch_sitting_in_temple_council.jpg", "Kural 740: The sovereign who crowns the land's greatness",
     "Photorealistic 16:9 cinematic grand hall, king seated on stone throne with ministers and sages, listening humbly to village representatives, embodiment of dharma."),
    ("74-naadu/34-n34_the_prosperous_realm_celebrating_under_golden_hour.jpg", "Kural 731-740: The immortal beauty of Tamil homeland",
     "Photorealistic 16:9 cinematic panoramic vista, vast view from hill temple over ancient Tamil country, gleaming rivers, fertile fields, stone gopurams, radiant peace."),
    ("74-naadu/35-n35_the_eternal_dawn_of_tamilakam.jpg", "Kural 731-740: Glorious sunrise over the ideal realm",
     "Photorealistic 16:9 cinematic final shot, celestial sunrise casting pure gold across the flourishing land of Tamilakam, symbolizing eternal peace, wisdom, and dharma.")
]

ALL_BATCH4_CHAPTERS = {
    60: {"name": "60-ookkamudaimai", "prompts": CH60_PROMPTS, "count": len(CH60_PROMPTS), "target": 50},
    62: {"name": "62-aalvinaiyudaimai", "prompts": CH62_PROMPTS, "count": len(CH62_PROMPTS), "target": 47},
    65: {"name": "65-solvanmai", "prompts": CH65_PROMPTS, "count": len(CH65_PROMPTS), "target": 54},
    66: {"name": "66-vinaithooymai", "prompts": CH66_PROMPTS, "count": len(CH66_PROMPTS), "target": 44},
    67: {"name": "67-vinaithitpam", "prompts": CH67_PROMPTS, "count": len(CH67_PROMPTS), "target": 49},
    74: {"name": "74-naadu", "prompts": CH74_PROMPTS, "count": len(CH74_PROMPTS), "target": 35},
}

if __name__ == "__main__":
    total = sum(c["count"] for c in ALL_BATCH4_CHAPTERS.values())
    print(f"Total Batch 4 Prompts defined: {total}")
    for ch, data in ALL_BATCH4_CHAPTERS.items():
        status = "MATCH ✔" if data["count"] == data["target"] else f"MISMATCH (got {data['count']}, expected {data['target']})"
        print(f"  • Chapter {ch} ({data['name']}): {data['count']} prompts [{status}]")
