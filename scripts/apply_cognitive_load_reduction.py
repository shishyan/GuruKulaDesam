#!/usr/bin/env python3
"""
scripts/apply_cognitive_load_reduction.py
Applies cognitive load reduction across all 12 grades (tharam-1.html to tharam-12.html):
1. Injects the Grade Focus Hub Switcher at top of the study area.
2. Injects the 15-sheet batch filter bar above .sheets-grid.
3. Adds the switchGradeStudyMode and filterSheetBatch JavaScript engine.
4. Hooks sidebar navigation links to activate corresponding focus tabs.
"""

import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

HUB_BAR_TEMPLATE = """
    <!-- COGNITIVE LOAD REDUCTION: GRADE FOCUS STUDY HUB -->
    <nav class="grade-focus-hub-bar" aria-label="கற்றல் பிரிவுகள்">
      <button type="button" class="grade-hub-btn active" onclick="switchGradeStudyMode('books')" id="hubBtn_books" title="7 ஆசிரமப் பாடநூல்கள் வாசிக்க">
        <span class="hub-icon">📖</span>
        <span class="hub-label">7 ஆசிரமப் பாடநூல்கள்</span>
        <span class="hub-count">7 நூல்கள்</span>
      </button>
      <button type="button" class="grade-hub-btn" onclick="switchGradeStudyMode('sheets')" id="hubBtn_sheets" title="பாடநூல் தாள்களைப் பகுதி வாரியாகக் காண்க">
        <span class="hub-icon">📑</span>
        <span class="hub-label">பாடநூல் தாள்கள்</span>
        <span class="hub-count">60 தாள்கள்</span>
      </button>
      <button type="button" class="grade-hub-btn" onclick="switchGradeStudyMode('highlights')" id="hubBtn_highlights" title="பாடத்திட்ட உள்ளடக்கக் குறிப்புகள்">
        <span class="hub-icon">🏛️</span>
        <span class="hub-label">பாடத்திட்டம் &amp; குறிப்புகள்</span>
        <span class="hub-count">பாடநெறி</span>
      </button>
      <button type="button" class="grade-hub-btn" onclick="switchGradeStudyMode('panpaadu')" id="hubBtn_panpaadu" title="தமிழர் பண்பாடும் சிறுவர் விழாக்களும்">
        <span class="hub-icon">🪔</span>
        <span class="hub-label">பண்பாடு &amp; விழாக்கள்</span>
        <span class="hub-count">வாழ்வியல்</span>
      </button>
      <button type="button" class="grade-hub-btn" onclick="switchGradeStudyMode('virtues')" id="hubBtn_virtues" title="நற்பண்புகள், வினாடி-வினா &amp; தினசரி சாதனா">
        <span class="hub-icon">🌸</span>
        <span class="hub-label">நற்பண்புகள் &amp; பயிற்சி</span>
        <span class="hub-count">தேர்வு &amp; சாதனா</span>
      </button>
      <button type="button" class="grade-hub-btn show-all-btn" onclick="switchGradeStudyMode('all')" id="hubBtn_all" title="அனைத்து பிரிவுகளையும் ஒரே பக்கத்தில் காண்க">
        <span class="hub-icon">📜</span>
        <span class="hub-label">முழுப் பார்வை</span>
      </button>
    </nav>
"""

BATCH_BAR_TEMPLATE = """
    <!-- SHEETS BATCH PAGINATION (Reduces scrolling fatigue & cognitive overload) -->
    <div class="sheets-batch-bar" id="sheetsBatchBar">
      <span style="font-size:0.82rem; font-weight:700; color:var(--gold-soft); margin-right:4px;">பகுதி தேர்வு:</span>
      <button type="button" class="sheet-batch-btn active" id="batchBtn_1" onclick="filterSheetBatch(1)">பகுதி 1 (1–15)</button>
      <button type="button" class="sheet-batch-btn" id="batchBtn_2" onclick="filterSheetBatch(2)">பகுதி 2 (16–30)</button>
      <button type="button" class="sheet-batch-btn" id="batchBtn_3" onclick="filterSheetBatch(3)">பகுதி 3 (31–45)</button>
      <button type="button" class="sheet-batch-btn" id="batchBtn_4" onclick="filterSheetBatch(4)">பகுதி 4 (46–60)</button>
      <button type="button" class="sheet-batch-btn" id="batchBtn_all" onclick="filterSheetBatch('all')">அனைத்து 60 தாள்களும்</button>
    </div>
"""

