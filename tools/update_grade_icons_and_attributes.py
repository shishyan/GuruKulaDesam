import re
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GRADE_ICONS = {
  1: '🌱',
  2: '🌿',
  3: '⭐',
  4: '🌊',
  5: '🪔',
  6: '🏹',
  7: '⚡',
  8: '🏛️',
  9: '⚖️',
  10: '📜',
  11: '☸️',
  12: '🪷'
}

for g in range(1, 13):
    fn = f'tharam-{g}.html'
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update <body ...> to include data-grade="X"
    # match <body class="has-left-strip"> or existing <body ...>
    content = re.sub(r'<body class="has-left-strip"(\s+data-grade="\d+")?>', f'<body class="has-left-strip" data-grade="{g}">', content)
    
    # 2. Update <span class="zen-grade-pill">...</span>
    icon = GRADE_ICONS[g]
    content = re.sub(r'<span class="zen-grade-pill">.*?</span>', f'<span class="zen-grade-pill">{icon} தரம் {g}</span>', content)

    with open(fn, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated {fn} with data-grade=\"{g}\" and icon {icon}")

print("\nDone updating all 12 tharam-*.html files.")
