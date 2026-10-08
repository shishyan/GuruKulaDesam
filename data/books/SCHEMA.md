# 7 Sacred Books (7 ஆசிரமப் பாடநூல்கள்) JSON Schema Specification

Each grade file must be saved as `data/books/grade_{N}.json` (where N is 1 to 12).

## 7 Standard Books per Grade:
1. `nanneri` - நன்னெறி (Good Ethics, Humility & Conduct - Sivaprakasar)
2. `nallaram` - நல்லறம் (Righteous Virtue, Dharma & Family Responsibility - Thirukkural / Naladiyar)
3. `nalvazhi` - நல்வழி (The Noble Path, Practical Wisdom & Honest Labor - Avvaiyar)
4. `narthunai` - நற்துணை (Sacred Anchor, Spiritual Refuge & Satsang - Appar Namachivaya / Friendship)
5. `narchinthanai` - நற்சிந்தனை (Pure Thought, Mind Mastery & Resilience - Yogaswami / Upanishadic Manana)
6. `narchol` - நற்சொல் (Truthful, Sweet & Non-violent Speech - Iniyavai Narpathu / Kural)
7. `narcheyal` - நற்செயல் (Righteous Action, Nishkama Seva & Offering - Bhagavad Gita / Vallalar)

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
- `lifeApplication`: Specific actionable householder / student daily dharma practice
- `exercise`: Contemplative question or practical task
