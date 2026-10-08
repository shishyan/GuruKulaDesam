# 7 Sacred Books (7 ஆசிரமப் பாடநூல்கள்) JSON Schema Specification

Each grade file must be saved as `data/books/grade_{N}.json` (where N is 1 to 12).

## 7 Standard Books per Grade:
1. `nanneri` - நன்னெறி (Good Ethics, Humility & Conduct - Sivaprakasar & Asarakkovai)
2. `nallaram` - நல்லறம் (Righteous Virtue, Householder Dharma & Ethics of Sharing - Thirukkural / Naladiyar)
3. `nalvazhi` - நல்வழி (The Noble Path, Practical Wisdom & Honest Labor - Avvaiyar Nalvazhi & Moodhurai)
4. `narthunai` - நற்துணை (Spiritual Anchor, Temple Visits, Yagnas & Sacred Rituals - Appar Thevaram, Agamas, Pancha Maha Yagnas)
5. `narchinthanai` - நற்சிந்தனை (All Buddha Teachings, Dhammapada, Mindfulness & Mind Mastery - 4 Noble Truths, Eightfold Path, Vipassana)
6. `narchol` - நற்சொல் (Thiru Manthiram, Sacred Mantras, Sound Science & Vak-Tapas - Thirumular, AUM, Gayatri, Mahamrityunjaya)
7. `narcheyal` - நற்செயல் (Duty, Discipline, Dignity - 3 Ds Action-Oriented Living graduated by age: play as duty for <8, coming to school as discipline, family life, earning wealth with dignity)

## Literature Base & Goal per Phase:
- **Phase 1: Grades 1–5 (The Puranas)**:
  - Grades 1–2: Wonder & Forms (Ganesha, Hanuman, Krishna, nature archetypes, simple emotions)
  - Grades 3–4: Cycles & Cosmic Harmony (Yugas, Samudra Manthan, alternating light and dark)
  - Grade 5: The Root of Intent (Boons, curses, Asura falls, choices having long-term structural consequences)
- **Phase 2: Grades 6–12 (The Itihasas & Bhagavad Gita)**:
  - Grades 6–8: The Blueprint of Duty (Ramayana - societal roles, gray areas like Vali Vadham, Sita's quiet resilience, Chatur Ashrama)
  - Grades 9–10: The Mechanics of Conflict (Mahabharata - institutional collapses, blind loyalty of Bhishma, toxic entitlement of Duryodhana, Yaksha Prasna, Vidura Neeti)
  - Grades 11–12: The Mastery of Mind (The Bhagavad Gita - managing burnout, performance anxiety, emotional equilibrium, Nishkama Karma)

## Chapter Structure (7 chapters per book):
Each book MUST contain at least 7 complete chapters with:
- `chapterNumber`: integer (1 to 7)
- `title`: Tamil chapter title
- `verse`: Authentic Tamil/Sanskrit classical verse or proverb
- `verseMeaning`: Word/line meaning in Tamil
- `exposition`: Detailed philosophical teaching (2-3 paragraphs in Tamil)
- `story`: Engaging narrative illustrating the principle (Puranic / Itihasic / real-life)
- `lifeApplication`: Specific actionable householder / student daily dharma practice (3 Ds: Duty, Discipline, Dignity)
- `exercise`: Contemplative question or practical task
- `images`: Array of 7 curated visual scenes (7 chapters × 7 images = 49 images per book, ~50 images overall; 4,116 images total across Grades 1–12):
  1. `hero` (முகப்பு ஓவியம்): Theme Hero Visual setting the spiritual/dharmic atmosphere.
  2. `verse` (செய்யுள் காட்சி): Sacred Verse Illustration depicting the sage/poet or scriptural setting.
  3. `exposition` (தத்துவ விளக்கம்): Philosophical Infographic / Conceptual Art visualizing the mental model.
  4. `story_start` (கதைத் தொடக்கம்): Narrative Scene 1 showing historical origin, characters, and ethical context.
  5. `story_climax` (கதை உச்சக்கட்டம்): Narrative Scene 2 depicting the moral victory, transformation, and divine darshan.
  6. `life_application` (வாழ்வியல் சாதனா): 3 Ds in Action (Duty, Discipline, Dignity) practical living scene.
  7. `meditation` (தியான & சிந்தனைக் காட்சி): Contemplative vision inspiring inner silence and meditation.
  Each image entry contains:
  - `index`: 1 to 7
  - `type`: string identifier
  - `typeTitle`: Tamil type badge
  - `caption`: Contextual Tamil caption
  - `url`: Path to verified image asset
  - `prompt`: Detailed generative AI art prompt for visual synthesis
