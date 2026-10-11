import sys
import re

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

test_desc = """A full-song cinematic devotional film for திருப்புலம்பல் 2026 (திருவாசகம்), set to the original Guru Kula Desam recording. Twelve distinct scenes follow a devotee’s prayer to Lord Shiva through temple halls and a brief rain-washed courtyard. The Guru Kula Desam emblem stays at lower left; paired lit dheepam and four slowly burning agarbaththi frame each lower corner with gentle white-grey smoke. The complete original song audio is preserved.

Original song: https://youtu.be/qQqwD3gjenE
Music: Guru Kula Desam
#Thiruppulambal #Thiruvasagam #LordShiva #GuruKulaDesam

பாடல் வரிகள் (Tamil Lyrics):
நமச்சிவாய வாழ்க நாதன் தாள் வாழ்க
இமைப்பொழுதும் என் நெஞ்சில் நீங்காதான் தாள் வாழ்க
தென்னாடுடைய சிவனே போற்றி எந்நாட்டவர்க்கும் இறைவா போற்றி!


பொருள் விளக்கம் (Spiritual Meaning):
அன்பே சிவம் என்னும் சைவப் பெருநெறியின்படி, பிறவிப் பிணியை அறுத்து ஆன்ம முக்தி அருளும் பரமசிவனின் திருவடிகளைப் போற்றிப் பாடும் திருமுறைத் தேவாரம்.

— குரு குல தேசம் | Guru Kula Desam
https://gurukuladesam.com"""

thirupulambal_lyrics = """பூங்கமலத் தயனொடுமால் அறியா நெறி பூவணத்தாய்
தாங்குசடை முடியானே தையலாள் ஓர் பாகத்தாய்
ஏங்குமடியவர்க் கருளும் ஈசனே எம்பெருமான்
பாங்குடைய நின்னடியே பணியுமா பணியாயே.

பாரொடு விண் ணீரனல் காலாகி நின்றாய்
ஆரொருவர் காண்கிற்பார் அன்னே உனைக்காணார்
சீரொடு நின்னடியே சிந்திப்பார் சிந்தையுள்
நீரொழுக நின்ற நெறியே திருப்புலம்பல்.

பொருள் விளக்கம் (Spiritual Meaning):
மாணிக்கவாசகப் பெருமான் திருவாசகத்தில் அருளிய திருப்புலம்பல். பிரமனும் திருமாலும் அறியவொணாத பெருமானே, உன்னை அன்போடு சிந்தித்து உருகும் நெறியைத் தந்தருள்வாயாக எனப் புலம்பி இறைஞ்சுகிறார்."""

parts = re.split(r'பாடல் வரிகள்\s*\(Tamil Lyrics\):', test_desc)
new_desc = parts[0] + "பாடல் வரிகள் (Tamil Lyrics):\n" + thirupulambal_lyrics + "\n\n— குரு குல தேசம் | Guru Kula Desam\nhttps://gurukuladesam.com"

print("Original length:", len(test_desc))
print("New length:", len(new_desc))
print("Has பூங்கமலத்:", "பூங்கமலத்" in new_desc)
print("Has Sivapuranam:", "நமச்சிவாய வாழ்க" in new_desc)
print("\n--- Output ---")
print(new_desc)
