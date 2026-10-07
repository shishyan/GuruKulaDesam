#!/usr/bin/env python3
"""
tools/curriculum/replace_all_unicode_icons.py
1. Replaces all raw unicode emoji icons in docs/*.html and main.js with modern professional SVG icons.
2. Applies universal borderless modern styling in style.css.
3. Upgrades hydrateModernIcons in main.js to automatically convert any dynamically rendered emojis.
"""

import os
import re
import glob

# Comprehensive SVG icon definitions
SVG_ICONS = {
    'home': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9.5z"/><polyline points="9 21 9 12 15 12 15 21"/></svg>',
    'temple': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v3"/><path d="M7 5h10l-1.5 4H8.5L7 5z"/><path d="M5 9h14l-1.5 5H6.5L5 9z"/><path d="M3 14h18v7H3v-7z"/><path d="M10 21v-4a2 2 0 0 1 4 0v4"/></svg>',
    'leaf': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 4 13a8.9 8.9 0 0 1 8.2-8.9 7 7 0 0 1 7.8 7.8A8.9 8.9 0 0 1 11 20z"/><path d="M12.5 4.5c.5 4.5-1 7.5-5 9.5"/></svg>',
    'om': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9.5"/><path d="M11.5 7.5c-1.8 0-2.8 1.2-2.8 2.5 0 1.8 2.5 2.2 2.5 4 0 .8-.6 1.2-1.2 1.2s-1.2-.4-1.2-1.2"/><path d="M11.5 11c.8-.8 1.8-.8 2.2 0s0 1.8-1.2 2.2"/><circle cx="14.8" cy="8.2" r=".6" fill="currentColor"/><path d="M13.5 6.5c.8 0 1.8.4 2.2 1.2"/></svg>',
    'trishul': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="M12 6c-3.5 0-6 2.5-6 6v3h2v-3c0-2.5 1.8-4 4-4s4 1.5 4 4v3h2v-3c0-3.5-2.5-6-6-6z"/><path d="M9 16h6"/><polygon points="12 2 10.5 5 13.5 5 12 2" fill="currentColor"/></svg>',
    'ganesha': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3c-4 0-7 3.5-7 7.5 0 2.5 1.2 4.7 3 6l1 4.5h6l1-4.5c1.8-1.3 3-3.5 3-6C19 6.5 16 3 12 3z"/><path d="M12 9v5a1.5 1.5 0 0 1-3 0"/><circle cx="9" cy="8" r="1" fill="currentColor"/><circle cx="15" cy="8" r="1" fill="currentColor"/></svg>',
    'vel': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22V9"/><path d="M12 2C9.5 5 7 8 7 11c0 3 2 4.5 5 5 3-.5 5-2 5-5 0-3-2.5-6-5-9z"/><line x1="9" y1="22" x2="15" y2="22"/></svg>',
    'lotus': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4c-1.5 3-2 6-2 9 1 0 2-1 2-2 0 1 1 2 2 2 0-3-.5-6-2-9z"/><path d="M7 10c0 3 1.5 5 3 6-2 0-4-1.5-4.5-4 .5-.7 1-1.3 1.5-2z"/><path d="M17 10c0 3-1.5 5-3 6 2 0 4-1.5 4.5-4-.5-.7-1-1.3-1.5-2z"/><path d="M4 15c2 3 5 4 8 4s6-1 8-4c-2.5 0-4.5 1-8 1s-5.5-1-8-1z"/></svg>',
    'chakra': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><line x1="12" y1="3" x2="12" y2="9"/><line x1="12" y1="15" x2="12" y2="21"/><line x1="3" y1="12" x2="9" y2="12"/><line x1="15" y1="12" x2="21" y2="12"/><line x1="5.6" y1="5.6" x2="9.9" y2="9.9"/><line x1="14.1" y1="14.1" x2="18.4" y2="18.4"/><line x1="18.4" y1="5.6" x2="14.1" y2="9.9"/><line x1="9.9" y1="14.1" x2="5.6" y2="18.4"/></svg>',
    'music': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>',
    'scroll': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H4a2 2 0 0 0-2 2v13a3 3 0 0 0 3 3h13a3 3 0 0 0 3-3V5a2 2 0 0 0-2-2h-7"/><path d="M19 18a3 3 0 0 0 0-6H6a2 2 0 0 0 0 4h12"/><line x1="8" y1="7" x2="14" y2="7"/><line x1="8" y1="11" x2="12" y2="11"/></svg>',
    'flame': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c1 3 3 4.5 4.5 7 1.5 2.5 1.5 5.5 0 8s-4 4-6.5 4c-3 0-5.5-2.5-5.5-6 0-3.5 2-6 4-8.5.5 1.5 1.5 2.5 2.5 2.5.5-2 .5-4.5 1-7z"/></svg>',
    'crown': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 18h20v2H2z"/><path d="M3 18l2-11 5 5 4-7 4 7 5-5 2 11H3z"/></svg>',
    'book': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
    'target': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    'school': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 2 3 3 6 3s6-1 6-3v-5"/></svg>',
    'grad': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 2 3 3 6 3s6-1 6-3v-5"/></svg>',
    'science': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="2" fill="currentColor"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(-30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(90 12 12)"/></svg>',
    'virtues': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L3 12.5V21h8.5z"/><line x1="16" y1="8" x2="2" y2="22"/><line x1="17.5" y1="15" x2="9" y2="15"/></svg>',
    'clock': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    'play': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3" fill="currentColor"/></svg>',
    'search': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    'close': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    'fullscreen': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg>',
    'bulb': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-7 7c0 2.5 1.3 4.7 3.2 6H15.8c1.9-1.3 3.2-3.5 3.2-6a7 7 0 0 0-7-7z"/></svg>',
    'pin': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="17" x2="12" y2="22"/><path d="M5 17h14l-2-6V4H7v7l-2 6z"/><line x1="9" y1="4" x2="15" y2="4"/></svg>',
    'pencil': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>',
    'palette': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>',
    'check': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    'print': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>',
    'deepam': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c-.8 2-1.5 3.5-1.5 5a1.5 1.5 0 0 0 3 0c0-1.5-.7-3-1.5-5z" fill="currentColor"/><path d="M5 13c0 4 3 6 7 6s7-2 7-6H5z"/><path d="M10 19v2h4v-2"/></svg>',
    'cinema': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="2" y1="17" x2="7" y2="17"/><line x1="17" y1="17" x2="22" y2="17"/><line x1="17" y1="7" x2="22" y2="7"/></svg>',
    'mapPin': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    'bell': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
    'question': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    'settings': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    'user': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    'back': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>',
    'theme': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>',
    'menu': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>',
    'arrowRight': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>',
    'arrowLeft': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>',
    'trophy': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2z"/></svg>',
    'medal': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="14" r="6"/><path d="M8.21 13.89L7 22l5-3 5 3-1.21-8.12"/><line x1="12" y1="2" x2="12" y2="8"/></svg>',
    'globe': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    'tierGreen': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="#10b981"><circle cx="12" cy="12" r="7"/></svg>',
    'tierYellow': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="#f59e0b"><circle cx="12" cy="12" r="7"/></svg>',
    'tierRed': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="#ef4444"><circle cx="12" cy="12" r="7"/></svg>'
}

EMOJI_TO_SVG = {
    '📍': SVG_ICONS['mapPin'],
    '🌐': SVG_ICONS['globe'],
    '👤': SVG_ICONS['user'],
    '🏆': SVG_ICONS['trophy'],
    '📜': SVG_ICONS['scroll'],
    '🎖': SVG_ICONS['medal'],
    '🔱': SVG_ICONS['trishul'],
    '🏫': SVG_ICONS['school'],
    '☀️': SVG_ICONS['flame'],
    '🎵': SVG_ICONS['music'],
    '🎶': SVG_ICONS['music'],
    '✓': SVG_ICONS['check'],
    '✔': SVG_ICONS['check'],
    '✅': SVG_ICONS['check'],
    '🌳': SVG_ICONS['leaf'],
    '🕊': SVG_ICONS['lotus'],
    '🕊️': SVG_ICONS['lotus'],
    '🏠': SVG_ICONS['home'],
    '🏡': SVG_ICONS['home'],
    '🌱': SVG_ICONS['leaf'],
    '❖': SVG_ICONS['om'],
    '🧘': SVG_ICONS['om'],
    '🔥': SVG_ICONS['flame'],
    '🧭': SVG_ICONS['target'],
    '🗂': SVG_ICONS['scroll'],
    '🗂️': SVG_ICONS['scroll'],
    '➔': SVG_ICONS['arrowRight'],
    '📚': SVG_ICONS['book'],
    '📖': SVG_ICONS['book'],
    '🪷': SVG_ICONS['lotus'],
    '🐄': SVG_ICONS['om'],
    '💧': SVG_ICONS['leaf'],
    '✨': SVG_ICONS['flame'],
    '🌟': SVG_ICONS['flame'],
    '💨': SVG_ICONS['om'],
    '🌅': SVG_ICONS['flame'],
    '🌇': SVG_ICONS['flame'],
    '👶': SVG_ICONS['user'],
    '🧹': SVG_ICONS['check'],
    '🤝': SVG_ICONS['check'],
    '🎬': SVG_ICONS['cinema'],
    '📺': SVG_ICONS['cinema'],
    '🔬': SVG_ICONS['science'],
    '🌺': SVG_ICONS['lotus'],
    '🌸': SVG_ICONS['lotus'],
    '⚡': SVG_ICONS['flame'],
    '🔴': SVG_ICONS['tierRed'],
    '🟢': SVG_ICONS['tierGreen'],
    '🟡': SVG_ICONS['tierYellow'],
    '🔤': SVG_ICONS['virtues'],
    '🪔': SVG_ICONS['deepam'],
    '🕯': SVG_ICONS['deepam'],
    '🕯️': SVG_ICONS['deepam'],
    '🏛': SVG_ICONS['temple'],
    '🏛️': SVG_ICONS['temple'],
    '🐘': SVG_ICONS['ganesha'],
    '👑': SVG_ICONS['crown'],
    '🎯': SVG_ICONS['target'],
    '🎨': SVG_ICONS['palette'],
    '❓': SVG_ICONS['question'],
    '💡': SVG_ICONS['bulb'],
    '📌': SVG_ICONS['pin'],
    '✍': SVG_ICONS['pencil'],
    '✍️': SVG_ICONS['pencil'],
    '🎓': SVG_ICONS['grad'],
    '🖨': SVG_ICONS['print'],
    '🖨️': SVG_ICONS['print'],
    '⚙': SVG_ICONS['settings'],
    '⚙️': SVG_ICONS['settings'],
    '⏱': SVG_ICONS['clock'],
    '⏱️': SVG_ICONS['clock'],
    '⏰': SVG_ICONS['clock'],
    '▶': SVG_ICONS['play'],
    '▶️': SVG_ICONS['play'],
    '🥛': SVG_ICONS['lotus'],
    '🙏': SVG_ICONS['lotus'],
    '🇮🇳': SVG_ICONS['temple'],
    '🧑‍🏫': SVG_ICONS['user'],
    '💎': SVG_ICONS['om'],
    '❤️': SVG_ICONS['lotus'],
    '🛡': SVG_ICONS['trishul'],
    '🛡️': SVG_ICONS['trishul'],
    '⛶': SVG_ICONS['fullscreen'],
    '✕': SVG_ICONS['close']
}

def clean_html_emojis(repo_root):
    docs_dir = os.path.join(repo_root, 'docs')
    total_replaced = 0
    for f in glob.glob(os.path.join(docs_dir, '*.html')):
        with open(f, 'r', encoding='utf-8') as fl:
            content = fl.read()

        replaced_in_file = 0
        for emoji_char, svg_html in EMOJI_TO_SVG.items():
            if emoji_char in content:
                count = content.count(emoji_char)
                content = content.replace(emoji_char, svg_html)
                replaced_in_file += count

        if replaced_in_file > 0:
            with open(f, 'w', encoding='utf-8') as fl:
                fl.write(content)
            total_replaced += replaced_in_file
            print(f"[OK] Replaced {replaced_in_file} unicode icons with SVGs in {os.path.basename(f)}")

    print(f"Total unicode emojis replaced in HTML: {total_replaced}")

def clean_css_borders(repo_root):
    css_path = os.path.join(repo_root, 'docs', 'assets', 'css', 'style.css')
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Neutralize border color variables in :root
    content = content.replace('--border-subtle: rgba(56, 189, 248, 0.14);', '--border-subtle: transparent;')
    content = content.replace('--border-gold: rgba(45, 212, 191, 0.32);', '--border-gold: transparent;')
    content = content.replace('--border-gold-hover: rgba(56, 189, 248, 0.65);', '--border-gold-hover: transparent;')

    # 2. Add universal borderless reset rule block if not already present
    borderless_block = """
/* ==========================================================================
   BORDERLESS MODERN DESIGN SYSTEM (UNIVERSAL BORDER REMOVAL)
   ========================================================================== */
*, *::before, *::after {
  border-color: transparent !important;
}

.card, .virtue-card, .video-card, .showcase-visual-card, .grade-card,
.degree-program-card, .lesson-unit-panel, .canonical-card, .sheet-item,
.pat-level-card, .guide-selector-card, .guide-section-box, .help-hero-banner,
.hero-banner, .dedicated-page-tabs-container, .dedicated-tab-pill,
.context-top-bar, .left-strip-bar, .header-back-btn, .context-tool-btn,
.site-header, .context-sensitive-bar, .objectives-card, .scripture-study-section,
.vedic-verse-box, .stem-fusion-card, .degree-tier-card, .degree-highlight-box,
.modal-box, .player-modal-box, .user-modal-box, .universal-search-box,
.profile-hero-card, .stat-pill, .family-charter-sheet, .charter-theme-gold,
.charter-theme-emerald, .charter-theme-indigo, .google-site-banner,
.grade-lms-tracker-banner, .portal-kpi-card, .study-hall-card, .cert-preview-card,
.flashcard, .context-bar-container, .header-container, .header-breadcrumbs,
.strip-footer-dock, .strip-item, .strip-sub-menu, .strip-header,
.filter-btn, .course-tab-btn, .modal-header, .search-result-item,
.modal-details, .modal-meta-row, .modal-meta-tag, .modal-btn,
.context-tabs-nav, .context-tab-pill, .sheet-modal-box, .sheet-modal-header,
.primary-hamburger-btn, .strip-brand-link, .strip-toggle-btn, .context-profile-pill,
.avatar-option, .settings-form-group, .settings-input, .settings-select,
.universal-search-header, .universal-search-input, .universal-search-close,
.faq-accordion-item, .faq-question-btn, .faq-answer-panel, .showcase-visual-caption {
  border: none !important;
  border-top: none !important;
  border-bottom: none !important;
  border-left: none !important;
  border-right: none !important;
  outline: none !important;
}

.showcase-visual-card, .grade-card, .virtue-card, .video-card,
.degree-program-card, .canonical-card, .sheet-item, .guide-selector-card,
.guide-section-box, .help-hero-banner, .dedicated-page-tabs-container {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45) !important;
}

.showcase-visual-card:hover, .grade-card:hover, .virtue-card:hover,
.video-card:hover, .degree-program-card:hover, .guide-selector-card:hover {
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.65), 0 0 25px rgba(56, 189, 248, 0.18) !important;
}
"""
    if "BORDERLESS MODERN DESIGN SYSTEM" not in content:
        content += "\n" + borderless_block
        print("[OK] Appended Universal Borderless Modern Design Rules to style.css")

    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(content)

def clean_main_js(repo_root):
    js_path = os.path.join(repo_root, 'docs', 'assets', 'js', 'main.js')
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update hydrateModernIcons to replace any text emoji across the entire DOM tree
    enhanced_hydrator = """// Global DOM Icon Hydrator (Comprehensive Universal Replacement)
function hydrateModernIcons(root) {
  const container = root || document.body;
  if (!container) return;

  const emojiMap = {
    '🏛️': GKD_ICONS.temple, '🏛': GKD_ICONS.temple, '🏠': GKD_ICONS.home, '🏡': GKD_ICONS.home,
    '🌿': GKD_ICONS.leaf, '🕉️': GKD_ICONS.om, '🕉': GKD_ICONS.om, '🎵': GKD_ICONS.music,
    '🎶': GKD_ICONS.music, '📜': GKD_ICONS.scroll, '✨': GKD_ICONS.flame, '🌟': GKD_ICONS.flame,
    '🔥': GKD_ICONS.flame, '👑': GKD_ICONS.crown, '📖': GKD_ICONS.book, '📚': GKD_ICONS.book,
    '🎯': GKD_ICONS.target, '🏫': GKD_ICONS.school, '🔬': GKD_ICONS.science, '🔤': GKD_ICONS.virtues,
    '⏰': GKD_ICONS.clock, '⏱️': GKD_ICONS.clock, '⏱': GKD_ICONS.clock, '🔱': GKD_ICONS.trishul,
    '🐘': GKD_ICONS.ganesha, '🪶': GKD_ICONS.vel, '🌸': GKD_ICONS.lotus, '🪷': GKD_ICONS.lotus,
    '▶️': GKD_ICONS.play, '▶': GKD_ICONS.play, '🎬': GKD_ICONS.cinema, '📺': GKD_ICONS.cinema,
    '🔍': GKD_ICONS.search, '💡': GKD_ICONS.bulb, '📌': GKD_ICONS.pin, '✍️': GKD_ICONS.pencil,
    '✍': GKD_ICONS.pencil, '🎨': GKD_ICONS.palette, '🎓': GKD_ICONS.grad, '✓': GKD_ICONS.check,
    '✔': GKD_ICONS.check, '✅': GKD_ICONS.check, '🖨️': GKD_ICONS.print, '🖨': GKD_ICONS.print,
    '🪔': GKD_ICONS.deepam, '🕯️': GKD_ICONS.deepam, '🕯': GKD_ICONS.deepam, '📍': GKD_ICONS.mapPin,
    '⚙️': GKD_ICONS.settings, '⚙': GKD_ICONS.settings, '👤': GKD_ICONS.user, '❓': GKD_ICONS.question,
    '⛶': GKD_ICONS.fullscreen, '✕': GKD_ICONS.close, '➔': GKD_ICONS.arrowRight, '🏆': GKD_ICONS.trophy,
    '🎖': GKD_ICONS.medal, '🌐': GKD_ICONS.globe, '🌳': GKD_ICONS.leaf, '🕊️': GKD_ICONS.lotus,
    '🕊': GKD_ICONS.lotus, '🌱': GKD_ICONS.leaf, '❖': GKD_ICONS.om, '🧘': GKD_ICONS.om,
    '🧭': GKD_ICONS.target, '🗂️': GKD_ICONS.scroll, '🗂': GKD_ICONS.scroll, '🐄': GKD_ICONS.om,
    '💧': GKD_ICONS.leaf, '💨': GKD_ICONS.om, '🌅': GKD_ICONS.flame, '🌇': GKD_ICONS.flame,
    '👶': GKD_ICONS.user, '🧹': GKD_ICONS.check, '🤝': GKD_ICONS.check, '🌺': GKD_ICONS.lotus,
    '⚡': GKD_ICONS.flame, '🔴': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="#ef4444"><circle cx="12" cy="12" r="7"/></svg>',
    '🟢': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="#10b981"><circle cx="12" cy="12" r="7"/></svg>',
    '🟡': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="#f59e0b"><circle cx="12" cy="12" r="7"/></svg>'
  };

  // 1. Check targeted icon containers
  const targets = container.querySelectorAll('.strip-item-icon, .strip-sub-icon, .card-type, .badge, .btn-icon, .search-icon, .item-badge, .pill-avatar, .drone-icon, .theme-icon, .source-badge, .sacred-tag, .avatar-option');
  targets.forEach(el => {
    const txt = el.textContent.trim();
    if (emojiMap[txt]) {
      el.innerHTML = emojiMap[txt];
    }
  });

  // 2. TreeWalker to catch raw emojis anywhere in text nodes
  const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, null, false);
  const nodesToReplace = [];
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (node.parentElement && ['SCRIPT', 'STYLE', 'TEXTAREA'].includes(node.parentElement.tagName)) continue;
    for (const em in emojiMap) {
      if (node.nodeValue.includes(em)) {
        nodesToReplace.push({ node, em, svg: emojiMap[em] });
      }
    }
  }

  nodesToReplace.forEach(({ node, em, svg }) => {
    if (!node.parentNode) return;
    const span = document.createElement('span');
    span.className = 'icon-svg-box';
    span.innerHTML = svg;
    const parts = node.nodeValue.split(em);
    const fragment = document.createDocumentFragment();
    parts.forEach((p, idx) => {
      if (p) fragment.appendChild(document.createTextNode(p));
      if (idx < parts.length - 1) fragment.appendChild(span.cloneNode(true));
    });
    node.parentNode.replaceChild(fragment, node);
  });
}"""

    # Replace old hydrateModernIcons block
    old_hydrator = re.search(r'// Global DOM Icon Hydrator.*?function hydrateModernIcons\(root\)\s*\{.*?\n\}', content, re.DOTALL)
    if old_hydrator:
        content = content[:old_hydrator.start()] + enhanced_hydrator + content[old_hydrator.end():]
        print("[OK] Replaced hydrateModernIcons with Universal TreeWalker Hydrator in main.js")

    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    print("=== Guru Kula Desam: Icon & Border Upgrade Engine ===")
    clean_html_emojis(repo_root)
    clean_css_borders(repo_root)
    clean_main_js(repo_root)
    print("\n[OK] Upgrades successfully executed!")

if __name__ == '__main__':
    main()
