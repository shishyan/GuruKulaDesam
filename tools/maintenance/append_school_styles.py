# -*- coding: utf-8 -*-
"""
Appends Online School and Vedic-Modern Fusion styles to style.css across all 3 directories.
"""

SCHOOL_CSS = """
/* ==========================================================================
   PROFESSIONAL ONLINE SCHOOL & VEDIC-MODERN FUSION SYSTEM
   ========================================================================== */

.school-hero {
  background: linear-gradient(135deg, rgba(10, 16, 28, 0.95) 0%, rgba(15, 23, 42, 0.92) 50%, rgba(10, 25, 47, 0.95) 100%);
  border: 1px solid rgba(56, 189, 248, 0.28);
  border-radius: 20px;
  padding: 36px 32px;
  margin-bottom: 32px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6), 0 0 30px rgba(56, 189, 248, 0.08);
  position: relative;
  overflow: hidden;
}

.school-hero::before {
  content: "";
  position: absolute;
  top: -50px;
  right: -50px;
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, transparent 70%);
  pointer-events: none;
}

.school-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(56, 189, 248, 0.12);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.35);
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 5px 14px;
  border-radius: 20px;
  margin-bottom: 14px;
}

.school-stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 24px;
}

.school-stat-card {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: transform 0.2s ease, border-color 0.2s ease;
}

.school-stat-card:hover {
  transform: translateY(-2px);
  border-color: rgba(56, 189, 248, 0.35);
}

.school-stat-icon {
  font-size: 2rem;
  line-height: 1;
  background: rgba(255, 255, 255, 0.05);
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.school-stat-val {
  font-size: 1.5rem;
  font-weight: 800;
  color: #ffffff;
  line-height: 1.1;
}

.school-stat-lbl {
  font-size: 0.8rem;
  color: #94a3b8;
  margin-top: 2px;
}

/* Fusion Matrix Cards */
.fusion-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
  margin: 24px 0;
}

.fusion-pillar-card {
  background: rgba(15, 23, 42, 0.85);
  border: 1px solid rgba(56, 189, 248, 0.2);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  transition: all 0.25s ease;
  position: relative;
  overflow: hidden;
}

.fusion-pillar-card:hover {
  transform: translateY(-3px);
  border-color: rgba(56, 189, 248, 0.5);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6), 0 0 20px rgba(56, 189, 248, 0.12);
}

.fusion-pillar-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}

.fusion-pillar-num {
  font-size: 0.75rem;
  font-weight: 800;
  color: #38bdf8;
  background: rgba(56, 189, 248, 0.12);
  border: 1px solid rgba(56, 189, 248, 0.3);
  padding: 2px 8px;
  border-radius: 6px;
  letter-spacing: 0.5px;
}

.fusion-pillar-title {
  color: #ffffff;
  font-size: 1.15rem;
  font-weight: 700;
  line-height: 1.3;
}

.fusion-desc-box {
  background: rgba(0, 0, 0, 0.3);
  border-left: 3px solid #38bdf8;
  border-radius: 0 8px 8px 0;
  padding: 12px 14px;
  margin-bottom: 12px;
  font-size: 0.88rem;
  line-height: 1.65;
  color: #cbd5e1;
}

.fusion-application-box {
  background: rgba(45, 212, 191, 0.05);
  border-left: 3px solid #2dd4bf;
  border-radius: 0 8px 8px 0;
  padding: 12px 14px;
  margin-bottom: 14px;
  font-size: 0.88rem;
  line-height: 1.65;
  color: #cbd5e1;
}

.fusion-sutra-tag {
  margin-top: auto;
  padding-top: 10px;
  border-top: 1px dashed rgba(255, 255, 255, 0.1);
  font-size: 0.8rem;
  color: var(--gold-soft);
  font-style: italic;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* Study Hall & Focus Timer */
.study-room-panel {
  background: linear-gradient(135deg, rgba(13, 19, 33, 0.95), rgba(19, 27, 46, 0.95));
  border: 1px solid rgba(212, 175, 55, 0.3);
  border-radius: 20px;
  padding: 32px;
  margin: 32px 0;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
}

.timer-box {
  text-align: center;
  padding: 24px;
  background: rgba(0, 0, 0, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  max-width: 440px;
  margin: 0 auto 24px;
}

.timer-digits {
  font-size: 4rem;
  font-family: 'Outfit', monospace;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: 2px;
  text-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
  line-height: 1.1;
  margin: 14px 0;
}

.timer-mode-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #cbd5e1;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  margin: 0 4px;
  transition: all 0.2s ease;
}

.timer-mode-btn.active {
  background: rgba(56, 189, 248, 0.2);
  border-color: #38bdf8;
  color: #ffffff;
}

.timer-ctrl-btn {
  background: linear-gradient(135deg, #0284c7, #0ea5e9);
  color: #ffffff;
  border: none;
  padding: 10px 28px;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4);
  transition: all 0.2s ease;
  margin: 0 6px;
}

.timer-ctrl-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(14, 165, 233, 0.6);
}

.timer-reset-btn {
  background: rgba(255, 255, 255, 0.08);
  color: #cbd5e1;
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 10px 20px;
  border-radius: 30px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin: 0 6px;
}

/* Breath Pacer (4-7-8 Pranayama Circle) */
.breath-pacer-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
  margin: 20px auto;
  max-width: 360px;
}

.breath-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.25) 0%, rgba(45, 212, 191, 0.05) 70%);
  border: 3px solid rgba(56, 189, 248, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 30px rgba(56, 189, 248, 0.25);
  transition: all 1s ease;
}

.breath-circle.inhale {
  transform: scale(1.4);
  border-color: #38bdf8;
  box-shadow: 0 0 40px rgba(56, 189, 248, 0.5);
}

.breath-circle.hold {
  transform: scale(1.4);
  border-color: var(--gold);
  box-shadow: 0 0 40px rgba(212, 175, 55, 0.5);
}

.breath-circle.exhale {
  transform: scale(0.85);
  border-color: #2dd4bf;
  box-shadow: 0 0 20px rgba(45, 212, 191, 0.3);
}

.breath-instruction {
  font-size: 1.15rem;
  font-weight: 700;
  color: #ffffff;
  margin-top: 16px;
  text-align: center;
}

.breath-sub-instruction {
  font-size: 0.85rem;
  color: #94a3b8;
  text-align: center;
  margin-top: 4px;
}

/* Certificate Generator */
.certificate-preview-card {
  background: linear-gradient(145deg, #0b111e 0%, #151e30 100%);
  border: 4px double var(--gold);
  border-radius: 16px;
  padding: 40px 32px;
  text-align: center;
  position: relative;
  box-shadow: 0 15px 45px rgba(0, 0, 0, 0.7), inset 0 0 40px rgba(212, 175, 55, 0.08);
  margin-top: 24px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.certificate-seal {
  width: 70px;
  height: 70px;
  margin: 0 auto 12px;
  border-radius: 50%;
  border: 2px solid var(--gold);
  background: radial-gradient(circle, rgba(212, 175, 55, 0.25) 0%, rgba(0,0,0,0.5) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.2rem;
  color: var(--gold-bright);
}

.certificate-title-tamil {
  font-family: 'Mukta Malar', serif;
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--gold-soft);
  letter-spacing: 1px;
}

.certificate-title-en {
  font-size: 0.9rem;
  font-weight: 700;
  color: #94a3b8;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-top: 2px;
}

.certificate-student-name {
  font-family: 'Mukta Malar', serif;
  font-size: 2rem;
  font-weight: 800;
  color: #ffffff;
  border-bottom: 2px solid rgba(212, 175, 55, 0.4);
  display: inline-block;
  padding: 6px 30px;
  margin: 18px 0;
  min-width: 280px;
}

.certificate-body-tamil {
  color: #cbd5e1;
  font-size: 1rem;
  line-height: 1.8;
  max-width: 600px;
  margin: 0 auto 16px;
}

.certificate-meta-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 20px;
  margin-top: 24px;
  font-size: 0.85rem;
  color: #94a3b8;
  flex-wrap: wrap;
  gap: 12px;
}

/* Flashcards */
.flashcards-container {
  max-width: 620px;
  margin: 24px auto;
  perspective: 1000px;
}

.flashcard-box {
  background: rgba(15, 23, 42, 0.9);
  border: 1px solid rgba(56, 189, 248, 0.3);
  border-radius: 18px;
  min-height: 240px;
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  cursor: pointer;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
  transition: all 0.3s ease;
}

.flashcard-box:hover {
  border-color: rgba(56, 189, 248, 0.6);
  transform: translateY(-2px);
}

.flashcard-badge {
  font-size: 0.75rem;
  font-weight: 700;
  color: #38bdf8;
  background: rgba(56, 189, 248, 0.1);
  border: 1px solid rgba(56, 189, 248, 0.25);
  padding: 3px 10px;
  border-radius: 12px;
  margin-bottom: 14px;
}

.flashcard-q {
  font-size: 1.25rem;
  font-weight: 700;
  color: #ffffff;
  line-height: 1.6;
}

.flashcard-a {
  font-size: 1.05rem;
  color: #2dd4bf;
  line-height: 1.7;
  margin-top: 12px;
  display: none;
}

.flashcard-flip-prompt {
  font-size: 0.8rem;
  color: #64748b;
  margin-top: 18px;
}

/* Grade LMS Tracker Inside Courseware */
.lms-chapter-complete-bar {
  background: rgba(255, 255, 255, 0.02);
  border: 1px dashed rgba(255, 255, 255, 0.18);
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 14px;
  margin: 24px 0;
}

.lms-mark-btn {
  background: rgba(56, 189, 248, 0.12);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.4);
  padding: 9px 18px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  font-family: inherit;
}

.lms-mark-btn:hover {
  background: rgba(56, 189, 248, 0.22);
  border-color: #38bdf8;
}

@media (max-width: 768px) {
  .school-hero {
    padding: 24px 18px;
  }
  .study-room-panel {
    padding: 20px 14px;
  }
  .timer-digits {
    font-size: 2.8rem;
  }
  .certificate-student-name {
    font-size: 1.4rem;
    min-width: 200px;
  }
}
"""

def append_to_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'PROFESSIONAL ONLINE SCHOOL & VEDIC-MODERN FUSION SYSTEM' not in content:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(SCHOOL_CSS)
        print(f"Appended school CSS to {path}")
    else:
        print(f"School CSS already present in {path}")

for target in ['assets/css/style.css', 'site/assets/css/style.css', 'docs/assets/css/style.css']:
    append_to_file(target)
