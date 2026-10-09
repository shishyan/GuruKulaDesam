with open('kalvi.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add hero image
text = text.replace(
    '</p>\n      <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-top: 14px;">',
    '</p>\n      <div style="margin: 16px auto; max-width: 580px;">\n        <img src="assets/images/gurukula-banyan-tree-bg.jpg" alt="குருகுல ஆலமர வித்யாபீடம்" style="width: 100%; height: 160px; object-fit: cover; border-radius: 14px; box-shadow: 0 16px 42px rgba(0,0,0,0.92);" loading="eager">\n      </div>\n      <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-top: 14px;">'
)

# 2. Add stage 1 image
text = text.replace(
    'புராணக் கதைகள்\n          </span>\n        </div>\n        <p style="color: #cbd5e1;',
    'புராணக் கதைகள்\n          </span>\n        </div>\n        <div style="margin: 10px 0;"><img src="assets/images/lessons/children_feeding_creatures.jpg" alt="பாலப் பருவம்" style="width: 100%; max-width: 280px; height: 130px; object-fit: cover; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.7);" loading="lazy"></div>\n        <p style="color: #cbd5e1;'
)

# 3. Add stage 2 image
text = text.replace(
    'பண்பாடு\n          </span>\n        </div>\n        <p style="color: #cbd5e1;',
    'பண்பாடு\n          </span>\n        </div>\n        <div style="margin: 10px 0;"><img src="assets/images/lessons/grade7_periyapuranam_sekkizhar.jpg" alt="இளம் பருவம்" style="width: 100%; max-width: 280px; height: 130px; object-fit: cover; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.7);" loading="lazy"></div>\n        <p style="color: #cbd5e1;'
)

# 4. Add stage 3 image
text = text.replace(
    'சன்மார்க்கம்\n          </span>\n        </div>\n        <p style="color: #cbd5e1;',
    'சன்மார்க்கம்\n          </span>\n        </div>\n        <div style="margin: 10px 0;"><img src="assets/images/lessons/grade9_body_is_temple.jpg" alt="உயர்நிலைப் பருவம்" style="width: 100%; max-width: 280px; height: 130px; object-fit: cover; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.7);" loading="lazy"></div>\n        <p style="color: #cbd5e1;'
)

# 5. Add stage 4 image
text = text.replace(
    'ஜீவன்முக்தி\n          </span>\n        </div>\n        <p style="color: #cbd5e1;',
    'ஜீவன்முக்தி\n          </span>\n        </div>\n        <div style="margin: 10px 0;"><img src="assets/images/lessons/thavam_tapas_meditation.jpg" alt="மேல்நிலை &amp; உயர்கல்வி" style="width: 100%; max-width: 280px; height: 130px; object-fit: cover; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.7);" loading="lazy"></div>\n        <p style="color: #cbd5e1;'
)

with open('kalvi.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Added heritage images to kalvi.html!')