FOCUS_ENGINE_JS = """
  <script>
    // =========================================================================
    // COGNITIVE LOAD REDUCTION ENGINE (Grade Focus Hub & Batching)
    // =========================================================================
    function switchGradeStudyMode(mode) {
      var hubBtns = document.querySelectorAll('.grade-hub-btn');
      hubBtns.forEach(function(b) {
        if (b.id === 'hubBtn_' + mode) b.classList.add('active');
        else b.classList.remove('active');
      });

      var booksSec = document.querySelector('.grade-7books-box');
      var highlightsSec = document.getElementById('syllabus-highlights');
      var panpaaduSec = document.getElementById('gradePanpaaduSection');
      var sheetsHeading = document.getElementById('sheets-section');
      var sheetsBatch = document.getElementById('sheetsBatchBar');
      var sheetsGrid = document.querySelector('.sheets-grid');
      var sheetsIntro = document.getElementById('sheetsIntroText');
      var virtueBox = document.getElementById('gradeVirtueBox');
      var quizSec = document.getElementById('quizSection');
      var sadhanaBox = document.getElementById('sadhanaBox') || document.querySelector('[id^="lms-box"]');

      var allSecs = [booksSec, highlightsSec, panpaaduSec, sheetsHeading, sheetsBatch, sheetsGrid, sheetsIntro, virtueBox, quizSec, sadhanaBox];

      if (mode === 'all') {
        allSecs.forEach(function(el) { if (el) el.style.display = ''; });
        if (sheetsHeading) sheetsHeading.style.display = 'flex';
        filterSheetBatch('all');
      } else {
        // Hide all first
        allSecs.forEach(function(el) { if (el) el.style.display = 'none'; });

        // Show only selected mode components
        if (mode === 'books') {
          if (booksSec) booksSec.style.display = 'block';
        } else if (mode === 'sheets') {
          if (sheetsHeading) sheetsHeading.style.display = 'flex';
          if (sheetsBatch) sheetsBatch.style.display = 'flex';
          if (sheetsGrid) sheetsGrid.style.display = 'grid';
          if (sheetsIntro) sheetsIntro.style.display = 'block';
          filterSheetBatch(1);
        } else if (mode === 'highlights') {
          if (highlightsSec) highlightsSec.style.display = 'block';
        } else if (mode === 'panpaadu') {
          if (panpaaduSec) panpaaduSec.style.display = 'block';
        } else if (mode === 'virtues') {
          if (virtueBox) virtueBox.style.display = 'block';
          if (quizSec) quizSec.style.display = 'block';
          if (sadhanaBox) sadhanaBox.style.display = 'block';
        }
      }

      // Smooth scroll to study area if user clicked
      var hubBar = document.querySelector('.grade-focus-hub-bar');
      if (hubBar && window.scrollY > hubBar.offsetTop) {
        hubBar.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }

      // Update URL hash without jumping
      if (history.replaceState) {
        var newHash = (mode === 'all') ? '' : '#' + mode;
        history.replaceState(null, null, window.location.pathname + window.location.search + newHash);
      }
    }

    function filterSheetBatch(batch) {
      var batchBtns = document.querySelectorAll('.sheet-batch-btn');
      batchBtns.forEach(function(b) {
        if ((batch === 'all' && b.id === 'batchBtn_all') || b.id === 'batchBtn_' + batch) {
          b.classList.add('active');
        } else {
          b.classList.remove('active');
        }
      });

      var cards = document.querySelectorAll('.sheets-grid .sheet-card');
      cards.forEach(function(card, idx) {
        var sheetNum = idx + 1;
        if (batch === 'all') {
          card.style.display = '';
        } else {
          var start = (batch - 1) * 15 + 1;
          var end = batch * 15;
          if (sheetNum >= start && sheetNum <= end) {
            card.style.display = '';
          } else {
            card.style.display = 'none';
          }
        }
      });
    }

    // Auto-initialize mode from URL hash or default to 'books'
    document.addEventListener('DOMContentLoaded', function() {
      var hash = window.location.hash.replace('#', '');
      var validModes = ['books', 'sheets', 'highlights', 'panpaadu', 'virtues', 'all'];
      if (validModes.indexOf(hash) !== -1) {
        switchGradeStudyMode(hash);
      } else {
        switchGradeStudyMode('books');
      }

      // Hook sidebar navigation links to focus mode switch
      var sideSheets = document.getElementById('side-group-sheets');
      if (sideSheets) {
        sideSheets.querySelector('a').onclick = function(e) { e.preventDefault(); switchGradeStudyMode('sheets'); };
      }
      var sideHighlights = document.getElementById('side-group-highlights');
      if (sideHighlights) {
        sideHighlights.querySelector('a').onclick = function(e) { e.preventDefault(); switchGradeStudyMode('highlights'); };
      }
      var sidePanpaadu = document.getElementById('side-group-panpaadu');
      if (sidePanpaadu) {
        sidePanpaadu.querySelector('a').onclick = function(e) { e.preventDefault(); switchGradeStudyMode('panpaadu'); };
      }
      var sideVirtue = document.getElementById('side-group-virtue');
      if (sideVirtue) {
        sideVirtue.querySelector('a').onclick = function(e) { e.preventDefault(); switchGradeStudyMode('virtues'); };
      }
    });
  </script>
"""

