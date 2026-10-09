import re

with open('grihastha.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. replace initial html
text = re.sub(
    r'<div id="dharmaStreakDisplay"[^>]*>[\s\S]*?</div>',
    '<div id="dharmaStreakDisplay" style="font-size: 1.6rem; font-weight: 800; color: #fbbf24;">🔥 1 நாள்</div>',
    text
)
text = re.sub(
    r'<div id="dharmaBadgeDisplay"[^>]*>[\s\S]*?</div>',
    '<div id="dharmaBadgeDisplay" style="font-size: 0.95rem; font-weight: 700; color: #c084fc; margin-top: 4px;">📜 தர்ம சாதகர்</div>',
    text
)

# 2. replace JS badgeDisplay.innerHTML
text = re.sub(
    r"badgeDisplay\.innerHTML = '<svg class=\"gkd-icon\"[^']*?உன்னத இல்லறம்';",
    'badgeDisplay.innerHTML = "🪔 உன்னத இல்லறம்";',
    text
)
text = re.sub(
    r"badgeDisplay\.innerHTML = '<svg class=\"gkd-icon\"[^']*?சான்றோன் இல்லறத்தார்';",
    'badgeDisplay.innerHTML = "🌿 சான்றோன் இல்லறத்தார்";',
    text
)
text = re.sub(
    r"badgeDisplay\.innerHTML = '<svg class=\"gkd-icon\"[^']*?தர்ம சாதகர்';",
    'badgeDisplay.innerHTML = "📜 தர்ம சாதகர்";',
    text
)

# 3. replace JS streakDisplay.innerHTML
text = re.sub(
    r"streakDisplay\.innerHTML = '<svg class=\"gkd-icon\"[^']*?' \+ streak \+ ' நாள்' \+ \(streak > 1 \? 'கள்' : ''\);",
    'streakDisplay.innerHTML = "🔥 " + streak + " நாள்" + (streak > 1 ? "கள்" : "");',
    text
)
text = re.sub(
    r"streakDisplay\.innerHTML = '<svg class=\"gkd-icon\"[^']*?' \+ streak \+ ' நாள்' \+ \(parseInt\(streak\) > 1 \? 'கள்' : ''\);",
    'streakDisplay.innerHTML = "🔥 " + streak + " நாள்" + (parseInt(streak) > 1 ? "கள்" : "");',
    text
)

with open('grihastha.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated grihastha.html streak & badge displays successfully!')
