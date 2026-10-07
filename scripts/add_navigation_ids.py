# -*- coding: utf-8 -*-
"""
Adds canonical navigation IDs to tharam-2.html through tharam-12.html:
- courseUnits: before or on id="course-content-start"
- gradeVirtueBox: on first class="scripture-study-section"
- visualDiagramCard: on first class="lesson-hero-visual-card"
- quizSection: before first class="quiz-card"
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

for g in range(2, 13):
    fn = ROOT / f"tharam-{g}.html"
    if not fn.exists():
        continue
    content = fn.read_text(encoding='utf-8')
    
    # 1. courseUnits
    if 'id="courseUnits"' not in content:
        if 'id="course-content-start"' in content:
            content = content.replace('id="course-content-start"', 'id="courseUnits" data-start="course-content-start"', 1)
        else:
            print(f"[WARN] No course-content-start in {fn.name}")

    # 2. gradeVirtueBox
    if 'id="gradeVirtueBox"' not in content:
        if 'class="scripture-study-section"' in content:
            content = content.replace('class="scripture-study-section"', 'id="gradeVirtueBox" class="scripture-study-section"', 1)
        else:
            print(f"[WARN] No scripture-study-section in {fn.name}")

    # 3. visualDiagramCard
    if 'id="visualDiagramCard"' not in content:
        if 'class="lesson-hero-visual-card"' in content:
            content = content.replace('class="lesson-hero-visual-card"', 'id="visualDiagramCard" class="lesson-hero-visual-card"', 1)
        else:
            print(f"[WARN] No lesson-hero-visual-card in {fn.name}")

    # 4. quizSection
    if 'id="quizSection"' not in content:
        if 'class="quiz-card"' in content:
            content = content.replace('class="quiz-card"', 'id="quizSection" class="quiz-card"', 1)
        else:
            print(f"[WARN] No quiz-card in {fn.name}")

    fn.write_text(content, encoding='utf-8')
    print(f"[UPDATED NAV IDs] {fn.name}")