# Process all 12 grades
for g in range(1, 13):
    fpath = os.path.join(REPO_ROOT, f'tharam-{g}.html')
    if not os.path.exists(fpath):
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Insert Hub Bar above 7 books section if not present
    if 'grade-focus-hub-bar' not in html:
        # Target location: right above `<section class="scripture-study-section grade-7books-box"`
        pattern = r'(<!-- 7 ASHRAM BOOKS SUMMARY FOR GRADE \d+ -->\s*<section class="[^"]*grade-7books-box)'
        if re.search(pattern, html):
            html = re.sub(pattern, HUB_BAR_TEMPLATE + r'\n    \1', html, count=1)
        else:
            # Alternate fallback: before grade-7books-box
            html = html.replace('<section class="scripture-study-section grade-7books-box"',
                                HUB_BAR_TEMPLATE + '\n    <section class="scripture-study-section grade-7books-box"', 1)

    # 2. Add id="sheetsIntroText" to the paragraph above .sheets-grid
    if 'id="sheetsIntroText"' not in html:
        html = re.sub(r'(<p style="color:var\(--text-muted\); font-size:0\.9rem; margin-top:6px;">)',
                      r'<p id="sheetsIntroText" style="color:var(--text-muted); font-size:0.9rem; margin-top:6px;">', html, count=1)

    # 3. Insert Batch Bar right before `<div class="sheets-grid">`
    if 'sheetsBatchBar' not in html:
        html = html.replace('<div class="sheets-grid">', BATCH_BAR_TEMPLATE + '\n    <div class="sheets-grid">', 1)

    # 4. Insert FOCUS_ENGINE_JS before `</body>`
    if 'COGNITIVE LOAD REDUCTION ENGINE' not in html:
        html = html.replace('</body>', FOCUS_ENGINE_JS + '\n</body>', 1)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Applied cognitive load reduction to tharam-{g}.html")

print("All 12 grades updated with Focus Hub & Batch Pagination successfully!")
