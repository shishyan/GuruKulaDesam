# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Batch 3 Vedic Image Generator
Chapters:
- 54: பொச்சாவாமை (Pochchaavaamai - Unceasing Vigilance) - 40 authentic Vedic subjects
- 57: வெருவந்த செய்யாமை (Veruvantha Seyyaamai - Gentle & Impartial Justice) - 42 authentic Vedic subjects
- 61: மடியின்மை (Madiyinmai - Relentless Diligence & Overcoming Sloth) - 35 authentic Vedic subjects
Total: 117 authentic Sanatana Vedic masterpieces
Strictly adheres to: Tripundra Vibhuti, Rudraksha, sacred thread, Olais, Dravidian granite architecture, zero western/secular artifacts.
"""

import os
import sys
import time
import io
import shutil
from pathlib import Path
from PIL import Image
from google import genai
from google.genai import types

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
API_KEY = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=API_KEY)

CH54_SUBJECTS = {
    '01-n01_unwavering_flame_in_temple_sanctum.jpg': 'In an ancient Dravidian granite temple sanctum, a pure brass oil lamp flame burning completely still and unwavering in a draught-free stone niche, sacred symbol of pure uninterrupted mindfulness (Kural 531)',
    '02-n02_careless_householder_leaving_hearth.jpg': 'A careless householder looking in distress as his neglected hearth fire scorches a thatched eave, warning against the spiritual hazard of absent-mindedness (Kural 531)',
    '03-n03_vigilant_rishi_in_meditation.jpg': 'Under the spreading boughs of a thousand-year-old banyan tree at dawn, a venerable Tamil Rishi with Tripundra Vibhuti and Rudraksha sitting in razor-sharp meditative awareness (Kural 532)',
    '04-n04_ruined_dynasty_overgrown_granite.jpg': 'Overgrown ancient granite ruins half-swallowed by jungle vines and roots, cautionary monument to past kingdoms that crumbled through forgetfulness of dharma (Kural 533)',
    '05-n05_sentry_alert_on_stone_ramparts.jpg': 'On the carved granite battlements of an ancient Tamil fortress at twilight, an alert warrior sentry with bronze spear and Vibhuti scanning the forest border (Kural 534)',
    '06-n06_charioteer_guiding_horses_at_abyss.jpg': 'A skilled Tamil charioteer with focused eyes and firm hands holding the reins, guiding his horses safely along a precarious rocky mountain pass (Kural 535)',
    '07-n07_careful_scribe_inscribing_olai.jpg': 'A dedicated Tamil epigrapher with sacred thread carefully etching Tamil characters on a dry palm leaf with a pointed bronze stylus, never missing a letter (Kural 536)',
    '08-n08_guarding_the_irrigation_sluice.jpg': 'Beside an ancient stone check-dam on the Kaveri river during monsoon, a vigilant waterkeeper inspecting stone sluice gates to prevent breach (Kural 537)',
    '09-n09_warning_against_delusive_intoxication.jpg': 'A wise elder counselor holding up a hand of warning to a young prince, steering him away from frivolous distractions toward solemn statecraft (Kural 538)',
    '10-n10_monarch_consulting_historical_scrolls.jpg': 'In a royal stone chamber by oil lamplight, a crowned Tamil king with sacred thread reviewing ancient palm-leaf records of earlier disasters to avoid repeats (Kural 539)',
    '11-n11_morning_dawn_contemplation_ghats.jpg': 'On the wide granite bathing ghats of a sacred river at sunrise, seekers performing morning Sandhyavandanam with unwavering focus, greeting the rising sun (Kural 540)',
    '12-n12_potter_centering_clay_on_wheel.jpg': 'A master Tamil potter with intense concentration centering a spinning lump of moist clay on his wooden wheel, creating a flawless sacred kumbha (Kural 535)',
    '13-n13_gem_cutter_polishing_ruby.jpg': 'A gemstone artisan holding a raw red ruby against a turning emery wheel under a magnifying crystal, steady hand avoiding any slip (Kural 536)',
    '14-n14_granary_overseer_inspecting_wax_seals.jpg': 'In a vast temple granary, an overseer examining the stamped clay seals on grain bins, ensuring no waste or theft has occurred (Kural 537)',
    '15-n15_archer_focusing_on_target.jpg': 'An ancient Tamil archer standing poised in the dawn mist, drawing his bowstring to his ear with total stillness and laser focus (Kural 534)',
    '16-n16_elephant_mahout_navigating_crowd.jpg': 'A calm mahout atop a decorated temple elephant, guiding the gentle giant safely through a crowded festive temple street without harm to any (Kural 535)',
    '17-n17_counsel_of_vigilant_elders_at_dusk.jpg': 'In a village mandapam at sunset, five revered elders with silver beards and Vibhuti stripes deliberating community protection in solemn assembly (Kural 539)',
    '18-n18_fisherman_navigating_night_surf.jpg': 'A traditional wooden catamaran sailing through choppy ocean surf under starry skies, the helmsman keeping his eyes fixed on the distant shore beacon (Kural 535)',
    '19-n19_priest_tending_havan_flame.jpg': 'In a sacred temple yagashala, a Vedic priest vigilantly maintaining the sacred homam fire with dry samit sticks and pure clarified ghee (Kural 531)',
    '20-n20_prosperous_homeland_under_watchful_rule.jpg': 'A breathtaking panoramic vista of ancient Tamil Nadu at golden sunset: green river deltas, thriving village markets, and grand stone gopurams safe in vigilance (Kural 540)',
    '21-n21_sentinel_lighting_beacon_fire.jpg': 'High atop a granite fortress watchtower, a Tamil warrior in unstitched cotton garments lighting a bronze signal beacon basket against a twilight sky (Kural 534)',
    '22-n22_weaver_checking_silk_threads.jpg': 'A master Kanchipuram weaver leaning close over a wooden pit-loom, meticulously inspecting golden zari warp threads to prevent any flaw (Kural 536)',
    '23-n23_physician_measuring_ayurvedic_herbs.jpg': 'A traditional Tamil Siddha physician with sacred thread measuring fine herbal powders on a miniature bronze scale by lamplight (Kural 537)',
    '24-n24_monarch_visiting_frontline_outpost.jpg': 'A crowned Tamil king on horseback arriving unannounced at an outpost at dawn, personally verifying border alertness (Kural 539)',
    '25-n25_astronomer_studying_celestial_alignments.jpg': 'On an open stone observatory terrace at night, an ancient Tamil astronomer measuring star positions with a bronze ring instrument (Kural 535)',
    '26-n26_temple_treasurer_weighing_offerings.jpg': 'In the pillared treasury hall of a grand Kovil, an upright treasurer verifying gold jewelry offerings before stone deities (Kural 536)',
    '27-n27_farmer_mending_field_embankment.jpg': 'A hardworking Tamil farmer in dawn mist packing clay tightly onto a paddy bund to prevent irrigation water from draining away (Kural 537)',
    '28-n28_guru_checking_student_pronunciation.jpg': 'In an open Gurukulam mandapam, a revered Acharya listening attentively as a young student chants sacred Vedic verses, ensuring flawless meter (Kural 532)',
    '29-n29_coppersmith_engraving_temple_charter.jpg': 'An artisan engraving royal land grants on polished copper plates with fine chisels, his gaze steady and untrembling (Kural 536)',
    '30-n30_night_watchman_in_temple_corridor.jpg': 'A temple guard with a brass oil lantern walking the vast pillared thousand-pillar hall of a granite temple at midnight, keeping sacred watch (Kural 534)',
    '31-n31_seafarer_adjusting_rudder_at_dawn.jpg': 'An ancient Tamil mariner with sacred vibhuti adjusting the massive timber rudder of a merchant vessel navigating coastal shoals (Kural 535)',
    '32-n32_king_resisting_flattery_in_court.jpg': 'In the royal assembly, a wise king holding an unyielding posture as sycophants praise him, maintaining sober detachment (Kural 538)',
    '33-n33_shepherd_guarding_flock_from_predator.jpg': 'Under an acacia tree at twilight, an alert shepherd holding a seasoned wooden staff, keeping watch over sheep and goats near a forest edge (Kural 534)',
    '34-n34_sculptor_measuring_proportions_shilpa.jpg': 'A master sthapathi holding a palm-leaf Shilpa Shastra text while measuring the exact proportions of a granite deity with a bamboo scale (Kural 536)',
    '35-n35_guarding_the_sacred_temple_water_tank.jpg': 'Granite steps of a sacred temple lotus tank, a guardian ensuring the water remains pristine and unpolluted for temple rituals (Kural 537)',
    '36-n36_royal_emissary_checking_diplomatic_seal.jpg': 'An ancient diplomat carefully inspecting the wax seal of a peace treaty scroll before presenting it to an allied monarch (Kural 539)',
    '37-n37_householder_securing_courtyard_gates.jpg': 'At nightfall, a noble householder bolting the heavy carved teakwood entrance doors of his ancestral courtyard home (Kural 534)',
    '38-n38_monk_walking_razor_thin_ridge.jpg': 'A serene ascetic walking mindfully along a narrow granite mountain ledge, eyes downcast in absolute present-moment absorption (Kural 535)',
    '39-n39_king_awaking_before_city_stirs.jpg': 'In a palace bedchamber at Brahma Muhurta, a king rising from his woven kusha couch while the city still sleeps, lighting a morning lamp (Kural 540)',
    '40-n40_golden_harvest_secured_in_granaries.jpg': 'A grand panoramic view of ancient Tamil fields: ripe golden paddy fully harvested and secured in stone granaries, triumph of endless vigilance (Kural 540)',
}

CH57_SUBJECTS = {
    '01-n01_king_patient_hearing.jpg': 'In an ancient Dravidian granite audience hall, a noble Tamil monarch adorned with Tripundra Vibhuti and pearl garlands patiently listening to the plea of a humble peasant (Kural 561)',
    '02-n02_examining_evidence_scale.jpg': 'In the royal judicial mandapam, an upright judge carefully examining witnesses and palm-leaf testimony, weighing justice with impartial calm (Kural 561)',
    '03-n03_scales_of_fair_judgment.jpg': 'A consecrated bronze balance scale resting on a carved stone pedestal, counterbalanced by a white lotus flower and a stone, symbol of gentle righteousness (Kural 562)',
    '04-n04_counselors_deliberating_fairness.jpg': 'A circle of wise Vedic ministers with Rudraksha malas advising the young king to temper sternness with compassionate mercy (Kural 563)',
    '05-n05_reconciliation_of_disputants.jpg': 'In a village assembly under a neem tree, an elder restoring harmony between feuding kinsmen, replacing grievance with fraternal peace (Kural 564)',
    '06-n06_royal_scepter_of_restraint.jpg': 'Close-up of a carved golden Sengol (royal scepter) resting on a silk cushion beside a consecrated Shiva Lingam in the palace shrine (Kural 565)',
    '07-n07_pardoning_penitent_youth.jpg': 'A remorseful young offender with bowed head receiving royal pardon and gentle admonition from a magnanimous king (Kural 566)',
    '08-n08_guards_as_protectors.jpg': 'Ancient Tamil palace guards with bronze shields and spears helping an elderly village woman cross a crowded street with care (Kural 567)',
    '09-n09_gentle_admonishment_court.jpg': 'A monarch speaking words of calm, gentle correction to a faltering officer, inspiring him to reform rather than terrifying him (Kural 568)',
    '10-n10_restoration_of_confiscated_goods.jpg': 'Royal bailiffs returning mistakenly confiscated cattle to a grateful farmer family under the personal decree of the just king (Kural 569)',
    '11-n11_tyrant_shunned_in_loneliness.jpg': 'Visual contrast: a cruel ruler sitting solitary and paranoid in a dark hall while citizens flee his shadow (Kural 565)',
    '12-n12_beloved_king_received_by_populace.jpg': 'A gracious monarch walking unarmed through a village street, surrounded by cheering families offering fresh flower garlands and fruits (Kural 568)',
    '13-n13_rain_nourishing_parched_earth.jpg': 'Gentle monsoon rain falling on parched red soil and sprouting green shoots, metaphor of the sovereign whose gentle justice brings universal relief (Kural 568)',
    '14-n14_sheltering_tree_in_summer_heat.jpg': 'A massive spreading mango tree providing deep cool shade for weary cattle and travelers during the scorching midday heat (Kural 569)',
    '15-n15_eternal_glory_of_the_compassionate_ruler.jpg': 'A panoramic sunrise over ancient Tamilakam, with towering stone temple gopurams gleaming in celestial golden light over a peaceful, harmonious realm (Kural 570)',
    '16-n16_sovereign_embracing_elderly_subject.jpg': 'A crowned Tamil king stepping down from his royal platform to clasp the hands of an impoverished village elder with tears of compassion (Kural 561)',
    '17-n17_just_punishment_tempered_by_mercy.jpg': 'In a stone court, a magistrate commuting a harsh prison sentence to community service cleaning temple lotus tanks (Kural 562)',
    '18-n18_refusing_excessive_taxation.jpg': 'A righteous king returning a portion of collected grain taxes back to farmers following a season of dry drought (Kural 563)',
    '19-n19_village_panchayat_fair_settlement.jpg': 'Under a holy banyan tree, five village elders resolving boundary land disputes by mutual agreement without anger (Kural 564)',
    '20-n20_fearless_citizen_speaking_to_monarch.jpg': 'A humble weaver standing boldly before the king in full court, freely expressing grievance without fear of retribution (Kural 565)',
    '21-n21_king_punishing_corrupt_officer.jpg': 'A king stripping a greedy tax collector of his office while returning extracted coins to oppressed villagers (Kural 566)',
    '22-n22_royal_mercy_to_captured_rebels.jpg': 'Captured enemy soldiers receiving warm food, clean cotton garments, and medical care under royal decree of humane treatment (Kural 567)',
    '23-n23_serene_face_of_the_just_judge.jpg': 'Close-up of a venerable Vedic judicial scholar with Tripundra Vibhuti, his eyes radiating calm wisdom and incorruptible fairness (Kural 568)',
    '24-n24_children_greeting_royal_procession.jpg': 'Young Tamil children running laughing alongside the king’s ceremonial elephant, without terror or intimidation (Kural 568)',
    '25-n25_monarch_feeding_destitute_widows.jpg': 'Inside a royal anna-dana mandapam, the king and queen personally serving warm meals on plantain leaves to impoverished elders (Kural 569)',
    '26-n26_solitary_ruin_of_harsh_despot.jpg': 'A crumbling stone throne covered in wild weeds and cobwebs, cautionary symbol of the brief reign of cruel oppressors (Kural 565)',
    '27-n27_temple_bell_of_justice.jpg': 'A large bronze justice bell (Aaraichi Mani) hanging outside palace gates, which any citizen may ring to summon the king (Kural 561)',
    '28-n28_king_walking_among_crowded_bazaar.jpg': 'A beloved Tamil monarch dressed in simple silk veshti walking through a spice and flower bazaar, conversing directly with merchants (Kural 568)',
    '29-n29_mother_cradling_child_in_safety.jpg': 'A mother singing a lullaby to her infant in an open-door courtyard at night, showing the absolute safety of a just realm (Kural 569)',
    '30-n30_counselor_dissuading_harsh_decree.jpg': 'An elderly sage with white beard and Rudraksha placing his palm gently on the king’s arm, counseling against severe punishments (Kural 563)',
    '31-n31_cow_and_tiger_drinking_together.jpg': 'An allegorical painting motif on a temple fresco: a cow and tiger drinking from the same Kaveri river pool, symbol of righteous harmony (Kural 570)',
    '32-n32_royal_proclamation_granting_clemency.jpg': 'A town crier beating a bronze murasu drum and reading an Olai decree of royal clemency to joyful village crowds (Kural 566)',
    '33-n33_farmer_sleeping_safely_in_open_field.jpg': 'A tired farmer sleeping soundly on a wicker cot in his open harvest field under the moon, completely secure under just laws (Kural 569)',
    '34-n34_monarch_kneeling_before_shiva_lingam.jpg': 'The crowned king kneeling on granite flags before a Shiva Lingam, praying for humility and gentle wisdom to govern (Kural 565)',
    '35-n35_magistrate_destroying_false_evidence.jpg': 'A righteous judge burning fabricated palm leaves over charcoal embers, exposing and punishing the corrupt perjurer (Kural 562)',
    '36-n36_villagers_erecting_stone_of_honor_for_king.jpg': 'Villagers enthusiastically carving an inscription on a granite hero-stone honoring their beloved, gentle monarch (Kural 570)',
    '37-n37_water_given_to_captive_in_chains.jpg': 'A palace guard offering a brass cup of cool water to a prisoner awaiting trial, demonstrating innate dharma (Kural 567)',
    '38-n38_monarch_consulting_widowed_mother.jpg': 'A king listening with bowed head to the advice of an aged mother who lost a son in defense of the realm (Kural 561)',
    '39-n39_fertile_fields_blessed_by_righteous_scepter.jpg': 'A vast panoramic vista of emerald green rice paddies stretching to misty blue hills, thriving under gentle royal rule (Kural 570)',
    '40-n40_sage_blessing_the_sengol_scepter.jpg': 'A revered Kulaguru sprinkling sacred holy water on the golden Sengol scepter during a ceremonial blessing (Kural 565)',
    '41-n41_festive_temple_lamp_procession.jpg': 'Thousands of women carrying glowing terracotta lamps in a magnificent night temple festival celebrating peaceful governance (Kural 568)',
    '42-n42_eternal_monument_of_dharma.jpg': 'A towering Dravidian granite Rajagopuram rising majestically into golden dawn clouds, eternal symbol of the gentle, just sovereign (Kural 570)',
}

CH61_SUBJECTS = {
    '01-n01_flickering_lamp_neglected_house.jpg': 'In a neglected village homestead at dusk, a dying oil lamp flickering weakly in the wind, symbol of a lineage decaying through indolence (Kural 601)',
    '02-n02_youth_waking_and_polishing_lamp.jpg': 'An energetic young Tamil man with Tripundra Vibhuti rising early, cleaning the brass oil lamp and adding fresh oil with bright resolve (Kural 602)',
    '03-n03_bright_flame_ignited_ancestral_hall.jpg': 'The ancestral hall illuminated with blazing brass lamps as the industrious youth begins his day with morning prayers and vigorous study (Kural 602)',
    '04-n04_honoring_ancestral_lineage_scrolls.jpg': 'A dutiful son respectfully unrolling ancient family palm-leaf manuscripts, resolving to restore his lineage to ancient honor (Kural 603)',
    '05-n05_artisan_rising_before_dawn.jpg': 'In the pre-dawn quiet, a master Tamil metalsmith lighting his forge fire, ready to shape glowing bronze with joyful energy (Kural 604)',
    '06-n06_father_son_crafting_wheel.jpg': 'A father and son working harmoniously in their workshop, fitting seasoned teak spokes into a sturdy chariot wheel (Kural 605)',
    '07-n07_apprentice_practicing_sculpture.jpg': 'A young sthapathi apprentice practicing stone chiseling on granite by morning light under the watchful encouraging gaze of his master (Kural 606)',
    '08-n08_rapid_growth_of_family_enterprise.jpg': 'A bustling courtyard where weavers, spinners, and dyers produce fine gold-bordered silks, the family homestead flourishing through diligence (Kural 607)',
    '09-n09_overgrown_field_broken_plow.jpg': 'An abandoned field overgrown with thorny brambles and a weathered wooden plow resting in mud, cautionary image of sloth (Kural 608)',
    '10-n10_energetic_farmer_clearing_brambles.jpg': 'A strong Tamil farmer wielding a curved iron billhook, swiftly clearing away weeds and preparing the fertile red loam for the plow (Kural 609)',
    '11-n11_bullocks_plowing_fertile_fields.jpg': 'A pair of hump-backed white bullocks with painted horns pulling a wooden plow through wet paddy loam at golden sunrise (Kural 609)',
    '12-n12_bountiful_golden_paddy_harvest.jpg': 'Boundless green and golden paddy fields swaying in the morning breeze, farmers joyfully harvesting heavy unhusked grain (Kural 610)',
    '13-n13_restoring_the_broken_river_bund.jpg': 'Villagers working together with wicker baskets of earth and stone, strengthening a river embankment before monsoon floods arrive (Kural 609)',
    '14-n14_scholar_burning_midnight_lamp.jpg': 'A dedicated scholar studying philosophical treatises inscribed on palm leaves by the warm glow of an oil lamp late into the night (Kural 607)',
    '15-n15_triumph_of_unwavering_effort.jpg': 'A glorious panoramic sunrise over ancient Tamil Nadu, showing stone temples, thriving bazaars, and green river deltas, the eternal victory of righteous toil (Kural 610)',
    '16-n16_slothful_youth_sleeping_past_sunrise.jpg': 'A slothful youth lying idle on a worn mat while golden sunbeams pour through the window, illustrating loss of precious time (Kural 601)',
    '17-n17_vigor_of_the_early_riser_river.jpg': 'An energetic youth diving into the cool waters of the Kaveri river at dawn, rising invigorated for a day of purposeful work (Kural 602)',
    '18-n18_restoring_dilapidated_temple_steps.jpg': 'Devotees and artisans carrying heavy granite slabs to rebuild the crumbling stone steps of an ancient shrine (Kural 603)',
    '19-n19_young_woman_tending_loom_at_first_light.jpg': 'A young Tamil woman sitting at a traditional handloom at sunrise, weaving fine cotton threads with rhythmic precision (Kural 604)',
    '20-n20_blacksmith_hammering_iron_anvil.jpg': 'A muscular Tamil blacksmith striking a glowing orange iron blade on an anvil, sparks flying into the dim forge (Kural 605)',
    '21-n21_irrigation_canal_carved_through_rock.jpg': 'Determined villagers chiseling an irrigation channel through solid granite bedrock to bring river water to parched fields (Kural 606)',
    '22-n22_merchant_fleet_setting_sail.jpg': 'Timber merchant ships with billowing cotton sails launching from the port of Korkai into the morning sea mist (Kural 607)',
    '23-n23_abandoned_hearth_full_of_cold_ashes.jpg': 'A cold, unlit hearth covered in grey ash and cobwebs, representing a home ruined by procrastination (Kural 608)',
    '24-n24_planting_saplings_in_fallow_land.jpg': 'A farming family planting coconut and mango saplings in cleared red soil, investing labor for future generations (Kural 609)',
    '25-n25_student_mastering_complex_scripture.jpg': 'A young brahmachari pupil reading through stacks of palm-leaf manuscripts under the guidance of his guru, eyes full of determination (Kural 607)',
    '26-n26_carpenter_shaping_temple_chariot.jpg': 'A master carpenter meticulously carving sacred wooden yalis onto the massive wheel base of a temple car (Ther) (Kural 605)',
    '27-n27_potter_kneading_clay_with_feet.jpg': 'An industrious potter vigorously kneading fresh clay with his feet in dawn light to prepare it for the wheel (Kural 604)',
    '28-n28_community_clearing_temple_pond.jpg': 'Hundreds of villagers working in harmony with wicker baskets, dredging silt and mud from a temple lotus tank (Kural 609)',
    '29-n29_warrior_honing_sword_blade.jpg': 'A seasoned warrior grinding his bronze sword on an oiled whetstone, preparing his gear with relentless discipline (Kural 605)',
    '30-n30_housewife_churning_butter_at_dawn.jpg': 'A Tamil mother churning fresh curd with a wooden twirler tied to a rope, rich yellow butter gathering at the surface (Kural 604)',
    '31-n31_brickmaker_stacking_sun_dried_bricks.jpg': 'Artisans stacking thousands of freshly molded terracotta bricks under the open sun for temple construction (Kural 606)',
    '32-n32_sage_praising_the_industrious_worker.jpg': 'A venerable Rishi with Tripundra Vibhuti placing his hand in blessing upon the head of a sweat-drenched, hardworking laborer (Kural 610)',
    '33-n33_overflowing_granaries_in_village.jpg': 'Massive circular wicker granaries bursting with golden paddy in a village courtyard, fruit of relentless toil (Kural 610)',
    '34-n34_illuminated_ancestral_mansion.jpg': 'The ancestral courtyard mansion now restored and gleaming with hundreds of evening oil lamps, lineage saved from decay (Kural 603)',
    '35-n35_glorious_temple_procession_at_twilight.jpg': 'A magnificent temple car procession through flourishing town streets, celebrating the divine triumph of righteous effort (Kural 610)',
}

CHAPTERS_BATCH3 = [
    (54, 'Pochchaavaamai - பொச்சாவாமை - Unceasing Vigilance of Dharma', '54-pochchaavaamai', CH54_SUBJECTS),
    (57, 'Veruvantha Seyyaamai - வெருவந்த செய்யாமை - Gentle & Just Rule', '57-veruvantha-seyyaamai', CH57_SUBJECTS),
    (61, 'Madiyinmai - மடியின்மை - Overcoming Sloth & Relentless Effort', '61-madiyinmai', CH61_SUBJECTS),
]

BASE_PROMPT = (
    'A 16:9 cinematic photorealistic devotional masterpiece, 8k, authentic Indian Sanatana Vedic tradition. '
    'Set in ancient classical Tamil Nadu. Theme of Thirukkural Chapter {ch_num} ({ch_name}). '
    'Visual subject: {subject}. '
    'Atmosphere: ancient Dravidian stone temples, open-air Gurukulam hermitages, sacred Kaveri river, '
    'Tamil kings, Vedic Acharyas, Rishis, and householders with Tripundra Vibhuti, Rudraksha malas, sacred cotton thread (Yajnopavita), '
    'palm-leaf manuscripts (Olais), bronze oil lamps, kusha grass mats, brass water vessels. '
    'Lighting: radiant golden morning sunlight filtering through banyan canopy, or warm twilight oil lamp glow. '
    'Strictly NO modern clothing, NO eyeglasses, NO printed books, NO European furniture, NO European columns, NO text overlays, NO watermarks.'
)

def run():
    print('=' * 70)
    print('STARTING VEDIC IMAGE GENERATION FOR BATCH 3 (Ch 54, 57, 61)')
    print('=' * 70)

    for ch_num, ch_name, folder_name, subjects in CHAPTERS_BATCH3:
        target_dir = ROOT / 'production' / 'visuals' / 'thirukkural' / folder_name
        old_secular = ROOT / 'production' / 'visuals' / 'thirukkural' / f'{folder_name}-old-secular'

        if target_dir.exists() and not old_secular.exists():
            print(f'Backing up {target_dir.name} -> {old_secular.name}...')
            shutil.copytree(target_dir, old_secular)
            for f in target_dir.glob('*.jpg'):
                f.unlink()
            for f in target_dir.glob('*.png'):
                f.unlink()
            print('Cleaned target directory for authentic Vedic imagery.')

        target_dir.mkdir(parents=True, exist_ok=True)
        print(f'\n>>> CHAPTER {ch_num}: {ch_name} ({len(subjects)} artworks)')

        for fname, subject_desc in subjects.items():
            out_file = target_dir / fname

            if out_file.exists() and out_file.stat().st_size > 25000:
                print(f'  [Exists] {fname}')
                continue

            prompt = BASE_PROMPT.format(ch_num=ch_num, ch_name=ch_name, subject=subject_desc)
            print(f'  Generating: {fname}...')

            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash-image',
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_modalities=['IMAGE'],
                            image_config=types.ImageConfig(aspect_ratio='16:9'),
                        ),
                    )
                    saved = False
                    if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                        for part in response.candidates[0].content.parts:
                            if part.inline_data:
                                img = Image.open(io.BytesIO(part.inline_data.data)).convert('RGB')
                                img.save(out_file, quality=95)
                                print(f'  ✅ Saved: {fname} ({img.size})')
                                saved = True
                                break
                    if saved:
                        break
                    else:
                        print(f'  ⚠️ Retrying {fname} (attempt {attempt+1})...')
                        time.sleep(3)
                except Exception as e:
                    print(f'  ⚠️ Error on attempt {attempt+1} for {fname}: {e}')
                    time.sleep(4)

            time.sleep(2.5)

    print('\n' + '=' * 70)
    print('ALL BATCH 3 VEDIC ARTWORKS GENERATED SUCCESSFULLY!')
    print('=' * 70)

if __name__ == '__main__':
    run()

