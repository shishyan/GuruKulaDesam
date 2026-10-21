/* Master Universal Drawer, Detail Modal & Interactive Card Engine */
(function() {
  'use strict';

  let currentLang = localStorage.getItem('gkd_lang') || 'ta';

  // Comprehensive metadata dictionary for all 14 Manus
  const manuDetails = {
    1: {
      order: 1,
      name_ta: "1. சுவாயம்புவ மனு",
      name_en: "1. Svayambhuva Manu",
      title_ta: "மனித குலத்தின் ஆதி தந்தை (மனுஸ்மிருதி அருளியவர்)",
      title_en: "First Manu of Cosmic Creation & Author of Manusmriti",
      epoch_ta: "1-ஆம் மன்வந்தரம் (கடந்த காலம்)",
      epoch_en: "1st Manvantara (Past)",
      parentage_ta: "பிரம்ம தேவன் மற்றும் சதரூபை",
      parentage_en: "Lord Brahma & Queen Shatarupa",
      saptarshis_ta: "மரீசி, அத்திரி, அங்கிரஸர், புலஸ்தியர், புலகர், கிரது, வசிஷ்டர்",
      saptarshis_en: "Marichi, Atri, Angiras, Pulastya, Pulaha, Kratu, Vashistha",
      indra_ta: "யக்ஞன் (ஹரி அவதாரம்)",
      indra_en: "Yajna (Incarnation of Lord Vishnu)",
      avatar_ta: "யக்ஞ அவதாரம் (துதிக்கும் வேள்வி வடிவம்)",
      avatar_en: "Yajna Avatara",
      purana_ta: "ஸ்ரீமத் பாகவதம் 8.1.5-18, விஷ்ணு புராணம் 3.1.6-10",
      purana_en: "Bhagavata Purana 8.1, Vishnu Purana 3.1",
      image: "assets/images/lessons/disciples_under_sacred_tree.jpg",
      summary_ta: "பிரம்மனின் திருமேனியிலிருந்து சதரூபையுடன் உதித்த முதல் மனித தந்தை. இவருக்கு பிரியவிரதன் மற்றும் உத்தானபாதன் (துருவனின் தந்தை) என்ற இரு மாபெரும் பேரரசர்களும், தேவஹூதி (கபில முனிவரின் தாய்), ஆகுதி, பிரசூதி என்ற மூன்று மகள்களும் அவதரித்தனர். மனிதகுல தர்ம நெறிக்கான ஆதி 'மனுஸ்மிருதி' அருளியவர்.",
      summary_en: "Born directly from the body of Lord Brahma along with Queen Shatarupa. Father of great emperors Priyavrata (who shaped 7 continents) and Uttanapada (father of Dhruva), and Devahuti (mother of Kapila Muni). Proclaimed the foundational Dharma for humankind."
    },
    2: {
      order: 2,
      name_ta: "2. சுவாரோசிஷ மனு",
      name_en: "2. Svarocisha Manu",
      title_ta: "இரண்டாம் மன்வந்தர அதிபதி",
      title_en: "Guardian of the 2nd Cosmic Epoch",
      epoch_ta: "2-ஆம் மன்வந்தரம் (கடந்த காலம்)",
      epoch_en: "2nd Manvantara (Past)",
      parentage_ta: "அக்னி தேவன் & வரூதினி மரபு",
      parentage_en: "Agni Deva / Dyumat lineage",
      saptarshis_ta: "ஊர்ஜர், ஸ்தம்பர், பிராணர், வாதர், பிரிஷவர், நிரயர், தம்போலி",
      saptarshis_en: "Urja, Stambha, Prana, Vata, Prishava, Niraya, Dambholi",
      indra_ta: "ரோசனன் (விபஸ்சித்)",
      indra_en: "Rochana (Vipaschit)",
      avatar_ta: "விபூதி அவதாரம்",
      avatar_en: "Vibhuti Avatara",
      purana_ta: "பாகவதம் 8.1.19-23, விஷ்ணு புராணம் 3.1.11-14",
      purana_en: "Bhagavata Purana 8.1.19-23",
      image: "assets/images/lessons/sage_sacred_scripture.jpg",
      summary_ta: "அக்னி தேவனின் ஒளியிலிருந்து உதித்தவர். இவரது ஆட்சியில் துஷ்டர்கள் அடக்கப்பட்டு வேத யாகங்கள் தடையின்றி நடைபெற்றன. விபூதி என்ற விஷ்ணுவின் அம்சத்தால் இப்பிரபஞ்சம் ரக்ஷிக்கப்பட்டது.",
      summary_en: "Born of the celestial radiance of Agni. In his epoch, the supreme lord incarnated as Vibhuti, establishing righteous conduct across the earth."
    },
    3: {
      order: 3,
      name_ta: "3. உத்தம (ஔத்தமி) மனு",
      name_en: "3. Auttami (Uttama) Manu",
      title_ta: "உத்தானபாத குல மனு",
      title_en: "Sovereign of 3rd Manvantara",
      epoch_ta: "3-ஆம் மன்வந்தரம் (கடந்த காலம்)",
      epoch_en: "3rd Manvantara (Past)",
      parentage_ta: "பிரியவிரத மகாராஜா (அல்லது உத்தானபாதன்)",
      parentage_en: "Emperor Priyavrata / Uttanapada line",
      saptarshis_ta: "கௌகுந்திஹி, குருந்தி, தல்பர், சங்கர், பிரவாஹனர், மிதர், கதர்",
      saptarshis_en: "Kaukundihi, Kurundi, Dalbha, Sankha, Pravahana, Mita, Gada",
      indra_ta: "சத்யஜித் (சுசாந்தி)",
      indra_en: "Satyajit (Sushanti)",
      avatar_ta: "சத்யசேன அவதாரம்",
      avatar_en: "Satyasena Avatara",
      purana_ta: "பாகவதம் 8.1.24-29, விஷ்ணு புராணம் 3.1.15-18",
      purana_en: "Bhagavata Purana 8.1.24-29",
      image: "assets/images/lessons/gentle_justice_governance.jpg",
      summary_ta: "பிரியவிரதரின் குலத்தில் உதித்த உத்தம மன்னர். சத்யசேனர் என்ற விஷ்ணு அவதாரம் சத்யஜித் இந்திரனுடன் இணைந்து உலகைத் துன்புறுத்திய அசுரர்களை அழித்து அமைதி நிலவச் செய்தார்.",
      summary_en: "Scion of Emperor Priyavrata. Lord Satyasena incarnated to destroy wicked Asuras, restoring truth and serenity in the cosmos."
    },
    4: {
      order: 4,
      name_ta: "4. தாமச மனு",
      name_en: "4. Tamasa Manu",
      title_ta: "கஜேந்திர மோக்ஷம் அருளப்பட்ட மன்வந்தர மனு",
      title_en: "Epoch of Gajendra Moksha",
      epoch_ta: "4-ஆம் மன்வந்தரம் (கடந்த காலம்)",
      epoch_en: "4th Manvantara (Past)",
      parentage_ta: "பிரியவிரத மகாராஜா",
      parentage_en: "Emperor Priyavrata line",
      saptarshis_ta: "ஜோதிர்தாமர், பிருது, காவ்யர், சைத்ரர், அக்னி, வனகர், பீவர்",
      saptarshis_en: "Jyotirdhama, Prithu, Kavya, Chaitra, Agni, Vanaka, Pivara",
      indra_ta: "திரிசிகன் (Trisikha)",
      indra_en: "Trisikha",
      avatar_ta: "ஹரி அவதாரம் (கஜேந்திர வரதன்)",
      avatar_en: "Hari Avatara (Redeemer of Gajendra)",
      purana_ta: "பாகவதம் 8.2-4, விஷ்ணு புராணம் 3.1.19-22",
      purana_en: "Bhagavata Purana 8.2-4",
      image: "assets/images/lessons/animals_peaceful_sanctuary.jpg",
      summary_ta: "புகழ்பெற்ற கஜேந்திர மோக்ஷ லீலை நிகழ்ந்த புண்ணிய மன்வந்தரம். முதலை கவ்வ யானை 'ஆதிமூலமே' என கதறியபோது ஸ்ரீமன் நாராயணன் கருடன் மேல் விரைந்து வந்து சக்ராயுதத்தால் முதலையை அழித்து யானைக்கு மோக்ஷமளித்தார்.",
      summary_en: "The historic epoch of Gajendra Moksha. When the king of elephants cried 'Adimoolame!', Lord Narayana rushed on Garuda and liberated Gajendra with His Sudarshana Chakra."
    },
    5: {
      order: 5,
      name_ta: "5. ரைவத மனு",
      name_en: "5. Raivata Manu",
      title_ta: "ஐந்தாம் மன்வந்தர மனு",
      title_en: "Fifth Manvantara Guardian",
      epoch_ta: "5-ஆம் மன்வந்தரம் (கடந்த காலம்)",
      epoch_en: "5th Manvantara (Past)",
      parentage_ta: "பிரியவிரத மகாராஜா (தாமச மனுவின் தம்பி)",
      parentage_en: "Emperor Priyavrata line",
      saptarshis_ta: "ஹிரண்யரோமர், வேதஸ்ரீ, ஊர்த்வபாகு, வேதபாஹு, சுதாமா, பர்ஜன்யர், மகாமுனி",
      saptarshis_en: "Hiranyaroma, Vedashri, Urdhvabahu, Vedabahu, Sudhama, Parjanya, Mahamuni",
      indra_ta: "விபு (Vibhu)",
      indra_en: "Vibhu",
      avatar_ta: "வைகுண்ட அவதாரம்",
      avatar_en: "Vaikuntha Avatara",
      purana_ta: "பாகவதம் 8.5.1-6, விஷ்ணு புராணம் 3.1.23-26",
      purana_en: "Bhagavata Purana 8.5.1-6",
      image: "assets/images/lessons/sage_universal_compassion.jpg",
      summary_ta: "தாமச மனுவின் சகோதரர். இக்காலத்தில் சுபத்ரா மற்றும் வைகுண்ட முனிவருக்குத் திருமகனாக வைகுண்ட அவதாரம் தோன்றி உலகை காத்தருளினார்.",
      summary_en: "Brother of Tamasa Manu. The Lord manifested as Vaikuntha at the prayer of Subhadra to preserve universal harmony."
    },
    6: {
      order: 6,
      name_ta: "6. சாக்ஷுஷ மனு",
      name_en: "6. Cakshusha Manu",
      title_ta: "சமுத்திர மந்தனம் & கூர்ம அவதார மன்வந்தரம்",
      title_en: "Epoch of Samudra Manthana & Kurma Avatara",
      epoch_ta: "6-ஆம் மன்வந்தரம் (கடந்த காலம்)",
      epoch_en: "6th Manvantara (Past)",
      parentage_ta: "சக்ஷு (அனமித்ர குலம்)",
      parentage_en: "Chakshu / Ripu line",
      saptarshis_ta: "சுமேதர், விரஜர், ஹவிஷ்மந்தர், உத்தமர், மது, அபிமானம், சகஸ்ணர்",
      saptarshis_en: "Sumedha, Viraja, Havishmanta, Uttama, Madhu, Abhinamana, Sahasna",
      indra_ta: "மனோத்யுமன் (மந்திரத்ருமன்)",
      indra_en: "Mantradhyuma (Manojava)",
      avatar_ta: "அஜித அவதாரம் & பகவான் கூர்ம மூர்த்தி",
      avatar_en: "Ajita Avatara & Kurma Avatara (Turtle)",
      purana_ta: "பாகவதம் 8.5-12, விஷ்ணு புராணம் 3.1.27-31",
      purana_en: "Bhagavata Purana 8.5-12",
      image: "assets/images/lessons/grade3_pancha_bhuta_temples.jpg",
      summary_ta: "தேவர்களும் அசுரர்களும் பாற்கடலைக் கடைந்து அமுதமும் காமதேனு, ஐராவதம், உச்சைச்சிரவஸ் மற்றும் ஸ்ரீ மஹாலக்ஷ்மியும் அவதரித்த மகத்தான மன்வந்தரம். மந்தர மலையைத் தாங்க விஷ்ணு கூர்ம அவதாரம் எடுத்தார்.",
      summary_en: "The momentous epoch of the Churning of the Milk Ocean (Samudra Manthana). Lord Vishnu manifested as the divine tortoise Kurma, bearing Mount Mandara upon His back."
    },
    7: {
      order: 7,
      name_ta: "7. வைவஸ்வத மனு (ஸ்ரத்தாதேவன்)",
      name_en: "7. Vaivasvata Manu (Sraddhadeva)",
      title_ta: "தற்போதைய 7-ஆம் மன்வந்தரத்தின் மனு (சூரியன் மகன்)",
      title_en: "Current Ruling Manu & Father of Solar & Lunar Lines",
      epoch_ta: "தற்போதைய 7-ஆம் மன்வந்தரம் (நிகழ்காலம்)",
      epoch_en: "Current 7th Manvantara (Present Era)",
      parentage_ta: "விவஸ்வான் (சூரிய பகவான்) & சமஞ்ஞா தேவி",
      parentage_en: "Vivasvan (Surya) & Samjna",
      saptarshis_ta: "கஷ்யபர், அத்ரி, வசிஷ்டர், விஸ்வாமித்திரர், கௌதமர், ஜமதக்னி, பரத்வாஜர்",
      saptarshis_en: "Kashyapa, Atri, Vashistha, Vishvamitra, Gautama, Jamadagni, Bharadvaja",
      indra_ta: "புரந்தரன் (தேவேந்திரன்)",
      indra_en: "Purandara (Indra)",
      avatar_ta: "மத்ஸ்ய அவதாரம் & வாமன அவதாரம்",
      avatar_en: "Matsya Avatara & Vamana Avatara",
      purana_ta: "மத்ஸ்ய புராணம், பாகவதம் 8.13, விஷ்ணு புராணம் 3.1.32-35",
      purana_en: "Matsya Purana, Bhagavata 8.13",
      image: "assets/images/lessons/dharma_cow_calf.jpg",
      summary_ta: "நாம் வாழும் தற்போதைய மன்வந்தரத்தின் அதிபதி! பிரளயத்தின்போது மத்ஸ்ய அவதாரத்தால் ரக்ஷிக்கப்பட்டவர். இவரது மூத்த மகன் இக்ஷ்வாகு அயோத்தியை நிறுவி சூரிய குலத்தைத் தோற்றுவித்தார்; இவரது மகள் இளை புதனுடன் கூடி சந்திர குலத்தைத் தோற்றுவித்தார். சகல பாரத வம்சங்களின் ஆதி வேர் இவர்!",
      summary_en: "The sovereign of our present living Manvantara! Saved by Matsya Avatara from the deluge. His son Ikshvaku founded the Solar Dynasty; his daughter Ila united with Budha to establish the Lunar Dynasty. The fountainhead of all Bharata lines."
    },
    8: {
      order: 8,
      name_ta: "8. சாவர்ணி மனு",
      name_en: "8. Savarni Manu",
      title_ta: "அடுத்த எட்டாம் மன்வந்தர மனு (சூரியன்-சாயா மகன்)",
      title_en: "Next 8th Manu & Son of Surya & Chhaya",
      epoch_ta: "8-ஆம் மன்வந்தரம் (வருங்காலம்)",
      epoch_en: "8th Manvantara (Future)",
      parentage_ta: "விவஸ்வான் (சூரிய பகவான்) & சாயாதேவி",
      parentage_en: "Surya & Chhaya",
      saptarshis_ta: "கால்வர், தீப்திமான், பரசுராமர், அஸ்வத்தாமன், கிருபர், ரிஷ்யசிருங்கர், வியாசர்",
      saptarshis_en: "Galava, Diptiman, Parashurama, Ashvatthama, Kripa, Rishyashringa, Vyasa",
      indra_ta: "பலி சக்கரவர்த்தி (மகாபலி)",
      indra_en: "Mahabali Chakravartin",
      avatar_ta: "சார்வபௌம அவதாரம்",
      avatar_en: "Sarvabhauma Avatara",
      purana_ta: "பாகவதம் 8.13.10-17, விஷ்ணு புராணம் 3.2.10-18",
      purana_en: "Bhagavata Purana 8.13.10-17",
      image: "assets/images/lessons/scholar_palm_manuscript.jpg",
      summary_ta: "அடுத்த மன்வந்தரத்தை ஆளப்போகும் மனு. வாமன மூர்த்தியால் பாதாள லோகத்தில் ஆசிர்வதிக்கப்பட்ட மகாபலி சக்கரவர்த்தி இந்த மன்வந்தரத்தில் தேவேந்திரனாக அரியணை ஏறுவார்! சிரஞ்சீவிகளான வியாசர், பரசுராமர், அஸ்வத்தாமன் சப்தரிஷிகளாக விளங்குவர்.",
      summary_en: "The forthcoming Manu of the 8th epoch. King Mahabali will ascend as the reigning Indra of heaven, while immortal Chiranjivis Vyasa, Parashurama, and Ashvatthama serve as Saptarshis."
    },
    9: {
      order: 9,
      name_ta: "9. தக்ஷ சாவர்ணி மனு",
      name_en: "9. Daksha-savarni Manu",
      title_ta: "ஒன்பதாம் மன்வந்தர மனு",
      title_en: "Ninth Manvantara Guardian",
      epoch_ta: "9-ஆம் மன்வந்தரம் (வருங்காலம்)",
      epoch_en: "9th Manvantara (Future)",
      parentage_ta: "வருண தேவன்",
      parentage_en: "Varuna Deva line",
      saptarshis_ta: "மேதாதிதி, வசு, சத்யன், ஜோதிஷ்மான், த்யுதிமான், சவனன், பவ்யன்",
      saptarshis_en: "Medhatithi, Vasu, Satya, Jyotishman, Dyutiman, Savana, Bhavya",
      indra_ta: "அற்புதன் (Adbbhuta)",
      indra_en: "Adbhuta",
      avatar_ta: "ரிஷப அவதாரம்",
      avatar_en: "Rishabha Avatara",
      purana_ta: "பாகவதம் 8.13.18-20, விஷ்ணு புராணம் 3.2.19-22",
      purana_en: "Bhagavata Purana 8.13",
      image: "assets/images/lessons/temple_architecture.jpg",
      summary_ta: "வருணனின் அருளால் உதிக்கும் ஒன்பதாம் மனு. ரிஷபர் என்ற அவதாரம் விஷ்ணுவால் எடுக்கப்பட்டு அற்புத இந்திரனுடன் இணைந்து உலகைக் காக்கும்.",
      summary_en: "Ninth Manu born of Varuna. The Lord manifests as Rishabha, aiding Indra Adbhuta in maintaining universal virtue."
    },
    10: {
      order: 10,
      name_ta: "10. பிரம்ம சாவர்ணி மனு",
      name_en: "10. Brahma-savarni Manu",
      title_ta: "பத்தாம் மன்வந்தர மனு",
      title_en: "Tenth Manvantara Guardian",
      epoch_ta: "10-ஆம் மன்வந்தரம் (வருங்காலம்)",
      epoch_en: "10th Manvantara (Future)",
      parentage_ta: "உபஸ்லோகன் (Upashloka)",
      parentage_en: "Upashloka",
      saptarshis_ta: "ஹவிஷ்மான், சுக்ருதி, சத்யன், ஜயன், மூர்த்தி, நாபாகன், சமித்ரன்",
      saptarshis_en: "Havishman, Sukriti, Satya, Jaya, Murti, Nabhaga, Chamitra",
      indra_ta: "சாந்தி (Santi)",
      indra_en: "Shanti",
      avatar_ta: "விஷ்வக்ஸேன அவதாரம்",
      avatar_en: "Vishvaksena Avatara",
      purana_ta: "பாகவதம் 8.13.21-23, விஷ்ணு புராணம் 3.2.23-25",
      purana_en: "Bhagavata Purana 8.13",
      image: "assets/images/lessons/grade9_body_is_temple.jpg",
      summary_ta: "உபஸ்லோகனின் தவத்தால் உதிக்கும் பத்தாம் மனு. பகவான் விஷ்வக்ஸேனராக அவதரித்து சாந்தி இந்திரனுடன் உலக நன்மை செய்வார்.",
      summary_en: "Tenth Manu of the cosmic cycle. Lord manifests as Vishvaksena, establishing peace and righteousness."
    },
    11: {
      order: 11,
      name_ta: "11. தர்ம சாவர்ணி மனு",
      name_en: "11. Dharma-savarni Manu",
      title_ta: "பதினொன்றாம் மன்வந்தர மனு",
      title_en: "Eleventh Manvantara Guardian",
      epoch_ta: "11-ஆம் மன்வந்தரம் (வருங்காலம்)",
      epoch_en: "11th Manvantara (Future)",
      parentage_ta: "சத்தியகன் (Satyaka)",
      parentage_en: "Satyaka",
      saptarshis_ta: "நிஸ்சரர், அக்னிதேஜஸ், வபுஷ்மான், ஆரூணி, அநகன், ஹவிஷ்மான், சுவார்த்தன்",
      saptarshis_en: "Nischara, Agnitejas, Vapushman, Aruni, Anagha, Havishman, Svartha",
      indra_ta: "வைதிருதன் (Vaidhrita)",
      indra_en: "Vaidhrita",
      avatar_ta: "தர்மசேது அவதாரம்",
      avatar_en: "Dharmasetu Avatara",
      purana_ta: "பாகவதம் 8.13.24-26, விஷ்ணு புராணம் 3.2.26-28",
      purana_en: "Bhagavata Purana 8.13",
      image: "assets/images/lessons/royal_administration_dharma.jpg",
      summary_ta: "தர்மத்தின் பாலமாக விளங்கும் மனு. தர்மசேது என்ற அவதாரத்தில் தோன்றும் விஷ்ணு வேத தர்மத்தைக் காப்பார்.",
      summary_en: "The bridge of Dharma. Lord manifests as Dharmasetu to uphold eternal spiritual principles."
    },
    12: {
      order: 12,
      name_ta: "12. ருத்ர சாவர்ணி மனு",
      name_en: "12. Rudra-savarni Manu",
      title_ta: "பன்னிரண்டாம் மன்வந்தர மனு",
      title_en: "Twelfth Manvantara Guardian",
      epoch_ta: "12-ஆம் மன்வந்தரம் (வருங்காலம்)",
      epoch_en: "12th Manvantara (Future)",
      parentage_ta: "ருத்ரன் (சிவ அம்சம்)",
      parentage_en: "Rudra line",
      saptarshis_ta: "துபிஷ்மான், ஆயுஷ்மான், த்யுதிமான், தபஸ்வி, சுதபா, தபோமூர்த்தி, தபோநிதி",
      saptarshis_en: "Dyutiman, Tapasvi, Sudhama, Tapomurti, Taponidhi, Ayushman",
      indra_ta: "ரிதுதாமா (Rtudhama)",
      indra_en: "Ritadhama",
      avatar_ta: "சுதாம அவதாரம்",
      avatar_en: "Sudhama Avatara",
      purana_ta: "பாகவதம் 8.13.27-29, விஷ்ணு புராணம் 3.2.29-31",
      purana_en: "Bhagavata Purana 8.13",
      image: "assets/images/lessons/grade10_temple_chariot_festival.jpg",
      summary_ta: "ருத்ர அம்சத்தால் தோன்றும் மனு. சுதாமா அவதாரம் உலக ஜீவன்களுக்கு முக்தி வழியை அருளும்.",
      summary_en: "Twelfth Manu carrying Rudra's majesty. Lord manifests as Sudhama."
    },
    13: {
      order: 13,
      name_ta: "13. ரௌச்ய (தேவ சாவர்ணி) மனு",
      name_en: "13. Raucya (Deva-savarni) Manu",
      title_ta: "பதின்மூன்றாம் மன்வந்தர மனு",
      title_en: "Thirteenth Manvantara Guardian",
      epoch_ta: "13-ஆம் மன்வந்தரம் (வருங்காலம்)",
      epoch_en: "13th Manvantara (Future)",
      parentage_ta: "ருசி மகரிஷி & மாலினி",
      parentage_en: "Sage Ruchi & Malini",
      saptarshis_ta: "நிர்மோகர், தத்வதர்சி, நிஷ்பிரகம்பர், த்ருதிமான், ஹவ்யவான், அவ்யயர், சுபக்ஷர்",
      saptarshis_en: "Nirmoha, Tatvadarshi, Nishprakampa, Dhritiman, Havyavan, Avyaya, Subhaksha",
      indra_ta: "திவஸ்பதி (Divaspati)",
      indra_en: "Divaspati",
      avatar_ta: "யோகேஸ்வர அவதாரம்",
      avatar_en: "Yogeshvara Avatara",
      purana_ta: "பாகவதம் 8.13.30-32, விஷ்ணு புராணம் 3.2.32-34",
      purana_en: "Bhagavata Purana 8.13",
      image: "assets/images/lessons/grade8_chatur_ashrama.jpg",
      summary_ta: "ருசி முனிவரின் தவப்புதல்வர். யோகேஸ்வரர் என்ற அவதாரத்தால் யோகக் கலை உலகெங்கும் நிலைபெறும்.",
      summary_en: "Thirteenth Manu. The Lord manifests as Yogeshvara, the supreme teacher of Yoga."
    },
    14: {
      order: 14,
      name_ta: "14. பௌத்ய (இந்திர சாவர்ணி) மனு",
      name_en: "14. Indra-savarni (Bhautya) Manu",
      title_ta: "கல்பத்தின் இறுதி பதினான்காம் மனு",
      title_en: "Final 14th Manu of the Kalpa Cycle",
      epoch_ta: "14-ஆம் மன்வந்தரம் (வருங்காலம்)",
      epoch_en: "14th Manvantara (Future)",
      parentage_ta: "பூதி மகரிஷி",
      parentage_en: "Sage Bhuti",
      saptarshis_ta: "அக்னிபாஹு, சுசி, சுக்ரன், மாகதர், கிருதன், ஜிதேந்திரியர், யுக்தர்",
      saptarshis_en: "Agnibahu, Shuchi, Shukra, Magadha, Krita, Jitendriya, Yukta",
      indra_ta: "சுசி (Shuchi)",
      indra_en: "Shuchi",
      avatar_ta: "பிருஹத்பானு அவதாரம்",
      avatar_en: "Brihadbhanu Avatara",
      purana_ta: "பாகவதம் 8.13.33-36, விஷ்ணு புராணம் 3.2.35-40",
      purana_en: "Bhagavata Purana 8.13",
      image: "assets/images/lessons/temple_bell_morning.jpg",
      summary_ta: "சுவேத வராக கல்பத்தின் இறுதி மனு! 14 மன்வந்தரங்களும் நிறைவடைந்து பிரம்மனின் ஒரு பகல் நிறைவுறும் தருணம். பிருஹத்பானு என்ற அவதாரம் சிருஷ்டியின் நிறைவு காலத்தில் ஆன்மாக்களை பரமபதத்திற்கு வழிநடத்தும்.",
      summary_en: "The culminating 14th Manu of the cosmic Kalpa day of Brahma. Lord manifests as Brihadbhanu, guiding souls to liberation before the cosmic night."
    }
  };

  // Drawer / Popup opening function
  window.openManuDrawer = function(order) {
    const data = manuDetails[order];
    if (!data) return;

    let drawer = document.getElementById('lineageUniversalDrawer');
    if (!drawer) {
      createUniversalDrawer();
      drawer = document.getElementById('lineageUniversalDrawer');
    }

    const drawerBody = document.getElementById('drawerDynamicContent');
    const isTa = currentLang === 'ta';

    drawerBody.innerHTML = `
      <div class="drawer-hero-img-wrap">
        <img src="${data.image}" alt="${data.name_en}" class="drawer-hero-img" onerror="this.style.display='none'">
        <div class="drawer-badge-floating">
          ${isTa ? `மன்வந்தரம் ${data.order} / 14` : `Manvantara ${data.order} / 14`}
        </div>
      </div>

      <div class="drawer-header-content">
        <h2 class="drawer-title">${isTa ? data.name_ta : data.name_en}</h2>
        <div class="drawer-subtitle">${isTa ? data.title_ta : data.title_en}</div>
        <div class="drawer-epoch-pill">⏳ ${isTa ? data.epoch_ta : data.epoch_en}</div>
      </div>

      <div class="drawer-grid-details">
        <div class="drawer-grid-item">
          <span class="d-label">${isTa ? 'தோற்றம் / பெற்றோர்:' : 'Parentage / Origin:'}</span>
          <span class="d-val">${isTa ? data.parentage_ta : data.parentage_en}</span>
        </div>
        <div class="drawer-grid-item">
          <span class="d-label">${isTa ? 'மன்வந்தர விஷ்ணு அவதாரம்:' : 'Vishnu Avatara:'}</span>
          <span class="d-val" style="color: #34d399; font-weight: 700;">🪷 ${isTa ? data.avatar_ta : data.avatar_en}</span>
        </div>
        <div class="drawer-grid-item">
          <span class="d-label">${isTa ? 'தேவேந்திரன் பதவி:' : 'Reigning Indra:'}</span>
          <span class="d-val">⚡ ${isTa ? data.indra_ta : data.indra_en}</span>
        </div>
        <div class="drawer-grid-item">
          <span class="d-label">${isTa ? 'புராண சான்றுகள்:' : 'Scriptural Reference:'}</span>
          <span class="d-val" style="color: #c084fc;">📖 ${isTa ? data.purana_ta : data.purana_en}</span>
        </div>
      </div>

      <div class="drawer-section-block">
        <h4 class="d-block-title">${isTa ? 'சப்தரிஷிகள் அவை (Council of Saptarshis):' : 'Council of Saptarshis:'}</h4>
        <div class="d-saptarshi-pills">
          ${(isTa ? data.saptarshis_ta : data.saptarshis_en).split(',').map(s => `<span class="s-pill">🧘 ${s.trim()}</span>`).join('')}
        </div>
      </div>

      <div class="drawer-section-block">
        <h4 class="d-block-title">${isTa ? 'தத்துவ & வரலாற்று முக்கியத்துவம்:' : 'Philosophical & Historical Role:'}</h4>
        <p class="d-summary-p">${isTa ? data.summary_ta : data.summary_en}</p>
      </div>
    `;

    document.getElementById('lineageDrawerOverlay').classList.add('active');
    drawer.classList.add('active');
  };

  window.closeUniversalDrawer = function() {
    const drawer = document.getElementById('lineageUniversalDrawer');
    const overlay = document.getElementById('lineageDrawerOverlay');
    if (drawer) drawer.classList.remove('active');
    if (overlay) overlay.classList.remove('active');
  };

  function createUniversalDrawer() {
    const overlay = document.createElement('div');
    overlay.id = 'lineageDrawerOverlay';
    overlay.className = 'drawer-backdrop-overlay';
    overlay.onclick = window.closeUniversalDrawer;

    const drawer = document.createElement('aside');
    drawer.id = 'lineageUniversalDrawer';
    drawer.className = 'lineage-drawer-panel';
    drawer.innerHTML = `
      <div class="drawer-top-bar">
        <span style="font-weight: 700; color: #e9d5ff; font-size: 0.9rem;">🕉️ குருகுல வம்சாவளி ஆவணம்</span>
        <button type="button" class="drawer-close-btn" onclick="window.closeUniversalDrawer()" title="மூடுக">✕</button>
      </div>
      <div id="drawerDynamicContent" class="drawer-scrollable-body">
        <!-- Content injected dynamically -->
      </div>
    `;

    document.body.appendChild(overlay);
    document.body.appendChild(drawer);
  }

  // Bind clicks to all 14 Manu cards in the DOM
  window.attachManuCardClicks = function() {
    for (let i = 1; i <= 14; i++) {
      const card = document.getElementById(`manu_card_${i}`);
      if (card) {
        card.style.cursor = 'pointer';
        card.setAttribute('title', 'கிளிக் செய்து விரிவான தகவல்களைப் படிக்கலாம்');
        card.onclick = () => window.openManuDrawer(i);
        
        // Add a visual 'Click for details' indicator if not present
        if (!card.querySelector('.card-click-hint')) {
          const hint = document.createElement('div');
          hint.className = 'card-click-hint';
          hint.innerHTML = `<span>🔍 முழு விவரம் காண கிளிக் செய்க ›</span>`;
          card.appendChild(hint);
        }
      }
    }
  };

  document.addEventListener('DOMContentLoaded', function() {
    createUniversalDrawer();
    window.attachManuCardClicks();
  });

})();
