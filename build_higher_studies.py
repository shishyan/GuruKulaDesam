# -*- coding: utf-8 -*-
"""
Builds the Higher Studies & Vedanta Vidyapeeth Portal (higher-studies.html).
Fuses best academic content from Chinmaya Mission / CVV, Arsha Vidya Gurukulam,
Ramakrishna Mission (RKMVERI), Yoga-Vedanta Forest Academy, and Shaiva Siddhanta Pathashalas.
Synchronizes across ., site/, and docs/.
"""

import os
import shutil

HIGHER_STUDIES_HTML = """<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>வேதாந்த வித்யாபீடம் — உயர்கல்வித் தளம் (Advanced Vedanta & Indic Higher Studies) | Guru Kula Desam</title>
  <meta name="description" content="பாரதத்தின் தலைசிறந்த வேதாந்தப் பல்கலைக்கழகங்கள் மற்றும் குருகுலங்களின் பாடத்திட்டங்களை உள்ளடக்கிய உயர்கல்வித் தளம். பிரஸ்தானத்ரயம், பிரகரண கிரந்தங்கள், சைவ சித்தாந்த சாத்திரங்கள் மற்றும் பிரயோக வேதாந்தம்.">
  <link rel="stylesheet" href="assets/css/style.css">
  <style>
    .vidya-hero {
      background: linear-gradient(135deg, rgba(8, 14, 26, 0.96) 0%, rgba(15, 23, 42, 0.94) 50%, rgba(13, 31, 56, 0.96) 100%);
      border: 1px solid rgba(212, 175, 55, 0.35);
      border-radius: 20px;
      padding: 38px 32px;
      margin-bottom: 32px;
      box-shadow: 0 16px 45px rgba(0, 0, 0, 0.65), 0 0 35px rgba(212, 175, 55, 0.1);
      position: relative;
      overflow: hidden;
    }
    .vidya-hero::after {
      content: "ॐ";
      position: absolute;
      right: 20px;
      top: -20px;
      font-size: 16rem;
      color: rgba(212, 175, 55, 0.03);
      font-family: serif;
      pointer-events: none;
    }
    .vidya-track-card {
      background: rgba(15, 23, 42, 0.88);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 22px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.45);
      transition: all 0.25s ease;
    }
    .vidya-track-card:hover {
      border-color: rgba(212, 175, 55, 0.5);
      transform: translateY(-2px);
      box-shadow: 0 12px 30px rgba(0,0,0,0.6), 0 0 20px rgba(212, 175, 55, 0.1);
    }
    .vidya-track-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 14px;
      margin-bottom: 16px;
    }
    .vidya-module-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
      margin-top: 14px;
    }
    .vidya-module-box {
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-left: 3px solid var(--gold);
      border-radius: 0 10px 10px 0;
      padding: 14px 16px;
    }
    .vidya-module-box.cyan {
      border-left-color: #38bdf8;
    }
    .vidya-module-box.emerald {
      border-left-color: #2dd4bf;
    }
    .vidya-module-box.amber {
      border-left-color: #f59e0b;
    }
    .vidya-module-title {
      font-weight: 700;
      color: #ffffff;
      font-size: 0.98rem;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .vidya-module-desc {
      color: #94a3b8;
      font-size: 0.86rem;
      line-height: 1.6;
    }
    .glossary-pill {
      display: inline-block;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.12);
      color: #cbd5e1;
      padding: 4px 12px;
      border-radius: 16px;
      font-size: 0.84rem;
      margin: 4px;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .glossary-pill:hover, .glossary-pill.active {
      background: rgba(212, 175, 55, 0.2);
      border-color: var(--gold);
      color: #ffffff;
    }
    @media print {
      .left-strip-bar, .context-top-bar, .no-print, header, footer, .vidya-hero, .glossary-section, .fellowship-controls {
        display: none !important;
      }
      body { background: #ffffff !important; color: #000000 !important; }
      .certificate-preview-card {
        border: 4px double #b8860b !important;
        background: #ffffff !important;
        color: #000000 !important;
        box-shadow: none !important;
        max-width: 100% !important;
      }
    }
  </style>
</head>
<body class="has-left-strip">

  <!-- LEFT STRIP BAR (PRIMARY GLOBAL SHELL) -->
  <aside class="left-strip-bar" id="leftStripBar" aria-label="Quick Access Sidebar">
    <div class="strip-header">
      <a href="index.html" class="strip-brand-link" title="குரு குல தேசம்">
        <span class="strip-emblem">ॐ</span>
        <span class="strip-brand-text">குரு குல தேசம்</span>
      </a>
      <button type="button" class="strip-toggle-btn" id="stripToggleBtn" onclick="toggleLeftStrip()" title="விரிவுபடுத்து / சுருக்கு" aria-label="Toggle Sidebar">
        <span class="strip-toggle-icon">⇤</span>
      </button>
    </div>

    <nav class="strip-nav-list" id="stripNavList">
      <a href="index.html" class="strip-item" data-tooltip="முகப்பு">
        <span class="strip-item-icon">🏠</span>
        <span class="strip-item-label">முகப்பு</span>
      </a>
      <a href="kalvi.html" class="strip-item" data-tooltip="கல்வி நெறி">
        <span class="strip-item-icon">🎓</span>
        <span class="strip-item-label">கல்வி நெறி</span>
      </a>
      <a href="school.html" class="strip-item" data-tooltip="இணையப் பள்ளி">
        <span class="strip-item-icon">🏫</span>
        <span class="strip-item-label">இணையப் பள்ளி</span>
      </a>
      <a href="higher-studies.html" class="strip-item active" data-tooltip="உயர்கல்வி">
        <span class="strip-item-icon">🏛️</span>
        <span class="strip-item-label">உயர்கல்வி</span>
      </a>
      <a href="virtues.html" class="strip-item" data-tooltip="நற்பண்புகள்">
        <span class="strip-item-icon">🔤</span>
        <span class="strip-item-label">நற்பண்புகள்</span>
      </a>
      <a href="saiva-neri.html" class="strip-item" data-tooltip="சைவ நெறி">
        <span class="strip-item-icon">🕉️</span>
        <span class="strip-item-label">சைவ நெறி</span>
      </a>
      <a href="irai-isai-virundhu.html" class="strip-item" data-tooltip="இறை இசை">
        <span class="strip-item-icon">🎵</span>
        <span class="strip-item-label">இறை இசை</span>
      </a>
      <a href="thirukkural.html" class="strip-item" data-tooltip="திருக்குறள்">
        <span class="strip-item-icon">📖</span>
        <span class="strip-item-label">திருக்குறள்</span>
      </a>
      <a href="sanmargam.html" class="strip-item" data-tooltip="சன்மார்க்கம்">
        <span class="strip-item-icon">🪔</span>
        <span class="strip-item-label">சன்மார்க்கம்</span>
      </a>
      <a href="murugan.html" class="strip-item" data-tooltip="முருகன்">
        <span class="strip-item-icon">🔱</span>
        <span class="strip-item-label">முருகன்</span>
      </a>
      <a href="sakthi.html" class="strip-item" data-tooltip="சக்தி நெறி">
        <span class="strip-item-icon">🌸</span>
        <span class="strip-item-label">சக்தி நெறி</span>
      </a>
      <a href="vinayagar.html" class="strip-item" data-tooltip="விநாயகர்">
        <span class="strip-item-icon">🐘</span>
        <span class="strip-item-label">விநாயகர்</span>
      </a>
      <a href="vaishnava.html" class="strip-item" data-tooltip="வைணவம்">
        <span class="strip-item-icon">🪷</span>
        <span class="strip-item-label">வைணவம்</span>
      </a>
      <a href="syllabus.html" class="strip-item" data-tooltip="பாடத்திட்டம்">
        <span class="strip-item-icon">📚</span>
        <span class="strip-item-label">பாடத்திட்டம்</span>
      </a>
      <a href="about.html" class="strip-item" data-tooltip="பெரியவா">
        <span class="strip-item-icon">🏛️</span>
        <span class="strip-item-label">பெரியவா</span>
      </a>
    </nav>

    <div class="strip-footer-dock">
      <button type="button" class="strip-dock-btn" onclick="openUserSettingsModal('preferences')" title="அமைப்புகள்">
        <span class="strip-dock-icon">⚙️</span>
        <span class="strip-dock-label">அமைப்புகள்</span>
      </button>
      <button type="button" class="strip-dock-btn profile-dock-btn" onclick="openUserSettingsModal('profile')" title="சுயவிவரம்">
        <span class="strip-dock-avatar" id="stripAvatarIcon">👤</span>
        <span class="strip-dock-label" id="stripUserName">சுயவிவரம்</span>
      </button>
    </div>
  </aside>

  <div class="strip-backdrop" id="stripBackdrop" onclick="closeMobileStrip()"></div>

  <!-- CONTEXT-SENSITIVE TOP BAR -->
  <header class="context-top-bar" id="contextTopBar">
    <div class="context-bar-container">
      <button type="button" class="context-mobile-btn" onclick="toggleLeftStrip()" title="பக்கப்பட்டி">☰</button>
      <nav class="context-tabs-nav" id="contextTabsNav" aria-label="Section Tabs">
        <button type="button" class="context-tab-pill active" onclick="scrollToId('vidyaHero')"><span class="context-tab-pill-icon">🏛️</span><span>அறிமுகம் &amp; பீடம்</span></button>
        <button type="button" class="context-tab-pill" onclick="scrollToId('tracksSection')"><span class="context-tab-pill-icon">📜</span><span>5 முதன்மைத் துறைகள்</span></button>
        <button type="button" class="context-tab-pill" onclick="scrollToId('glossarySection')"><span class="context-tab-pill-icon">🔍</span><span>சாத்திர கலைச்சொற்களஞ்சியம்</span></button>
        <button type="button" class="context-tab-pill" onclick="scrollToId('fellowshipSection')"><span class="context-tab-pill-icon">🎓</span><span>உயர் பட்டயச் சான்றிதழ்</span></button>
        <a href="school.html" class="context-tab-pill" style="border-color:rgba(56,189,248,0.4); color:#38bdf8;"><span class="context-tab-pill-icon">🏫</span><span>பள்ளி போர்டல்</span></a>
      </nav>
    </div>
  </header>

  <main class="page-container" style="max-width:1300px; margin: 0 auto; padding: 24px 20px 80px;">

    <!-- 1. HERO SECTION -->
    <section class="vidya-hero" id="vidyaHero">
      <div style="max-width:880px;">
        <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(212,175,55,0.12); color:var(--gold-bright); border:1px solid rgba(212,175,55,0.35); font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; padding:5px 14px; border-radius:20px; margin-bottom:14px;">
          <span>🏛️ Higher Collegiate Indic Studies • Post-School Academy</span>
        </div>
        <h1 style="color:#ffffff; font-size:2.25rem; font-weight:800; line-height:1.2; margin-bottom:12px;">
          வேதாந்த வித்யாபீடம் — உயர்கல்வித் தளம்
        </h1>
        <p style="color:var(--gold-soft); font-size:1.15rem; font-weight:600; margin-bottom:12px;">
          The Advanced Institute of Vedanta, Shaiva Siddhanta &amp; Indic Knowledge Systems
        </p>
        <p style="color:#cbd5e1; font-size:0.98rem; line-height:1.8; margin-bottom:18px;">
          பாரதத்தின் புகழ்பெற்ற <strong>சின்மயா மிஷன் (CIF &amp; CVV), ஆர்ஷ வித்யா குருகுலம் (சுவாமி தயானந்த சரஸ்வதி), ராமகிருஷ்ண மிஷன் விவேகானந்தா பல்கலைக்கழகம் (RKMVERI), யோக-வேதாந்த வனக் கல்விக்கூடம் (ரிஷிகேஷ் - சுவாமி சிவானந்தா &amp; கிருஷ்ணானந்தா)</strong> மற்றும் <strong>காஞ்சி மெய்கண்ட சாத்திர பாடசாலைகளின்</strong> ஆழமான உயர்கல்விப் பாடத்திட்டங்களை ஒருங்கிணைத்து உருவாக்கப்பட்டுள்ள அதிநவீன தத்துவப் பெருவளாகம்.
        </p>

        <!-- Institutional Inspirations Pills -->
        <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:14px;">
          <span style="background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); color:#cbd5e1; font-size:0.78rem; padding:4px 10px; border-radius:12px;">🎓 Arsha Vidya Tradition</span>
          <span style="background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); color:#cbd5e1; font-size:0.78rem; padding:4px 10px; border-radius:12px;">🪔 Chinmaya Vishwa Vidyapeeth</span>
          <span style="background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); color:#cbd5e1; font-size:0.78rem; padding:4px 10px; border-radius:12px;">🔱 Yoga-Vedanta Forest Academy</span>
          <span style="background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); color:#cbd5e1; font-size:0.78rem; padding:4px 10px; border-radius:12px;">🌺 Ramakrishna Mission Institute</span>
          <span style="background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); color:#cbd5e1; font-size:0.78rem; padding:4px 10px; border-radius:12px;">📜 Meykanda Shastra Sampradaya</span>
        </div>
      </div>
    </section>

    <!-- 2. THE 5 ADVANCED DEGREE & FELLOWSHIP TRACKS -->
    <section id="tracksSection" style="margin: 48px 0;">
      <div style="text-align:center; max-width:850px; margin:0 auto 32px;">
        <div style="display:inline-block; font-size:0.8rem; font-weight:700; color:var(--gold); background:rgba(212,175,55,0.1); border:1px solid rgba(212,175,55,0.3); padding:4px 14px; border-radius:20px; text-transform:uppercase; margin-bottom:10px;">
          Curriculum of Collegiate Excellence
        </div>
        <h2 style="color:#ffffff; font-size:1.85rem; font-weight:800; margin-bottom:10px;">
          📜 வேதாந்த வித்யாபீடத்தின் 5 முதன்மைத் துறைகள்
        </h2>
        <p style="color:#94a3b8; font-size:0.95rem; line-height:1.7;">
          பள்ளிப் படிப்பைக் கடந்த ஆய்வாளர்கள், இளைஞர்கள் மற்றும் தீவிர ஆன்மீகச் சாதகர்களுக்காக வடிவமைக்கப்பட்ட சாஸ்திர பூர்வமான உயர்கல்வித் தடங்கள்.
        </p>
      </div>

      <!-- TRACK 1: PRASTHANATRAYA MASTERY -->
      <article class="vidya-track-card">
        <div class="vidya-track-header">
          <div>
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              <span class="wbs-code wbs-code-primary">TRACK 01</span>
              <span style="font-size:0.82rem; color:var(--gold); font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">பிரஸ்தானத்ரய ஆய்வுப் பட்டயம் (Prasthanatraya Fellowship)</span>
            </div>
            <h3 style="color:#ffffff; font-size:1.4rem; font-weight:800; margin:0;">
              பிரஸ்தானத்ரய பிரவேசம் — உபநிடதங்கள், பகவத் கீதை &amp; பிரம்ம சூத்திரம்
            </h3>
          </div>
          <span style="font-size:0.85rem; color:#38bdf8; background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.25); padding:6px 14px; border-radius:20px; font-weight:600;">
            ஆர்ஷ வித்யா &amp; சின்மயா மரபு
          </span>
        </div>

        <p style="color:#cbd5e1; font-size:0.93rem; line-height:1.75;">
          அத்வைத வேதாந்தத்தின் மூன்று அழியாத மூலத் தூண்களான ஸ்ருதி பிரஸ்தானம் (உபநிடதங்கள்), ஸ்மிருதி பிரஸ்தானம் (பகவத் கீதை) மற்றும் நியாய பிரஸ்தானம் (பிரம்ம சூத்திரம்) ஆகியவற்றை ஆதிசங்கரரின் மூல பாஷ்ய விளக்கங்களுடன் கற்கும் உச்சக்கட்ட உயர் ஆய்வு நெறி.
        </p>

        <div class="vidya-module-grid">
          <div class="vidya-module-box">
            <div class="vidya-module-title"><span>📖</span> தச உபநிடதங்கள் (10 Principal Upanishads)</div>
            <div class="vidya-module-desc">ஈசாவாஸ்யம், கேனம், கடோபநிடதம் (நசிகேதன் மரண விசாரணை), பிரச்னம், முண்டகம் (இரண்டு பறவைகள் தத்துவம்), மாண்டூக்யம் (ஓம் &amp; துரிய நிலை), தைத்திரீயம் (பஞ்ச கோசம்), ஐதரேயம், சாந்தோக்யம் (தத்வமஸி) &amp; பிருஹதாரண்யகம் (நேதி நேதி).</div>
          </div>

          <div class="vidya-module-box cyan">
            <div class="vidya-module-title"><span>🪷</span> பகவத் கீதை சாங்கர பாஷ்யம்</div>
            <div class="vidya-module-desc">அர்ஜுன விஷாத யோகம் முதல் மோக்ஷ சந்யாச யோகம் வரையிலான 18 அத்தியாயங்கள். சாங்கிய யோகம் (அத். 2), கர்ம யோகம் (அத். 3), புருஷோத்தம யோகம் (அத். 15) மற்றும் ஸ்திதப்பிரக்ஞன் லட்சணங்களின் ஆழமான உளவியல் ஆய்வு.</div>
          </div>

          <div class="vidya-module-box emerald">
            <div class="vidya-module-title"><span>⚖️</span> பிரம்ம சூத்திரம் &amp; அத்யாச பாஷ்யம்</div>
            <div class="vidya-module-desc">பாதராயணரின் சூத்திரங்கள். குறிப்பாக முதல் நான்கு சூத்திரங்களான 'சதுஸ்-சூத்ரி' (அதாத்தோ பிரம்ம ஜிக்ஞாசா, ஜன்மாத்யஸ்ய யதஃ, சாஸ்திர யோனித்வாத், தத்து சமன்வயாதாத்) மற்றும் மனிதன் மாயையில் உண்மைக்கு மாறாக அறிவதை விளக்கும் 'அத்யாச பாஷ்யம்'.</div>
          </div>
        </div>
      </article>

      <!-- TRACK 2: PRAKARANA GRANTHAS -->
      <article class="vidya-track-card">
        <div class="vidya-track-header">
          <div>
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              <span class="wbs-code wbs-code-primary">TRACK 02</span>
              <span style="font-size:0.82rem; color:var(--gold); font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">பிரகரண கிரந்தப் பட்டயம் (Classical Prakarana Granthas)</span>
            </div>
            <h3 style="color:#ffffff; font-size:1.4rem; font-weight:800; margin:0;">
              அடிப்படைக் கோட்பாடுகள் முதல் விவேகசூடாமணி &amp; பஞ்சதசி வரை
            </h3>
          </div>
          <span style="font-size:0.85rem; color:#2dd4bf; background:rgba(45,212,191,0.1); border:1px solid rgba(45,212,191,0.25); padding:6px 14px; border-radius:20px; font-weight:600;">
            CIF Foundation &amp; Advanced Course
          </span>
        </div>

        <p style="color:#cbd5e1; font-size:0.93rem; line-height:1.75;">
          நேரடியாக உபநிடதங்களுக்குள் நுழையும் முன், வேதாந்த கலைச்சொற்கள், மனித உடலின் 3 சரீரங்கள், 3 அவஸ்தைகள், பஞ்ச கோசங்கள் மற்றும் பகுத்தறியும் விவேகத்தைப் பயிற்றுவிக்கும் அடிப்படை மற்றும் இடைநிலை நூல்களின் தொகுப்பு.
        </p>

        <div class="vidya-module-grid">
          <div class="vidya-module-box">
            <div class="vidya-module-title"><span>📜</span> தத்வ போதம் (Tattva Bodha)</div>
            <div class="vidya-module-desc">ஆதிசங்கரரின் பாலபாட நூல். அதிகாரி லக்ஷணம் (விவேகம், வைராக்கியம், சம-தமாதி ஷட்க சம்பத்து, முமுக்ஷுத்துவம்), ஸ்தூல, சூக்ஷ்ம, காரண சரீரப் பகுப்பாய்வு, ஜாக்கிரத், ஸ்வப்ன, சுஷுப்தி அவஸ்தா த்ரய விவேகம்.</div>
          </div>

          <div class="vidya-module-box cyan">
            <div class="vidya-module-title"><span>💎</span> விவேகசூடாமணி (Vivekachudamani)</div>
            <div class="vidya-module-desc">580 சுலோகங்கள் கொண்ட அத்வைத கிரீட ரத்தினம். மாயையின் விக்ஷேப, ஆவரண சக்திகள், மனிதனின் அனான்ம அடையாளங்களை அறுத்தெறியும் 'நேதி நேதி' வழிமுறை மற்றும் பிரம்ம நிர்வாணத்தின் ஆனந்த அனுபவம்.</div>
          </div>

          <div class="vidya-module-box amber">
            <div class="vidya-module-title"><span>🕯️</span> பஞ்சதசி &amp; ஆத்ம போதம் (Panchadasi &amp; Atmabodha)</div>
            <div class="vidya-module-desc">வித்யாரண்ய சுவாமிகளின் 'பஞ்சதசி' — விவேக தீபம், நாடக தீபம், தியான தீபம் மற்றும் பிரம்மானந்தத்தின் 15 அத்தியாய பகுப்பாய்வு. ஆத்ம போதத்தின் 68 எளிய உவமை விளக்கங்கள்.</div>
          </div>

          <div class="vidya-module-box emerald">
            <div class="vidya-module-title"><span>🌿</span> உபதேச சாரம் (Upadesha Sara)</div>
            <div class="vidya-module-desc">பகவான் ரமண மகரிஷி அருளிய 30 சுலோகங்கள். கர்மம், பக்தி, யோகப் பிராணாயாமம் ஆகியவற்றைத் தாண்டி 'நான் யார்?' என்ற நேரடி ஆன்ம விசாரத்தின் உன்னதப் படிநிலைகள்.</div>
          </div>
        </div>
      </article>

      <!-- TRACK 3: ADVANCED SHAIVA SIDDHANTA -->
      <article class="vidya-track-card">
        <div class="vidya-track-header">
          <div>
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              <span class="wbs-code wbs-code-primary">TRACK 03</span>
              <span style="font-size:0.82rem; color:var(--gold); font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">சைவ சித்தாந்த உயர் சாத்திரங்கள் (Shaiva Siddhanta Shastras)</span>
            </div>
            <h3 style="color:#ffffff; font-size:1.4rem; font-weight:800; margin:0;">
              மெய்கண்ட சாத்திரங்கள் 14 &amp; சிவாக்கிர பாஷ்ய தத்துவ இயல்
            </h3>
          </div>
          <span style="font-size:0.85rem; color:var(--gold); background:rgba(212,175,55,0.1); border:1px solid rgba(212,175,55,0.3); padding:6px 14px; border-radius:20px; font-weight:600;">
            தமிழ் மெய்யியல் உச்சக்கட்டம்
          </span>
        </div>

        <p style="color:#cbd5e1; font-size:0.93rem; line-height:1.75;">
          தென்தமிழகத்தின் 14 மெய்கண்ட சாத்திரங்களின் ஆழமான தர்க்கவியல் பார்வை. பதி-பசு-பாச முப்பொருள் உண்மை, ஆணவ மலத்தின் இருப்பு, வினைக் கொள்கை, சத்தினிபாதம் மற்றும் சிவானந்தப் பேறு பற்றிய முழுமையான சாத்திர ஆய்வு.
        </p>

        <div class="vidya-module-grid">
          <div class="vidya-module-box">
            <div class="vidya-module-title"><span>🔱</span> சிவஞானபோதம் &amp; மாபாடியம்</div>
            <div class="vidya-module-desc">மெய்கண்ட தேவநாயனாரின் 12 சூத்திரங்கள். மாதவச் சிவஞான யோகிகள் அருளிய உலகப் புகழ் பெற்ற 'திராவிட மகாபாஷ்யம்'. பிரமாண இயல், இலக்கண இயல், சாதன இயல், பயன் இயல் ஆகிய நான்கு பிரிவுகள்.</div>
          </div>

          <div class="vidya-module-box cyan">
            <div class="vidya-module-title"><span>🛡️</span> சிவஞான சித்தியார் (Siddhiyar)</div>
            <div class="vidya-module-desc">அருணந்தி சிவாச்சாரியாரின் பெருநூல். உலகாயதம், பௌத்தம், ஜைனம், மாயாவாதம் போன்ற பிற தத்துவங்களின் வாதங்களை மறுக்கும் 'பரபக்கம்' மற்றும் சித்தாந்தத்தை நிறுவும் 'சுபக்கம்'.</div>
          </div>

          <div class="vidya-module-box emerald">
            <div class="vidya-module-title"><span>✨</span> திருவருட்பயன் &amp; உண்மை விளக்கம்</div>
            <div class="vidya-module-desc">கொற்றவன்குடி உமாபதி சிவாச்சாரியாரின் குறள் வெண்பாக்கள். பதிமுதுநிலை, உயிர்க்குயிராதல், பாசமறுத்தல் மற்றும் மனவாசகங்கடந்தாரின் உண்மை விளக்கக் கேனோபநிடத ஒப்புமை.</div>
          </div>

          <div class="vidya-module-box amber">
            <div class="vidya-module-title"><span>🏛️</span> 28 ஆகம கிரியா தத்துவம் (Agamic Tantra)</div>
            <div class="vidya-module-desc">காமிகம், காரணம் முதலான 28 சிவ ஆகமங்கள். சரியை, கிரியை, யோகம், ஞானம் ஆகிய பாதங்கள். ஆலயம் நிர்மாணித்தல், மூர்த்திப் பிரதிஷ்டை மற்றும் மந்திர உபாசனா இரகசியங்கள்.</div>
          </div>
        </div>
      </article>

      <!-- TRACK 4: SHAD-DARSHANAS & COMPARATIVE EPISTEMOLOGY -->
      <article class="vidya-track-card">
        <div class="vidya-track-header">
          <div>
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              <span class="wbs-code wbs-code-primary">TRACK 04</span>
              <span style="font-size:0.82rem; color:var(--gold); font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">பாரத தர்சன தர்க்கவியல் &amp; மேலைநாட்டு மெய்யியல்</span>
            </div>
            <h3 style="color:#ffffff; font-size:1.4rem; font-weight:800; margin:0;">
              ஷட்தர்சனங்கள், அளவையியல் &amp; உலக மெய்யியல் ஒப்பாய்வு
            </h3>
          </div>
          <span style="font-size:0.85rem; color:#38bdf8; background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.25); padding:6px 14px; border-radius:20px; font-weight:600;">
            Forest Academy &amp; University Rigor
          </span>
        </div>

        <p style="color:#cbd5e1; font-size:0.93rem; line-height:1.75;">
          நியாய, வைசேஷிக, சாங்கிய, யோக, மீமாம்ச, வேதாந்த தத்துவங்களின் அளவையியல் (Epistemology). மேலும் இம்மானுவேல் காண்ட், ஸ்பினோஸா, ஷோபன்ஹாவர் போன்ற மேலைநாட்டு சிந்தனையாளர்களோடு வேதாந்தத்தை ஒப்பிடும் அறிவார்ந்த பகுப்பாய்வு.
        </p>

        <div class="vidya-module-grid">
          <div class="vidya-module-box">
            <div class="vidya-module-title"><span>⚖️</span> நியாய-வைசேஷிக பிரமாண சாஸ்திரம்</div>
            <div class="vidya-module-desc">அட்சபாத கௌதமரின் தர்க்க நியாயங்கள். பிரத்யக்ஷம் (நேரடிக் காட்சி), அனுமானம் (ஊகம் - வியாப்தி, ஹேது), உபமானம் (ஒப்பீடு), சப்தம் (வேத வாக்கு). அன்னம்பட்டரின் 'தர்க்க சங்கிரஹம்'.</div>
          </div>

          <div class="vidya-module-box cyan">
            <div class="vidya-module-title"><span>🧘</span> சாங்கிய-யோக உளவியல்</div>
            <div class="vidya-module-desc">கபிலரின் சாங்கிய காரிகைகள் — 25 தத்துவங்கள். பிரகிருதி-புருஷ விவேகம். பதஞ்சலி மகரிஷியின் யோக சூத்திரங்கள் (சமாதி பாதம், சாதன பாதம், விபூதி பாதம், கைவல்ய பாதம்).</div>
          </div>

          <div class="vidya-module-box emerald">
            <div class="vidya-module-title"><span>🌍</span> மேலைநாட்டு மெய்யியல் ஒப்பாய்வு</div>
            <div class="vidya-module-desc">பிளேட்டோவின் 'Cave Allegory' vs. மாயை. காண்ட்டின் 'Thing-in-itself' (Noumenon) vs. பிரம்மம். ஸ்பினோஸாவின் Pantheism vs. அத்வைதம். ஷோபன்ஹாவரின் உபநிடதப் புகழுரைகள்.</div>
          </div>
        </div>
      </article>

      <!-- TRACK 5: APPLIED VEDANTA & CONSCIOUSNESS STUDIES -->
      <article class="vidya-track-card">
        <div class="vidya-track-header">
          <div>
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              <span class="wbs-code wbs-code-primary">TRACK 05</span>
              <span style="font-size:0.82rem; color:var(--gold); font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">பிரயோக வேதாந்தமும் உணர்வுநிலை ஆய்வுகளும்</span>
            </div>
            <h3 style="color:#ffffff; font-size:1.4rem; font-weight:800; margin:0;">
              சுவாமி விவேகானந்தரின் பிரயோக வேதாந்தம் &amp; குவாண்டம் அறிவாற்றல்
            </h3>
          </div>
          <span style="font-size:0.85rem; color:#2dd4bf; background:rgba(45,212,191,0.1); border:1px solid rgba(45,212,191,0.25); padding:6px 14px; border-radius:20px; font-weight:600;">
            RKMVERI &amp; Modern Indic Science
          </span>
        </div>

        <p style="color:#cbd5e1; font-size:0.93rem; line-height:1.75;">
          வேதாந்தத்தை காடுகளிலிருந்தும் மடாலயங்களிலிருந்தும் அன்றாட மனித வாழ்வின் உழைப்புக் களத்திற்கும், நவீன அறிவியல் ஆய்வுகூடங்களுக்கும் கொண்டுவந்த சுவாமி விவேகானந்தரின் பிரயோக வேதாந்தம் (Practical Vedanta).
        </p>

        <div class="vidya-module-grid">
          <div class="vidya-module-box">
            <div class="vidya-module-title"><span>⚡</span> விவேகானந்தரின் பிரயோக வேதாந்தம்</div>
            <div class="vidya-module-desc">மனிதனை உருவாக்கும் கல்வி (Man-Making Education), 'ஏழையின் கண்ணீரைத் துடைப்பதே உண்மையான சிவபூஜை' (சிவஞானத்தில் ஜீவகாருண்யம்), மற்றும் அச்சமின்மை (Abhaya).</div>
          </div>

          <div class="vidya-module-box cyan">
            <div class="vidya-module-title"><span>⚛️</span> குவாண்டம் இயற்பியலும் அத்வைதமும்</div>
            <div class="vidya-module-desc">எர்வின் ஷ்ரோடிங்கர் (Erwin Schrödinger), வெர்னர் ஹைசன்பர்க் (Werner Heisenberg) மற்றும் நீல்ஸ் போர் (Niels Bohr) ஆகியோரின் குவாண்டம் சிந்தனைகளுக்கும் உபநிடதங்களுக்குமான நேரடித் தொடர்புகள்.</div>
          </div>

          <div class="vidya-module-box emerald">
            <div class="vidya-module-title"><span>🧠</span> அறிவாற்றல் மறுவடிவமைப்பும் மன நலமும்</div>
            <div class="vidya-module-desc">நவீன CBT (Cognitive Behavioral Therapy) மற்றும் Acceptance &amp; Commitment Therapy முறைகளை விட வலிமையான விவேக-வைராக்கிய மனப்பயிற்சி. மன அழுத்தம், பர்ன்-அவுட் தவிர்த்து ஆன்ம பலத்துடன் சாதனை படைத்தல்.</div>
          </div>
        </div>
      </article>

    </section>

    <!-- 3. PRAKARANA GRANTHAS & SHASTRA GLOSSARY -->
    <section class="glossary-section" id="glossarySection" style="margin: 56px 0; background:rgba(15,23,42,0.85); border:1px solid rgba(212,175,55,0.25); border-radius:18px; padding:32px;">
      <div style="text-align:center; max-width:800px; margin:0 auto 24px;">
        <div style="font-size:0.8rem; font-weight:700; color:var(--gold); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">
          Epistemic Terminology Engine
        </div>
        <h2 style="color:#ffffff; font-size:1.6rem; font-weight:800; margin-bottom:8px;">
          🔍 வேதாந்த-சித்தாந்த சாத்திரக் கலைச்சொற்களஞ்சியம்
        </h2>
        <p style="color:#94a3b8; font-size:0.92rem;">
          உயர்கல்விப் பாடங்களைப் பயில்வதற்கு அவசியமான முதன்மை சாத்திரக் கலைச்சொற்களைச் சொடுக்கி அவற்றின் துல்லியமான விளக்கத்தைக் காண்க.
        </p>
      </div>

      <!-- Keyword Pills -->
      <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:6px; margin-bottom:20px;">
        <button type="button" class="glossary-pill active" onclick="showGlossaryTerm('adhikari')">அதிகாரி லக்ஷணம்</button>
        <button type="button" class="glossary-pill" onclick="showGlossaryTerm('viveka')">நித்தியாநித்திய விவேகம்</button>
        <button type="button" class="glossary-pill" onclick="showGlossaryTerm('vairagya')">வைராக்கியம்</button>
        <button type="button" class="glossary-pill" onclick="showGlossaryTerm('shatsampat')">சம-தமாதி ஷட்க சம்பத்து</button>
        <button type="button" class="glossary-pill" onclick="showGlossaryTerm('mumukshutva')">முமுக்ஷுத்துவம்</button>
        <button type="button" class="glossary-pill" onclick="showGlossaryTerm('adhyasa')">அத்யாசம் (Superimposition)</button>
        <button type="button" class="glossary-pill" onclick="showGlossaryTerm('vivarta')">விவர்த்த வாதம்</button>
        <button type="button" class="glossary-pill" onclick="showGlossaryTerm('maya')">மாயை &amp; மித்யை</button>
        <button type="button" class="glossary-pill" onclick="showGlossaryTerm('anavam')">ஆணவ மலம்</button>
        <button type="button" class="glossary-pill" onclick="showGlossaryTerm('satchitananda')">சச்சிதானந்தம்</button>
      </div>

      <!-- Detail Box -->
      <div id="glossaryDisplayBox" style="background:rgba(0,0,0,0.4); border:1px solid rgba(212,175,55,0.3); border-radius:12px; padding:22px; max-width:850px; margin:0 auto;">
        <h4 id="glossaryTitle" style="color:var(--gold-bright); font-size:1.2rem; margin-bottom:10px;">அதிகாரி லக்ஷணம் (Qualifications of a Seeker)</h4>
        <div id="glossaryDesc" style="color:#cbd5e1; font-size:0.95rem; line-height:1.75;">
          வேதாந்த சாத்திரங்களைக் கற்றுணர்வதற்கு மாணவரிடம் இருக்க வேண்டிய நான்கு பிரதான தகுதிகள்: 1. விவேகம் (நித்தியமானது எது, அநித்தியமானது எது எனப் பிரித்தறியும் அறிவு), 2. வைராக்கியம் (அநித்தியமான உலகப் பொருட்களின் மீதான பற்றின்மை), 3. சம-தமாதிகள் (மனக்கட்டுப்பாடு, புலனடக்கம் உள்ளிட்ட 6 நற்பண்புகள்), 4. முமுக்ஷுத்துவம் (விடுதலை பெற வேண்டும் என்ற தீவிர வேட்கை).
        </div>
      </div>
    </section>

    <!-- 4. VIDYAPEETH FELLOWSHIP CERTIFICATE GENERATOR -->
    <section id="fellowshipSection" style="margin: 56px 0;">
      <div style="text-align:center; max-width:800px; margin:0 auto 24px;">
        <div style="display:inline-block; font-size:0.8rem; font-weight:700; color:var(--gold); background:rgba(212,175,55,0.1); border:1px solid rgba(212,175,55,0.3); padding:4px 14px; border-radius:20px; text-transform:uppercase; margin-bottom:10px;">
          Collegiate Academic Fellowship
        </div>
        <h2 style="color:#ffffff; font-size:1.85rem; font-weight:800; margin-bottom:10px;">
          🎓 வேதாந்த வித்யாபீடப் பட்டயச் சான்றிதழ் இயற்றி
        </h2>
        <p style="color:#cbd5e1; font-size:0.95rem; line-height:1.7;">
          உயர்கல்வித் தடங்களை ஆய்வு செய்த மாணவர்களும் அறிஞர்களும் தங்களின் அதிகாரப்பூர்வ வித்யாபீட ஆய்வுப் பட்டயச் சான்றிதழைப் பெற்று அச்சிடலாம்.
        </p>
      </div>

      <div class="no-print" style="background:rgba(15,23,42,0.85); border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:18px 24px; max-width:800px; margin:0 auto 24px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
        <div>
          <label style="font-size:0.8rem; color:#94a3b8; display:block; margin-bottom:4px;">தேர்ந்தெடுக்கப்பட்ட ஆய்வுத் துறை (Specialization Track):</label>
          <select id="fellowshipTrackSelect" onchange="updateFellowshipPreview()" style="background:#0b111e; border:1px solid var(--gold); color:#ffffff; padding:7px 12px; border-radius:6px; font-family:inherit;">
            <option value="பிரஸ்தானத்ரய ஆய்வுப் பட்டயம் (Prasthanatraya Fellowship)">துறை 1: பிரஸ்தானத்ரய பிரவேசம் (உபநிடதங்கள், கீதை, பிரம்ம சூத்திரம்)</option>
            <option value="வேதாந்தப் பிரகரண கிரந்த சான்றிதழ் (Prakarana Granthas)">துறை 2: தத்வ போதம், விவேகசூடாமணி, பஞ்சதசி &amp; ரமண உபதேசம்</option>
            <option value="சைவ சித்தாந்த மெய்கண்ட சாத்திரப் பட்டயம் (Meykanda Shastras)">துறை 3: சிவஞானபோதம், சிவஞான சித்தியார் &amp; ஆகம கிரியைகள்</option>
            <option value="பாரத தர்சன தர்க்கவியல் சான்றிதழ் (Comparative Epistemology)">துறை 4: ஷட்தர்சனங்கள், நியாய தர்க்கம் &amp; மேலைநாட்டு மெய்யியல்</option>
            <option value="பிரயோக வேதாந்த ஆய்வாளர் பட்டயம் (Applied Vedanta &amp; Science)">துறை 5: விவேகானந்தர் பிரயோக வேதாந்தம் &amp; குவாண்டம் அறிவியல்</option>
          </select>
        </div>

        <button type="button" onclick="window.print()" class="sheet-btn sheet-btn-view" style="padding:10px 22px; font-weight:700; display:inline-flex; align-items:center; gap:8px;">
          <span>🖨️ பட்டயத்தை அச்சிடுக / PDF</span>
        </button>
      </div>

      <!-- Live Certificate Frame -->
      <div class="certificate-preview-card" id="fellowshipFrame">
        <div class="certificate-seal">ॐ</div>
        <div class="certificate-title-tamil">குரு குல தேசம் — வேதாந்த வித்யாபீடம்</div>
        <div class="certificate-title-en">INSTITUTE OF ADVANCED VEDANTA &amp; INDIC SHASTRA STUDIES</div>
        
        <div style="font-size:0.85rem; color:#94a3b8; margin-top:14px; text-transform:uppercase; letter-spacing:2px;">
          உயர் ஆய்வாளர் பட்டயம் • POST-GRADUATE ACADEMIC FELLOWSHIP
        </div>

        <div style="margin-top:20px; color:#cbd5e1; font-size:1.05rem;">
          இச்சான்றொப்பம் தகுதியுடைய ஆய்வுச் சாதகருக்கு வழங்கப்படுகிறது:
        </div>

        <div class="certificate-student-name" id="fellowshipStudentNameDisplay">
          செல்வன் / செல்வி ஆய்வாளர்
        </div>

        <div class="certificate-body-tamil" id="fellowshipBodyDisplay">
          மேற்குறிப்பிட்ட மாணவர் குரு குல தேச வேதாந்த வித்யாபீடத்தின் <strong>பிரஸ்தானத்ரய ஆய்வுப் பட்டயம் (Prasthanatraya Fellowship)</strong> உயர்நிலைத் தத்துவப் பாடநெறிகள், மூல சாத்திர பாஷ்யங்கள், தர்க்க விவாதங்கள் மற்றும் பிரயோக வேதாந்த வாழ்வியல் ஆய்வுகளை மிகச் சிறந்த முறையில் நிறைவு செய்து இப்பேறுபெற்ற பட்டயத்தை எய்துகிறார் எனச் சான்றளிக்கப்படுகிறது.
        </div>

        <div class="certificate-meta-row">
          <div style="text-align:left;">
            <div>சான்றிதழ் பதிவு எண்: <strong style="color:#ffffff;" id="fellowshipUidDisplay">GKD-VIDYA-2026-9901</strong></div>
            <div>வழங்கப்பட்ட நாள்: <span id="fellowshipDateDisplay">07-10-2026</span></div>
          </div>
          <div style="text-align:center;">
            <div style="font-size:1.4rem; color:var(--gold);">🏛️</div>
            <div style="font-size:0.75rem; color:#cbd5e1; letter-spacing:1px;">வித்யாபீடப் பேரவை முத்திரை</div>
          </div>
          <div style="text-align:right;">
            <div style="border-bottom:1px solid rgba(255,255,255,0.3); padding-bottom:4px; min-width:140px; font-weight:700; color:#ffffff;">குலபதி &amp; ஆச்சார்ய சபை</div>
            <div style="font-size:0.75rem; color:#94a3b8; margin-top:2px;">Dean of Shastra Studies</div>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- JAVASCRIPT LOGIC -->
  <script>
    function scrollToId(id) {
      var el = document.getElementById(id);
      if (el) {
        var top = el.getBoundingClientRect().top + window.pageYOffset - 90;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    }

    function toggleLeftStrip() {
      var bar = document.getElementById('leftStripBar');
      var backdrop = document.getElementById('stripBackdrop');
      if (bar) bar.classList.toggle('open');
      if (backdrop) backdrop.classList.toggle('active');
    }

    function closeMobileStrip() {
      var bar = document.getElementById('leftStripBar');
      var backdrop = document.getElementById('stripBackdrop');
      if (bar) bar.classList.remove('open');
      if (backdrop) backdrop.classList.remove('active');
    }

    // Glossary dictionary
    var glossary = {
      adhikari: {
        title: "அதிகாரி லக்ஷணம் (Qualifications of a Seeker)",
        desc: "வேதாந்த சாத்திரங்களைக் கற்றுணர்வதற்கு மாணவரிடம் இருக்க வேண்டிய நான்கு பிரதான தகுதிகள்: 1. விவேகம், 2. வைராக்கியம், 3. சம-தமாதிகள் (6 நற்பண்புகள்), 4. முமுக்ஷுத்துவம் (தீவிர விடுதலை வேட்கை)."
      },
      viveka: {
        title: "நித்தியாநித்திய வஸ்து விவேகம் (Discrimination of Real vs Transient)",
        desc: "எப்போதும் அழியாமல் நிலையானதாக இருக்கும் சச்சிதானந்த பரம்பொருள் மட்டுமே 'நித்தியம்' என்றும், தோன்றி மறையும் உலகம் மற்றும் உடலின் இன்ப துன்பங்கள் யாவும் 'அநித்தியம்' என்றும் பகுத்தறியும் விவேக அறிவு."
      },
      vairagya: {
        title: "இக-அமுத்ர பலபோக விராகம் / வைராக்கியம் (Dispassion & Freedom from Craving)",
        desc: "இவ்வுலகிலும் மேலுலகிலும் உள்ள நிலையற்ற சுகபோகங்கள் மீதான பற்றின்மை; உள்ளத்தில் தோன்றும் ஆசைகளை விடுத்து தர்மத்திலும் ஞானத்திலும் மனம் உறுதியுடன் நிற்றல்."
      },
      shatsampat: {
        title: "சம-தமாதி ஷட்க சம்பத்து (The Six Inner Wealths)",
        desc: "1. சமம் (மனக்கட்டுப்பாடு), 2. தமம் (ஐம்புலன் கட்டுப்பாடு), 3. உபரதி (தேவையற்ற விவகாரங்களிலிருந்து விலகுதல்), 4. திதிக்ஷை (இன்ப துன்பங்களை சமமாகத் தாங்கும் பொறுமை), 5. சிரத்தை (சாஸ்திரத்திலும் குருவிலும் தளராத நம்பிக்கை), 6. சமாதானம் (இலக்கில் மனதை ஒருமுகப்படுத்துதல்)."
      },
      mumukshutva: {
        title: "முமுக்ஷுத்துவம் (Intense Yearning for Liberation)",
        desc: "பிறவிப் பெருங்கடலிலிருந்தும் அறியாமைத் தளைகளிலிருந்தும் எப்போது விடுதலை அடைவோம் என்ற தாகம். நெருப்புப் பற்றிய அறையிலிருந்து வெளியேறத் துடிக்கும் ஒருவனின் வேகத்தைப் போன்ற தீவிர வேட்கை."
      },
      adhyasa: {
        title: "அத்யாசம் (Superimposition)",
        desc: "ஒன்றின் மீது மற்றொன்றை ஏற்றி அறிதல். எ.கா: இருட்டில் கிடக்கும் கயிற்றை பாம்பு என அஞ்சுதல் போல, நித்தியமான ஆன்மாவின் மீது அழியக்கூடிய உடல், மனம், அகந்தையை ஏற்றி 'நான் அழியக்கூடியவன்' என மயங்குவதே அத்யாசம்."
      },
      vivarta: {
        title: "விவர்த்த வாதம் (Apparent Transformation vs Modification)",
        desc: "பால் தயிராக மாறுவது பரிணாமம் (மீளாத மாற்றம்). ஆனால் கயிறு பாம்பாகத் தெரிவது விவர்த்தம் (பொருள் மாறாமல் தோற்றத்தால் மட்டுமே மாறுவது போலத் தோன்றுதல்). பிரம்மம் மாறாமல் உலகமாகத் தோன்றுவது விவர்த்த வாதமாகும்."
      },
      maya: {
        title: "மாயை & மித்யை (The Cosmic Principle of Appearance)",
        desc: "மாயை என்பது சத் (உண்மை) என்றும் கூற முடியாத, அசத் (முற்றிலும் பொய்) என்றும் கூற முடியாத 'அநிர்வசனீயம்'. மித்யை என்பது ஆதாரமில்லாமல் தனித்து இயங்க முடியாத சார்பு நிலை (Dependent Reality)."
      },
      anavam: {
        title: "ஆணவ மலம் (The Innate Impurity in Shaiva Siddhanta)",
        desc: "சைவ சித்தாந்தத்தில் ஆன்மாவின் மூலப் பேரறிவை மறைத்து 'நான்', 'எனது' என்ற அகந்தையை உண்டாக்கும் மூல இருள் மலமாகும். இறைவனின் திருவருளாலேயே இது நீங்கும்."
      },
      satchitananda: {
        title: "சச்சிதானந்தம் (Existence-Consciousness-Bliss)",
        desc: "சத் (எக்காலத்திலும் அழியாத இருப்பு), சித் (தன்னைத் தானே ஒளிரச் செய்து பிறவற்றை அறியும் தூய உணர்வுநிலை), ஆனந்தம் (எல்லையற்ற பேரமைதி). இதுவே பரம்பொருளின் மற்றும் மனிதனின் மெய்யியற்கை."
      }
    };

    function showGlossaryTerm(key) {
      document.querySelectorAll('.glossary-pill').forEach(function(p) { p.classList.remove('active'); });
      event.target.classList.add('active');
      var item = glossary[key];
      if (item) {
        document.getElementById('glossaryTitle').textContent = item.title;
        document.getElementById('glossaryDesc').textContent = item.desc;
      }
    }

    function updateFellowshipPreview() {
      var track = document.getElementById('fellowshipTrackSelect').value;
      var bodyEl = document.getElementById('fellowshipBodyDisplay');
      if (bodyEl) {
        bodyEl.innerHTML = 'மேற்குறிப்பிட்ட மாணவர் குரு குல தேச வேதாந்த வித்யாபீடத்தின் <strong>' + track + '</strong> உயர்நிலைத் தத்துவப் பாடநெறிகள், மூல சாத்திர பாஷ்யங்கள், தர்க்க விவாதங்கள் மற்றும் பிரயோக வேதாந்த வாழ்வியல் ஆய்வுகளை மிகச் சிறந்த முறையில் நிறைவு செய்து இப்பேறுபெற்ற பட்டயத்தை எய்துகிறார் எனச் சான்றளிக்கப்படுகிறது.';
      }
    }

    document.addEventListener('DOMContentLoaded', function() {
      var savedName = localStorage.getItem('gkd_student_name') || 'செல்வன் / செல்வி ஆய்வாளர்';
      var nameEl = document.getElementById('fellowshipStudentNameDisplay');
      if (nameEl) nameEl.textContent = savedName;
      updateFellowshipPreview();
    });
  </script>
</body>
</html>
"""

def main():
    targets = ['higher-studies.html', 'site/higher-studies.html', 'docs/higher-studies.html']
    for t in targets:
        os.makedirs(os.path.dirname(t) if os.path.dirname(t) else '.', exist_ok=True)
        with open(t, 'w', encoding='utf-8') as f:
            f.write(HIGHER_STUDIES_HTML)
        print(f"Created {t}")

if __name__ == '__main__':
    main()
