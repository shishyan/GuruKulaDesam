# -*- coding: utf-8 -*-
"""
Builder for Gurukuladesam 'Who We Are' (யார் நாம்?) interactive page.
Generates who-we-are.html and mirrors it to docs/ and site/.
"""
import os
import json
import shutil

ROOT_DIR = r"C:\GitHub\Gurukuladesam"
DATA_FILE = os.path.join(ROOT_DIR, "data", "genealogy_puranic_research.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    purana_data = json.load(f)

print(f"Loaded puranic research data with keys: {list(purana_data.keys())}")

# Convert data into embedded JSON strings for the client explorer
data_json_str = json.dumps(purana_data, ensure_ascii=False)

html_content = '''<!DOCTYPE html>
<html lang="ta">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>யார் நாம்? (Who We Are?) — பிரம்மன் முதல் மனுக்கள், சூரிய-சந்திர குல அரச பரம்பரை | Guru Kula Desam</title>
  <meta name="description" content="யார் நாம்? சனாதன பிரபஞ்ச தோற்றம், பிரம்மன், பிரஜாபதிகள், 14 மனுக்கள், வைவஸ்வத மனுவின் சூரிய-சந்திர குல அரச பரம்பரை, சோழர்-பாண்டியர் மரபு மற்றும் 12 புராண ஒப்பீட்டு வம்சாவளி வரைபடம்.">
  <link rel="stylesheet" href="assets/css/style.css">
  <style>
    /* AUTHORITATIVE OVERRIDES FOR LEFT STRIP BAR IN WARM RED-ORANGE GRADIENT */
    .left-strip-bar {
      position: fixed !important;
      top: 0 !important;
      bottom: 0 !important;
      left: 0 !important;
      width: var(--strip-collapsed-width, 68px) !important;
      background: linear-gradient(180deg, #7f1d1d 0%, #dc2626 35%, #ea580c 70%, #c2410c 100%) !important;
      backdrop-filter: blur(20px) !important;
      -webkit-backdrop-filter: blur(20px) !important;
      border-right: 1.5px solid rgba(251, 146, 60, 0.45) !important;
      z-index: 1200 !important;
      box-shadow: 4px 0 24px rgba(234, 88, 12, 0.35), 2px 0 16px rgba(0, 0, 0, 0.55) !important;
    }
    .left-strip-bar.expanded,
    .left-strip-bar.open,
    body.primary-menu-open .left-strip-bar {
      width: var(--strip-expanded-width, 290px) !important;
      background: linear-gradient(180deg, #450a0a 0%, #991b1b 30%, #ea580c 70%, #7c2d12 100%) !important;
      border-right: 1.5px solid rgba(251, 146, 60, 0.60) !important;
      box-shadow: 10px 0 50px rgba(0, 0, 0, 0.85), 0 0 35px rgba(234, 88, 12, 0.35) !important;
    }

    /* WHO WE ARE STYLING & COSMIC DASHBOARD */
    :root {
      --gold-royal: #fbbf24;
      --gold-light: #fef08a;
      --orange-accent: #f97316;
      --crimson-accent: #e11d48;
      --solar-amber: #f59e0b;
      --lunar-silver: #93c5fd;
      --rishi-emerald: #10b981;
      --dark-card-bg: rgba(15, 23, 42, 0.88);
      --dark-border: rgba(251, 146, 60, 0.28);
    }

    .who-hero {
      position: relative;
      background: linear-gradient(135deg, rgba(30, 10, 5, 0.92) 0%, rgba(15, 23, 42, 0.95) 50%, rgba(20, 10, 30, 0.92) 100%);
      border: 1.5px solid rgba(249, 115, 22, 0.45);
      border-radius: 24px;
      padding: 42px 36px;
      margin-bottom: 32px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), inset 0 0 40px rgba(249, 115, 22, 0.12);
      overflow: hidden;
    }
    .who-hero::before {
      content: "";
      position: absolute;
      top: -50%;
      right: -20%;
      width: 500px;
      height: 500px;
      background: radial-gradient(circle, rgba(249, 115, 22, 0.18) 0%, transparent 70%);
      pointer-events: none;
      z-index: 0;
    }
    .who-hero-content {
      position: relative;
      z-index: 1;
    }
    .hero-badge-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
      margin-bottom: 16px;
    }
    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 14px;
      border-radius: 999px;
      font-size: 0.82rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }
    .badge-solar {
      background: rgba(245, 158, 11, 0.18);
      border: 1px solid rgba(245, 158, 11, 0.45);
      color: #fde047;
    }
    .badge-lunar {
      background: rgba(147, 197, 253, 0.18);
      border: 1px solid rgba(147, 197, 253, 0.45);
      color: #bfdbfe;
    }
    .badge-rishi {
      background: rgba(16, 185, 129, 0.18);
      border: 1px solid rgba(16, 185, 129, 0.45);
      color: #6ee7b7;
    }
    .who-hero-title {
      font-size: 2.6rem;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.2;
      margin-bottom: 12px;
      text-shadow: 0 4px 15px rgba(0, 0, 0, 0.6);
    }
    .who-hero-title span {
      background: linear-gradient(90deg, #fdba74, #f59e0b, #f43f5e);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .who-hero-subtitle {
      font-size: 1.15rem;
      color: #cbd5e1;
      max-width: 900px;
      line-height: 1.7;
      margin-bottom: 24px;
    }
    .who-quick-nav {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      padding-top: 14px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    .who-jump-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #f1f5f9;
      padding: 8px 16px;
      border-radius: 12px;
      text-decoration: none;
      font-size: 0.88rem;
      font-weight: 600;
      transition: all 0.2s ease;
    }
    .who-jump-btn:hover {
      background: rgba(249, 115, 22, 0.25);
      border-color: #f97316;
      color: #ffffff;
      transform: translateY(-2px);
    }

    /* SECTION CONTAINERS */
    .genealogy-section {
      background: var(--dark-card-bg);
      border: 1px solid var(--dark-border);
      border-radius: 20px;
      padding: 32px 30px;
      margin-bottom: 36px;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }
    .section-header-box {
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 1.5px solid rgba(249, 115, 22, 0.3);
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
    }
    .section-header-box h2 {
      font-size: 1.85rem;
      color: #ffffff;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .section-header-box h2 span.icon-badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 44px;
      height: 44px;
      border-radius: 12px;
      background: rgba(249, 115, 22, 0.18);
      border: 1px solid rgba(249, 115, 22, 0.4);
      color: #fb923c;
    }
    .section-subtext {
      color: #94a3b8;
      font-size: 0.95rem;
      line-height: 1.6;
      margin-top: 6px;
    }

    /* COSMIC ORIGIN TREE LEVEL 1 */
    .cosmic-hierarchy {
      display: flex;
      flex-direction: column;
      gap: 24px;
    }
    .cosmic-node-supreme {
      background: linear-gradient(135deg, rgba(234, 88, 12, 0.25), rgba(124, 45, 18, 0.3));
      border: 1.5px solid rgba(251, 146, 60, 0.5);
      border-radius: 16px;
      padding: 24px;
      text-align: center;
    }
    .cosmic-supreme-title {
      font-size: 1.5rem;
      font-weight: 800;
      color: #fed7aa;
      margin-bottom: 6px;
    }
    .cosmic-connector {
      display: flex;
      justify-content: center;
      align-items: center;
      color: #f97316;
      font-size: 1.5rem;
      margin: -12px 0;
    }

    /* RISHIS & PRAJAPATIS GRID */
    .prajapati-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 16px;
      margin-top: 14px;
    }
    .prajapati-card {
      background: rgba(30, 41, 59, 0.65);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 14px;
      padding: 18px;
      transition: all 0.25s ease;
      cursor: pointer;
    }
    .prajapati-card:hover {
      transform: translateY(-3px);
      border-color: rgba(249, 115, 22, 0.6);
      background: rgba(30, 41, 59, 0.9);
      box-shadow: 0 8px 24px rgba(249, 115, 22, 0.15);
    }
    .prajapati-card-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
    }
    .prajapati-name {
      font-size: 1.18rem;
      font-weight: 700;
      color: #f8fafc;
    }
    .prajapati-origin-tag {
      font-size: 0.75rem;
      background: rgba(249, 115, 22, 0.15);
      color: #fdba74;
      padding: 2px 8px;
      border-radius: 6px;
      border: 1px solid rgba(249, 115, 22, 0.3);
    }
    .prajapati-info {
      font-size: 0.86rem;
      color: #94a3b8;
      line-height: 1.5;
    }
    .prajapati-info strong {
      color: #e2e8f0;
    }
    .prajapati-scripture {
      margin-top: 8px;
      font-size: 0.78rem;
      color: #38bdf8;
      font-family: monospace;
    }

    /* 14 MANUS CAROUSEL & TABS */
    .manus-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
    }
    .manu-card {
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 14px;
      padding: 18px;
      position: relative;
      transition: all 0.25s ease;
    }
    .manu-card.current-manu {
      border: 2px solid #f59e0b;
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.18), rgba(30, 41, 59, 0.85));
      box-shadow: 0 0 25px rgba(245, 158, 11, 0.25);
    }
    .manu-badge {
      display: inline-block;
      font-size: 0.75rem;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 6px;
      margin-bottom: 6px;
    }
    .manu-badge-current {
      background: #f59e0b;
      color: #000;
    }
    .manu-badge-past {
      background: rgba(148, 163, 184, 0.2);
      color: #cbd5e1;
    }
    .manu-badge-future {
      background: rgba(168, 85, 247, 0.2);
      color: #d8b4fe;
    }
    .manu-title {
      font-size: 1.15rem;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 6px;
    }
    .manu-details {
      font-size: 0.85rem;
      color: #94a3b8;
      line-height: 1.5;
    }

    /* TWO GREAT DYNASTIES TABS & TREES */
    .dynasty-tabs {
      display: flex;
      gap: 12px;
      margin-bottom: 24px;
      flex-wrap: wrap;
    }
    .dynasty-tab-btn {
      flex: 1;
      min-width: 220px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      padding: 14px 20px;
      border-radius: 14px;
      border: 1.5px solid rgba(255, 255, 255, 0.15);
      background: rgba(15, 23, 42, 0.6);
      color: #cbd5e1;
      font-size: 1.05rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.25s ease;
    }
    .dynasty-tab-btn:hover {
      background: rgba(255, 255, 255, 0.1);
      color: #ffffff;
    }
    .dynasty-tab-btn.active.tab-surya {
      background: linear-gradient(135deg, rgba(234, 88, 12, 0.35), rgba(180, 83, 9, 0.35));
      border-color: #f59e0b;
      color: #fef08a;
      box-shadow: 0 6px 20px rgba(245, 158, 11, 0.3);
    }
    .dynasty-tab-btn.active.tab-chandra {
      background: linear-gradient(135deg, rgba(37, 99, 235, 0.35), rgba(30, 64, 175, 0.35));
      border-color: #60a5fa;
      color: #bfdbfe;
      box-shadow: 0 6px 20px rgba(96, 165, 250, 0.3);
    }
    .dynasty-tab-btn.active.tab-gotra {
      background: linear-gradient(135deg, rgba(5, 150, 105, 0.35), rgba(4, 120, 87, 0.35));
      border-color: #34d399;
      color: #a7f3d0;
      box-shadow: 0 6px 20px rgba(52, 211, 153, 0.3);
    }

    /* TIMELINE TREE NODES */
    .timeline-tree {
      position: relative;
      padding-left: 28px;
    }
    .timeline-tree::before {
      content: "";
      position: absolute;
      left: 8px;
      top: 15px;
      bottom: 15px;
      width: 3px;
      background: linear-gradient(180deg, #f59e0b, #ef4444, #3b82f6, #10b981);
      border-radius: 2px;
    }
    .tree-milestone {
      position: relative;
      margin-bottom: 24px;
    }
    .tree-milestone::before {
      content: "";
      position: absolute;
      left: -28px;
      top: 18px;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #f59e0b;
      border: 3px solid #0f172a;
      box-shadow: 0 0 10px rgba(245, 158, 11, 0.8);
    }
    .tree-milestone.lunar::before {
      background: #60a5fa;
      box-shadow: 0 0 10px rgba(96, 165, 250, 0.8);
    }
    .tree-milestone.chola::before {
      background: #f43f5e;
      box-shadow: 0 0 10px rgba(244, 63, 94, 0.8);
    }
    .milestone-card {
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 16px;
      padding: 20px 22px;
      transition: all 0.25s ease;
    }
    .milestone-card:hover {
      border-color: rgba(251, 146, 60, 0.6);
      transform: translateX(4px);
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
    }
    .milestone-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 8px;
    }
    .milestone-name {
      font-size: 1.25rem;
      font-weight: 800;
      color: #ffffff;
    }
    .milestone-gen-badge {
      font-size: 0.75rem;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 12px;
      background: rgba(245, 158, 11, 0.2);
      border: 1px solid rgba(245, 158, 11, 0.4);
      color: #fde047;
    }
    .milestone-epithet {
      color: #fb923c;
      font-weight: 600;
      font-size: 0.92rem;
      margin-bottom: 6px;
    }
    .milestone-desc {
      color: #cbd5e1;
      font-size: 0.9rem;
      line-height: 1.6;
    }
    .milestone-scriptures {
      margin-top: 10px;
      padding-top: 8px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      font-size: 0.8rem;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* TAMIL KINGS CONNECTION BOXES */
    .tamil-connection-box {
      background: linear-gradient(135deg, rgba(159, 18, 57, 0.3), rgba(30, 41, 59, 0.85));
      border: 1.5px solid rgba(244, 63, 94, 0.45);
      border-radius: 16px;
      padding: 24px;
      margin-top: 24px;
    }
    .tamil-box-title {
      font-size: 1.35rem;
      font-weight: 800;
      color: #fecdd3;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .tamil-kings-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 14px;
      margin-top: 14px;
    }
    .tamil-king-card {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid rgba(244, 63, 94, 0.3);
      border-radius: 12px;
      padding: 14px;
    }
    .tamil-king-name {
      font-size: 1.05rem;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 4px;
    }
    .tamil-king-desc {
      font-size: 0.85rem;
      color: #cbd5e1;
      line-height: 1.45;
    }

    /* INTERACTIVE EXPLORER */
    .explorer-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      margin-bottom: 24px;
    }
    .explorer-search-input {
      flex: 2;
      min-width: 260px;
      background: rgba(15, 23, 42, 0.8);
      border: 1.5px solid rgba(251, 146, 60, 0.4);
      border-radius: 12px;
      padding: 12px 18px;
      color: #ffffff;
      font-size: 1rem;
      font-family: inherit;
    }
    .explorer-search-input:focus {
      outline: none;
      border-color: #f97316;
      box-shadow: 0 0 15px rgba(249, 115, 22, 0.35);
    }
    .explorer-filter-select {
      flex: 1;
      min-width: 180px;
      background: rgba(15, 23, 42, 0.8);
      border: 1.5px solid rgba(251, 146, 60, 0.4);
      border-radius: 12px;
      padding: 12px 16px;
      color: #ffffff;
      font-size: 0.95rem;
      font-family: inherit;
      cursor: pointer;
    }
    .explorer-filter-select option {
      background: #0f172a;
      color: #ffffff;
    }

    /* CONCORDANCE TABLE OF 12 PURANAS */
    .concordance-table-wrapper {
      overflow-x: auto;
      margin-top: 18px;
    }
    .concordance-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
      text-align: left;
    }
    .concordance-table th {
      background: rgba(234, 88, 12, 0.25);
      color: #fde047;
      padding: 12px 16px;
      border-bottom: 2px solid rgba(251, 146, 60, 0.4);
      white-space: nowrap;
    }
    .concordance-table td {
      padding: 12px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      color: #cbd5e1;
      vertical-align: top;
    }
    .concordance-table tr:hover td {
      background: rgba(255, 255, 255, 0.03);
    }

    /* MODAL FOR KING / ANCESTOR DETAILS */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 2000;
      padding: 20px;
    }
    .modal-overlay.open {
      display: flex;
    }
    .ancestor-modal-card {
      background: #0b1329;
      border: 1.5px solid #f97316;
      border-radius: 20px;
      max-width: 650px;
      width: 100%;
      padding: 28px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8), 0 0 35px rgba(249, 115, 22, 0.25);
      position: relative;
      max-height: 90vh;
      overflow-y: auto;
    }
    .modal-close-btn {
      position: absolute;
      top: 18px;
      right: 18px;
      background: rgba(255, 255, 255, 0.1);
      border: none;
      color: #ffffff;
      width: 34px;
      height: 34px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.2rem;
      transition: all 0.2s;
    }
    .modal-close-btn:hover {
      background: #ef4444;
    }

    /* RESPONSIVE TWEAKS */
    @media (max-width: 768px) {
      .who-hero {
        padding: 26px 20px;
      }
      .who-hero-title {
        font-size: 1.85rem;
      }
      .genealogy-section {
        padding: 22px 18px;
      }
    }
  </style>
</head>
<body class="has-left-strip theme-cosmic">

  <!-- LEFT STRIP BAR (PRIMARY GLOBAL SHELL - WARM RED-ORANGE ACCORDION) -->
  <aside class="left-strip-bar" id="leftStripBar" aria-label="குருகுல முதன்மை பட்டி">
    <div class="strip-header">
      <a href="index.html" class="strip-brand-link" title="குரு குல ஆசிரமம்">
        <span class="strip-emblem"><svg class="gkd-icon gkd-om-icon" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8.2 10.5c-.3-.7-.2-1.5.3-2.1.8-.9 2.2-.9 3 .1.4.5.5 1.2.2 1.8-.4.7-1.1 1.2-1.7 1.7.9.3 1.7.9 2 1.7.4 1.1 0 2.4-1 3.1-1.2.9-2.9.7-3.9-.4-.4-.5-.6-1.1-.6-1.7h1.4c0 .4.2.8.5 1 .6.5 1.5.4 2-.1.4-.4.5-1 .2-1.5-.4-.7-1.2-1-2-1v-1.2c.6 0 1.2-.2 1.5-.7.3-.4.3-.9 0-1.3-.4-.5-1.1-.6-1.6-.2-.3.2-.5.6-.5 1H8.2zm6.3-2.5c.8 0 1.5.5 1.8 1.2l-1.2.5c-.2-.4-.5-.6-.8-.6-.6 0-1 .4-1 1s.4 1 1 1c.5 0 .9-.3 1.1-.7l1.1.6c-.4.8-1.2 1.3-2.2 1.3-1.4 0-2.4-1-2.4-2.4 0-1.3 1-2.4 2.4-2.4zm1.5-1.5c.3 0 .5.2.5.5s-.2.5-.5.5-.5-.2-.5-.5.2-.5.5-.5z"/></svg></span>
        <div style="display: flex; flex-direction: column;">
          <span class="strip-brand-text">குரு குல ஆசிரமம்</span>
          <span style="font-size: 0.68rem; color: #2dd4bf; letter-spacing: 0.05em; font-weight: 600;">தொன்மை மரபு & வம்சாவளி</span>
        </div>
      </a>
      <button type="button" class="strip-toggle-btn" id="stripToggleBtn" onclick="togglePrimaryMenu()" data-tooltip="பட்டி விரிவாக்குக / சுருக்குக" title="முதன்மை பட்டி" aria-label="பட்டி மாற்று">
        <span class="strip-toggle-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg></span>
      </button>
    </div>

    <nav class="strip-nav-list" id="stripNavList">

      <!-- 1. பாடத்திட்ட முகப்பு -->
      <div class="strip-group" data-group="home">
        <a href="index.html" class="strip-item" data-tooltip="பாடத்திட்ட முகப்பு">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v3"/><path d="M7 5h10l-1.5 4H8.5L7 5z"/><path d="M5 9h14l-1.5 5H6.5L5 9z"/><path d="M3 14h18v7H3v-7z"/><path d="M10 21v-4a2 2 0 0 1 4 0v4"/></svg></span>
          <span class="strip-item-label">பாடத்திட்ட முகப்பு</span>
        </a>
      </div>

      <!-- 2. பருவம் 1: பாலப் பருவம் (1–4) -->
      <div class="strip-group" data-group="stage1">
        <a href="tharam-1.html" class="strip-item strip-has-sub" data-tooltip="1. பாலப் பருவம் (1–4)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3 7h-6l3-7z"/><line x1="12" y1="9" x2="12" y2="22"/></svg></span>
          <span class="strip-item-label">1. பாலப் பருவம் (1–4)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #38bdf8;">பாலப் பருவம் • தொடக்கக் கல்வி</div>
          <a href="tharam-1.html" class="strip-sub-item"><span class="strip-sub-icon">1️⃣</span><span>தரம் 1 (Grade 1) • நற்செயல்</span></a>
          <a href="tharam-2.html" class="strip-sub-item"><span class="strip-sub-icon">2️⃣</span><span>தரம் 2 (Grade 2) • நற்செயல்</span></a>
          <a href="tharam-3.html" class="strip-sub-item"><span class="strip-sub-icon">3️⃣</span><span>தரம் 3 (Grade 3) • நற்பண்பு</span></a>
          <a href="tharam-4.html" class="strip-sub-item"><span class="strip-sub-icon">4️⃣</span><span>தரம் 4 (Grade 4) • நற்பண்பு</span></a>
        </div>
      </div>

      <!-- 3. பருவம் 2: இளம் பருவம் (5–8) -->
      <div class="strip-group" data-group="stage2">
        <a href="tharam-5.html" class="strip-item strip-has-sub" data-tooltip="2. இளம் பருவம் (5–8)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></span>
          <span class="strip-item-label">2. இளம் பருவம் (5–8)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #34d399;">இளம் பருவம் • 5 ஆசிரம நூல்கள்</div>
          <a href="tharam-5.html" class="strip-sub-item"><span class="strip-sub-icon">5️⃣</span><span>தரம் 5 (Grade 5)</span></a>
          <a href="tharam-6.html" class="strip-sub-item"><span class="strip-sub-icon">6️⃣</span><span>தரம் 6 (Grade 6)</span></a>
          <a href="tharam-7.html" class="strip-sub-item"><span class="strip-sub-icon">7️⃣</span><span>தரம் 7 (Grade 7)</span></a>
          <a href="tharam-8.html" class="strip-sub-item"><span class="strip-sub-icon">8️⃣</span><span>தரம் 8 (Grade 8)</span></a>
        </div>
      </div>

      <!-- 4. பருவம் 3: உயர்நிலைப் பருவம் (9–10) -->
      <div class="strip-group" data-group="stage3">
        <a href="tharam-9.html" class="strip-item strip-has-sub" data-tooltip="3. உயர்நிலைப் பருவம் (9–10)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H4a2 2 0 0 0-2 2v13a3 3 0 0 0 3 3h13a3 3 0 0 0 3-3V5a2 2 0 0 0-2-2h-7"/><path d="M19 18a3 3 0 0 0 0-6H6a2 2 0 0 0 0 4h12"/><line x1="8" y1="7" x2="14" y2="7"/></svg></span>
          <span class="strip-item-label">3. உயர்நிலை (9–10)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #facc15;">உயர்நிலைப் பருவம் • 6 நூல்கள்</div>
          <a href="tharam-9.html" class="strip-sub-item"><span class="strip-sub-icon">9️⃣</span><span>தரம் 9 (Grade 9)</span></a>
          <a href="tharam-10.html" class="strip-sub-item"><span class="strip-sub-icon">🔟</span><span>தரம் 10 (Grade 10)</span></a>
        </div>
      </div>

      <!-- 5. பருவம் 4: மேல்நிலைப் பருவம் (11–12) -->
      <div class="strip-group" data-group="stage4">
        <a href="tharam-11.html" class="strip-item strip-has-sub" data-tooltip="4. மேல்நிலைப் பருவம் (11–12)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l9 4.9V17L12 22 3 17V6.9L12 2z"/><path d="M12 22V12"/></svg></span>
          <span class="strip-item-label">4. மேல்நிலை (11–12)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #fb923c;">மேல்நிலை • 6 நூல்கள்</div>
          <a href="tharam-11.html" class="strip-sub-item"><span class="strip-sub-icon">1️⃣1️⃣</span><span>தரம் 11 (Grade 11)</span></a>
          <a href="tharam-12.html" class="strip-sub-item"><span class="strip-sub-icon">1️⃣2️⃣</span><span>தரம் 12 (Grade 12)</span></a>
        </div>
      </div>

      <!-- 6. பருவம் 5: உயர்கல்வி வித்யாபீடம் (BA, MA, PhD) -->
      <div class="strip-group" data-group="higher_studies">
        <a href="higher-studies.html" class="strip-item strip-has-sub" data-tooltip="5. உயர்கல்வி (BA, MA, PhD)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="2" fill="currentColor"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(-30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(90 12 12)"/></svg></span>
          <span class="strip-item-label">5. உயர்கல்வி (BA, MA)</span>
          <span class="strip-sub-indicator"><svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg></span>
        </a>
        <div class="strip-sub-menu">
          <div class="strip-sub-header" style="color: #ffd700;">பட்டப் படிப்புகள் & ஆய்வு</div>
          <a href="higher-studies.html#tierUG" class="strip-sub-item"><span class="strip-sub-icon">🎓</span><span>இளங்கலை (B.A./B.Sc.)</span></a>
          <a href="higher-studies.html#tierPG" class="strip-sub-item"><span class="strip-sub-icon">📜</span><span>முதுகலை (M.A./Acharya)</span></a>
          <a href="higher-studies.html#tierPhD" class="strip-sub-item"><span class="strip-sub-icon">⚛️</span><span>முனைவர் ஆய்வு (Ph.D.)</span></a>
        </div>
      </div>

      <!-- 7. 7 ஆசிரமப் பாடநூல்கள் -->
      <div class="strip-group" data-group="books">
        <a href="books.html" class="strip-item" data-tooltip="7 ஆசிரமப் பாடநூல்கள்">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></span>
          <span class="strip-item-label">7 ஆசிரமப் பாடநூல்கள்</span>
        </a>
      </div>

      <!-- 8. வித்யா குடீரம் பள்ளி போர்டல் -->
      <div class="strip-group" data-group="school">
        <a href="school.html" class="strip-item" data-tooltip="வித்யா குடீரம் பள்ளி">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 2 3 3 6 3s6-1 6-3v-5"/></svg></span>
          <span class="strip-item-label">வித்யா குடீரம் பள்ளி</span>
        </a>
      </div>

      <!-- 9. நிர்வாகப் பிரிவு -->
      <div class="strip-group" data-group="admin">
        <a href="admissions.html" class="strip-item" data-tooltip="நிர்வாகப் பிரிவு (Admin)">
          <span class="strip-item-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></span>
          <span class="strip-item-label">நிர்வாகப் பிரிவு (Admin)</span>
        </a>
      </div>

      <!-- 10. யார் நாம்? (Who We Are? — தொன்மை சனாதன வம்சாவளி & பரம்பரை) ACTIVE -->
      <div class="strip-group" data-group="who_we_are">
        <a href="who-we-are.html" class="strip-item active" data-tooltip="யார் நாம்? (Who We Are)">
          <span class="strip-item-icon" style="background: rgba(251, 146, 60, 0.3); border: 1px solid #fb923c;"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span>
          <span class="strip-item-label" style="color: #fbbf24; font-weight: 700;">யார் நாம்? (Who We Are)</span>
        </a>
      </div>

    </nav>

    <div class="strip-footer-dock">
      <button type="button" class="strip-dock-btn" onclick="openUserSettingsModal('preferences')" title="அமைப்புகள்" data-tooltip="அமைப்புகள்">
        <span class="strip-dock-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/></svg></span>
        <span class="strip-dock-label">அமைப்புகள்</span>
      </button>
      <button type="button" class="strip-dock-btn profile-dock-btn" onclick="openUserSettingsModal('profile')" title="சுயவிவரம்" data-tooltip="சுயவிவரம்">
        <span class="strip-dock-avatar" id="stripAvatarIcon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span>
        <span class="strip-dock-label" id="stripUserName">மாணவர்</span>
      </button>
    </div>
  </aside>

  <div class="strip-backdrop" id="stripBackdrop" onclick="closePrimaryMenu()"></div>

  <!-- CONTEXT-SENSITIVE TOP BAR -->
  <header class="context-top-bar" id="contextTopBar">
    <div class="context-bar-container">
      <div class="context-bar-left">
        <button type="button" class="mobile-hamburger-btn" onclick="togglePrimaryMenu()" title="பட்டி திறக்க" aria-label="முதன்மை பட்டி">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <button type="button" class="breadcrumb-back-btn" onclick="if(window.history.length > 1){ window.history.back(); } else { window.location.href='index.html'; }" title="பின்னே செல்ல">
          <svg class="gkd-icon gkd-arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          <span>பின்னே</span>
        </button>
        <nav class="context-breadcrumbs" id="contextBreadcrumbs" aria-label="தள வழிகாட்டல்">
          <a href="index.html" class="crumb-link crumb-home" title="முகப்பு">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
            <span class="crumb-text">முகப்பு</span>
          </a>
          <span class="crumb-sep">/</span>
          <span class="crumb-current" id="topBarCurrentCrumb">யார் நாம்? — தொன்மை சனாதன வம்சாவளி & பரம்பரை</span>
        </nav>
      </div>
      <div class="header-right-tools">
        <div class="context-tool-group">
          <button type="button" class="context-tool-btn" id="langSwitchBtn" onclick="toggleBilingual()" title="மொழி மாற்றம் / Switch Language" style="font-weight:700; font-size:0.85rem; padding: 4px 10px; border-radius: 8px;">
            <span>தமிழ் / ENG</span>
          </button>
        </div>
        <div class="context-search-wrapper">
          <span class="context-search-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></span>
          <input type="text" id="contextQuickSearch" class="context-search-input" placeholder="அரசர் / ரிஷி தேடுக... [/]" oninput="filterLineage(this.value)" autocomplete="off">
          <button type="button" class="context-search-clear" id="contextSearchClear" onclick="clearLineageSearch()" style="display: none;"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
        </div>
        <div class="context-tool-group">
          <button type="button" class="context-tool-btn font-dec-btn" onclick="adjustFontSize(-0.06)" title="எழுத்தளவைக் குறைக்க"><span style="font-size:0.9em; font-weight:700">A-</span></button>
          <button type="button" class="context-tool-btn font-inc-btn" onclick="adjustFontSize(0.06)" title="எழுத்தளவை அதிகரிக்க"><span style="font-size:0.9em; font-weight:700">A+</span></button>
        </div>
        <button type="button" class="context-tool-btn theme-quick-btn" onclick="cycleTheme()" title="வண்ணக் கருப்பொருள்">
          <span class="theme-icon" id="themeQuickIcon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg></span>
        </button>
      </div>
    </div>
  </header>

  <main class="main-content" style="padding: 24px 28px 60px;">

    <!-- HERO SECTION -->
    <section class="who-hero">
      <div class="who-hero-content">
        <div class="hero-badge-row">
          <span class="hero-badge badge-solar">☀️ சூர்ய வம்சம் • Solar Line</span>
          <span class="hero-badge badge-lunar">🌙 சந்திர வம்சம் • Lunar Line</span>
          <span class="hero-badge badge-rishi">🪔 ரிஷி கோத்திர பரம்பரை • Saptarshi Lineage</span>
          <span class="hero-badge" style="background: rgba(239, 68, 68, 0.18); border: 1px solid rgba(239, 68, 68, 0.45); color: #fca5a5;">🏛️ 12 மகாபுராண ஆதாரங்கள்</span>
        </div>
        <h1 class="who-hero-title">
          <span>யார் நாம்? (Who We Are?)</span><br>
          பிரம்மோத்பத்தி முதல் மனுக்கள் &amp; சூரிய-சந்திர குல அரச பரம்பரை
        </h1>
        <p class="who-hero-subtitle">
          நாராயண பரப்பிரம்மம் மற்றும் பிரம்மனின் மானஸபுத்திரர்களான சப்தரிஷிகள் &amp; பிரஜாபதிகள் முதல் 14 மன்வந்தர மனுக்கள், தற்போதைய 7-ஆம் வைவஸ்வத மனுவின் மாபெரும் சூரிய-சந்திர குலங்கள், ஸ்ரீராமர், பாண்டவர்கள், மற்றும் தமிழகத்தின் பெருமைமிகு சோழ-பாண்டிய அரச மரபுகள் வரை சனாதன வம்சாவளி தொடர்ச்சி.
        </p>
        <div class="who-quick-nav">
          <a href="#level1_prajapatis" class="who-jump-btn">⚡ 1. பிரம்மன் &amp; பிரஜாபதிகள்</a>
          <a href="#level2_manus" class="who-jump-btn">📜 2. 14 மனுக்கள் (Manvantaras)</a>
          <a href="#level3_dynasties" class="who-jump-btn">👑 3. சூரிய &amp; சந்திர குலங்கள்</a>
          <a href="#chola_pandya_legacy" class="who-jump-btn">🐅 4. சோழ-பாண்டிய தமிழ் மரபு</a>
          <a href="#rishi_gotras" class="who-jump-btn">🪔 5. ரிஷி கோத்திர வம்சம்</a>
          <a href="#dynasty_explorer" class="who-jump-btn">🔍 6. வம்சாவளி தேடு பொறி</a>
          <a href="#purana_concordance" class="who-jump-btn">📖 7. 12 புராண ஒப்பீடு</a>
        </div>
      </div>
    </section>

    <!-- LEVEL 1: BRAHMODBHATTI & PRAJAPATIS -->
    <section class="genealogy-section" id="level1_prajapatis">
      <div class="section-header-box">
        <div>
          <h2><span class="icon-badge">🪐</span> பிரம்மோத்பத்தி &amp; பிரஜாபதிகள் (Cosmic Genesis &amp; 10 Mind-Born Sons)</h2>
          <div class="section-subtext">
            பாகவதம் (3.12, 4.1) மற்றும் விஷ்ணு புராணம் (1.7) ஆதாரங்களின்படி பிரம்மனின் சிந்தனை, வாக்கு, நயனம் முதலான அங்கங்களிலிருந்து அவதரித்த பிரஜாபதிகள் &amp; ரிஷிகள்.
          </div>
        </div>
      </div>

      <div class="cosmic-hierarchy">
        <div class="cosmic-node-supreme">
          <div style="font-size: 0.85rem; text-transform: uppercase; color: #f97316; font-weight: 800; letter-spacing: 0.1em; margin-bottom: 4px;">ஆதி மூல பரம்பொருள் • Primordial Source</div>
          <div class="cosmic-supreme-title">நாராயண / பரப்பிரம்மம் ➔ பிரம்மதேவன் (ஹிரண்யகர்ப்பன்)</div>
          <div style="color: #cbd5e1; font-size: 0.95rem; max-width: 780px; margin: 0 auto;">
            பிரபஞ்ச சிருஷ்டியின் தொடக்கத்தில் உலக உயிர்களைத் தோற்றுவிக்க பிரம்மன் தனது மனதிலிருந்து 10 மானஸபுத்திரர்களையும், தனது உடலிலிருந்து முதல் மனுவான சுவாயம்புவ மனு மற்றும் சதரூபையையும் தோற்றுவித்தார்.
          </div>
        </div>

        <div class="cosmic-connector">▼</div>

        <!-- 10 Prajapatis Grid -->
        <div class="prajapati-grid" id="prajapatisGrid">
          <!-- Injected via JS -->
        </div>
      </div>
    </section>

    <!-- LEVEL 2: 14 MANUS (THE 14 MANVANTARAS) -->
    <section class="genealogy-section" id="level2_manus">
      <div class="section-header-box">
        <div>
          <h2><span class="icon-badge">⏳</span> 14 மனுக்கள் (The 14 Manus &amp; Cosmic Epochs)</h2>
          <div class="section-subtext">
            பிரம்மனின் ஒரு பகலில் 14 மன்வந்தரங்கள் நடைபெறுகின்றன. தற்போது நாம் வாழ்வது 7-ஆம் மனுவான <strong>வைவஸ்வத மனுவின் (ஸ்ராத்ததேவர்)</strong> காலமாகும்.
          </div>
        </div>
        <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); padding: 6px 14px; border-radius: 10px; color: #fde047; font-size: 0.84rem; font-weight: 700;">
          தற்போதைய யுகம்: 7-ஆம் மன்வந்தரம் • 28-ஆம் சதுர்யுக கலியுகம்
        </div>
      </div>

      <div class="manus-grid" id="manusGrid">
        <!-- Injected via JS -->
      </div>
    </section>

    <!-- LEVEL 3: THE TWO GREAT DYNASTIES OF 7TH MANU -->
    <section class="genealogy-section" id="level3_dynasties">
      <div class="section-header-box">
        <div>
          <h2><span class="icon-badge">👑</span> தற்போதைய 7-ஆம் வைவஸ்வத மனுவின் இரு பெருங்குலங்கள்</h2>
          <div class="section-subtext">
            சூரிய குலம் (இக்ஷ்வாகு வம்சம்) &amp; சந்திர குலம் (ஐல / யது-புரு வம்சம்) — பாரத வர்ஷத்தின் மூல அரச பரம்பரைகள்.
          </div>
        </div>
      </div>

      <!-- Tab Buttons -->
      <div class="dynasty-tabs">
        <button type="button" class="dynasty-tab-btn active tab-surya" id="tabSuryaBtn" onclick="switchDynastyTab('surya')">
          <span>☀️ சூரிய வம்சம் (Solar Dynasty)</span>
        </button>
        <button type="button" class="dynasty-tab-btn tab-chandra" id="tabChandraBtn" onclick="switchDynastyTab('chandra')">
          <span>🌙 சந்திர வம்சம் (Lunar Dynasty)</span>
        </button>
        <button type="button" class="dynasty-tab-btn tab-gotra" id="tabGotraBtn" onclick="switchDynastyTab('gotra')">
          <span>🪔 ரிஷி கோத்திர மரபு (Gotra Lineages)</span>
        </button>
      </div>

      <!-- SURYA VAMSHAM TAB CONTENT -->
      <div id="suryaTabContent">
        <div style="background: rgba(245, 158, 11, 0.08); border-left: 4px solid #f59e0b; border-radius: 0 12px 12px 0; padding: 16px 20px; margin-bottom: 24px;">
          <h3 style="color: #fde047; font-size: 1.2rem; margin-bottom: 4px;">சூரிய குல தொடர்ச்சி (Surya Vamsham / Raghuvamsha)</h3>
          <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.6; margin: 0;">
            விவஸ்வான் (சூரியன்) ➔ வைவஸ்வத மனு ➔ இக்ஷ்வாகு (அயோத்தியின் முதல் அரசர்) ➔ மாந்தாதா ➔ ஹரிச்சந்திரன் ➔ சகரன் ➔ பகீரதன் (கங்கையை பூமிக்குக் கொணர்ந்தவர்) ➔ ரகு (ரகு வம்சம்) ➔ தசரதர் ➔ <strong>மரியாதா புருஷோத்தமர் ஸ்ரீராமர்</strong> ➔ லவ & குச ➔ பிருஹத்பலன் (மகாபாரதப் போரில் கலந்துகொண்டவர்) ➔ சுமித்திரன் (கலியுக இறுதி இக்ஷ்வாகு மன்னர்).
          </p>
        </div>

        <div class="timeline-tree" id="suryaTimelineTree">
          <!-- Injected via JS -->
        </div>

        <!-- CHOLA CONNECTION BOX -->
        <div class="tamil-connection-box" id="chola_pandya_legacy">
          <div class="tamil-box-title">
            <span>🐅</span>
            <span>சூரிய குலமும் தமிழக சோழர் மரபும் (Solar Descent of the Chola Emperors)</span>
          </div>
          <p style="color: #cbd5e1; font-size: 0.94rem; line-height: 1.65;">
            அன்பில் செப்பேடுகள் (Anbil Plates of Sundara Chola), திருவாலங்காடு செப்பேடுகள் (Thiruvallangadu Plates of Rajendra Chola), மற்றும் கன்யாகுமரி கல்வெட்டுகளின் மெய்க்கீர்த்திகள் சோழ மன்னர்களை சூரிய வம்சத்தில் தோன்றிய இக்ஷ்வாகு, மாந்தாதா, சிபி சக்கரவர்த்தி ஆகியோரின் நேரடி வாரிசுகளாக ஆவணப்படுத்துகின்றன.
          </p>
          <div class="tamil-kings-grid">
            <div class="tamil-king-card">
              <div class="tamil-king-name">மனுநீதிச் சோழன் (எல்லாளன்)</div>
              <div class="tamil-king-desc">தன் மகனின் தேர்க்காலில் இறந்துபோன கன்றுக்காகத் தன் சொந்த மகனையே தேர்க்காலில் இட்டுக் கொன்று நீதி காத்து மனுவின் அறநெறியை நிலைநிறுத்திய சூரியகுலச் செம்மல்.</div>
            </div>
            <div class="tamil-king-card">
              <div class="tamil-king-name">சிபிச் சக்கரவர்த்தி</div>
              <div class="tamil-king-desc">புறாவின் உயிரைக் காக்க தன் தொடை சதையை அறுத்துக் கொடுத்த தியாக சீலர்; சோழர்களின் முன்னோடியாகப் புறநானூறு மற்றும் சிலப்பதிகாரத்தில் போற்றப்படுபவர்.</div>
            </div>
            <div class="tamil-king-card">
              <div class="tamil-king-name">கரிகால் பெருவளத்தான்</div>
              <div class="tamil-king-desc">காவிரியின் குறுக்கே கல்லணையைக் கட்டிய மாவீரன்; இமயத்தில் புலிப்பொறி பொறித்த சூரியகுலப் பேராற்றல்.</div>
            </div>
            <div class="tamil-king-card">
              <div class="tamil-king-name">முதலாம் இராஜராஜ சோழன் &amp; இராஜேந்திரன்</div>
              <div class="tamil-king-desc">தஞ்சைப் பெரியகோயில் மற்றும் கங்கைகொண்ட சோழபுரத்தை நிர்மாணித்து, கடல் கடந்து சனாதன சைவதர்மத்தையும் கடாரத்தையும் வென்ற பெருவேந்தர்கள்.</div>
            </div>
          </div>
        </div>
      </div>

      <!-- CHANDRA VAMSHAM TAB CONTENT (Initially Hidden) -->
      <div id="chandraTabContent" style="display: none;">
        <div style="background: rgba(59, 130, 246, 0.08); border-left: 4px solid #3b82f6; border-radius: 0 12px 12px 0; padding: 16px 20px; margin-bottom: 24px;">
          <h3 style="color: #bfdbfe; font-size: 1.2rem; margin-bottom: 4px;">சந்திர குல தொடர்ச்சி (Chandra Vamsham / Aila Lineage)</h3>
          <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.6; margin: 0;">
            பிரம்மன் ➔ அத்திரி மகரிஷி ➔ சந்திரன் (சோமன்) ➔ புதன் + வைவஸ்வத மனுவின் மகள் இளை ➔ புரூரவஸ் ➔ நகுஷன் ➔ யயாதி (ஐந்து குமாரர்கள்: யது, துர்வசு, துருஹ்யு, அனு, புரு).<br>
            <strong>யது கிளை:</strong> யாதவர்கள், கார்த்தவீரிய அர்ஜுனன், விருஷ்ணிகள், வாசுதேவர் ➔ <strong>பகவான் ஸ்ரீகிருஷ்ணர் &amp; பலராமர்</strong>.<br>
            <strong>புரு கிளை:</strong> துஷ்யந்தன் ➔ <strong>பரதன்</strong> (பாரத வர்ஷம் என நம் தேசம் பெயர் பெறக் காரணமானவர்) ➔ ஹஸ்தின் (ஹஸ்தினாபுரம்) ➔ குரு ➔ சந்தனு ➔ பீஷ்மர் & விதுரர் ➔ பாண்டு ➔ <strong>பஞ்ச பாண்டவர்கள் (தர்மர், பீமன், அர்ஜுனன், நகுலன், சகாதேவன்)</strong> ➔ அபிமன்யு ➔ பரீக்ஷித்து ➔ ஜனமேஜயன்.
          </p>
        </div>

        <div class="timeline-tree" id="chandraTimelineTree">
          <!-- Injected via JS -->
        </div>

        <!-- PANDYA CONNECTION BOX -->
        <div class="tamil-connection-box" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.35), rgba(15, 23, 42, 0.85)); border-color: rgba(96, 165, 250, 0.45);">
          <div class="tamil-box-title" style="color: #bfdbfe;">
            <span>🐟</span>
            <span>சந்திர குலமும் தமிழக பாண்டியர் மரபும் (Lunar Descent of the Pandya Sovereigns)</span>
          </div>
          <p style="color: #cbd5e1; font-size: 0.94rem; line-height: 1.65;">
            வேள்விக்குடி செப்பேடுகள் (Velvikkudi Grant) மற்றும் சின்னமனூர் செப்பேடுகள் (Sinnamanur Plates) பாண்டிய மன்னர்களை 'சந்திர குல திலகம்' (Ornaments of the Lunar Lineage) என்று மெய்க்கீர்த்திகளில் சான்றளிக்கின்றன. மகாபாரத சபா பர்வத்தில் பாண்டவர்களுடன் பாண்டிய மன்னர்களின் நேசமும் உறவும் பாடப்பட்டுள்ளது.
          </p>
          <div class="tamil-kings-grid">
            <div class="tamil-king-card" style="border-color: rgba(96, 165, 250, 0.3);">
              <div class="tamil-king-name">மலையத்துவச பாண்டியன் &amp; தடாகைப் பிராட்டி</div>
              <div class="tamil-king-desc">மதுரையை ஆண்ட மாமன்னன்; வேள்வித் தீயில் தோன்றிய அங்கயற்கண்ணி அன்னை மீனாட்சியை மகளாகப் பெற்று சோமசுந்தரப் பெருமானை மருமகனாக அடைந்த புண்ணியவான்.</div>
            </div>
            <div class="tamil-king-card" style="border-color: rgba(96, 165, 250, 0.3);">
              <div class="tamil-king-name">சித்திராங்கதை &amp; பப்ருவாகனன்</div>
              <div class="tamil-king-desc">அர்ஜுனன் தென்னாட்டிற்குத் தீர்த்த யாத்திரை வந்தபோது மணந்த பாண்டிய இளவரசி சித்திராங்கதை; அவர்களது மகன் பப்ருவாகனன் பாண்டிய நாட்டை அரசாண்டான்.</div>
            </div>
            <div class="tamil-king-card" style="border-color: rgba(96, 165, 250, 0.3);">
              <div class="tamil-king-name">நெடுஞ்செழியன் (தலையாலங்கானத்து செருவென்றவன்)</div>
              <div class="tamil-king-desc">சங்ககாலத்து மாவீரன்; புறநானூற்றில் தன் கடமை, நீதி மற்றும் அறவழியைத் தவறாத சந்திரகுலத் தலைவனாகப் புகழப்பட்டவன்.</div>
            </div>
          </div>
        </div>
      </div>

      <!-- GOTRA LINAGES TAB CONTENT (Initially Hidden) -->
      <div id="gotraTabContent" style="display: none;">
        <div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid #10b981; border-radius: 0 12px 12px 0; padding: 16px 20px; margin-bottom: 24px;" id="rishi_gotras">
          <h3 style="color: #6ee7b7; font-size: 1.2rem; margin-bottom: 4px;">ரிஷி கோத்திர மரபு — நமது இல்லங்களின் ஆதி வேர்கள்</h3>
          <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.6; margin: 0;">
            இன்று பாரதத்திலும் உலகெங்கிலும் வாழும் ஒவ்வொரு சனாதன குடும்பமும் தங்களின் முன்னோர்களாக சப்தரிஷிகளையும் பிரஜாபதிகளையும் வணங்குகின்றனர். உபநயனம், திருமணம், திதி முதலான சடங்குகளில் ஓதப்படும் <strong>அபிவாதயே (Abhivadaye)</strong> சூத்திரம் நமது தலைமுறைகளை இந்த மகரிஷிகளுடன் நேரிடையாக இணைக்கிறது.
          </p>
        </div>

        <div class="prajapati-grid" id="gotrasGrid">
          <!-- Injected via JS -->
        </div>
      </div>
    </section>

    <!-- INTERACTIVE EXPLORER & SEARCH -->
    <section class="genealogy-section" id="dynasty_explorer">
      <div class="section-header-box">
        <div>
          <h2><span class="icon-badge">🔎</span> வம்சாவளி ஊடாடும் தேடு பொறி (Interactive Lineage Explorer)</h2>
          <div class="section-subtext">
            அரசர் அல்லது முன்னோரின் பெயரைக் கொண்டு தேடுங்கள்; அவர்களின் தலைமுறை எண், சிறப்புப் பட்டங்கள், புராணக் குறிப்புகள் ஆகியவற்றை உடனடியாகக் கண்டறியலாம்.
          </div>
        </div>
      </div>

      <div class="explorer-bar">
        <input type="text" id="ancestorSearchInput" class="explorer-search-input" placeholder="எ.கா. இக்ஷ்வாகு, மாந்தாதா, ஸ்ரீராமர், யயாதி, அர்ஜுனன், பகீரதன்..." oninput="handleSearch(this.value)">
        <select id="lineageFilterSelect" class="explorer-filter-select" onchange="handleFilter(this.value)">
          <option value="all">அனைத்து மரபுகளும் (All Lineages)</option>
          <option value="surya">சூரிய வம்சம் (Solar Dynasty)</option>
          <option value="chandra">சந்திர வம்சம் (Lunar Dynasty)</option>
          <option value="prajapati">பிரஜாபதிகள் & ரிஷிகள்</option>
          <option value="manu">14 மனுக்கள்</option>
        </select>
      </div>

      <div style="color: #94a3b8; font-size: 0.88rem; margin-bottom: 12px;" id="explorerCountText">
        காண்பிக்கப்படும் முன்னோர்கள்: 140+
      </div>

      <div class="prajapati-grid" id="explorerResultsGrid">
        <!-- Injected dynamically -->
      </div>
    </section>

    <!-- 12 PURANAS CONCORDANCE TABLE -->
    <section class="genealogy-section" id="purana_concordance">
      <div class="section-header-box">
        <div>
          <h2><span class="icon-badge">📚</span> 12 மகாபுராண ஒப்பீட்டு ஆவணம் (Concordance Across 12 Puranas &amp; Itihasas)</h2>
          <div class="section-subtext">
            விஷ்ணு புராணம், ஸ்ரீமத் பாகவதம், மத்ஸ்ய புராணம், வாயு புராணம், பிரம்மாண்ட புராணம், வால்மீகி ராமாயணம், மகாபாரதம் முதலான 12 மூலநூல்களில் வம்சாவளி ஆவணப்படுத்தப்பட்டுள்ள அத்தியாயங்கள்.
          </div>
        </div>
      </div>

      <div class="concordance-table-wrapper">
        <table class="concordance-table">
          <thead>
            <tr>
              <th>புராணம் / இதிகாசம் (Text)</th>
              <th>வம்சாவளி அமைவிடம் (Location)</th>
              <th>முக்கியத்துவம் &amp; ஆய்வுக் குறிப்பு (Scholarly Focus)</th>
              <th>மூல சமஸ்கிருத சுலோகம் (Key Verse)</th>
            </tr>
          </thead>
          <tbody id="concordanceTableBody">
            <!-- Injected via JS -->
          </tbody>
        </table>
      </div>
    </section>

  </main>

  <!-- ANCESTOR DETAIL MODAL -->
  <div class="modal-overlay" id="ancestorModal" onclick="if(event.target === this) closeModal()">
    <div class="ancestor-modal-card">
      <button type="button" class="modal-close-btn" onclick="closeModal()">✕</button>
      <div id="modalContent">
        <!-- Injected via JS -->
      </div>
    </div>
  </div>

  <!-- SITE FOOTER -->
  <footer class="site-footer">
    <div class="footer-container">
      <div class="footer-col">
        <div class="footer-brand">
          <span class="footer-emblem">🕉️</span>
          <div class="footer-brand-text">
            <h3>குரு குல ஆசிரமம்</h3>
            <span>Guru Kula Ashram • ஆன்மீகப் பள்ளி</span>
          </div>
        </div>
        <p class="footer-desc">
          பிரம்மன், மனுக்கள், சூரிய-சந்திர குல மன்னர்கள் மற்றும் ரிஷிகளின் உன்னத பண்பாட்டு மரபையும் தர்ம நெறியையும் அடுத்த தலைமுறைக்கு வழங்கும் ஒப்பற்ற களஞ்சியம்.
        </p>
      </div>
      <div class="footer-col">
        <h4>பள்ளிப் பருவங்கள்</h4>
        <ul class="footer-links">
          <li><a href="tharam-1.html">1. பாலப் பருவம் (தரம் 1–4)</a></li>
          <li><a href="tharam-5.html">2. இளம் பருவம் (தரம் 5–8)</a></li>
          <li><a href="tharam-9.html">3. உயர்நிலைப் பருவம் (தரம் 9–10)</a></li>
          <li><a href="tharam-11.html">4. மேல்நிலைப் பருவம் (தரம் 11–12)</a></li>
          <li><a href="higher-studies.html">5. உயர்கல்வி வித்யாபீடம்</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>7 ஆசிரம நூல்கள்</h4>
        <ul class="footer-links">
          <li><a href="books.html?book=nanneri">1. நன்னெறி (Nanneri)</a></li>
          <li><a href="books.html?book=nallaram">2. நல்லறம் (Nallaram)</a></li>
          <li><a href="books.html?book=nalvazhi">3. நற்பண்பு (Narpanbu)</a></li>
          <li><a href="books.html?book=narthunai">4. நற்துணை (Narthunai)</a></li>
          <li><a href="books.html?book=narchinthanai">5. நற்சிந்தனை (Narchinthanai)</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>வம்சாவளி &amp; நிர்வாகம்</h4>
        <ul class="footer-links">
          <li><a href="who-we-are.html" style="color: #fbbf24; font-weight:700;">👑 யார் நாம்? (Who We Are)</a></li>
          <li><a href="admissions.html">📋 மாணவர் சேர்க்கை</a></li>
          <li><a href="school.html#parentGuide">👨‍👩‍👧 பெற்றோர் வழிகாட்டி</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      &copy; 2026 குரு குல ஆசிரமம் (Guru Kula Ashram) | சனாதன வம்சாவளி &amp; வேத நெறிப் பள்ளி | அனைத்து உரிமைகளும் இறைப்பணிக்கே சமர்ப்பணம்.
    </div>
  </footer>

  <!-- SCRIPT DATA & APP LOGIC -->
  <script>
    // Embedded Puranic Research Database
    window.GKD_GENEALOGY = ''' + data_json_str + ''';

    // Global state
    let isEnglish = false;
    let currentFilter = 'all';
    let currentSearchTerm = '';

    // Initialize UI on load
    document.addEventListener('DOMContentLoaded', () => {
      renderPrajapatis();
      renderManus();
      renderSuryaTree();
      renderChandraTree();
      renderGotras();
      renderConcordance();
      renderExplorer();
    });

    function toggleBilingual() {
      isEnglish = !isEnglish;
      const btn = document.getElementById('langSwitchBtn');
      if (btn) btn.innerHTML = isEnglish ? 'ENG / தமிழ்' : 'தமிழ் / ENG';
      renderPrajapatis();
      renderManus();
      renderSuryaTree();
      renderChandraTree();
      renderGotras();
      renderExplorer();
    }

    // 1. Render Prajapatis (Level 1)
    function renderPrajapatis() {
      const container = document.getElementById('prajapatisGrid');
      if (!container || !window.GKD_GENEALOGY.section_1_cosmic_origin) return;
      const list = window.GKD_GENEALOGY.section_1_cosmic_origin.manasaputras_and_prajapatis;
      container.innerHTML = list.map((p, idx) => `
        <div class="prajapati-card" onclick="openPrajapatiModal(${idx})">
          <div class="prajapati-card-header">
            <span class="prajapati-name">${idx + 1}. ${p.name} Maharshi</span>
            <span class="prajapati-origin-tag">${p.origin}</span>
          </div>
          <div class="prajapati-info">
            <div><strong>தேவி (Consort):</strong> ${p.consort}</div>
            <div><strong>வம்சத் தோற்றம்:</strong> ${p.prominent_descendants}</div>
          </div>
          <div class="prajapati-scripture">📖 ${p.scriptural_reference}</div>
        </div>
      `).join('');
    }

    // 2. Render 14 Manus (Level 2)
    function renderManus() {
      const container = document.getElementById('manusGrid');
      if (!container || !window.GKD_GENEALOGY.section_2_the_14_manus) return;
      const list = window.GKD_GENEALOGY.section_2_the_14_manus;
      container.innerHTML = list.map(m => {
        const isCurrent = m.order === 7;
        const badgeClass = isCurrent ? 'manu-badge-current' : (m.epoch.includes('Past') ? 'manu-badge-past' : 'manu-badge-future');
        const badgeLabel = isCurrent ? '★ தற்போதைய மனு (Current 7th)' : (m.epoch.includes('Past') ? 'கடந்த மனு (Past)' : 'வருங்கால மனு (Future)');
        return `
          <div class="manu-card ${isCurrent ? 'current-manu' : ''}">
            <span class="manu-badge ${badgeClass}">${m.order}. ${badgeLabel}</span>
            <div class="manu-title">${m.name}</div>
            <div class="manu-details">
              <div><strong>தோற்றம்:</strong> ${m.parentage}</div>
              <div><strong>இந்திரன்:</strong> ${m.indra} | <strong>அவதாரம்:</strong> ${m.avatar}</div>
              <div style="margin-top: 4px;"><strong>சப்தரிஷிகள்:</strong> ${m.saptarshis.slice(0, 4).join(', ')}...</div>
              <div style="font-size: 0.78rem; color: #38bdf8; margin-top: 6px; font-family: monospace;">📖 ${m.scriptural_reference}</div>
            </div>
          </div>
        `;
      }).join('');
    }

    // 3. Render Surya Vamsham Milestones (Level 3)
    function renderSuryaTree() {
      const container = document.getElementById('suryaTimelineTree');
      if (!container || !window.GKD_GENEALOGY.section_4_surya_vamsha) return;
      const kings = window.GKD_GENEALOGY.section_4_surya_vamsha.lineage;

      // Select hallmark milestone kings for timeline presentation
      const hallmarks = [1, 2, 3, 11, 19, 23, 29, 30, 38, 41, 42, 45, 50, 56, 58, 60, 61, 62, 79, 85, 91, 112, 113, 119];
      const milestoneKings = kings.filter(k => hallmarks.includes(k.gen));

      container.innerHTML = milestoneKings.map(k => `
        <div class="tree-milestone">
          <div class="milestone-card" onclick="openKingModal('surya', ${k.gen})">
            <div class="milestone-header">
              <span class="milestone-name">${k.name}</span>
              <span class="milestone-gen-badge">தலைமுறை ${k.gen} (Gen ${k.gen})</span>
            </div>
            <div class="milestone-epithet">${k.epithet}</div>
            <div class="milestone-desc">${k.notes || 'அயோத்தியை தலைநகராகக் கொண்டு ஆட்சி புரிந்த சூரியகுல சக்கரவர்த்தி.'}</div>
            <div class="milestone-scriptures">
              <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
              <span>விஷ்ணு புராணம் 4.1-4, வால்மீகி ராமாயணம் பால-70, ரகுவம்சம்</span>
            </div>
          </div>
        </div>
      `).join('');
    }

    // 4. Render Chandra Vamsham Milestones (Level 3)
    function renderChandraTree() {
      const container = document.getElementById('chandraTimelineTree');
      if (!container || !window.GKD_GENEALOGY.section_5_chandra_vamsha) return;
      const cv = window.GKD_GENEALOGY.section_5_chandra_vamsha;
      const puruLine = cv.five_sons_of_yayati_and_five_royal_houses.branch_2_puru.key_sub_lineage;
      const yaduLine = cv.five_sons_of_yayati_and_five_royal_houses.branch_1_yadu.key_sub_lineage;

      let html = '';

      // Roots
      cv.origin_chain.forEach(node => {
        html += `
          <div class="tree-milestone lunar">
            <div class="milestone-card">
              <div class="milestone-header">
                <span class="milestone-name">${node.name}</span>
                <span class="milestone-gen-badge">மூலத் தோற்றம் (Origin)</span>
              </div>
              <div class="milestone-desc">${node.notes}</div>
            </div>
          </div>
        `;
      });

      // Puru Hallmark Kings
      puruLine.forEach((p, idx) => {
        html += `
          <div class="tree-milestone lunar">
            <div class="milestone-card">
              <div class="milestone-header">
                <span class="milestone-name">${p.name}</span>
                <span class="milestone-gen-badge">புரு-பாண்டவ கிளை</span>
              </div>
              <div class="milestone-desc">${p.role}</div>
            </div>
          </div>
        `;
      });

      container.innerHTML = html;
    }

    // 5. Render Gotras Grid
    function renderGotras() {
      const container = document.getElementById('gotrasGrid');
      if (!container) return;
      const gotras = [
        { name: "கௌசிக / விஸ்வாமித்திர கோத்திரம் (Vishvamitra)", pravara: "விஸ்வாமித்திர, மாரீச, கௌசிக த்ரயார்ஷேய பிரவரம்", origin: "கன்னியாகுப்ஜ அரசர் காதி மகன்; காயத்ரி மந்திர திருஷ்டா." },
        { name: "கௌதம கோத்திரம் (Gautama)", pravara: "ஆங்கீரச, ஆயாஸ்ய, கௌதம த்ரயார்ஷேய பிரவரம்", origin: "அஹல்யையின் பர்த்தா; ந்யாய சாஸ்திர பிரவர்த்தகர்." },
        { name: "பாரத்வாஜ கோத்திரம் (Bharadvaja)", pravara: "ஆங்கீரச, பார்ஹஸ்பத்ய, பாரத்வாஜ த்ரயார்ஷேய பிரவரம்", origin: "பிருஹஸ்பதியின் புதல்வர்; ஆயுர்வேதத்திலும் தனுர்வேதத்திலும் இணையற்றவர்." },
        { name: "வசிஷ்ட கோத்திரம் (Vashistha)", pravara: "வாசிஷ்ட, சாக்ர, பாராசர்ய பிரவரம்", origin: "பிரம்மனின் பிராண புதல்வர்; இக்ஷ்வாகு குல குரு; அருந்ததியின் பர்த்தா." },
        { name: "காசியப கோத்திரம் (Kashyapa)", pravara: "காச்யப, ஆவத்ஸார, நைத்ருவ த்ரயார்ஷேய பிரவரம்", origin: "மரீசியின் புதல்வர்; தேவர்கள், ஆதித்யர்கள் மற்றும் மானவர்களின் மூல தந்தை." },
        { name: "அகஸ்திய கோத்திரம் (Agastya)", pravara: "ஆகஸ்த்ய, தார்டவ்யுத, சௌமவாஹ பிரவரம்", origin: "தமிழுக்கு இலக்கணம் தந்த குறுமுனி; விந்திய மலையை அடக்கிய தென்னாட்டு ஞானக்கொடை." },
        { name: "ஆத்ரேய கோத்திரம் (Atri)", pravara: "ஆத்ரேய, அர்ச்சநானச, சியாவாச்வ த்ரயார்ஷேய பிரவரம்", origin: "அனுசூயையின் பர்த்தா; தத்தாத்ரேயர் மற்றும் சந்திரனின் பிதா." },
        { name: "ஜாமதக்னிய / பார்கவ கோத்திரம் (Jamadagni)", pravara: "பார்கவ, சியாவன, ஆப்னவான, ஔர்வ, ஜாமதக்ந்ய பஞ்சார்ஷேய பிரவரம்", origin: "பிருகு வம்சம்; ரேணுகா தேவியின் பர்த்தா; பரசுராமரின் பிதா." }
      ];

      container.innerHTML = gotras.map(g => `
        <div class="prajapati-card" style="border-left: 4px solid #10b981;">
          <div class="prajapati-name" style="color: #6ee7b7;">${g.name}</div>
          <div style="font-size: 0.82rem; color: #fde047; margin: 4px 0 8px 0; font-family: monospace;">${g.pravara}</div>
          <div class="prajapati-info">${g.origin}</div>
        </div>
      `).join('');
    }

    // 6. Render Concordance Table
    function renderConcordance() {
      const tbody = document.getElementById('concordanceTableBody');
      if (!tbody || !window.GKD_GENEALOGY.section_5_twelve_puranas_concordance) return;
      const list = window.GKD_GENEALOGY.section_5_twelve_puranas_concordance.concordance_table;

      tbody.innerHTML = list.map(c => `
        <tr>
          <td><strong style="color: #fed7aa; font-size: 1rem;">${c.purana}</strong></td>
          <td><span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 2px 8px; border-radius: 6px; font-size: 0.82rem; font-weight: 600;">${c.genealogical_location}</span></td>
          <td>${c.special_focus}</td>
          <td style="font-family: serif; color: #a7f3d0; font-size: 0.95rem;">${c.key_sanskrit_verses}</td>
        </tr>
      `).join('');
    }

    // 7. Interactive Explorer Rendering
    function renderExplorer() {
      const container = document.getElementById('explorerResultsGrid');
      const countText = document.getElementById('explorerCountText');
      if (!container) return;

      const suryaKings = window.GKD_GENEALOGY.section_4_surya_vamsha ? window.GKD_GENEALOGY.section_4_surya_vamsha.lineage : [];
      const puruKings = window.GKD_GENEALOGY.section_5_chandra_vamsha ? window.GKD_GENEALOGY.section_5_chandra_vamsha.five_sons_of_yayati_and_five_royal_houses.branch_2_puru.key_sub_lineage : [];
      const yaduKings = window.GKD_GENEALOGY.section_5_chandra_vamsha ? window.GKD_GENEALOGY.section_5_chandra_vamsha.five_sons_of_yayati_and_five_royal_houses.branch_1_yadu.key_sub_lineage : [];
      const prajapatis = window.GKD_GENEALOGY.section_1_cosmic_origin ? window.GKD_GENEALOGY.section_1_cosmic_origin.manasaputras_and_prajapatis : [];
      const manus = window.GKD_GENEALOGY.section_2_the_14_manus || [];

      let items = [];

      if (currentFilter === 'all' || currentFilter === 'surya') {
        suryaKings.forEach(k => {
          items.push({
            name: k.name,
            tag: `சூரிய வம்சம் • தலைமுறை ${k.gen}`,
            type: 'surya',
            desc: `${k.epithet} — ${k.notes}`,
            ref: 'விஷ்ணு புராணம் 4.1-4, ஸ்ரீமத் பாகவதம் 9.1-12'
          });
        });
      }

      if (currentFilter === 'all' || currentFilter === 'chandra') {
        puruKings.forEach(k => {
          items.push({
            name: k.name,
            tag: 'சந்திர வம்சம் • புரு-பாண்டவர் மரபு',
            type: 'chandra',
            desc: k.role,
            ref: 'மகாபாரதம் ஆதி பர்வம், பாகவதம் 9.20-22'
          });
        });
        yaduKings.forEach(k => {
          items.push({
            name: k.name,
            tag: 'சந்திர வம்சம் • யாதவ-கிருஷ்ண மரபு',
            type: 'chandra',
            desc: k.role,
            ref: 'ஹரிவம்சம் 1.30-38, பாகவதம் 9.23-24'
          });
        });
      }

      if (currentFilter === 'all' || currentFilter === 'prajapati') {
        prajapatis.forEach(p => {
          items.push({
            name: `${p.name} Maharshi`,
            tag: `பிரஜாபதி • ${p.origin}`,
            type: 'prajapati',
            desc: `தேவி: ${p.consort}. வம்ச சந்ததிகள்: ${p.prominent_descendants}`,
            ref: p.scriptural_reference
          });
        });
      }

      if (currentFilter === 'all' || currentFilter === 'manu') {
        manus.forEach(m => {
          items.push({
            name: m.name,
            tag: `${m.order}-ஆம் மனு (${m.epoch})`,
            type: 'manu',
            desc: `தோற்றம்: ${m.parentage}. அவதாரம்: ${m.avatar}. இந்திரன்: ${m.indra}`,
            ref: m.scriptural_reference
          });
        });
      }

      // Filter by search term
      if (currentSearchTerm.trim()) {
        const q = currentSearchTerm.toLowerCase();
        items = items.filter(it => it.name.toLowerCase().includes(q) || it.desc.toLowerCase().includes(q) || it.tag.toLowerCase().includes(q));
      }

      if (countText) {
        countText.innerText = `காண்பிக்கப்படும் முன்னோர்கள்: ${items.length}`;
      }

      container.innerHTML = items.slice(0, 100).map(it => {
        const borderCol = it.type === 'surya' ? '#f59e0b' : (it.type === 'chandra' ? '#3b82f6' : (it.type === 'prajapati' ? '#10b981' : '#a855f7'));
        return `
          <div class="prajapati-card" style="border-left: 4px solid ${borderCol};">
            <div class="prajapati-card-header">
              <span class="prajapati-name">${it.name}</span>
              <span class="prajapati-origin-tag" style="background: rgba(255,255,255,0.06); color: #cbd5e1;">${it.tag}</span>
            </div>
            <div class="prajapati-info">${it.desc}</div>
            <div class="prajapati-scripture">📖 ${it.ref}</div>
          </div>
        `;
      }).join('');
    }

    function handleSearch(val) {
      currentSearchTerm = val;
      renderExplorer();
    }

    function handleFilter(val) {
      currentFilter = val;
      renderExplorer();
    }

    function filterLineage(val) {
      const searchBox = document.getElementById('ancestorSearchInput');
      const clearBtn = document.getElementById('contextSearchClear');
      if (searchBox) searchBox.value = val;
      if (clearBtn) clearBtn.style.display = val ? 'block' : 'none';
      handleSearch(val);
      // smoothly scroll down to explorer
      const sec = document.getElementById('dynasty_explorer');
      if (sec && val.length > 2) {
        sec.scrollIntoView({ behavior: 'smooth' });
      }
    }

    function clearLineageSearch() {
      const topInput = document.getElementById('contextQuickSearch');
      const searchBox = document.getElementById('ancestorSearchInput');
      const clearBtn = document.getElementById('contextSearchClear');
      if (topInput) topInput.value = '';
      if (searchBox) searchBox.value = '';
      if (clearBtn) clearBtn.style.display = 'none';
      handleSearch('');
    }

    // Tab switcher
    function switchDynastyTab(tab) {
      document.getElementById('tabSuryaBtn').classList.remove('active');
      document.getElementById('tabChandraBtn').classList.remove('active');
      document.getElementById('tabGotraBtn').classList.remove('active');

      document.getElementById('suryaTabContent').style.display = 'none';
      document.getElementById('chandraTabContent').style.display = 'none';
      document.getElementById('gotraTabContent').style.display = 'none';

      if (tab === 'surya') {
        document.getElementById('tabSuryaBtn').classList.add('active');
        document.getElementById('suryaTabContent').style.display = 'block';
      } else if (tab === 'chandra') {
        document.getElementById('tabChandraBtn').classList.add('active');
        document.getElementById('chandraTabContent').style.display = 'block';
      } else if (tab === 'gotra') {
        document.getElementById('tabGotraBtn').classList.add('active');
        document.getElementById('gotraTabContent').style.display = 'block';
      }
    }

    // Modal Details
    function openPrajapatiModal(idx) {
      const p = window.GKD_GENEALOGY.section_1_cosmic_origin.manasaputras_and_prajapatis[idx];
      const modal = document.getElementById('ancestorModal');
      const content = document.getElementById('modalContent');
      if (!modal || !content || !p) return;

      content.innerHTML = `
        <div style="font-size: 0.85rem; color: #f97316; font-weight: 700; text-transform: uppercase;">பிரம்மனின் மானஸபுத்திரர் • Prajapati ${idx + 1}</div>
        <h2 style="color: #ffffff; font-size: 1.8rem; margin: 6px 0 14px 0;">${p.name} Maharshi</h2>
        <div style="background: rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 14px; margin-bottom: 16px;">
          <div><strong style="color: #fed7aa;">பிரம்மனின் அங்கம் (Origin):</strong> ${p.origin}</div>
          <div style="margin-top: 4px;"><strong style="color: #fed7aa;">தேவி (Consort):</strong> ${p.consort}</div>
        </div>
        <div style="color: #cbd5e1; line-height: 1.6; margin-bottom: 16px;">
          <h4 style="color: #fbbf24; margin-bottom: 4px;">வம்ச வழித்தோன்றல்கள்:</h4>
          ${p.prominent_descendants}
        </div>
        <div style="background: rgba(56, 189, 248, 0.1); border-left: 3px solid #38bdf8; padding: 10px 14px; border-radius: 0 8px 8px 0; color: #7dd3fc; font-size: 0.88rem;">
          <strong>வேத & புராண ஆதாரங்கள்:</strong> ${p.scriptural_reference}
        </div>
      `;
      modal.classList.add('open');
    }

    function openKingModal(dynasty, gen) {
      const kings = window.GKD_GENEALOGY.section_4_surya_vamsha.lineage;
      const k = kings.find(item => item.gen === gen);
      const modal = document.getElementById('ancestorModal');
      const content = document.getElementById('modalContent');
      if (!modal || !content || !k) return;

      content.innerHTML = `
        <div style="font-size: 0.85rem; color: #f59e0b; font-weight: 700; text-transform: uppercase;">சூரிய வம்சம் • இக்ஷ்வாகு குலம் • தலைமுறை ${k.gen}</div>
        <h2 style="color: #ffffff; font-size: 1.8rem; margin: 6px 0 6px 0;">${k.name}</h2>
        <div style="color: #fdba74; font-weight: 600; font-size: 1.05rem; margin-bottom: 16px;">${k.epithet}</div>
        <div style="background: rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 16px; margin-bottom: 16px; color: #cbd5e1; line-height: 1.65;">
          ${k.notes || 'அயோத்தியை ஆளுகை செய்த சூரியகுல சக்கரவர்த்தி.'}
        </div>
        <div style="background: rgba(245, 158, 11, 0.1); border-left: 3px solid #f59e0b; padding: 10px 14px; border-radius: 0 8px 8px 0; color: #fde047; font-size: 0.88rem;">
          <strong>புராணக் குறிப்புகள்:</strong> விஷ்ணு புராணம் 4.2-4.4, ஸ்ரீமத் பாகவதம் ஸ்கந்தம் 9, வால்மீகி ராமாயணம் பால காண்டம் 70-ஆம் சர்க்கம்.
        </div>
      `;
      modal.classList.add('open');
    }

    function closeModal() {
      const modal = document.getElementById('ancestorModal');
      if (modal) modal.classList.remove('open');
    }
  </script>
  <script src="assets/js/main.js"></script>
</body>
</html>
'''

# Write to root who-we-are.html
root_file = os.path.join(ROOT_DIR, "who-we-are.html")
with open(root_file, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Generated {root_file}")

# Mirror to docs/who-we-are.html
docs_file = os.path.join(ROOT_DIR, "docs", "who-we-are.html")
os.makedirs(os.path.dirname(docs_file), exist_ok=True)
with open(docs_file, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Generated {docs_file}")

# Mirror to site/who-we-are.html
site_file = os.path.join(ROOT_DIR, "site", "who-we-are.html")
os.makedirs(os.path.dirname(site_file), exist_ok=True)
with open(site_file, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Generated {site_file}")

print("All who-we-are.html pages built and mirrored successfully!")
