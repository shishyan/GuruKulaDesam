// Modern Professional SVG Icon System
const GKD_ICONS = {
  home: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9.5z"/><polyline points="9 21 9 12 15 12 15 21"/></svg>',
  temple: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v3"/><path d="M7 5h10l-1.5 4H8.5L7 5z"/><path d="M5 9h14l-1.5 5H6.5L5 9z"/><path d="M3 14h18v7H3v-7z"/><path d="M10 21v-4a2 2 0 0 1 4 0v4"/></svg>',
  leaf: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 4 13a8.9 8.9 0 0 1 8.2-8.9 7 7 0 0 1 7.8 7.8A8.9 8.9 0 0 1 11 20z"/><path d="M12.5 4.5c.5 4.5-1 7.5-5 9.5"/></svg>',
  tree: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22v-8"/><path d="M12 14c-4 0-7-3-7-6a7 7 0 0 1 14 0c0 3-3 6-7 6z"/></svg>',
  om: '<svg class="gkd-icon gkd-om-icon" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8.2 10.5c-.3-.7-.2-1.5.3-2.1.8-.9 2.2-.9 3 .1.4.5.5 1.2.2 1.8-.4.7-1.1 1.2-1.7 1.7.9.3 1.7.9 2 1.7.4 1.1 0 2.4-1 3.1-1.2.9-2.9.7-3.9-.4-.4-.5-.6-1.1-.6-1.7h1.4c0 .4.2.8.5 1 .6.5 1.5.4 2-.1.4-.4.5-1 .2-1.5-.4-.7-1.2-1-2-1v-1.2c.6 0 1.2-.2 1.5-.7.3-.4.3-.9 0-1.3-.4-.5-1.1-.6-1.6-.2-.3.2-.5.6-.5 1H8.2zm6.3-2.5c.8 0 1.5.5 1.8 1.2l-1.2.5c-.2-.4-.5-.6-.8-.6-.6 0-1 .4-1 1s.4 1 1 1c.5 0 .9-.3 1.1-.7l1.1.6c-.4.8-1.2 1.3-2.2 1.3-1.4 0-2.4-1-2.4-2.4 0-1.3 1-2.4 2.4-2.4zm1.5-1.5c.3 0 .5.2.5.5s-.2.5-.5.5-.5-.2-.5-.5.2-.5.5-.5z"/></svg>',
  trishul: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20"/><path d="M12 6c-3.5 0-6 2.5-6 6v3h2v-3c0-2.5 1.8-4 4-4s4 1.5 4 4v3h2v-3c0-3.5-2.5-6-6-6z"/><path d="M9 16h6"/><polygon points="12 2 10.5 5 13.5 5 12 2" fill="currentColor"/></svg>',
  ganesha: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3c-4 0-7 3.5-7 7.5 0 2.5 1.2 4.7 3 6l1 4.5h6l1-4.5c1.8-1.3 3-3.5 3-6C19 6.5 16 3 12 3z"/><path d="M12 9v5a1.5 1.5 0 0 1-3 0"/><circle cx="9" cy="8" r="1" fill="currentColor"/><circle cx="15" cy="8" r="1" fill="currentColor"/></svg>',
  vel: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22V9"/><path d="M12 2C9.5 5 7 8 7 11c0 3 2 4.5 5 5 3-.5 5-2 5-5 0-3-2.5-6-5-9z"/><line x1="9" y1="22" x2="15" y2="22"/></svg>',
  lotus: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4c-1.5 3-2 6-2 9 1 0 2-1 2-2 0 1 1 2 2 2 0-3-.5-6-2-9z"/><path d="M7 10c0 3 1.5 5 3 6-2 0-4-1.5-4.5-4 .5-.7 1-1.3 1.5-2z"/><path d="M17 10c0 3-1.5 5-3 6 2 0 4-1.5 4.5-4-.5-.7-1-1.3-1.5-2z"/><path d="M4 15c2 3 5 4 8 4s6-1 8-4c-2.5 0-4.5 1-8 1s-5.5-1-8-1z"/></svg>',
  chakra: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><line x1="12" y1="3" x2="12" y2="9"/><line x1="12" y1="15" x2="12" y2="21"/><line x1="3" y1="12" x2="9" y2="12"/><line x1="15" y1="12" x2="21" y2="12"/><line x1="5.6" y1="5.6" x2="9.9" y2="9.9"/><line x1="14.1" y1="14.1" x2="18.4" y2="18.4"/><line x1="18.4" y1="5.6" x2="14.1" y2="9.9"/><line x1="9.9" y1="14.1" x2="5.6" y2="18.4"/></svg>',
  music: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>',
  scroll: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H4a2 2 0 0 0-2 2v13a3 3 0 0 0 3 3h13a3 3 0 0 0 3-3V5a2 2 0 0 0-2-2h-7"/><path d="M19 18a3 3 0 0 0 0-6H6a2 2 0 0 0 0 4h12"/><line x1="8" y1="7" x2="14" y2="7"/><line x1="8" y1="11" x2="12" y2="11"/></svg>',
  flame: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c1 3 3 4.5 4.5 7 1.5 2.5 1.5 5.5 0 8s-4 4-6.5 4c-3 0-5.5-2.5-5.5-6 0-3.5 2-6 4-8.5.5 1.5 1.5 2.5 2.5 2.5.5-2 .5-4.5 1-7z"/></svg>',
  crown: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 18h20v2H2z"/><path d="M3 18l2-11 5 5 4-7 4 7 5-5 2 11H3z"/></svg>',
  book: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
  target: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
  school: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 2 3 3 6 3s6-1 6-3v-5"/></svg>',
  grad: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 2 3 3 6 3s6-1 6-3v-5"/></svg>',
  science: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="2" fill="currentColor"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(-30 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(90 12 12)"/></svg>',
  virtues: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L3 12.5V21h8.5z"/><line x1="16" y1="8" x2="2" y2="22"/><line x1="17.5" y1="15" x2="9" y2="15"/></svg>',
  clock: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
  play: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>',
  search: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
  close: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
  fullscreen: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg>',
  bulb: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-7 7c0 2.5 1.3 4.7 3.2 6H15.8c1.9-1.3 3.2-3.5 3.2-6a7 7 0 0 0-7-7z"/></svg>',
  pin: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
  pencil: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>',
  palette: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>',
  check: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
  print: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>',
  chevronDown: '<svg class="gkd-icon gkd-sub-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>',
  chevronUp: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>',
  chevronRight: '<svg class="gkd-icon gkd-chevron-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>',
  deepam: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c-.8 2-1.5 3.5-1.5 5a1.5 1.5 0 0 0 3 0c0-1.5-.7-3-1.5-5z" fill="currentColor"/><path d="M5 13c0 4 3 6 7 6s7-2 7-6H5z"/><path d="M10 19v2h4v-2"/></svg>',
  cinema: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="2.18"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="2" y1="17" x2="7" y2="17"/><line x1="17" y1="17" x2="22" y2="17"/><line x1="17" y1="7" x2="22" y2="7"/></svg>',
  mapPin: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
  bell: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
  question: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
  settings: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
  user: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
  external: '<svg class="gkd-icon gkd-external-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>',
  arrowRight: '<svg class="gkd-icon gkd-arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
  arrowLeft: '<svg class="gkd-icon gkd-arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>',
  arrowUp: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>',
  copy: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>',
  pranam: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 11V6a2 2 0 0 0-2-2 2 2 0 0 0-2 2v3"/><path d="M14 10V4a2 2 0 0 0-2-2 2 2 0 0 0-2 2v6"/><path d="M10 10.5V6a2 2 0 0 0-2-2 2 2 0 0 0-2 2v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.83L7 15"/></svg>',
  headphone: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>',
  star: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
  starEmpty: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
  sound: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>',
  mute: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/></svg>',
  theme: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>'
};

// Global DOM Icon Hydrator
function hydrateModernIcons(root) {
  const container = root || document.body;
  if (!container) return;

  const emojiMap = {
    '🏛️': GKD_ICONS.temple, '🏛': GKD_ICONS.temple, '🏠': GKD_ICONS.home, '🏡': GKD_ICONS.home,
    '🌿': GKD_ICONS.leaf, '🌱': GKD_ICONS.leaf, '🍃': GKD_ICONS.leaf, '🌳': GKD_ICONS.tree,
    '🕉️': GKD_ICONS.om, '🕉': GKD_ICONS.om, 'ॐ': GKD_ICONS.om,
    '🎵': GKD_ICONS.music, '🎶': GKD_ICONS.music, '🎧': GKD_ICONS.headphone,
    '📜': GKD_ICONS.scroll, '✨': GKD_ICONS.flame, '🌟': GKD_ICONS.flame, '🔥': GKD_ICONS.flame,
    '👑': GKD_ICONS.crown, '⚜️': GKD_ICONS.crown, '⚜': GKD_ICONS.crown,
    '📖': GKD_ICONS.book, '📚': GKD_ICONS.book, '🎯': GKD_ICONS.target,
    '🏫': GKD_ICONS.school, '🎓': GKD_ICONS.grad, '🔬': GKD_ICONS.science,
    '🔤': GKD_ICONS.virtues, '⏰': GKD_ICONS.clock, '🔱': GKD_ICONS.trishul,
    '🐘': GKD_ICONS.ganesha, '🪶': GKD_ICONS.vel, '🌸': GKD_ICONS.lotus, '🌺': GKD_ICONS.lotus, '🪷': GKD_ICONS.lotus,
    '▶️': GKD_ICONS.play, '▶': GKD_ICONS.play, '🎬': GKD_ICONS.cinema, '📺': GKD_ICONS.cinema,
    '🔍': GKD_ICONS.search, '💡': GKD_ICONS.bulb, '📌': GKD_ICONS.pin,
    '✍️': GKD_ICONS.pencil, '✍': GKD_ICONS.pencil, '🎨': GKD_ICONS.palette,
    '✓': GKD_ICONS.check, '✔': GKD_ICONS.check, '✅': GKD_ICONS.check,
    '🖨️': GKD_ICONS.print, '🖨': GKD_ICONS.print, '🪔': GKD_ICONS.deepam,
    '📍': GKD_ICONS.mapPin, '⚙️': GKD_ICONS.settings, '⚙': GKD_ICONS.settings,
    '👤': GKD_ICONS.user, '🧑': GKD_ICONS.user, '❓': GKD_ICONS.question,
    '🏆': GKD_ICONS.star, '🎖': GKD_ICONS.star, '💎': GKD_ICONS.om,
    '🌍': GKD_ICONS.temple, '🌐': GKD_ICONS.temple, '🙏': GKD_ICONS.pranam,
    '📋': GKD_ICONS.copy, '🔔': GKD_ICONS.bell, '🔊': GKD_ICONS.sound, '🔕': GKD_ICONS.mute,
    '✕': GKD_ICONS.close, '✖': GKD_ICONS.close, '☰': '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>'
  };

  const targets = container.querySelectorAll('.strip-item-icon, .strip-sub-icon, .card-type, .badge, .btn-icon, .search-icon, .item-badge, .ashram-pedagogy-icon, .strip-dock-icon, .hb-icon, .context-tab-pill-icon, .dropdown-item-icon, .modal-box-icon');
  targets.forEach(el => {
    const txt = el.textContent.trim();
    if (emojiMap[txt]) {
      el.innerHTML = emojiMap[txt];
    }
  });
}


// Guru Kula Desam - Modern Video Portal Logic with Full Lyrics & Meaning Support
let currentFilter = 'all';
let currentSearch = '';

function enrichItem(it) {
  if (!it) return it;
  const lookup = (window.GURUKULA_ITEMS_BY_ID && window.GURUKULA_ITEMS_BY_ID[it.id]) || {};
  return {
    ...lookup,
    ...it,
    author: it.author || lookup.author || '',
    source: it.source || lookup.source || '',
    lyrics: it.lyrics || lookup.lyrics || '',
    meaning: it.meaning || lookup.meaning || '',
    category: it.category || lookup.category || ''
  };
}

function initPage(itemsData) {
  if (Array.isArray(itemsData)) {
    window.pageItems = itemsData.map(enrichItem);
  } else {
    window.pageItems = [];
  }
  renderCards();
}

function getFilteredItems() {
  if (!window.pageItems) return [];
  return window.pageItems.filter(it => {
    if (currentFilter !== 'all' && it.type !== currentFilter) return false;
    if (currentSearch) {
      const q = currentSearch.toLowerCase();
      const titleMatch = (it.title || '').toLowerCase().includes(q);
      const idMatch = (it.id || '').toLowerCase().includes(q);
      const authorMatch = (it.author || '').toLowerCase().includes(q);
      const sourceMatch = (it.source || '').toLowerCase().includes(q);
      const lyricsMatch = (it.lyrics || '').toLowerCase().includes(q);
      const meaningMatch = (it.meaning || '').toLowerCase().includes(q);
      return titleMatch || idMatch || authorMatch || sourceMatch || lyricsMatch || meaningMatch;
    }
    return true;
  });
}

function escapeHtml(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function renderCards() {
  const items = getFilteredItems();
  const grid = document.getElementById('cardsGrid');
  const countBadge = document.getElementById('itemCountBadge');

  if (countBadge) {
    countBadge.innerText = `காட்டப்படும் பாடல்கள்: ${items.length}`;
  }

  if (!grid) return;

  if (items.length === 0) {
    grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 70px 20px; color: var(--text-muted); font-size: 1.15rem;">பொருத்தமான பாடல்கள் காணப்படவில்லை (No matching items found)</div>';
    return;
  }

  grid.innerHTML = items.map(it => {
    const safeTitle = escapeHtml(it.title);
    const safeAuthor = escapeHtml(it.author);
    const safeSource = escapeHtml(it.source);
    const formattedLyrics = it.lyrics ? escapeHtml(it.lyrics).replace(/\\n/g, '<br>') : '';
    const safeMeaning = escapeHtml(it.meaning);
    const hasDetails = Boolean(it.lyrics || it.meaning || it.author);

    return `
    <div class="video-card" id="card-${it.id}" onclick="if(!event.target.closest('.card-lyrics-toggle-btn, .card-lyrics-drawer, .card-yt-link, a, button')) openPlayer('${it.id}', '${safeTitle.replace(/'/g, "\\'")}')" style="cursor: pointer;">
      <div class="card-thumbnail" onclick="openPlayer('${it.id}', '${safeTitle.replace(/'/g, "\\'")}')">
        <img src="https://i.ytimg.com/vi/${it.id}/mqdefault.jpg" loading="lazy" alt="${safeTitle}">
        <span class="card-badge ${it.type === 'film' ? 'badge-film' : 'badge-audio'}">${it.type === 'film' ? 'Film' : 'Audio'}</span>
        <div class="card-play-btn" title="காணொளியை இயக்குக">${GKD_ICONS.play}</div>
      </div>
      <div class="card-body">
        <div class="card-title" onclick="openPlayer('${it.id}', '${safeTitle.replace(/'/g, "\\'")}')" title="${safeTitle}">
          ${safeTitle}
        </div>

        ${(safeAuthor || safeSource) ? `
          <div class="card-meta-line">
            ${safeAuthor ? `<span class="card-meta-tag">${GKD_ICONS.pencil} ${safeAuthor}</span>` : ''}
            ${safeSource ? `<span class="card-meta-tag">${GKD_ICONS.book} ${safeSource}</span>` : ''}
          </div>
        ` : ''}

        <div class="card-footer">
          <span class="tag">${it.type === 'film' ? `${GKD_ICONS.cinema} முழுப் படம் (Film)` : `${GKD_ICONS.music} இசை வெளியீடு (Audio)`}</span>
          <a href="https://www.youtube.com/watch?v=${it.id}" target="_blank" rel="noopener noreferrer" class="card-yt-link" onclick="event.stopPropagation()">YouTube ${GKD_ICONS.external}</a>
        </div>

        ${hasDetails ? `
          <button type="button" class="card-lyrics-toggle-btn" onclick="toggleCardLyrics(event, '${it.id}')" aria-expanded="false">
            <span>${GKD_ICONS.scroll} வரிகள் &amp; பொருள் விளக்கம்</span>
            <span class="lyrics-chevron">${GKD_ICONS.chevronDown}</span>
          </button>

          <div class="card-lyrics-drawer" id="drawer-${it.id}" style="display: none;">
            ${it.lyrics ? `
              <div class="drawer-section">
                <div class="drawer-section-title">${GKD_ICONS.scroll} பாடல் வரிகள் (Lyrics)</div>
                <div class="drawer-lyrics-text">${formattedLyrics}</div>
              </div>
            ` : ''}

            ${it.meaning ? `
              <div class="drawer-section">
                <div class="drawer-section-title">${GKD_ICONS.bulb} பொருள் விளக்கம் (Meaning)</div>
                <div class="drawer-meaning-text">${safeMeaning}</div>
              </div>
            ` : ''}

            <button type="button" class="drawer-play-btn" onclick="openPlayer('${it.id}', '${safeTitle.replace(/'/g, "\\'")}')">
              ${GKD_ICONS.play} இந்த காணொளியை இயக்குக (Play Video)
            </button>
          </div>
        ` : ''}
      </div>
    </div>
    `;
  }).join('');
}

function toggleCardLyrics(e, itemId) {
  if (e) {
    e.preventDefault();
    e.stopPropagation();
  }
  const drawer = document.getElementById('drawer-' + itemId);
  const card = document.getElementById('card-' + itemId);
  const btn = card ? card.querySelector('.card-lyrics-toggle-btn') : null;
  if (!drawer) return;

  const isOpen = drawer.style.display !== 'none';
  drawer.style.display = isOpen ? 'none' : 'block';
  if (btn) {
    btn.classList.toggle('open', !isOpen);
    btn.setAttribute('aria-expanded', !isOpen ? 'true' : 'false');
  }
}

function setTypeFilter(type) {
  currentFilter = type;
  document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
  const target = document.getElementById('filter-' + type);
  if (target) target.classList.add('active');
  renderCards();
}

function onSearchInput(val) {
  currentSearch = val;
  renderCards();
}

function openPlayer(videoId, title) {
  let modal = document.getElementById('playerModal');
  let iframe = document.getElementById('modalIframe');
  let titleEl = document.getElementById('modalTitle');

  // If modal doesn't exist on page, create dynamically
  if (!modal) {
    modal = createPlayerModalElement();
    document.body.appendChild(modal);
    iframe = document.getElementById('modalIframe');
    titleEl = document.getElementById('modalTitle');
  }

  if (!iframe) return;

  iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1&enablejsapi=1&rel=0&playsinline=1`;
  if (titleEl) titleEl.innerText = title;

  // Render or update direct YouTube link notice (guarantees playback if embed is restricted)
  let directNotice = document.getElementById('modalDirectYtNotice');
  if (!directNotice) {
    directNotice = document.createElement('div');
    directNotice.id = 'modalDirectYtNotice';
    directNotice.className = 'modal-direct-yt-notice';
    const iframeWrap = document.getElementById('modalIframeWrapper') || (modal && modal.querySelector('.modal-iframe-wrapper'));
    if (iframeWrap && iframeWrap.parentNode) {
      iframeWrap.parentNode.insertBefore(directNotice, iframeWrap.nextSibling);
    }
  }
  if (directNotice) {
    directNotice.innerHTML = `
      <div class="direct-notice-inner">
        <span>${GKD_ICONS.bulb} காணொளி அல்லது ஆடியோ இங்கு இயங்கவில்லை எனில் (If video playback is restricted):</span>
        <a href="https://www.youtube.com/watch?v=${videoId}" target="_blank" rel="noopener noreferrer" class="direct-yt-btn">
          ${GKD_ICONS.play} YouTube-ல் நேரடியாகத் திறக்க (Watch on YouTube) ${GKD_ICONS.external}
        </a>
      </div>
    `;
  }

  // Resolve item details
  let item = (window.GURUKULA_ITEMS_BY_ID && window.GURUKULA_ITEMS_BY_ID[videoId]) ||
             (window.pageItems && window.pageItems.find(x => x.id === videoId)) ||
             { id: videoId, title: title };
  item = enrichItem(item);

  // Render modal details section below the video
  let detailsEl = document.getElementById('modalDetails');
  if (!detailsEl) {
    detailsEl = document.createElement('div');
    detailsEl.id = 'modalDetails';
    detailsEl.className = 'modal-details';
    const box = document.getElementById('playerModalBox') || modal.querySelector('.player-modal-box');
    if (box) box.appendChild(detailsEl);
  }

  const safeTitle = escapeHtml(item.title || title);
  const safeAuthor = escapeHtml(item.author || '');
  const safeSource = escapeHtml(item.source || '');
  const formattedLyrics = item.lyrics ? escapeHtml(item.lyrics).replace(/\n/g, '<br>') : 'இப்பாடலின் வரிகள் சேகரிக்கப்பட்டு வருகின்றன.';
  const safeMeaning = escapeHtml(item.meaning || 'இப்பாடலின் தத்துவப் பொருள் விளக்கம் சேகரிக்கப்பட்டு வருகிறது.');
  const rawLyrics = item.lyrics || '';

  detailsEl.innerHTML = `
    <div class="modal-meta-row">
      <div class="modal-meta-tags">
        <span class="modal-meta-tag badge-${item.type === 'film' ? 'film' : 'audio'}">
          ${item.type === 'film' ? `${GKD_ICONS.cinema} முழுப் படம் (Cinematic Film)` : `${GKD_ICONS.music} இசை வெளியீடு (Sacred Audio)`}
        </span>
        ${safeAuthor ? `<span class="modal-meta-tag">${GKD_ICONS.pencil} ஆசிரியர்: <strong>${safeAuthor}</strong></span>` : ''}
        ${safeSource ? `<span class="modal-meta-tag">${GKD_ICONS.book} மூலம்: <strong>${safeSource}</strong></span>` : ''}
      </div>

      <div class="modal-action-buttons">
        <a href="https://www.youtube.com/watch?v=${videoId}" target="_blank" rel="noopener noreferrer" class="modal-btn modal-btn-yt">
          ${GKD_ICONS.play} YouTube-ல் காண்க ${GKD_ICONS.external}
        </a>
        ${rawLyrics ? `
          <button type="button" class="modal-btn modal-btn-copy" onclick="copyLyricsText(this, ${JSON.stringify(rawLyrics)})">
            ${GKD_ICONS.copy} வரிகளை நகலெடு
          </button>
        ` : ''}
      </div>
    </div>

    <div class="modal-content-grid">
      <div class="modal-box modal-lyrics-box">
        <div class="modal-box-header">
          <span class="modal-box-icon">${GKD_ICONS.scroll}</span>
          <h4 class="modal-box-title">பாடல் வரிகள் (Sacred Lyrics)</h4>
        </div>
        <div class="modal-box-body lyrics-body">${formattedLyrics}</div>
      </div>

      <div class="modal-box modal-meaning-box">
        <div class="modal-box-header">
          <span class="modal-box-icon">${GKD_ICONS.bulb}</span>
          <h4 class="modal-box-title">பொருள் விளக்கம் &amp; தத்துவம் (Spiritual Meaning)</h4>
        </div>
        <div class="modal-box-body meaning-body">${safeMeaning}</div>
      </div>
    </div>

    <div class="modal-bottom-actions">
      <button type="button" class="modal-btn modal-btn-top" onclick="scrollToModalTop()">
        ${GKD_ICONS.arrowUp} காணொளிக்குத் திரும்புக (Back to Video)
      </button>
      <button type="button" class="modal-btn modal-btn-close-bottom" onclick="closePlayer()">
        ${GKD_ICONS.close} மூடுக (Close Player)
      </button>
    </div>
  `;

  modal.classList.add('active');
  document.body.style.overflow = 'hidden';

  // Scroll modal box to top when opening
  const modalBox = document.getElementById('playerModalBox') || modal.querySelector('.player-modal-box');
  if (modalBox) {
    modalBox.scrollTop = 0;
  }
}

function toggleModalFullscreen() {
  const modalBox = document.getElementById('playerModalBox') || document.querySelector('.player-modal-box');
  const btn = document.querySelector('.modal-fullscreen-btn');
  
  // 1. If currently in CSS Big / Theater mode, exit it
  if (modalBox && modalBox.classList.contains('modal-theater-mode')) {
    modalBox.classList.remove('modal-theater-mode');
    if ((document.fullscreenElement || document.webkitFullscreenElement) && document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    }
    if (btn) btn.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg> பெரிய திரை (Big Mode)';
    return;
  }

  // 2. If currently in native hardware fullscreen, exit it
  if (document.fullscreenElement || document.webkitFullscreenElement) {
    if (document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }
    if (modalBox) modalBox.classList.remove('modal-theater-mode');
    if (btn) btn.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg> பெரிய திரை (Big Mode)';
    return;
  }

  // 3. Otherwise enter Big Mode: attempt hardware fullscreen, fallback gracefully to CSS theater mode
  const target = modalBox || document.documentElement;
  const req = target.requestFullscreen || target.webkitRequestFullscreen || target.mozRequestFullScreen || target.msRequestFullscreen;

  if (req) {
    try {
      const p = req.call(target);
      if (p && p.then) {
        p.then(() => {
          if (btn) btn.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14h6v6M20 10h-6V4M14 10l7-7M3 21l7-7"/></svg> இயல்பு (Exit Big Mode)';
        }).catch(() => {
          // Hardware fullscreen not allowed by browser/permissions-policy: activate CSS Big Mode!
          if (modalBox) modalBox.classList.add('modal-theater-mode');
          if (btn) btn.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14h6v6M20 10h-6V4M14 10l7-7M3 21l7-7"/></svg> இயல்பு (Exit Big Mode)';
        });
      } else {
        if (btn) btn.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14h6v6M20 10h-6V4M14 10l7-7M3 21l7-7"/></svg> இயல்பு (Exit Big Mode)';
      }
    } catch (e) {
      if (modalBox) modalBox.classList.add('modal-theater-mode');
      if (btn) btn.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14h6v6M20 10h-6V4M14 10l7-7M3 21l7-7"/></svg> இயல்பு (Exit Big Mode)';
    }
  } else {
    if (modalBox) modalBox.classList.add('modal-theater-mode');
    if (btn) btn.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14h6v6M20 10h-6V4M14 10l7-7M3 21l7-7"/></svg> இயல்பு (Exit Big Mode)';
  }
}

document.addEventListener('fullscreenchange', function() {
  const btn = document.querySelector('.modal-fullscreen-btn');
  const modalBox = document.getElementById('playerModalBox') || document.querySelector('.player-modal-box');
  if (!document.fullscreenElement) {
    if (modalBox && !modalBox.classList.contains('modal-theater-mode')) {
      if (btn) btn.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg> பெரிய திரை (Big Mode)';
    }
  } else {
    if (btn) btn.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14h6v6M20 10h-6V4M14 10l7-7M3 21l7-7"/></svg> இயல்பு (Exit Big Mode)';
  }
});

function scrollToModalDetails() {
  const details = document.getElementById('modalDetails');
  const box = document.getElementById('playerModalBox') || document.querySelector('.player-modal-box');
  if (details && box) {
    const topPos = details.offsetTop - 55;
    box.scrollTo({ top: Math.max(0, topPos), behavior: 'smooth' });
  }
}

function scrollToModalTop() {
  const box = document.getElementById('playerModalBox') || document.querySelector('.player-modal-box');
  if (box) {
    box.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

function createPlayerModalElement() {
  const modal = document.createElement('div');
  modal.className = 'player-modal';
  modal.id = 'playerModal';
  modal.onclick = function(e) { if (e.target === this) closePlayer(); };
  modal.innerHTML = `
    <div class="player-modal-box" id="playerModalBox">
      <div class="modal-header">
        <div class="modal-title" id="modalTitle">Now Playing</div>
        <div class="modal-header-actions">
          <button type="button" class="modal-fullscreen-btn" onclick="toggleModalFullscreen()" title="பெரிய திரை (Toggle Big Mode / Fullscreen)"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg> பெரிய திரை (Big Mode)</button>
          <button type="button" class="modal-scroll-btn" onclick="scrollToModalDetails()" title="வரிகளுக்குச் செல்க">
            <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg> வரிகள் &amp; பொருள் <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><polyline points="19 12 12 19 5 12"></polyline></svg>
          </button>
          <button type="button" class="modal-close-btn" onclick="closePlayer()" title="மூடுக"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg> மூடுக (Close)</button>
        </div>
      </div>
      <div class="modal-iframe-wrapper" id="modalIframeWrapper">
        <iframe id="modalIframe" src="" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share; fullscreen" referrerpolicy="strict-origin-when-cross-origin"></iframe>
      </div>
      <div class="modal-scroll-hint" onclick="scrollToModalDetails()">
        <span><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg> கீழே பாடல் வரிகள் &amp; தத்துவப் பொருள் விளக்கம் (Scroll down for Lyrics &amp; Meaning) <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg></span>
      </div>
      <div class="modal-details" id="modalDetails"></div>
    </div>
  `;
  return modal;
}

// Global escape key listener
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closePlayer();
  }
});

function copyLyricsText(btn, text) {
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {
    const originalText = btn.innerHTML;
    btn.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg> நகலெடுக்கப்பட்டது!';
    btn.style.borderColor = 'var(--gold)';
    btn.style.color = 'var(--gold-bright)';
    setTimeout(() => {
      btn.innerHTML = originalText;
      btn.style.borderColor = '';
      btn.style.color = '';
    }, 2200);
  }).catch(err => {
    console.error('Failed to copy lyrics:', err);
  });
}

function closePlayer() {
  if (document.fullscreenElement) { document.exitFullscreen().catch(() => {}); }
  const modal = document.getElementById('playerModal');
  const iframe = document.getElementById('modalIframe');

  if (modal && iframe) {
    iframe.src = '';
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

function toggleMobileNav() {
  toggleLeftStrip();
}

function closeMobileNav() {
  closeMobileStrip();
}

// Multi-dropdown support
function toggleDropdown(e, dropdownId) {
  if (e) {
    e.preventDefault();
    e.stopPropagation();
  }
  const targetId = dropdownId || (e && e.currentTarget && e.currentTarget.id ? e.currentTarget.id.replace('Btn', '') : null);
  const dropdown = targetId ? document.getElementById(targetId) : (e ? e.currentTarget.closest('.nav-dropdown') : document.querySelector('.nav-dropdown'));
  if (!dropdown) return;
  const wasOpen = dropdown.classList.contains('open');
  document.querySelectorAll('.nav-dropdown').forEach(d => {
    if (d !== dropdown) d.classList.remove('open');
  });
  dropdown.classList.toggle('open', !wasOpen);
  const toggleBtn = dropdown.querySelector('.dropdown-toggle');
  if (toggleBtn) toggleBtn.setAttribute('aria-expanded', !wasOpen ? 'true' : 'false');
}

document.addEventListener('click', (e) => {
  document.querySelectorAll('.nav-dropdown').forEach(dropdown => {
    if (!dropdown.contains(e.target)) {
      dropdown.classList.remove('open');
      const toggleBtn = dropdown.querySelector('.dropdown-toggle');
      if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
    }
  });
});

// Close player and menus on ESC key
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    closePlayer();
    closeMobileNav();
    document.querySelectorAll('.nav-dropdown').forEach(d => d.classList.remove('open'));
  }
});

// Sheet Modal Handlers
function openSheetModal(imgSrc, pageNum, pageTitle, gradeLabel) {
  const modal = document.getElementById('sheetModal');
  const modalImg = document.getElementById('sheetModalImg');
  const modalTitle = document.getElementById('sheetModalTitle');
  if (modal && modalImg) {
    modalImg.src = imgSrc;
    const label = gradeLabel || 'பாடநூல்';
    if (modalTitle) modalTitle.innerText = `${label} — பக்கம் ${pageNum} ${pageTitle ? '• ' + pageTitle : ''}`;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeSheetModal() {
  const modal = document.getElementById('sheetModal');
  const modalImg = document.getElementById('sheetModalImg');
  if (modal) {
    modal.classList.remove('active');
    if (modalImg) modalImg.src = '';
    document.body.style.overflow = '';
  }
}



/* ========================================================================== */
/* GURUKULA APP SHELL: LEFT STRIP, CONTEXT BAR, USER PROFILE & PREFERENCES     */

const GKD_AVATAR_SVGS = {
  user: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
  om: GKD_ICONS.om,
  deepam: GKD_ICONS.deepam,
  trishul: GKD_ICONS.trishul,
  lotus: GKD_ICONS.lotus,
  flower: GKD_ICONS.flower,
  book: GKD_ICONS.book,
  meditation: GKD_ICONS.meditation,
  crown: GKD_ICONS.crown
};

function getAvatarSvg(avatarKey) {
  if (!avatarKey) return GKD_AVATAR_SVGS.user;
  if (GKD_AVATAR_SVGS[avatarKey]) return GKD_AVATAR_SVGS[avatarKey];
  const legacyMap = {
    '👤': GKD_AVATAR_SVGS.user,
    '🕉️': GKD_AVATAR_SVGS.om, '🕉': GKD_AVATAR_SVGS.om, 'ॐ': GKD_AVATAR_SVGS.om,
    '🪔': GKD_AVATAR_SVGS.deepam,
    '🔱': GKD_AVATAR_SVGS.trishul,
    '🌸': GKD_AVATAR_SVGS.lotus,
    '🌺': GKD_AVATAR_SVGS.flower,
    '📖': GKD_AVATAR_SVGS.book,
    '🧘': GKD_AVATAR_SVGS.meditation,
    '👑': GKD_AVATAR_SVGS.crown
  };
  return legacyMap[avatarKey] || GKD_AVATAR_SVGS.user;
}

/* ========================================================================== */

const DEFAULT_USER_PREFS = {
  name: 'அன்பான சாதகர்',
  tier: 'tier1',
  avatar: 'user',
  theme: 'cosmic',
  fontStyle: 'mukta',
  fontScale: 1.0,
  navLayout: 'sidebar', // 'sidebar' (default), 'topbar' (classic), 'hybrid' (both)
  autoplay: false,
  continuous: false,
  dailyVirtue: true,
  streakDays: 1,
  lastVisit: new Date().toISOString().split('T')[0],
  completedLessons: 0,
  bookmarks: []
};

let userPrefs = { ...DEFAULT_USER_PREFS };

function loadUserPreferences() {
  try {
    const saved = localStorage.getItem('GURUKULA_USER_PREFS');
    if (saved) {
      userPrefs = { ...DEFAULT_USER_PREFS, ...JSON.parse(saved) };
      if (userPrefs.theme === 'gold' || !userPrefs.theme) userPrefs.theme = 'cosmic';
    }
  } catch (e) {
    console.warn('Failed to load user preferences:', e);
  }

  // Track visit streak
  const today = new Date().toISOString().split('T')[0];
  if (userPrefs.lastVisit !== today) {
    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
    if (userPrefs.lastVisit === yesterday) {
      userPrefs.streakDays = (userPrefs.streakDays || 1) + 1;
    } else {
      userPrefs.streakDays = 1;
    }
    userPrefs.lastVisit = today;
    saveUserPreferences();
  }

  applyUserPreferences();
}

function saveUserPreferences() {
  try {
    localStorage.setItem('GURUKULA_USER_PREFS', JSON.stringify(userPrefs));
  } catch (e) {
    console.warn('Failed to save preferences:', e);
  }
}

function applyUserPreferences() {
  // Theme
  document.body.classList.remove('theme-cosmic', 'theme-midnight', 'theme-amoled');
  if (userPrefs.theme === 'midnight') document.body.classList.add('theme-midnight');
  else if (userPrefs.theme === 'amoled') document.body.classList.add('theme-amoled');
  else document.body.classList.add('theme-cosmic');

  // Font Style
  document.body.classList.remove('font-noto', 'font-mukta');
  if (userPrefs.fontStyle === 'noto') document.body.classList.add('font-noto');
  else document.body.classList.add('font-mukta');

  // Font Scale
  const scale = userPrefs.fontScale || 1.0;
  document.documentElement.style.setProperty('--user-font-scale', scale);
  const indicator = document.getElementById('fontScaleIndicator');
  if (indicator) indicator.innerText = Math.round(scale * 100) + '%';
  const sliderLabel = document.getElementById('sliderFontLabel');
  if (sliderLabel) sliderLabel.innerText = Math.round(scale * 100) + '% ' + (scale === 1.0 ? '(இயல்பு)' : '');

  // Navigation Shell Layout Mode
  const layout = userPrefs.navLayout || 'sidebar';
  const strip = document.getElementById('leftStripBar');
  const oldNav = document.getElementById('mainNav');
  const contextTabsNav = document.getElementById('contextTabsNav');

  document.body.classList.remove('layout-sidebar', 'layout-topbar', 'layout-hybrid');
  document.body.classList.add('layout-' + layout);

  if (layout === 'topbar') {
    // Classic top navbar mode
    if (strip) strip.style.display = 'none';
    if (oldNav) oldNav.style.display = 'flex';
    if (contextTabsNav) contextTabsNav.style.display = 'none';
    document.body.style.paddingLeft = '0';
  } else if (layout === 'hybrid') {
    // Dual Hybrid Shell
    if (strip) strip.style.display = 'flex';
    if (oldNav) oldNav.style.display = 'flex';
    if (contextTabsNav) contextTabsNav.style.display = 'flex';
    if (window.innerWidth >= 992) {
      const isExp = strip && strip.classList.contains('expanded');
      document.body.style.paddingLeft = isExp ? '230px' : '68px';
    }
  } else {
    // 'sidebar' (DEFAULT): Left sidebar dock + clean context-sensitive top tabs
    if (strip) strip.style.display = 'flex';
    if (oldNav) oldNav.style.display = 'none';
    if (contextTabsNav) contextTabsNav.style.display = 'flex';
    if (window.innerWidth >= 992) {
      const isExp = strip && strip.classList.contains('expanded');
      document.body.style.paddingLeft = isExp ? '230px' : '68px';
    }
  }

  // Update layout radio in Settings modal
  const layoutRadios = document.querySelectorAll('input[name="layoutChoice"]');
  layoutRadios.forEach(r => { r.checked = (r.value === layout); });

  // Profile Badges & Avatars in UI
  const pillAvatar = document.getElementById('pillAvatarIcon');
  const pillName = document.getElementById('pillUserName');
  const pillTier = document.getElementById('pillUserTier');
  const stripAvatar = document.getElementById('stripAvatarIcon');
  const stripName = document.getElementById('stripUserName');

  const tierMap = {
    'tier1': 'தரம் 1-4',
    'tier2': 'தரம் 5-8',
    'tier3': 'தரம் 9-12'
  };

  if (pillAvatar) pillAvatar.innerHTML = getAvatarSvg(userPrefs.avatar);
  if (pillName) pillName.innerText = userPrefs.name || 'சாதகர்';
  if (pillTier) pillTier.innerText = tierMap[userPrefs.tier] || 'சாதகர்';
  if (stripAvatar) stripAvatar.innerHTML = getAvatarSvg(userPrefs.avatar);
  if (stripName) stripName.innerText = userPrefs.name || 'சுயவிவரம்';

  // Update modal fields if open
  const largeAvatar = document.getElementById('profileLargeAvatar');
  const dispHead = document.getElementById('profileDisplayNameHead');
  const tierBadge = document.getElementById('profileTierBadge');
  const streakText = document.getElementById('profileStreakDays');
  const lessonsText = document.getElementById('profileLessonsCount');
  const nameInput = document.getElementById('prefUserNameInput');
  const tierSelect = document.getElementById('prefUserTierSelect');

  if (largeAvatar) largeAvatar.innerHTML = getAvatarSvg(userPrefs.avatar);
  if (dispHead) dispHead.innerText = userPrefs.name || 'அன்பான சாதகர்';
  if (tierBadge) {
    const fullTierMap = {
      'tier1': 'தொடக்க சாதகர் (Grade 1-4)',
      'tier2': 'இடைநிலை சாதகர் (Grade 5-8)',
      'tier3': 'உயர்நிலை சிவநேசர் (Grade 9-12)'
    };
    tierBadge.innerText = fullTierMap[userPrefs.tier] || fullTierMap['tier1'];
  }
  if (streakText) streakText.innerText = (userPrefs.streakDays || 1) + ' நாள்';
  if (lessonsText) lessonsText.innerText = (userPrefs.completedLessons || 0).toString();
  if (nameInput && nameInput.value !== userPrefs.name) nameInput.value = userPrefs.name;
  if (tierSelect) tierSelect.value = userPrefs.tier || 'tier1';

  // Radio choices in Settings modal
  const themeRadios = document.querySelectorAll('input[name="themeChoice"]');
  themeRadios.forEach(r => { r.checked = (r.value === userPrefs.theme); });
  const fontRadios = document.querySelectorAll('input[name="fontChoice"]');
  fontRadios.forEach(r => { r.checked = (r.value === userPrefs.fontStyle); });

  const apCb = document.getElementById('prefAutoplay');
  if (apCb) apCb.checked = Boolean(userPrefs.autoplay);
  const contCb = document.getElementById('prefContinuous');
  if (contCb) contCb.checked = Boolean(userPrefs.continuous);
  const dvCb = document.getElementById('prefDailyVirtue');
  if (dvCb) dvCb.checked = Boolean(userPrefs.dailyVirtue);

  // Update stats box
  const sDays = document.getElementById('statDaysVisited');
  const sLessons = document.getElementById('statLessonsCompleted');
  const sBooks = document.getElementById('statBookmarksCount');
  if (sDays) sDays.innerText = userPrefs.streakDays || 1;
  if (sLessons) sLessons.innerText = userPrefs.completedLessons || 0;
  if (sBooks) sBooks.innerText = (userPrefs.bookmarks && userPrefs.bookmarks.length) || 0;
}

function adjustFontSize(delta) {
  let scale = (userPrefs.fontScale || 1.0) + delta;
  scale = Math.max(0.82, Math.min(1.28, Math.round(scale * 100) / 100));
  userPrefs.fontScale = scale;
  saveUserPreferences();
  applyUserPreferences();
}

function changeNavLayout(layout) {
  userPrefs.navLayout = layout;
  saveUserPreferences();
  applyUserPreferences();
}

function changeTheme(themeName) {
  userPrefs.theme = themeName;
  saveUserPreferences();
  applyUserPreferences();
}

function cycleTheme() {
  const themes = ['cosmic', 'midnight', 'amoled'];
  const curIdx = themes.indexOf(userPrefs.theme || 'cosmic');
  const nextTheme = themes[(curIdx + 1) % themes.length];
  changeTheme(nextTheme);
}

function changeFontStyle(fontName) {
  userPrefs.fontStyle = fontName;
  saveUserPreferences();
  applyUserPreferences();
}

function selectAvatar(icon) {
  userPrefs.avatar = icon;
  document.querySelectorAll('.avatar-option').forEach(btn => {
    btn.classList.toggle('selected', btn.innerText.trim() === icon);
  });
  saveUserPreferences();
  applyUserPreferences();
}

function saveUserProfileFields() {
  const nameInput = document.getElementById('prefUserNameInput');
  const tierSelect = document.getElementById('prefUserTierSelect');
  if (nameInput) userPrefs.name = nameInput.value.trim() || 'அன்பான சாதகர்';
  if (tierSelect) userPrefs.tier = tierSelect.value;
  saveUserPreferences();
  applyUserPreferences();
}

function savePreferences() {
  const apCb = document.getElementById('prefAutoplay');
  if (apCb) userPrefs.autoplay = apCb.checked;
  const contCb = document.getElementById('prefContinuous');
  if (contCb) userPrefs.continuous = contCb.checked;
  const dvCb = document.getElementById('prefDailyVirtue');
  if (dvCb) userPrefs.dailyVirtue = dvCb.checked;
  saveUserPreferences();
}

function resetUserSettings() {
  if (confirm('அனைத்து அமைப்புகளையும் இயல்பு நிலைக்கு மீட்டமைக்க வேண்டுமா?')) {
    userPrefs = { ...DEFAULT_USER_PREFS };
    saveUserPreferences();
    applyUserPreferences();
  }
}

// --------------------------------------------------------------------------
// PRIMARY 6-GROUP MENU DRAWER & SIDEBAR CONTROLS
// --------------------------------------------------------------------------
function togglePrimaryMenu() {
  const strip = document.getElementById('leftStripBar');
  const backdrop = document.getElementById('stripBackdrop');
  if (!strip) return;
  const isOpen = strip.classList.toggle('open');
  document.body.classList.toggle('primary-menu-open', isOpen);
  if (backdrop) backdrop.classList.toggle('active', isOpen);
}

function openPrimaryMenu() {
  const strip = document.getElementById('leftStripBar');
  const backdrop = document.getElementById('stripBackdrop');
  if (!strip) return;
  strip.classList.add('open');
  document.body.classList.add('primary-menu-open');
  if (backdrop) backdrop.classList.add('active');
}

function closePrimaryMenu() {
  const strip = document.getElementById('leftStripBar');
  const backdrop = document.getElementById('stripBackdrop');
  if (strip) {
    strip.classList.remove('open');
    strip.classList.remove('mobile-open');
  }
  document.body.classList.remove('primary-menu-open');
  if (backdrop) backdrop.classList.remove('active');
}

function toggleLeftStrip() {
  togglePrimaryMenu();
}

function closeMobileStrip() {
  closePrimaryMenu();
}

function openUserSettingsModal(tab) {
  let modal = document.getElementById('userSettingsModal');
  if (!modal) {
    mountAppShell();
  hydrateModernIcons();
    modal = document.getElementById('userSettingsModal');
  }
  if (modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    switchUserTab(tab || 'profile');
  }
}

function closeUserSettingsModal() {
  const modal = document.getElementById('userSettingsModal');
  if (modal) {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

function switchUserTab(tabId) {
  const tabProfileBtn = document.getElementById('userTabProfileBtn');
  const tabPrefsBtn = document.getElementById('userTabPrefsBtn');
  const contentProfile = document.getElementById('tabContentProfile');
  const contentPrefs = document.getElementById('tabContentPreferences');

  if (tabId === 'preferences') {
    if (tabProfileBtn) tabProfileBtn.classList.remove('active');
    if (tabPrefsBtn) tabPrefsBtn.classList.add('active');
    if (contentProfile) contentProfile.classList.remove('active');
    if (contentPrefs) contentPrefs.classList.add('active');
  } else {
    if (tabProfileBtn) tabProfileBtn.classList.add('active');
    if (tabPrefsBtn) tabPrefsBtn.classList.remove('active');
    if (contentProfile) contentProfile.classList.add('active');
    if (contentPrefs) contentPrefs.classList.remove('active');
  }
}

// --------------------------------------------------------------------------
// CONTEXT-SENSITIVE SEARCH DISPATCHER
// --------------------------------------------------------------------------
function handleContextSearch(val) {
  const clearBtn = document.getElementById('contextSearchClear');
  if (clearBtn) clearBtn.style.display = val ? 'inline-block' : 'none';

  // 1. If catalog search function exists on this page
  if (typeof onSearchInput === 'function') {
    onSearchInput(val);
  }

  // 2. Also filter in-page text or cards
  const query = val.toLowerCase().trim();
  const searchTargets = document.querySelectorAll('.video-card, .virtue-card, .lesson-unit-panel, .canonical-card, .quiz-card, .grade-card, .degree-program-card, .sheet-item');
  if (searchTargets.length > 0 && typeof onSearchInput !== 'function') {
    searchTargets.forEach(el => {
      const text = el.innerText.toLowerCase();
      el.style.display = (!query || text.includes(query)) ? '' : 'none';
    });
  }
}

function clearContextSearch() {
  const input = document.getElementById('contextQuickSearch');
  if (input) {
    input.value = '';
    handleContextSearch('');
    input.focus();
  }
}

// Keyboard shortcuts: '/' or 'Ctrl+K' to open universal search, 'Esc' to close modals
document.addEventListener('keydown', e => {
  if ((e.key === '/' || ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k')) && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
    e.preventDefault();
    openUniversalSearch();
  }
  if (e.key === 'Escape') {
    closeUniversalSearch();
    closeUserSettingsModal();
    closeMobileStrip();
  }
});

// --------------------------------------------------------------------------
// 1. AMBIENT MEDITATIVE TANPURA DRONE (Web Audio API)
// --------------------------------------------------------------------------
let droneAudioCtx = null;
let droneOscillators = [];
let droneGainNode = null;
let isDronePlaying = false;

function toggleAmbientDrone() {
  if (isDronePlaying) {
    stopAmbientDrone();
  } else {
    startAmbientDrone();
  }
}

function startAmbientDrone() {
  try {
    const AudioCtxClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtxClass) return;
    if (!droneAudioCtx) {
      droneAudioCtx = new AudioCtxClass();
    }
    if (droneAudioCtx.state === 'suspended') {
      droneAudioCtx.resume();
    }

    droneGainNode = droneAudioCtx.createGain();
    droneGainNode.gain.setValueAtTime(0.001, droneAudioCtx.currentTime);
    droneGainNode.gain.exponentialRampToValueAtTime(0.12, droneAudioCtx.currentTime + 2.5);
    droneGainNode.connect(droneAudioCtx.destination);

    // C# Tanpura Harmonic Frequencies:
    // Kharaj Sa (C#3 - 138.59 Hz), Pa (G#3 - 207.65 Hz), Sa (C#4 - 277.18 Hz), Sa (C#4 - 277.65 Hz)
    const freqs = [138.59, 207.65, 277.18, 277.65];
    droneOscillators = freqs.map((freq, i) => {
      const osc = droneAudioCtx.createOscillator();
      const oscGain = droneAudioCtx.createGain();
      osc.type = (i === 0) ? 'triangle' : 'sine';
      osc.frequency.setValueAtTime(freq, droneAudioCtx.currentTime);

      const lfo = droneAudioCtx.createOscillator();
      lfo.frequency.setValueAtTime(0.12 + (i * 0.04), droneAudioCtx.currentTime);
      const lfoGain = droneAudioCtx.createGain();
      lfoGain.gain.setValueAtTime(0.4, droneAudioCtx.currentTime);
      lfo.connect(lfoGain);
      lfoGain.connect(osc.frequency);
      lfo.start();

      oscGain.gain.setValueAtTime(i === 0 ? 0.35 : 0.22, droneAudioCtx.currentTime);
      osc.connect(oscGain);
      oscGain.connect(droneGainNode);
      osc.start();
      return { osc, lfo };
    });

    isDronePlaying = true;
    updateDroneUI(true);
  } catch (err) {
    console.error('Ambient drone initialization error:', err);
  }
}

function stopAmbientDrone() {
  if (droneGainNode && droneAudioCtx) {
    try {
      droneGainNode.gain.exponentialRampToValueAtTime(0.0001, droneAudioCtx.currentTime + 1.2);
    } catch(e){}
    setTimeout(() => {
      droneOscillators.forEach(o => {
        try { o.osc.stop(); o.lfo.stop(); } catch(e){}
      });
      droneOscillators = [];
      isDronePlaying = false;
      updateDroneUI(false);
    }, 1200);
  } else {
    isDronePlaying = false;
    updateDroneUI(false);
  }
}

function updateDroneUI(playing) {
  const btns = document.querySelectorAll('.ambient-drone-btn');
  btns.forEach(btn => {
    if (playing) {
      btn.classList.add('playing');
      btn.title = 'நாத தியான ஒலி இயங்குகிறது (நிறுத்த கிளிக் செய்க)';
    } else {
      btn.classList.remove('playing');
      btn.title = 'நாத தியான ஒலி (Ambient Tanpura Drone)';
    }
  });
}

// --------------------------------------------------------------------------
// 2. UNIVERSAL SITE-WIDE SEARCH MODAL ENGINE
// --------------------------------------------------------------------------
const UNIVERSAL_SEARCH_ITEMS = [
  // Flagship Living Dharma Tools
  { title: "பஞ்ச மகா யக்ஞ டிராக்கர் (Daily Pancha Maha Yagna Habit Tracker)", desc: "தினசரி 5 வேள்விகள், சினமின்மை, இல்லற நல்லிணக்கம் & தொடர் சாதனா டிராக்கர்", url: "kalvi.html#grihasthaTracker", category: "இல்லற சாதனா", badge: "தினசரி சாதனா" },
  { title: "மாண்புறு குடும்ப அறநெறி சாசனம் (Printable Noble Family Living Charter)", desc: "இல்லத்தின் பெயர், உறுப்பினர்கள் & ஐம்பெரும் குடும்பச் சூளுரைகளுடன் சட்டமிடக்கூடிய சாசனம்", url: "kalvi.html#familyCharter", category: "இல்லற சாதனா", badge: "அச்சிடுக / PDF" },
  { title: "பதஞ்சலி 7 படிநிலைகள் (Patanjali 7-Level Self-Realization Curriculum)", desc: "சுபேச்சை முதல் துரியகா வரை 7 யோக மெய்ஞ்ஞான படிநிலைகள் & சுயமதிப்பீட்டுத் தேர்வு", url: "syllabus.html#patanjaliSyllabus", category: "பாடத்திட்டம்", badge: "7 படிநிலைகள்" },
  { title: "திருக்குறள் இல்லறவியல் 20 அதிகாரங்கள் அரங்கம் (Illaraviyal Cinema Lounge)", desc: "இல்வாழ்க்கை, துணைநலம், அன்புடைமை, பொறையுடைமை முதல் புகழ் வரை 20 தூண்கள்", url: "thirukkural.html#illaraviyalLounge", category: "திருக்குறள்", badge: "20 அதிகாரங்கள்" },
  { title: "இணையப் பள்ளி போர்டல் (Vedic-Modern Online School LMS)", desc: "21-ஆம் நூற்றாண்டு அறிவியல்-வேத சங்கமம், மாணவர் போர்டல் & படிப்பு அரங்கம்", url: "school.html", category: "பள்ளி", badge: "Online School" },
  
  // Degrees
  { title: "B.A. Grihastha Dharma (DEG-BA-GRI)", desc: "இல்லற தர்ம இளங்கலை — அறம், இல்லற மேலாண்மை & சான்றாண்மை விழுமியங்கள்", url: "higher-studies.html", category: "உயர்கல்வி", badge: "B.A. பட்டம்" },
  { title: "M.A. Applied Domestic Vedanta (DEG-MA-GRI)", desc: "பயன்முறை இல்லற வேதாந்த முதுகலை — சங்கர அத்வைதம், ராமானுஜ விசிஷ்டாத்வைதம் & இல்லற சமரசம்", url: "higher-studies.html", category: "உயர்கல்வி", badge: "M.A. பட்டம்" },
  { title: "Ph.D. in Family Self-Sacrifice as Fastest Vehicle for Nirvana (DOC-PHD-GRI)", desc: "இல்லறத் தியாக அன்பே அதிவேக முக்தி தரும் பெருவழி — முனைவர் பட்ட ஆய்வுநெறி", url: "higher-studies.html", category: "உயர்கல்வி", badge: "Ph.D. ஆய்வு" },
  { title: "Fellowship in Applied Domestic Dharma (FEL-GRI-01)", desc: "சான்றோன் இல்லற ஆய்வு கூட்டுறவு — தலைமுறை தலைமுறையாக தர்மத்தை நிலைநிறுத்தும் சாசனம்", url: "higher-studies.html", category: "உயர்கல்வி", badge: "Fellowship" },

  // Grades 1-12
  { title: "தரம் 1 — பாலப் பருவ வாழ்வியல் நெறி (Grade 1)", desc: "பாலப் பருவ அன்பு, பெற்றோர் பணிவிடை & நற்பண்புத் தொடக்கம்", url: "tharam-1.html", category: "பள்ளிக் கல்வி", badge: "Grade 1" },
  { title: "தரம் 2 — சிவ சின்னங்கள் & ஆலய வழிபாடு (Grade 2)", desc: "திருநீறு, ருத்ராட்சம், பஞ்சாட்சரம் & ஒழுக்கம்", url: "tharam-2.html", category: "பள்ளிக் கல்வி", badge: "Grade 2" },
  { title: "தரம் 3 — பஞ்சபூதம் & விழிப்புணர்வு (Grade 3)", desc: "நல்வழி, இயற்கை ஆராதனை & ஆசாரக் கல்வி", url: "tharam-3.html", category: "பள்ளிக் கல்வி", badge: "Grade 3" },
  { title: "தரம் 4 — பன்னிரு திருமுறை & சாத்வீக உணவு (Grade 4)", desc: "கொன்றை வேந்தன், திருமுறை பக்தி & அஹிம்சை", url: "tharam-4.html", category: "பள்ளிக் கல்வி", badge: "Grade 4" },
  { title: "தரம் 5 — 63 நாயன்மார்கள் & அறத்துப்பால் (Grade 5)", desc: "திருத்தொண்டர் தொகை, சுற்றந்தழால் & தேவாரம்", url: "tharam-5.html", category: "பள்ளிக் கல்வி", badge: "Grade 5" },
  { title: "தரம் 6 — நான்கு வேதங்கள் & சைவ சித்தாந்தம் (Grade 6)", desc: "தைத்திரீய சாந்தி மந்திரம், பதி-பசு-பாசம் & பஞ்ச மகா யக்ஞம்", url: "tharam-6.html", category: "பள்ளிக் கல்வி", badge: "Grade 6" },
  { title: "தரம் 7 — உபநிடத மகா வாக்கியங்கள் & கர்ம விதி (Grade 7)", desc: "பிரக்ஞானம் பிரம்ம, தத்வமஸி & புனர்ஜென்ம கர்ம நியதி", url: "tharam-7.html", category: "பள்ளிக் கல்வி", badge: "Grade 7" },
  { title: "தரம் 8 — பகவத் கீதை கர்ம யோகம் & வள்ளலார் (Grade 8)", desc: "கடமையைச் செய் பலனை எதிர்பாராதே & ஜீவகாருண்யம்", url: "tharam-8.html", category: "பள்ளிக் கல்வி", badge: "Grade 8" },
  { title: "தரம் 9 — ஆகமங்கள், ஆலய தத்துவம் & யோகம் (Grade 9)", desc: "உடலே ஆலயம், குண்டலினி சக்கரங்கள் & தியான அறிவியல்", url: "tharam-9.html", category: "பள்ளிக் கல்வி", badge: "Grade 9" },
  { title: "தரம் 10 — பதி பசு பாசம் & O/L வாழ்வியல் தேர்ச்சி (Grade 10)", desc: "சைவ சித்தாந்த முப்பொருள் உண்மை & முக்தி தத்துவம்", url: "tharam-10.html", category: "பள்ளிக் கல்வி", badge: "Grade 10" },
  { title: "தரம் 11 — கடோபநிடதம் & A/L தத்துவார்த்த ஒப்பாய்வு (Grade 11)", desc: "மரணத்தை வென்ற நசிகேதன் & பஞ்ச கோச உளவியல்", url: "tharam-11.html", category: "பள்ளிக் கல்வி", badge: "Grade 11" },
  { title: "தரம் 12 — ஜீவன் முக்தி, நடராஜர் & குவாண்டம் சங்கமம் (Grade 12)", desc: "உன்னத இல்லற வாழ்வு வழி அதிவேக முக்திப் பேறு", url: "tharam-12.html", category: "பள்ளிக் கல்வி", badge: "Grade 12" },

  // Canonical Paths
  { title: "சிவ நெறி — பன்னிரு திருமுறைகள் (Saiva Neri)", desc: "172 சிவத் திருப்பதிகங்கள், தேவாரப் பண்கள் & ஸ்ரீ ருத்ரம்", url: "saiva-neri.html", category: "ஆன்மீக நெறி", badge: "172 பாடல்கள்" },
  { title: "திருக்குறள் — உலகப் பொதுமறை அறநெறி (Thirukkural)", desc: "1330 அருங்குறள்கள், சினிமாத் திரைப்படங்கள் & இசை வெளியீடுகள்", url: "thirukkural.html", category: "ஆன்மீக நெறி", badge: "185 வெளியீடுகள்" },
  { title: "சுத்த சன்மார்க்கம் — வள்ளலார் பெருமான் (Sanmargam)", desc: "திருவருட்பா, ஜோதி வழிபாடு & பசிப்பிணி போக்கும் அன்னதானம்", url: "sanmargam.html", category: "ஆன்மீக நெறி", badge: "94 பாடல்கள்" },
  { title: "முருக நெறி — கௌமாரம் (Murugan)", desc: "கந்த சஷ்டி கவசம், திருப்புகழ் & அறுபடை வீடு திருவருள்", url: "murugan.html", category: "ஆன்மீக நெறி", badge: "முருகன்" },
  { title: "சக்தி நெறி — சாக்தம் (Sakthi)", desc: "அபிராமி அந்தாதி, லலிதா திரிசதி & தேவி போற்றிகள்", url: "sakthi.html", category: "ஆன்மீக நெறி", badge: "அம்பாள்" },
  { title: "விநாயகர் & வைணவ நெறி (Vinayagar & Vaishnavam)", desc: "விநாயகர் அகவல், திவ்யப் பிரபந்தம் & விஷ்ணு-கிருஷ்ண கானங்கள்", url: "vinayagar.html", category: "ஆன்மீக நெறி", badge: "விநாயகர்/வைணவம்" },
  { title: "காஞ்சி மகா பெரியவா அருளுரைகள் (Deivathin Kural)", desc: "வேத தர்மம், சனாதன சம்ஸ்கிருதி & மகா பெரியவா திவ்ய உபதேசங்கள்", url: "about.html", category: "குருவருள்", badge: "தெய்வத்தின் குரல்" }
];

function ensureUniversalSearchModal() {
  let modal = document.getElementById('universalSearchModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'universalSearchModal';
    modal.className = 'universal-search-modal';
    modal.onclick = function(e) { if (e.target === this) closeUniversalSearch(); };
    modal.innerHTML = `
      <div class="universal-search-box">
        <div class="universal-search-header">
          <span style="display:inline-flex; align-items:center; color:#38bdf8;"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg></span>
          <input type="text" id="universalSearchInput" class="universal-search-input" placeholder="குருகுல தேசத்தில் தேடுக... (எ.கா: தரம் 1, இல்லறம், குறள், PhD, யக்ஞம்)" autocomplete="off" oninput="handleUniversalSearchQuery(this.value)">
          <button type="button" class="universal-search-close" onclick="closeUniversalSearch()">Esc</button>
        </div>
        <div class="universal-search-results" id="universalSearchResults"></div>
      </div>
    `;
    document.body.appendChild(modal);
  }
  return modal;
}

function openUniversalSearch() {
  const modal = ensureUniversalSearchModal();
  modal.classList.add('open');
  const input = document.getElementById('universalSearchInput');
  if (input) {
    input.value = '';
    input.focus();
  }
  handleUniversalSearchQuery('');
}

function closeUniversalSearch() {
  const modal = document.getElementById('universalSearchModal');
  if (modal) modal.classList.remove('open');
}

function handleUniversalSearchQuery(q) {
  const container = document.getElementById('universalSearchResults');
  if (!container) return;

  const query = q.toLowerCase().trim();
  let results = [];

  if (!query) {
    results = UNIVERSAL_SEARCH_ITEMS.slice(0, 8);
  } else {
    results = UNIVERSAL_SEARCH_ITEMS.filter(item => {
      const haystack = (item.title + ' ' + item.desc + ' ' + item.category + ' ' + (item.badge || '')).toLowerCase();
      return haystack.includes(query);
    });

    if (window.GURUKULA_CATALOG && query.length >= 2) {
      let catalogMatches = [];
      Object.keys(window.GURUKULA_CATALOG).forEach(cat => {
        const list = window.GURUKULA_CATALOG[cat];
        if (Array.isArray(list)) {
          list.forEach(item => {
            const h = (item.title + ' ' + (item.lyrics || '') + ' ' + (item.meaning || '')).toLowerCase();
            if (h.includes(query)) {
              catalogMatches.push({
                title: item.title,
                desc: (item.meaning || item.lyrics || '').slice(0, 90) + '...',
                url: (cat === 'thirukkural') ? 'thirukkural.html' : (cat === 'shiva' ? 'saiva-neri.html' : 'index.html'),
                category: cat === 'thirukkural' ? 'திருக்குறள்' : (cat === 'shiva' ? 'சிவ நெறி' : 'பக்தி இசை'),
                badge: item.type === 'film' ? '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="2" y1="17" x2="7" y2="17"/><line x1="17" y1="17" x2="22" y2="17"/><line x1="17" y1="7" x2="22" y2="7"/></svg> படம்' : '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg> பாடல்'
              });
            }
          });
        }
      });
      results = results.concat(catalogMatches.slice(0, 10));
    }
  }

  if (results.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:30px 10px; color:#94a3b8;">
        <div style="display:flex; justify-content:center; margin-bottom:8px; color:var(--gold);"><svg class="gkd-icon" style="width:36px; height:36px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg></div>
        <div>"${q}" என்பதற்குரிய முடிவுகள் கிடைக்கவில்லை.</div>
        <div style="font-size:0.82rem; margin-top:4px; color:#64748b;">வேத தர்மம், குறள், தரம் 1-12, அல்லது இல்லறம் எனத் தேடிப் பாருங்கள்.</div>
      </div>
    `;
    return;
  }

  let html = '';
  if (!query) {
    html += '<div class="search-group-title"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg> பரிந்துரைக்கப்படும் முதன்மை வாழ்வியல் &amp; தர்மப் பாதைகள்:</div>';
  } else {
    html += `<div class="search-group-title"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg> கண்டறியப்பட்ட தேடல் முடிவுகள் (${results.length}):</div>`;
  }

  results.forEach(r => {
    html += `
      <a href="${r.url}" class="search-result-item" onclick="closeUniversalSearch()">
        <div class="search-item-info">
          <span class="search-item-title">${r.title}</span>
          <span class="search-item-desc">${r.desc}</span>
        </div>
        <span class="search-item-badge">${r.badge || r.category}</span>
      </a>
    `;
  });

  container.innerHTML = html;
}

// --------------------------------------------------------------------------
// APP SHELL DOM MOUNTING & CONTEXT RESOLUTION
// --------------------------------------------------------------------------
function resolvePageContext() {
  const path = window.location.pathname.toLowerCase();
  const filename = path.split('/').pop() || 'index.html';

  const contextMap = {
    'index.html': { root: 'முகப்பு', title: 'ஆன்மீகப் பெருவெளி', desc: '580 பக்தி இசை வெளியீடுகள்' },
    'kalvi.html': { root: 'வாழ்வியல்', title: '12 வகுப்புகள் பாடநெறி & வாழ்வியல் மையம்', desc: 'தரம் 1 முதல் 12 வரையிலான உன்னத இல்லற தர்மம் & சான்றாண்மை' },
    'school.html': { root: 'கல்வி', title: 'குருகுல இணையப் பள்ளி போர்டல்', desc: '21-ஆம் நூற்றாண்டு நவீன மாணவர் கற்றல் தளம்' },
    'higher-studies.html': { root: 'கல்வி', title: 'வேதாந்த வித்யாபீடம் — உயர்கல்வித் தளம்', desc: 'பிரஸ்தானத்ரயம், மெய்கண்ட சாத்திரங்கள் & அத்வைத ஆய்வு' },
    'virtues.html': { root: 'வாழ்வியல்', title: 'அகர வரிசை நற்பண்பு நெறிமுறை', desc: '30+ நற்பண்புகள் • 4 வாழ்வியல் பருவங்கள்' },
    'syllabus.html': { root: 'பாடத்திட்டம்', title: 'முழுமையான சைவ சித்தாந்த பாடத்திட்டம்', desc: 'WBS முறைசார் பாடநெறி & பதஞ்சலி 7-படிநிலை மதிப்பீடு' },
    'classes.html': { root: 'வகுப்புகள்', title: 'பாடநெறி நேரடி வகுப்புகள் & அட்டவணை', desc: 'குருகுல முறை நேரடிப் பயிற்சி & வழிகாட்டல்' },
    'tharam-1.html': { root: 'வாழ்வியல்', title: 'தரம் 1 (Grade 1)', desc: 'பாலப் பருவ அன்பு & இல்லறத் தொடக்கப் பழக்கங்கள் (60 தாள்கள்)' },
    'tharam-2.html': { root: 'வாழ்வியல்', title: 'தரம் 2 (Grade 2)', desc: 'சிவ சின்னங்கள், பக்தி & இல்லற தர்மம்' },
    'tharam-3.html': { root: 'வாழ்வியல்', title: 'தரம் 3 (Grade 3)', desc: 'நல்வழி, ஒழுக்கம் & ஆசாரக் கல்வி' },
    'tharam-4.html': { root: 'வாழ்வியல்', title: 'தரம் 4 (Grade 4)', desc: 'கொன்றை வேந்தன் & இல்லற நன்னெறி' },
    'tharam-5.html': { root: 'வாழ்வியல்', title: 'தரம் 5 (Grade 5)', desc: 'திருமுறைகள் & சுற்றந்தழால் தர்மம்' },
    'tharam-6.html': { root: 'வாழ்வியல்', title: 'தரம் 6 (Grade 6)', desc: 'சைவ சித்தாந்த ஆரம்ப நெறி & கடமை உணர்வு' },
    'tharam-7.html': { root: 'வாழ்வியல்', title: 'தரம் 7 (Grade 7)', desc: 'திருமுறைகள் & நாயன்மார் தியாக வரலாறு' },
    'tharam-8.html': { root: 'வாழ்வியல்', title: 'தரம் 8 (Grade 8)', desc: 'பொறையுடைமை, ஆசிரம தர்மம் & ஆலய தத்துவம்' },
    'tharam-9.html': { root: 'வாழ்வியல்', title: 'தரம் 9 (Grade 9)', desc: 'சான்றாண்மை, புலனடக்கம் & குடும்ப மாண்பு' },
    'tharam-10.html': { root: 'வாழ்வியல்', title: 'தரம் 10 (Grade 10)', desc: 'O/L வாழ்வியல் நன்னெறி & பதி-பசு-பாச ஆய்வு' },
    'tharam-11.html': { root: 'வாழ்வியல்', title: 'தரம் 11 (Grade 11)', desc: 'A/L உயர்தர தத்துவ ஒப்பாய்வு & சிவஞானபோதம்' },
    'tharam-12.html': { root: 'வாழ்வியல்', title: 'தரம் 12 (Grade 12)', desc: 'உன்னத இல்லற தர்மம் வழி ஆத்ம நிர்வாணம் / முக்தி' },
    'saiva-neri.html': { root: 'சைவ நெறி', title: 'பன்னிரு திருமுறைகள்', desc: '172 சிவத் திருப்பதிகங்கள் & ருத்ரம்' },
    'murugan.html': { root: 'வழிபாட்டு நெறி', title: 'முருகன் (Kaumaram)', desc: 'கந்த சஷ்டி, திருப்புகழ் & கானங்கள்' },
    'sakthi.html': { root: 'வழிபாட்டு நெறி', title: 'சக்தி (Shaktham)', desc: 'அபிராமி அந்தாதி & லலிதா போற்றிகள்' },
    'vinayagar.html': { root: 'வழிபாட்டு நெறி', title: 'விநாயகர் (Ganapathyam)', desc: 'விநாயகர் அகவல் & மூல கணபதி' },
    'vaishnava.html': { root: 'வழிபாட்டு நெறி', title: 'வைணவம் (Vaishnavam)', desc: 'விஷ்ணு, கிருஷ்ணர் & திவ்வியப் பிரபந்தம்' },
    'thirukkural.html': { root: 'தமிழ்மறை', title: 'திருக்குறள் (Thirukkural)', desc: '1330 அருங்குறள்கள் & இசைப்பாடல்கள்' },
    'sanmargam.html': { root: 'சன்மார்க்கம்', title: 'வள்ளலார் சுத்த சன்மார்க்கம்', desc: 'திருவருட்பா & ஆன்மநேய ஒருமைப்பாடு' },
    'irai-isai-virundhu.html': { root: 'இசை', title: 'இறை இசை விருந்து', desc: '5 சிறப்புப் பக்தி ஆல்பங்கள்' },
    'youtube.html': { root: 'காணொளி', title: 'YouTube காணொளி அரங்கம்', desc: '580 பக்தி இசை & பாடல்கள்' },
    'about.html': { root: 'காஞ்சி மகா பெரியவா', title: 'தெய்வத்தின் குரல் & தரிசனம்', desc: 'அருளுரைகள் & வழிகாட்டல்' },
    'google-site.html': { root: 'இணைப்பு', title: 'அதிகாரப்பூர்வ கூகிள் தளம்', desc: 'Google Sites நேரடி பார்வை' },
    'review_quality.html': { root: 'தமிழ்மறை', title: 'திரைத் தர ஆய்வு அரங்கம் (Film Quality Screening Room)', desc: 'திருக்குறள் மாஸ்டர் சினிமா ஆய்வு & காட்சி சரிபார்ப்பு' },
    'help.html': { root: 'உதவி', title: 'உதவி & வழிகாட்டல் மையம் (Help & Support)', desc: 'மாணவர், ஆசான் & பயனர் வழிகாட்டிகள்' }
  };

  return contextMap[filename] || { root: 'குரு குல தேசம்', title: 'ஆன்மீகக் களஞ்சியம்', desc: '' };
}


/* ========================================================================== */
/* GURUKULA CONTEXT-SENSITIVE TOP MENU TABS & APP SHELL                       */
/* ========================================================================== */

function getContextTabsForPage() {
  const path = window.location.pathname.toLowerCase();
  const filename = path.split('/').pop() || 'index.html';

  // 1. Grade / Tharam Pages (tharam-1.html to tharam-12.html)
  const gradeMatch = filename.match(/^tharam-(\d+)\.html$/);
  if (gradeMatch) {
    const gradeNum = parseInt(gradeMatch[1], 10);
    const prevGrade = gradeNum > 1 ? `tharam-${gradeNum - 1}.html` : null;
    const nextGrade = gradeNum < 12 ? `tharam-${gradeNum + 1}.html` : null;

    return [
      { id: 'tab-units', icon: GKD_ICONS.book, label: 'பாட அலகுகள்', action: "scrollToSection('courseUnits', 'lessonUnitPanel1')" },
      { id: 'tab-virtues', icon: GKD_ICONS.virtues, label: 'நற்பண்பு நெறி', action: "scrollToSection('gradeVirtueBox')" },
      { id: 'tab-diagram', icon: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>', label: 'காட்சி விளக்கம்', action: "scrollToSection('visualDiagramCard')" },
      { id: 'tab-quiz', icon: GKD_ICONS.question, label: 'சுய வினாடி-வினா', action: "scrollToSection('quizSection')" },
      { id: 'tab-sadhana', icon: GKD_ICONS.deepam, label: 'தினசரி சாதனை', action: "scrollToSection('sadhanaBox')" },
      ...(prevGrade ? [{ id: 'tab-prev', icon: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="11 17 6 12 11 7"/><polyline points="18 17 13 12 18 7"/></svg>', label: `தரம் ${gradeNum - 1}`, href: prevGrade }] : []),
      ...(nextGrade ? [{ id: 'tab-next', icon: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="13 17 18 12 13 7"/><polyline points="6 17 11 12 6 7"/></svg>', label: `தரம் ${gradeNum + 1}`, href: nextGrade }] : []),
      { id: 'tab-all-grades', icon: GKD_ICONS.leaf, label: '12 வாழ்வியல் நிலைகள்', href: 'kalvi.html' }
    ];
  }

  // 2. Curriculum Hub (kalvi.html)
  if (filename === 'kalvi.html') {
    return [
      { id: 'tab-overview', icon: GKD_ICONS.leaf, label: 'வாழ்வியல் நெறி அறிமுகம்', action: "scrollToSection('kalviOverview')", active: true },
      { id: 'tab-grades', icon: GKD_ICONS.book, label: '12 வகுப்புகள் பாடநெறி', action: "scrollToSection('gradesPortalSection')" },
      { id: 'tab-stages', icon: GKD_ICONS.virtues, label: '4 வாழ்வியல் பருவங்கள்', action: "scrollToSection('virtue-mapping')" },
      { id: 'tab-tracker', icon: GKD_ICONS.check, label: 'பஞ்ச மகா யக்ஞ டிராக்கர்', action: "scrollToSection('grihasthaTracker')" },
      { id: 'tab-charter', icon: GKD_ICONS.scroll, label: 'குடும்ப சாசனம்', action: "scrollToSection('familyCharter')" },
      { id: 'tab-portals', icon: GKD_ICONS.temple, label: 'வித்யாபீடங்கள்', action: "scrollToSection('relatedPortals')" },
      { id: 'tab-school', icon: GKD_ICONS.school, label: 'இணையப் பள்ளி', href: 'school.html' },
      { id: 'tab-higher', icon: GKD_ICONS.science, label: 'உயர்கல்வி', href: 'higher-studies.html' },
      { id: 'tab-syllabus', icon: GKD_ICONS.scroll, label: 'முழு பாடத்திட்டம்', href: 'syllabus.html' }
    ];
  }

  // 2b. Gurukula Academy Portal (school.html)
  if (filename === 'school.html') {
    return [
      { id: 'tab-portal', icon: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>', label: 'மாணவர் போர்டல்', action: "scrollToSection('portalDashboard')", active: true },
      { id: 'tab-fusion', icon: GKD_ICONS.science, label: 'அறிவியல்-வேத சங்கமம்', action: "scrollToSection('stemFusionSection')" },
      { id: 'tab-hall', icon: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>', label: 'தியான & படிப்பு அரங்கம்', action: "scrollToSection('focusStudyHall')" },
      { id: 'tab-cert', icon: GKD_ICONS.scroll, label: 'பட்டயச் சான்றிதழ்', action: "scrollToSection('certificateSection')" },
      { id: 'tab-cards', icon: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>', label: 'நினைவாற்றல் அட்டைகள்', action: "scrollToSection('flashcardsSection')" },
      { id: 'tab-roadmap', icon: '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>', label: '12 தரப் பாடநெறி', action: "scrollToSection('roadmapSection')" },
      { id: 'tab-tracker', icon: GKD_ICONS.check, label: 'தினசரி தர்ம டிராக்கர்', href: 'kalvi.html#grihasthaTracker' },
      { id: 'tab-charter', icon: GKD_ICONS.scroll, label: 'குடும்ப சாசனம்', href: 'kalvi.html#familyCharter' }
    ];
  }

  // 2c. Higher Studies Vidyapeeth (higher-studies.html)
  if (filename === 'higher-studies.html') {
    return [
      { id: 'tab-hs-hero', icon: GKD_ICONS.temple, label: 'வித்யாபீட அறிமுகம்', action: "scrollToSection('vidyaHero')", active: true },
      { id: 'tab-hs-ug', icon: GKD_ICONS.scroll, label: 'இளநிலை: பிரஸ்தானத்ரயம்', action: "scrollToSection('tierUG')" },
      { id: 'tab-hs-pg', icon: GKD_ICONS.trishul, label: 'முதுநிலை: மெய்கண்ட சாத்திரங்கள்', action: "scrollToSection('tierPG')" },
      { id: 'tab-hs-phd', icon: GKD_ICONS.crown, label: 'கலாநிதி ஆய்வுப் பீடம்', action: "scrollToSection('tierPhD')" },
      { id: 'tab-hs-glossary', icon: GKD_ICONS.book, label: 'வேதாந்தக் கலைச்சொற்கள்', action: "scrollToSection('glossarySection')" },
      { id: 'tab-hs-cert', icon: GKD_ICONS.scroll, label: 'ஆய்வுப் பட்டயம்', action: "scrollToSection('fellowshipSection')" },
      { id: 'tab-hs-school', icon: GKD_ICONS.school, label: 'இணையப் பள்ளி', href: 'school.html' },
      { id: 'tab-hs-grades', icon: GKD_ICONS.leaf, label: '12 நிலைகள்', href: 'kalvi.html' }
    ];
  }

  // 3. Virtues Matrix (virtues.html)
  if (filename === 'virtues.html') {
    return [
      { id: 'tab-all', icon: GKD_ICONS.flame, label: 'அனைத்து நற்பண்புகள் (30+)', action: "filterVirtues('all')", active: true },
      { id: 'tab-t1', icon: '<svg class="gkd-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="7" fill="#22c55e"/></svg>', label: 'பருவம் 1: அறிதல் (தரம் 1-4)', action: "filterVirtues('tier-1')" },
      { id: 'tab-t2', icon: '<svg class="gkd-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="7" fill="#eab308"/></svg>', label: 'பருவம் 2: செய்தல் (தரம் 5-8)', action: "filterVirtues('tier-2')" },
      { id: 'tab-t3', icon: '<svg class="gkd-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="7" fill="#ef4444"/></svg>', label: 'பருவம் 3: காத்தல் (தரம் 9-12)', action: "filterVirtues('tier-3')" },
      { id: 'tab-kalvi', icon: GKD_ICONS.leaf, label: 'வாழ்வியல் மையம்', href: 'kalvi.html' }
    ];
  }

  // 4. Master Home (index.html - Guru Kula Ashram Sanctuary)
  if (filename === 'index.html' || filename === '') {
    return [
      { id: 'tab-home', icon: GKD_ICONS.temple, label: 'ஆசிரம முகப்பு', href: 'index.html', active: true },
      { id: 'tab-kalvi', icon: GKD_ICONS.leaf, label: 'தர்ம குடீரம் (12 நிலைகள்)', href: 'kalvi.html' },
      { id: 'tab-school', icon: GKD_ICONS.school, label: 'வித்யா குடீரம்', href: 'school.html' },
      { id: 'tab-pedagogy', icon: GKD_ICONS.scroll, label: 'போதனை மரபு', action: "scrollToSection('ashramPedagogy')" },
      { id: 'tab-dinacharya', icon: GKD_ICONS.deepam, label: 'தினசரி காலச்சக்கரம்', action: "scrollToSection('ashramDinacharya')" },
      { id: 'tab-yagna', icon: GKD_ICONS.flame, label: 'பஞ்ச மகா யக்ஞம்', action: "scrollToSection('ashramPanchaYagna')" },
      { id: 'tab-featured', icon: GKD_ICONS.cinema, label: 'கான அரங்கம்', action: "scrollToSection('featuredScreeningRoom')" },
      { id: 'tab-catalog', icon: GKD_ICONS.cinema, label: '580 சுவடிக் களஞ்சியம்', href: 'youtube.html' },
      { id: 'tab-contact', icon: GKD_ICONS.mapPin, label: 'ஆசிரம முகவரி', action: "scrollToSection('siteFooter')" }
    ];
  }

  // 5. Saiva Neri (saiva-neri.html)
  if (filename === 'saiva-neri.html') {
    return [
      { id: 'tab-all-shiva', icon: GKD_ICONS.trishul, label: 'அனைத்து சிவப்பதிகங்கள் (172)', action: "setTypeFilter('all')", active: true },
      { id: 'tab-thevaram', icon: GKD_ICONS.leaf, label: 'தேவாரம்', action: "filterByText('தேவாரம்')" },
      { id: 'tab-thiruvasagam', icon: GKD_ICONS.om, label: 'திருவாசகம்', action: "filterByText('திருவாசகம்')" },
      { id: 'tab-thirumandhiram', icon: GKD_ICONS.om, label: 'திருமந்திரம்', action: "filterByText('திருமந்திரம்')" },
      { id: 'tab-rudram', icon: GKD_ICONS.flame, label: 'ஸ்ரீ ருத்ரம்', action: "filterByText('ருத்ரம்')" }
    ];
  }

  // 6. Traditions / Deities
  if (['murugan.html', 'sakthi.html', 'vinayagar.html', 'vaishnava.html'].includes(filename)) {
    return [
      { id: 'tab-murugan', icon: GKD_ICONS.trishul, label: 'முருகன் (Kaumaram)', href: 'murugan.html', active: filename === 'murugan.html' },
      { id: 'tab-sakthi', icon: GKD_ICONS.lotus, label: 'சக்தி (Shaktham)', href: 'sakthi.html', active: filename === 'sakthi.html' },
      { id: 'tab-vinayagar', icon: GKD_ICONS.ganesha, label: 'விநாயகர் (Ganapathyam)', href: 'vinayagar.html', active: filename === 'vinayagar.html' },
      { id: 'tab-vaishnava', icon: GKD_ICONS.lotus, label: 'வைணவம் (Vaishnavam)', href: 'vaishnava.html', active: filename === 'vaishnava.html' }
    ];
  }

  // 7. Thirukkural (thirukkural.html)
  if (filename === 'thirukkural.html') {
    return [
      { id: 'tab-all-tk', icon: GKD_ICONS.book, label: 'அனைத்து குறள்கள் (185)', action: "setTypeFilter('all')", active: true },
      { id: 'tab-illaraviyal', icon: GKD_ICONS.home, label: 'இல்லறவியல் (20)', action: "filterIllaraviyal()" },
      { id: 'tab-aram', icon: GKD_ICONS.leaf, label: 'அறத்துப்பால்', action: "filterByText('அறத்துப்பால்')" },
      { id: 'tab-porul', icon: GKD_ICONS.crown, label: 'பொருட்பால்', action: "filterByText('பொருட்பால்')" },
      { id: 'tab-inbam', icon: GKD_ICONS.lotus, label: 'காமத்துப்பால்', action: "filterByText('காமத்துப்பால்')" },
      { id: 'tab-films-tk', icon: GKD_ICONS.cinema, label: 'குறள் திரைப்படங்கள்', action: "setTypeFilter('film')" },
      { id: 'tab-review-qa', icon: GKD_ICONS.science, label: 'திரைப் பரிசோதனை கூடம் (QA)', href: 'review_quality.html' }
    ];
  }

  // 7b. Film Quality Screening Room (review_quality.html)
  if (filename === 'review_quality.html') {
    return [
      { id: 'tab-rev-5', icon: GKD_ICONS.home, label: 'அதி 5 (இல்வாழ்க்கை)', action: "loadChapter(5)" },
      { id: 'tab-rev-8', icon: GKD_ICONS.lotus, label: 'அதி 8 (அன்புடைமை)', action: "loadChapter(8)" },
      { id: 'tab-rev-16', icon: GKD_ICONS.temple, label: 'அதி 16 (பொறையுடைமை)', action: "loadChapter(16)" },
      { id: 'tab-rev-26', icon: GKD_ICONS.leaf, label: 'அதி 26 (புலால்)', action: "loadChapter(26)" },
      { id: 'tab-rev-27', icon: GKD_ICONS.om, label: 'அதி 27 (தவம்)', action: "loadChapter(27)" },
      { id: 'tab-rev-52', icon: GKD_ICONS.crown, label: 'அதி 52 (தெரிந்து)', action: "loadChapter(52)" },
      { id: 'tab-rev-54', icon: GKD_ICONS.target, label: 'அதி 54 (பொச்சா)', action: "loadChapter(54)" },
      { id: 'tab-rev-57', icon: GKD_ICONS.book, label: 'அதி 57 (வெருவந்த)', action: "loadChapter(57)" },
      { id: 'tab-rev-61', icon: GKD_ICONS.flame, label: 'அதி 61 (மடி)', action: "loadChapter(61)" },
      { id: 'tab-rev-back', icon: GKD_ICONS.book, label: 'திருக்குறள் தளம்', href: 'thirukkural.html' }
    ];
  }

  // 8. Sanmargam (sanmargam.html)
  if (filename === 'sanmargam.html') {
    return [
      { id: 'tab-all-san', icon: GKD_ICONS.deepam, label: 'திருவருட்பா படைப்புகள் (94)', action: "setTypeFilter('all')", active: true },
      { id: 'tab-jeeva', icon: GKD_ICONS.flame, label: 'ஜீவகாருண்யம்', action: "filterByText('ஜீவகாருண்யம்')" },
      { id: 'tab-jyoti', icon: GKD_ICONS.deepam, label: 'ஜோதி வழிபாடு', action: "filterByText('ஜோதி')" },
      { id: 'tab-audio-san', icon: GKD_ICONS.music, label: 'சன்மார்க்க இசை', action: "setTypeFilter('audio')" }
    ];
  }

  // 9. Irai Isai Virundhu (irai-isai-virundhu.html)
  if (filename === 'irai-isai-virundhu.html') {
    return [
      { id: 'tab-isai-all', icon: GKD_ICONS.music, label: '5 சிறப்புப் படைப்புகள்', action: "setTypeFilter('all')", active: true },
      { id: 'tab-isai-palum', icon: GKD_ICONS.deepam, label: 'பாலும் தெளிதேனும்', action: "filterByText('பாலும்')" },
      { id: 'tab-isai-guru', icon: GKD_ICONS.pranam, label: 'குரு வணக்கம்', action: "filterByText('குரு வணக்கம்')" },
      { id: 'tab-isai-kandhar', icon: GKD_ICONS.trishul, label: 'கந்தர் அநுபூதி', action: "filterByText('அநுபூதி')" },
      { id: 'tab-isai-bharathi', icon: GKD_ICONS.temple, label: 'பாரதியார் கானம்', action: "filterByText('பாரதியார்')" },
      { id: 'tab-isai-sivapuranam', icon: GKD_ICONS.deepam, label: 'சிவபுராணம்', action: "filterByText('சிவபுராணம்')" },
      { id: 'tab-isai-yt', icon: GKD_ICONS.play, label: 'காணொளிகள்', href: 'youtube.html' }
    ];
  }

  // 10. YouTube Vault (youtube.html)
  if (filename === 'youtube.html') {
    return [
      { id: 'tab-yt-all', icon: GKD_ICONS.play, label: 'அனைத்து காணொளிகள் (580)', action: "setTypeFilter('all')", active: true },
      { id: 'tab-yt-films', icon: GKD_ICONS.cinema, label: 'திரைப்படங்கள்', action: "setTypeFilter('film')" },
      { id: 'tab-yt-audio', icon: GKD_ICONS.music, label: 'இசைப் பாடல்கள்', action: "setTypeFilter('audio')" },
      { id: 'tab-yt-isai', icon: GKD_ICONS.music, label: 'இறை இசை', href: 'irai-isai-virundhu.html' },
      { id: 'tab-yt-saiva', icon: GKD_ICONS.trishul, label: 'சைவ நெறி', href: 'saiva-neri.html' },
      { id: 'tab-yt-kural', icon: GKD_ICONS.book, label: 'திருக்குறள்', href: 'thirukkural.html' }
    ];
  }

  // 11. About / Periyava (about.html)
  if (filename === 'about.html') {
    return [
      { id: 'tab-periyava-darshan', icon: GKD_ICONS.flame, label: 'மகா பெரியவா தரிசனம்', action: "scrollToSection('darshanSection')", active: true },
      { id: 'tab-deivathin-kural', icon: GKD_ICONS.book, label: 'தெய்வத்தின் குரல்', action: "scrollToSection('teachingsSection')" },
      { id: 'tab-vedic-preservation', icon: GKD_ICONS.om, label: 'வேத சம்ரக்ஷணம்', action: "scrollToSection('vedicSection')" },
      { id: 'tab-hq-address', icon: GKD_ICONS.mapPin, label: 'மைய முகவரி', action: "scrollToSection('siteFooter')" }
    ];
  }

  // 12. Syllabus (syllabus.html)
  if (filename === 'syllabus.html') {
    return [
      { id: 'tab-syl-patanjali', icon: GKD_ICONS.om, label: 'பதஞ்சலி 7 படிநிலைகள்', action: "scrollToSection('patanjaliSyllabus')", active: true },
      { id: 'tab-syl-meter', icon: GKD_ICONS.search, label: 'சுய ஆய்வு மதிப்பீடு', action: "scrollToSection('patanjaliAssessmentTool')" },
      { id: 'tab-syl-virtues', icon: GKD_ICONS.virtues, label: '4 வாழ்வியல் பருவங்கள்', action: "scrollToSection('virtue-mapping')" },
      { id: 'tab-syl-grades', icon: GKD_ICONS.leaf, label: '12 வகுப்புகள் பாடநெறி', href: 'kalvi.html' },
      { id: 'tab-syl-classes', icon: GKD_ICONS.clock, label: 'வகுப்பு அட்டவணை', href: 'classes.html' }
    ];
  }

  // 13. Classes (classes.html)
  if (filename === 'classes.html') {
    return [
      { id: 'tab-classes-overview', icon: GKD_ICONS.temple, label: 'வகுப்புகள் அட்டவணை', action: "scrollToSection('timetableSection')", active: true },
      { id: 'tab-classes-syl', icon: GKD_ICONS.book, label: 'முழு பாடத்திட்டம்', href: 'syllabus.html' },
      { id: 'tab-classes-grades', icon: GKD_ICONS.leaf, label: '12 வாழ்வியல் நிலைகள்', href: 'kalvi.html' },
      { id: 'tab-classes-school', icon: GKD_ICONS.school, label: 'இணையப் பள்ளி', href: 'school.html' }
    ];
  }

  // 14. Google Sites Mirror (google-site.html)
  if (filename === 'google-site.html') {
    return [
      { id: 'tab-gs-frame', icon: GKD_ICONS.globe, label: 'கூகிள் தளம்', action: "scrollToSection('googleSiteLinks')", active: true },
      { id: 'tab-gs-about', icon: GKD_ICONS.temple, label: 'குருவருள்', href: 'about.html' },
      { id: 'tab-gs-home', icon: GKD_ICONS.home, label: 'முகப்பு', href: 'index.html' }
    ];
  }

  // 15. Help & Support Hub (help.html)
  if (filename === 'help.html') {
    return [
      { id: 'tab-help-student', icon: GKD_ICONS.grad, label: 'மாணவர் வழிகாட்டி', action: "scrollToSection('studentGuideSection')", active: true },
      { id: 'tab-help-guru', icon: GKD_ICONS.school, label: 'ஆசான் வழிகாட்டி', action: "scrollToSection('guruGuideSection')" },
      { id: 'tab-help-user', icon: GKD_ICONS.user, label: 'பயனர் வழிகாட்டி', action: "scrollToSection('userGuideSection')" },
      { id: 'tab-help-faq', icon: GKD_ICONS.question, label: 'பொதுக் கேள்விகள் (FAQ)', action: "scrollToSection('faqSection')" },
      { id: 'tab-help-school', icon: GKD_ICONS.school, label: 'இணையப் பள்ளி', href: 'school.html' }
    ];
  }

  // Default fallback
  return [
    { id: 'tab-home', icon: GKD_ICONS.home, label: 'முகப்பு', href: 'index.html' },
    { id: 'tab-kalvi', icon: GKD_ICONS.leaf, label: 'வாழ்வியல் நெறி', href: 'kalvi.html' },
    { id: 'tab-virtues', icon: GKD_ICONS.virtues, label: 'நற்பண்புகள்', href: 'virtues.html' },
    { id: 'tab-saiva', icon: GKD_ICONS.om, label: 'சைவ நெறி', href: 'saiva-neri.html' }
  ];
}

function scrollToSection(id, optionalTabId) {
  if (optionalTabId && typeof switchCourseTab === 'function') {
    switchCourseTab(optionalTabId);
  }
  let el = document.getElementById(id) || document.querySelector('.' + id);
  if (!el) {
    const fallbacks = {
      'courseUnits': ['#course-content-start', '#unit-panel-1', '.sheets-grid', '#sheets-section', '.course-layout', '#curriculumGrid'],
      'gradeVirtueBox': ['#syllabus-highlights', '.scripture-study-section', '#side-group-virtue', '.virtue-card', '#virtue-mapping', '.virtue-section'],
      'visualDiagramCard': ['.lesson-hero-visual-card', '.visual-card', '.infographic-card', '.lesson-video-microclip-card', '.poster-container'],
      'quizSection': ['.interactive-quiz', '.quiz-card', '.quiz-container', '.quiz-panel', '#quizSection'],
      'sadhanaBox': ['.sadhana-box', '#grihasthaTracker', '#familyCharter']
    };
    if (fallbacks[id]) {
      for (let i = 0; i < fallbacks[id].length; i++) {
        el = document.querySelector(fallbacks[id][i]);
        if (el) break;
      }
    }
  }
  if (el) {
    const yOffset = -75;
    const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
    window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' });
  }
}

function filterByText(keyword) {
  const searchInput = document.getElementById('contextQuickSearch') || document.getElementById('searchInput');
  if (searchInput) {
    searchInput.value = keyword;
    handleContextSearch(keyword);
  }
}

function renderContextTabsIntoHeader() {
  const headerContainer = document.querySelector('.header-container');
  if (!headerContainer) return;

  // 1. Remove or hide the old duplicate main-nav
  const oldNav = document.getElementById('mainNav');
  if (oldNav) {
    oldNav.style.display = 'none';
  }

  // 2. Remove any previous context-tabs-nav or right tools
  const existingTabs = document.getElementById('contextTabsNav');
  if (existingTabs && existingTabs.parentNode) existingTabs.parentNode.removeChild(existingTabs);
  const existingTools = document.querySelector('.header-right-tools');
  if (existingTools && existingTools.parentNode) existingTools.parentNode.removeChild(existingTools);

  // 3. Build Context-Sensitive Menu Tabs with Primary Hamburger Trigger
  const tabs = getContextTabsForPage();
  const tabsNav = document.createElement('nav');
  tabsNav.id = 'contextTabsNav';
  tabsNav.className = 'context-tabs-nav';
  tabsNav.setAttribute('aria-label', 'Context Specific Tabs');

  const hamburgerBtnHtml = `
    <button type="button" class="primary-hamburger-btn" onclick="togglePrimaryMenu()" title="முதன்மை பட்டி (6 பிரிவுகள்)" aria-label="முதன்மை பட்டி">
      <span class="hb-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg></span>
      <span class="hb-emblem"><svg class="gkd-icon gkd-om-icon" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8.2 10.5c-.3-.7-.2-1.5.3-2.1.8-.9 2.2-.9 3 .1.4.5.5 1.2.2 1.8-.4.7-1.1 1.2-1.7 1.7.9.3 1.7.9 2 1.7.4 1.1 0 2.4-1 3.1-1.2.9-2.9.7-3.9-.4-.4-.5-.6-1.1-.6-1.7h1.4c0 .4.2.8.5 1 .6.5 1.5.4 2-.1.4-.4.5-1 .2-1.5-.4-.7-1.2-1-2-1v-1.2c.6 0 1.2-.2 1.5-.7.3-.4.3-.9 0-1.3-.4-.5-1.1-.6-1.6-.2-.3.2-.5.6-.5 1H8.2zm6.3-2.5c.8 0 1.5.5 1.8 1.2l-1.2.5c-.2-.4-.5-.6-.8-.6-.6 0-1 .4-1 1s.4 1 1 1c.5 0 .9-.3 1.1-.7l1.1.6c-.4.8-1.2 1.3-2.2 1.3-1.4 0-2.4-1-2.4-2.4 0-1.3 1-2.4 2.4-2.4zm1.5-1.5c.3 0 .5.2.5.5s-.2.5-.5.5-.5-.2-.5-.5.2-.5.5-.5z"/></svg></span>
      <span class="hb-label">முதன்மை பட்டி</span>
    </button>
  `;

  tabsNav.innerHTML = hamburgerBtnHtml + tabs.map((t, idx) => {
    if (t.href) {
      return `
        <a href="${t.href}" class="context-tab-pill ${t.active ? 'active' : ''}" id="${t.id}">
          <span class="context-tab-pill-icon">${t.icon}</span>
          <span>${t.label}</span>
        </a>
      `;
    } else {
      return `
        <button type="button" class="context-tab-pill ${t.active || idx === 0 ? 'active' : ''}" id="${t.id}" onclick="handleTabClick(this, '${t.action}')">
          <span class="context-tab-pill-icon">${t.icon}</span>
          <span>${t.label}</span>
        </button>
      `;
    }
  }).join('');

  // 4. Build Right Tools Dock
  const rightTools = document.createElement('div');
  rightTools.className = 'header-right-tools';
  rightTools.innerHTML = `
    <div class="context-search-wrapper">
      <span class="context-search-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></span>
      <input type="text" id="contextQuickSearch" class="context-search-input" placeholder="தேடுக... [/]" oninput="handleContextSearch(this.value)" autocomplete="off">
      <button type="button" class="context-search-clear" id="contextSearchClear" onclick="clearContextSearch()" style="display: none;"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
    </div>

    <div class="context-tool-group">
      <button type="button" class="context-tool-btn font-dec-btn" onclick="adjustFontSize(-0.06)" title="எழுத்தளவைக் குறைக்க (A-)">A⁻</button>
      <span class="font-scale-indicator" id="fontScaleIndicator" title="தற்போதைய எழுத்தளவு">100%</span>
      <button type="button" class="context-tool-btn font-inc-btn" onclick="adjustFontSize(0.06)" title="எழுத்தளவை அதிகரிக்க (A+)">A⁺</button>
    </div>

    <button type="button" class="context-tool-btn ambient-drone-btn" id="ambientDroneBtn" onclick="toggleAmbientDrone()" title="நாத தியான ஒலி (Ambient Tanpura Drone)"><span class="drone-icon" id="ambientDroneIcon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2c-.8 2-1.5 3.5-1.5 5a1.5 1.5 0 0 0 3 0c0-1.5-.7-3-1.5-5z" fill="currentColor"/><path d="M5 13c0 4 3 6 7 6s7-2 7-6H5z"/><path d="M10 19v2h4v-2"/></svg></span></button>
        <button type="button" class="context-tool-btn theme-quick-btn" onclick="cycleTheme()" title="வண்ணக் கருப்பொருள் மாற்று">
      <span class="theme-icon" id="themeQuickIcon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg></span>
    </button>

    <button type="button" class="context-profile-pill" onclick="openUserSettingsModal('profile')" title="பயனர் சுயவிவரம் &amp; அமைப்புகள்">
      <span class="pill-avatar" id="pillAvatarIcon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span>
      <span class="pill-name" id="pillUserName">சாதகர்</span>
    </button>
  `;

  headerContainer.appendChild(tabsNav);
  headerContainer.appendChild(rightTools);
}

function handleTabClick(btn, actionStr) {
  // Update active pill state
  const parent = btn.closest('.context-tabs-nav');
  if (parent) {
    parent.querySelectorAll('.context-tab-pill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }
  // Execute action
  try {
    const fn = new Function(actionStr);
    fn();
  } catch (e) {
    console.error('Error executing tab action:', e);
  }
}


function mountAppShell() {
  if (document.getElementById('leftStripBar')) return;

  const currentPath = (window.location.pathname.split('/').pop() || 'index.html').toLowerCase();
  const ctx = resolvePageContext();

  renderContextTabsIntoHeader();

  // 1. Mobile Backdrop
  const backdrop = document.createElement('div');
  backdrop.id = 'stripBackdrop';
  backdrop.className = 'strip-backdrop';
  backdrop.onclick = closeMobileStrip;
  document.body.appendChild(backdrop);

  // 2. Left Strip Bar
  const strip = document.createElement('aside');
  strip.id = 'leftStripBar';
  strip.className = 'left-strip-bar';
  strip.setAttribute('aria-label', 'Quick Portals');

  const navItems = [
    { href: 'index.html', icon: GKD_ICONS.home, label: 'முகப்பு' },
    { href: 'kalvi.html', icon: GKD_ICONS.leaf, label: 'வாழ்வியல் நெறி' },
    { href: 'virtues.html', icon: GKD_ICONS.virtues, label: 'நற்பண்புகள்' },
    { href: 'saiva-neri.html', icon: GKD_ICONS.om, label: 'சைவ நெறி' },
    { href: 'irai-isai-virundhu.html', icon: GKD_ICONS.music, label: 'இறை இசை' },
    { href: 'thirukkural.html', icon: GKD_ICONS.scroll, label: 'திருக்குறள்' },
    { href: 'sanmargam.html', icon: GKD_ICONS.flame, label: 'சன்மார்க்கம்' },
    { href: 'murugan.html', icon: GKD_ICONS.vel, label: 'முருகன்' },
    { href: 'sakthi.html', icon: GKD_ICONS.lotus, label: 'சக்தி நெறி' },
    { href: 'vinayagar.html', icon: GKD_ICONS.ganesha, label: 'விநாயகர்' },
    { href: 'vaishnava.html', icon: GKD_ICONS.chakra, label: 'வைணவம்' },
    { href: 'syllabus.html', icon: GKD_ICONS.book, label: 'பாடத்திட்டம்' },
    { href: 'about.html', icon: GKD_ICONS.temple, label: 'பெரியவா' }
  ];

  strip.innerHTML = `
    <div class="strip-header">
      <a href="index.html" class="strip-brand-link" title="குரு குல தேசம்">
        <span class="strip-emblem">ॐ</span>
        <span class="strip-brand-text">குரு குல தேசம்</span>
      </a>
      <button type="button" class="strip-toggle-btn" id="stripToggleBtn" onclick="toggleLeftStrip()" title="விரிவுபடுத்து / சுருக்கு">
        <span class="strip-toggle-icon"><svg class="gkd-icon gkd-arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg></span>
      </button>
    </div>

    <nav class="strip-nav-list" id="stripNavList">
      ${navItems.map(item => `
        <a href="${item.href}" class="strip-item ${currentPath === item.href ? 'active' : ''}" data-tooltip="${item.label}">
          <span class="strip-item-icon">${item.icon}</span>
          <span class="strip-item-label">${item.label}</span>
        </a>
      `).join('')}
    </nav>

    <div class="strip-footer-dock">
      <a href="help.html" class="strip-dock-btn" title="உதவி &amp; வழிகாட்டல் (Help &amp; Support)">
        <span class="strip-item-icon">${GKD_ICONS.question}</span>
        <span class="strip-dock-label">உதவி மையம்</span>
      </a>
      <button type="button" class="strip-dock-btn" onclick="openUserSettingsModal('preferences')" title="அமைப்புகள்">
        <span class="strip-item-icon">${GKD_ICONS.settings}</span>
        <span class="strip-dock-label">அமைப்புகள்</span>
      </button>
      <button type="button" class="strip-dock-btn profile-dock-btn" onclick="openUserSettingsModal('profile')" title="சுயவிவரம்">
        <span class="strip-dock-avatar" id="stripAvatarIcon">${GKD_ICONS.user}</span>
        <span class="strip-dock-label" id="stripUserName">சுயவிவரம்</span>
      </button>
    </div>
  `;

  document.body.prepend(strip);

  // Restore strip expanded state on desktop
  if (window.innerWidth >= 992 && localStorage.getItem('GURUKULA_STRIP_EXPANDED') === 'true') {
    strip.classList.add('expanded');
    document.body.classList.add('strip-expanded');
    const toggleIcon = strip.querySelector('.strip-toggle-icon');
    if (toggleIcon) toggleIcon.innerHTML = '<svg class="gkd-icon gkd-arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>';
  }

  // 3. Context Sensitive Top Bar
  const contextBar = document.createElement('div');
  contextBar.id = 'contextSensitiveBar';
  contextBar.className = 'context-sensitive-bar';
  contextBar.innerHTML = `
    <div class="context-bar-inner">
      <div class="context-left">
        <button type="button" class="context-strip-trigger" onclick="toggleLeftStrip()" title="பக்கப்பட்டி திறக்க/மூட">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <button type="button" class="context-back-btn" onclick="if(window.history.length > 1){ window.history.back(); } else { window.location.href='index.html'; }" title="பின்னே செல்ல (Go Back)">
          <svg class="gkd-icon gkd-arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          <span class="context-back-label">பின்னே</span>
        </button>
        <div class="context-breadcrumbs" id="contextBreadcrumbs">
          <span class="crumb-root">${ctx.root}</span>
          <span class="crumb-separator">/</span>
          <span class="crumb-current" id="contextCurrentTitle">${ctx.title}</span>
        </div>
      </div>

      <div class="context-right">
        <div class="context-search-wrapper">
          <span class="context-search-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></span>
          <input type="text" id="contextQuickSearch" class="context-search-input" placeholder="தேடுக... [/]" oninput="handleContextSearch(this.value)" autocomplete="off">
          <button type="button" class="context-search-clear" id="contextSearchClear" onclick="clearContextSearch()" style="display: none;"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
        </div>

        <div class="context-tool-group">
          <button type="button" class="context-tool-btn font-dec-btn" onclick="adjustFontSize(-0.06)" title="எழுத்தளவைக் குறைக்க (A-)"><span style="font-size:0.9em; font-weight:700">A</span><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" style="width:0.7em; height:0.7em; vertical-align:0.35em"><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
          <span class="font-scale-indicator" id="fontScaleIndicator" title="தற்போதைய எழுத்தளவு">100%</span>
          <button type="button" class="context-tool-btn font-inc-btn" onclick="adjustFontSize(0.06)" title="எழுத்தளவை அதிகரிக்க (A+)"><span style="font-size:0.9em; font-weight:700">A</span><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" style="width:0.7em; height:0.7em; vertical-align:0.35em"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></button>
        </div>

        <button type="button" class="context-tool-btn ambient-drone-btn" id="ambientDroneBtn" onclick="toggleAmbientDrone()" title="நாத தியான ஒலி (Ambient Tanpura Drone)"><span class="drone-icon" id="ambientDroneIcon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2c-.8 2-1.5 3.5-1.5 5a1.5 1.5 0 0 0 3 0c0-1.5-.7-3-1.5-5z" fill="currentColor"/><path d="M5 13c0 4 3 6 7 6s7-2 7-6H5z"/><path d="M10 19v2h4v-2"/></svg></span></button>
        <button type="button" class="context-tool-btn theme-quick-btn" onclick="cycleTheme()" title="வண்ணக் கருப்பொருள் மாற்று">
          <span class="theme-icon" id="themeQuickIcon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg></span>
        </button>
        <a href="help.html" class="context-tool-btn" title="உதவி &amp; வழிகாட்டல் (Help &amp; Support)">
          <span class="theme-icon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></span>
        </a>

        <button type="button" class="context-profile-pill" onclick="openUserSettingsModal('profile')" title="பயனர் சுயவிவரம் &amp; அமைப்புகள்">
          <span class="pill-avatar" id="pillAvatarIcon"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span>
          <span class="pill-name" id="pillUserName">சாதகர்</span>
          <span class="pill-badge" id="pillUserTier">தரம் 1-4</span>
        </button>
      </div>
    </div>
  `;

  // Attach inside header for unified sticky behavior
  const header = document.querySelector('header.site-header');
  if (header) {
    header.appendChild(contextBar);
  } else {
    document.body.prepend(contextBar);
  }

  // 4. User Profile & Settings Modal
  const modal = document.createElement('div');
  modal.id = 'userSettingsModal';
  modal.className = 'user-settings-modal';
  modal.onclick = function(e) { if (e.target === this) closeUserSettingsModal(); };
  modal.innerHTML = `
    <div class="user-modal-box">
      <div class="user-modal-header">
        <div class="user-modal-tabs">
          <button type="button" class="user-tab-btn active" id="userTabProfileBtn" onclick="switchUserTab('profile')">
            <span><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> சுயவிவரம்</span>
          </button>
          <button type="button" class="user-tab-btn" id="userTabPrefsBtn" onclick="switchUserTab('preferences')">
            <span><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg> விருப்பங்கள் &amp; அமைப்புகள்</span>
          </button>
        </div>
        <button type="button" class="user-modal-close-btn" onclick="closeUserSettingsModal()" title="மூடுக"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg></button>
      </div>

      <div class="user-modal-body">
        <!-- PROFILE TAB -->
        <div class="user-tab-content active" id="tabContentProfile">
          <div class="profile-hero-card">
            <div class="profile-avatar-large" id="profileLargeAvatar"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>
            <div class="profile-hero-info">
              <h3 id="profileDisplayNameHead">அன்பான சாதகர்</h3>
              <span class="profile-tier-badge" id="profileTierBadge">தொடக்க சாதகர் (Grade 1-4)</span>
              <p class="profile-streak-line"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c1 3 3 4.5 4.5 7 1.5 2.5 1.5 5.5 0 8s-4 4-6.5 4c-3 0-5.5-2.5-5.5-6 0-3.5 2-6 4-8.5.5 1.5 1.5 2.5 2.5 2.5.5-2 .5-4.5 1-7z"/></svg> தொடர் கற்றல்: <strong id="profileStreakDays">1 நாள்</strong> • படித்த அலகுகள்: <strong id="profileLessonsCount">0</strong></p>
            </div>
          </div>

          <div class="settings-form-group">
            <label class="settings-label">உங்கள் பெயர் அல்லது ஆன்மீகப் பெயர்:</label>
            <input type="text" id="prefUserNameInput" class="settings-input" placeholder="உங்கள் பெயர்" maxlength="30" oninput="saveUserProfileFields()">
          </div>

          <div class="settings-form-group">
            <label class="settings-label">ஆன்மீக நிலை / தரம் (Spiritual Learning Level):</label>
            <select id="prefUserTierSelect" class="settings-select" onchange="saveUserProfileFields()">
              <option value="tier1">தொடக்க சாதகர் — தரம் 1 முதல் 4 (அறம் அறிதல்)</option>
              <option value="tier2">இடைநிலை சாதகர் — தரம் 5 முதல் 8 (அறம் பின்பற்றுதல்)</option>
              <option value="tier3">உயர்நிலை சிவநேசர் — தரம் 9 முதல் 12 (அறம் காத்தல்)</option>
            </select>
          </div>

          <div class="settings-form-group">
            <label class="settings-label">சுயவிவரச் சின்னம் (Choose Avatar Icon):</label>
            <div class="avatar-selection-grid" id="avatarSelectionGrid">
              <button type="button" class="avatar-option" onclick="selectAvatar('user')" title="சாதகர்"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></button>
              <button type="button" class="avatar-option" onclick="selectAvatar('om')" title="பிரணவம்"><svg class="gkd-icon gkd-om-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 14.5a3.5 3.5 0 0 1-3.5-3.5 1 1 0 0 1 2 0 1.5 1.5 0 0 0 3 0 1.5 1.5 0 0 0-1.5-1.5H12a1 1 0 0 1 0-2h1a1.5 1.5 0 0 0 1.5-1.5A1.5 1.5 0 0 0 13 6.5a1 1 0 0 1 0-2 3.5 3.5 0 0 1 3.5 3.5 3.5 3.5 0 0 1-1.3 2.7A3.5 3.5 0 0 1 13 16.5z"/></svg></button>
              <button type="button" class="avatar-option" onclick="selectAvatar('deepam')" title="தீபம்"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c.5 2 2 3.5 2 5.5a2 2 0 1 1-4 0c0-2 1.5-3.5 2-5.5z"/><path d="M4 14c0 3 3.5 5 8 5s8-2 8-5H4z"/><path d="M9 19v3h6v-3"/></svg></button>
              <button type="button" class="avatar-option" onclick="selectAvatar('trishul')" title="திரிசூலம்"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M12 11a5 5 0 0 1 5-5v3M12 11a5 5 0 0 0-5-5v3"/></svg></button>
              <button type="button" class="avatar-option" onclick="selectAvatar('lotus')" title="தாமரை"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3c-2 4-2 8 0 11 2-3 2-7 0-11z"/><path d="M12 14c-4-1-7-4-8-8 3 0 7 3 8 8z"/><path d="M12 14c4-1 7-4 8-8-3 0-7 3-8 8z"/><path d="M3 16c3 2 6 2 9 0 3 2 6 2 9 0"/></svg></button>
              <button type="button" class="avatar-option" onclick="selectAvatar('flower')" title="மலர்"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2a4 4 0 0 0-4 4v1a4 4 0 0 0 8 0V6a4 4 0 0 0-4-4z"/><path d="M12 17a4 4 0 0 0-4 4v1a4 4 0 0 0 8 0v-1a4 4 0 0 0-4-4z"/><path d="M22 12a4 4 0 0 0-4-4h-1a4 4 0 0 0 0 8h1a4 4 0 0 0 4-4z"/><path d="M2 12a4 4 0 0 0 4-4h1a4 4 0 0 1 0 8H6a4 4 0 0 0-4-4z"/></svg></button>
              <button type="button" class="avatar-option" onclick="selectAvatar('book')" title="திருமுறை நூல்"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></button>
              <button type="button" class="avatar-option" onclick="selectAvatar('meditation')" title="தியானம்"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="5" r="2.5"/><path d="M6 21c1-4 3-7 6-7s5 3 6 7"/><path d="M4 13l4-2 4 3 4-3 4 2"/></svg></button>
              <button type="button" class="avatar-option" onclick="selectAvatar('crown')" title="மகுடம்"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 4l3 12h14l3-12-6 7-4-7-4 7-6-7zm3 16h14v2H5v-2z"/></svg></button>
            </div>
          </div>

          <div class="profile-stats-card">
            <h4><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg> உங்கள் ஆன்மீகப் பயணக் குறிப்பு (Personal Dashboard)</h4>
            <div class="stats-grid">
              <div class="stat-box">
                <div class="stat-number" id="statDaysVisited">1</div>
                <div class="stat-desc">வருகை நாட்கள்</div>
              </div>
              <div class="stat-box">
                <div class="stat-number" id="statLessonsCompleted">0</div>
                <div class="stat-desc">முடித்த பாடங்கள்</div>
              </div>
              <div class="stat-box">
                <div class="stat-number" id="statBookmarksCount">0</div>
                <div class="stat-desc">சேமித்தவை</div>
              </div>
            </div>
          </div>
        </div>

        <!-- PREFERENCES TAB -->
        <div class="user-tab-content" id="tabContentPreferences">
          <div class="settings-form-group">
            <label class="settings-label"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r=".5" fill="currentColor"/><circle cx="17.5" cy="10.5" r=".5" fill="currentColor"/><circle cx="8.5" cy="7.5" r=".5" fill="currentColor"/><circle cx="6.5" cy="12.5" r=".5" fill="currentColor"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg> வண்ணக் கருப்பொருள் (Theme Appearance):</label>
            <div class="radio-pill-group">
              <label class="radio-pill">
                <input type="radio" name="themeChoice" value="cosmic" onchange="changeTheme('cosmic')">
                <span>தர்மப் பேரொளி (Teal-Violet-Blue-Green - Default)</span>
              </label>
              <label class="radio-pill">
                <input type="radio" name="themeChoice" value="midnight" onchange="changeTheme('midnight')">
                <span>ஆழ்கடல் நீலம் (Midnight Ocean)</span>
              </label>
              <label class="radio-pill">
                <input type="radio" name="themeChoice" value="amoled" onchange="changeTheme('amoled')">
                <span>அடர் கருப்பு (OLED Pure Black)</span>
              </label>
            </div>
          </div>

          <div class="settings-form-group">
            <label class="settings-label"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L3 12.5V21h8.5z"/><line x1="16" y1="8" x2="2" y2="22"/><line x1="17.5" y1="15" x2="9" y2="15"/></svg> தமிழ் எழுத்துரு பாணி (Tamil Font Style):</label>
            <div class="radio-pill-group">
              <label class="radio-pill">
                <input type="radio" name="fontChoice" value="mukta" onchange="changeFontStyle('mukta')">
                <span>முக்த மலர் (மரபுச் செம்மொழி - Mukta Malar)</span>
              </label>
              <label class="radio-pill">
                <input type="radio" name="fontChoice" value="noto" onchange="changeFontStyle('noto')">
                <span>நோட்டோ சான்ஸ் (நவீனத் தெளிவு - Noto Sans Tamil)</span>
              </label>
            </div>
          </div>

          <div class="settings-form-group">
            <label class="settings-label"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg> தளத்தின் பொது எழுத்தளவு (Base Font Scaling):</label>
            <div class="font-size-slider-row">
              <button type="button" class="btn-secondary" onclick="adjustFontSize(-0.06)">A⁻ சிறிதாக்கு</button>
              <span id="sliderFontLabel" class="slider-font-label">100% (இயல்பு)</span>
              <button type="button" class="btn-secondary" onclick="adjustFontSize(0.06)">A⁺ பெரிதாக்கு</button>
            </div>
          </div>

          <div class="settings-form-group">
            <label class="settings-label"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="2.18"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="2" y1="17" x2="7" y2="17"/><line x1="17" y1="17" x2="22" y2="17"/><line x1="17" y1="7" x2="22" y2="7"/></svg> காணொளி &amp; ஒலி விருப்பங்கள் (Media Playback):</label>
            <div class="toggle-option-row">
              <span>தானியங்கி இயக்கம் (Autoplay Video on Open)</span>
              <input type="checkbox" id="prefAutoplay" class="toggle-checkbox" onchange="savePreferences()">
            </div>
            <div class="toggle-option-row">
              <span>தொடர் பின்னணி இசை பயன்முறை (Continuous Loop)</span>
              <input type="checkbox" id="prefContinuous" class="toggle-checkbox" onchange="savePreferences()">
            </div>
          </div>

          <div class="settings-form-group">
            <label class="settings-label"><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg> நற்பண்பு வழிகாட்டல் (Virtue Prompt):</label>
            <div class="toggle-option-row">
              <span>தினம் ஒரு ஆத்திசூடி / குறள் நற்பண்பு நினைவூட்டல்</span>
              <input type="checkbox" id="prefDailyVirtue" class="toggle-checkbox" onchange="savePreferences()">
            </div>
          </div>

          <div class="settings-actions-row">
            <a href="help.html" class="btn-secondary" style="text-decoration:none; display:inline-flex; align-items:center; gap:6px;">
              <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg> உதவி மையம்
            </a>
            <button type="button" class="btn-secondary" onclick="resetUserSettings()">
              <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg> மீட்டமை (Reset)
            </button>
            <button type="button" class="btn-primary" onclick="closeUserSettingsModal()">
              <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> சேமித்து மூடுக (Save &amp; Close)
            </button>
          </div>
        </div>
      </div>
    </div>
  `;

  document.body.appendChild(modal);

  // Initialize preferences
  loadUserPreferences();
  restorePatanjaliAssessment();
  restorePalmLeafMode();
  ensurePageBreadcrumb();
  highlightActiveSidebarGroup();
  restoreLMSProgress();
}

/**
 * Standardized Page Breadcrumb: Ensures every non-home page has a clear,
 * elegant navigation breadcrumb at the top of its main content area.
 */
function ensurePageBreadcrumb() {
  const main = document.querySelector('main.main-content');
  if (!main) return;
  // If a breadcrumb already exists in the document, don't duplicate
  if (main.querySelector('.page-breadcrumb') || main.querySelector('.breadcrumb-container')) return;

  const path = window.location.pathname.toLowerCase();
  const filename = path.split('/').pop() || 'index.html';
  if (filename === 'index.html' || filename === '') return; // No breadcrumb needed on root homepage

  const ctx = resolvePageContext();
  let rootLink = 'index.html';
  if (ctx.root === 'வாழ்வியல்' || ctx.root === 'கல்வி' || ctx.root === 'பாடத்திட்டம்' || ctx.root === 'வகுப்புகள்') {
    rootLink = 'kalvi.html';
  } else if (ctx.root === 'சைவ நெறி' || ctx.root === 'வழிபாட்டு நெறி') {
    rootLink = 'saiva-neri.html';
  } else if (ctx.root === 'தமிழ்மறை') {
    rootLink = 'thirukkural.html';
  } else if (ctx.root === 'சன்மார்க்கம்') {
    rootLink = 'sanmargam.html';
  } else if (ctx.root === 'இசை' || ctx.root === 'காணொளி') {
    rootLink = 'irai-isai-virundhu.html';
  } else if (ctx.root === 'காஞ்சி மகா பெரியவா') {
    rootLink = 'about.html';
  }

  const bc = document.createElement('div');
  bc.className = 'page-breadcrumb';
  bc.innerHTML = `
    <button type="button" class="breadcrumb-back-btn" onclick="if(window.history.length > 1){ window.history.back(); } else { window.location.href='${rootLink}'; }" title="பின்னே செல்ல (Go Back)">
      <svg class="gkd-icon gkd-arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
      <span>பின்னே</span>
    </button>
    <a href="index.html">${GKD_ICONS.home} முகப்பு</a>
    <span class="bc-sep">${GKD_ICONS.chevronRight}</span>
    <a href="${rootLink}">${ctx.root}</a>
    <span class="bc-sep">${GKD_ICONS.chevronRight}</span>
    <span class="bc-current">${ctx.title}</span>
  `;
  main.prepend(bc);
}

/**
 * Automatically highlights and expands the active group in the left strip bar
 * so the user always knows exactly where they are in the site hierarchy.
 */
function highlightActiveSidebarGroup() {
  const path = window.location.pathname.toLowerCase();
  const filename = path.split('/').pop() || 'index.html';

  document.querySelectorAll('#leftStripBar .strip-group').forEach(group => {
    // Check if any link inside matches current filename
    const matchingLink = group.querySelector(`a[href="${filename}"]`);
    if (matchingLink) {
      group.classList.add('active', 'open');
      matchingLink.classList.add('active');
      const ind = group.querySelector('.strip-sub-indicator');
      // Handled via CSS transform rotate
      // ind.innerText = '▴';
    } else if (filename.startsWith('tharam-') && group.getAttribute('data-group') === 'kalvi') {
      group.classList.add('active', 'open');
      const ind = group.querySelector('.strip-sub-indicator');
      // Handled via CSS transform rotate
      // ind.innerText = '▴';
      const gradePill = group.querySelector(`a[href="${filename}"]`);
      if (gradePill) gradePill.classList.add('active');
    }
  });
}

// Auto mount when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', mountAppShell);
} else {
  mountAppShell();
  hydrateModernIcons();
}

// Accordion support and Drawer auto-close on selection
document.addEventListener('click', (e) => {
  // 1. If clicked on a group header that has sub-items, TOGGLE THE ACCORDION!
  const subToggle = e.target.closest('.strip-item.strip-has-sub');
  if (subToggle) {
    e.preventDefault();
    e.stopPropagation();
    const group = subToggle.closest('.strip-group');
    if (group) {
      const wasOpen = group.classList.contains('open');
      // Close other open groups for clean single-accordion behavior
      document.querySelectorAll('.strip-group').forEach(g => {
        if (g !== group) {
          g.classList.remove('open');
          const ind = g.querySelector('.strip-sub-indicator');
          // Handled via CSS transform rotate
          // ind.innerText = '▾';
        }
      });
      group.classList.toggle('open', !wasOpen);
      const indicator = subToggle.querySelector('.strip-sub-indicator');
      if (indicator) {
        // Handled via CSS transform rotate
        // indicator.innerText = !wasOpen ? '▴' : '▾';
      }
    }
    return;
  }

  // 2. If clicked on an actual destination leaf link inside the drawer, close drawer
  const leafLink = e.target.closest('#leftStripBar .strip-sub-item, #leftStripBar .strip-item:not(.strip-has-sub)');
  if (leafLink) {
    closePrimaryMenu();
    return;
  }

  // 3. If clicked on backdrop, close drawer
  if (e.target.id === 'stripBackdrop') {
    closePrimaryMenu();
    return;
  }
});

// Graceful fallback for Google Sites scan images blocked cross-site (CORP: same-site)
document.addEventListener('error', function (e) {
  var img = e.target;
  if (!img || img.tagName !== 'IMG' || !/sitesv-images-rt/.test(img.src || '')) return;
  img.style.display = 'none';
  var thumb = img.closest('.sheet-thumb');
  if (thumb && !thumb.querySelector('.sheet-fallback')) {
    var d = document.createElement('div');
    d.className = 'sheet-fallback';
    d.style.cssText = 'display:flex;align-items:center;justify-content:center;min-height:140px;color:#94a3b8;font-size:0.85rem;text-align:center;padding:12px;';
    d.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H4a2 2 0 0 0-2 2v13a3 3 0 0 0 3 3h13a3 3 0 0 0 3-3V5a2 2 0 0 0-2-2h-7"/><path d="M19 18a3 3 0 0 0 0-6H6a2 2 0 0 0 0 4h12"/><line x1="8" y1="7" x2="14" y2="7"/><line x1="8" y1="11" x2="12" y2="11"/></svg> பக்கம் — Google Site இல் காண்க <svg class="gkd-icon gkd-external-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>';
    thumb.appendChild(d);
    var ov = thumb.querySelector('.sheet-zoom-overlay'); if (ov) ov.style.display = 'none';
    thumb.removeAttribute('onclick');
  }
}, true);

/* ========================================================================== */
/* FEATURE 1: PATANJALI 7-STAGE SELF-REALIZATION ASSESSMENT & RATING ENGINE   */
/* ========================================================================== */

function calculatePatanjaliScore() {
  const qNames = ['pq1', 'pq2', 'pq3', 'pq4', 'pq5', 'pq6', 'pq7'];
  let totalScore = 0;
  const answers = {};

  for (let i = 0; i < qNames.length; i++) {
    const radios = document.getElementsByName(qNames[i]);
    let val = 1;
    for (let r of radios) {
      if (r.checked) {
        val = parseInt(r.value, 10);
        break;
      }
    }
    answers[qNames[i]] = val;
    totalScore += val;
  }

  try {
    localStorage.setItem('gurukula_patanjali_answers', JSON.stringify(answers));
    localStorage.setItem('gurukula_patanjali_score', totalScore);
  } catch (e) {}

  renderPatanjaliResult(totalScore);
}

function renderPatanjaliResult(score) {
  const resultBox = document.getElementById('patScoreResultBox');
  const levelNameEl = document.getElementById('patResultLevelName');
  const starsEl = document.getElementById('patResultStars');
  const descEl = document.getElementById('patResultDesc');
  const actionEl = document.getElementById('patResultAction');

  if (!resultBox) return;

  let levelName = '';
  let stars = '';
  let desc = '';
  let badgeColor = '#38bdf8';
  let ratingNum = '1.0';
  let legacyAdvice = '';

  if (score <= 9) {
    ratingNum = '1.5';
    levelName = 'நிலை 1: சுபேச்சை (Subheccha) — நல்விருப்ப தொடக்க நிலை';
    stars = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>';
    badgeColor = '#38bdf8';
    desc = 'நீங்கள் தர்ம நெறியின் முதற்படியில் அடியெடுத்து வைத்துள்ளீர்கள். ஆன்மீக அமைதியை நாட வேண்டும் என்ற உன்னத விருப்பம் (சுபேச்சை) மலர்ந்துள்ளது. தரம் 1 - 4 தொடக்கப் பாடங்களை வாசித்து, கோபம் தணித்தல், தாய்-தந்தை வழிபாடு மற்றும் தினசரி எளிய தியானத்தில் ஈடுபடுங்கள்.';
    legacyAdvice = 'இல்லற அடித்தளம்: குடும்பத்தில் தினசரி 10 நிமிடம் அமைதி காத்தல், ஒரு குறள் வாசித்தல்.';
  } else if (score <= 12) {
    ratingNum = '2.8';
    levelName = 'நிலை 2: விசாரணை (Vicharana) — மெய்விசாரணை சாதகர் நிலை';
    stars = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>';
    badgeColor = '#2dd4bf';
    desc = 'சாத்திர விவேகமும் மெய்ப்பொருள் ஆய்வும் உங்களில் மலர்ந்துள்ளது. நித்திய-அநித்திய பகுத்தறிவுடன் வாழ்வியல் முடிவுகளை எடுக்கிறீர்கள். தரம் 5 - 8 பாடங்கள், திருமுறைத் தேவாரங்கள் மற்றும் பகவத் கீதை சிந்தனைகள் உங்கள் விவேகத்தை மேலும் கூர்மையாக்கும்.';
    legacyAdvice = 'இல்லற தர்மம்: குழந்தைகளுக்கு நல்லொழுக்கக் கதைகள் கற்பித்தல், எளிய ஜீவகாருண்ய தானம்.';
  } else if (score <= 15) {
    ratingNum = '4.2';
    levelName = 'நிலை 3: தனுமானசி (Tanumanasa) — நுண்ணிய மன அடக்கம் & இல்லற ஒழுக்கம்';
    stars = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>';
    badgeColor = '#c084fc';
    desc = 'புலனடக்கமும், கோப மேலாண்மையும் கைகூடியுள்ளது. மனம் சிதறாமல் தர்மத்தில் ஒருமுகப்பட்டுள்ளது. இல்லறத்தில் பஞ்ச மகா யக்ஞங்களைத் தவறாது கடைப்பிடித்து, சினமின்மை என்ற மாபெரும் தவத்தை உங்கள் இல்லத்தில் நிலைநிறுத்துங்கள்.';
    legacyAdvice = 'இல்லற தர்மம்: தினசரி பஞ்ச மகா யக்ஞ டிராக்கரை 30 நாட்கள் தொடர்ச்சியாக பூர்த்தி செய்தல்.';
  } else if (score <= 17) {
    ratingNum = '5.4';
    levelName = 'நிலை 4: சத்வாபத்தி (Sattvapatti) — தூய சத்துவ நிலை & பிரம்ம பாவனை';
    stars = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>';
    badgeColor = '#facc15';
    desc = 'அகத்தூய்மையும், விருப்பு-வெறுப்பற்ற சமநிலையும் ஆழமாக நிலவுகிறது. உலக சவால்கள் உங்கள் நிம்மதியைக் குலைப்பதில்லை. பதி, பசு, பாச மெய்யறிவை உணர்ந்து, உங்கள் குடும்பத்தை ஆன்மீகத் திருத்தலமாக வழிநடத்தும் சான்றோனாக மிளிர்கிறீர்கள்.';
    legacyAdvice = 'இல்லற தலைமை: குடும்ப அறநெறி சாசனம் (Family Charter) உருவாக்கி தலைமுறை நெறியாக்குதல்.';
  } else if (score <= 19) {
    ratingNum = '6.3';
    levelName = 'நிலை 5: அசம்சக்தி (Asamsakti) — பற்றற்ற நிஷ்காம கர்ம யோகம்';
    stars = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>';
    badgeColor = '#fb923c';
    desc = 'தாமரை இலைத் தண்ணீர் போல குடும்பப் பொறுப்புகளை முழுமையான அன்போடும் கடமையுணர்ச்சியோடும் நிறைவேற்றுகிறீர்கள்; அதே சமயம் எவ்வித சுயநலப் பற்றுமின்றி ஈசன் செயல் என சரணடைகிறீர்கள். மரண பயமற்ற ஜீவன் முக்திப் பாதைக்கு மிக அருகில் உள்ளீர்கள்.';
    legacyAdvice = 'உன்னத மரபு (Legacy): சமுதாய அறப்பணிகள், வித்யா தானம், இளைஞர்களுக்கு தர்ம வழிகாட்டல்.';
  } else {
    ratingNum = '7.0';
    levelName = 'நிலை 6 & 7: பதார்த்த பாவனை & துரியகா (Turiya) — ஜீவன் முக்தி & உன்னத சால்பு';
    stars = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 18h20v2H2z"/><path d="M3 18l2-11 5 5 4-7 4 7 5-5 2 11H3z"/></svg> <svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg><svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg> <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 18h20v2H2z"/><path d="M3 18l2-11 5 5 4-7 4 7 5-5 2 11H3z"/></svg>';
    badgeColor = '#e11d48';
    desc = '‘வையத்துள் வாழ்வாங்கு வாழ்பவன் வான்உறையும் தெய்வத்துள் வைக்கப் படும்’ (குறள் 50). குடும்பத்தை அறவழியில் உயர்த்தி, தலைமுறைகள் போற்றும் அழியாத தர்ம மரபை (Enduring Legacy) நிறுவிய நிறைவு நிலை. பிறவிப் பெருங்கடலை நீந்தி அதிவேக முக்தியை அடைந்துவிட்டீர்கள்!';
    legacyAdvice = 'மரபுச் சின்னம்: முழு சமுதாயத்திற்கும் தெய்விக சான்றாண்மையின் நேரடி கலங்கரை விளக்கம்.';
  }

  if (levelNameEl) levelNameEl.innerHTML = `<span style="color:${badgeColor}; font-size:1.1rem; display:block; margin-bottom:4px;">ஆன்ம முதிர்ச்சி எண்: ${ratingNum} / 7.0 (மதிப்பெண்: ${score}/21)</span>${levelName}`;
  if (starsEl) starsEl.innerHTML = stars;
  if (descEl) {
    descEl.innerHTML = `
      <div style="margin-bottom:12px;">${desc}</div>
      <div style="background:rgba(255,255,255,0.06); border-left:3px solid ${badgeColor}; padding:10px 14px; border-radius:6px; font-size:0.88rem; color:#f1f5f9; text-align:left;">
        <strong><svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 4 13a8.9 8.9 0 0 1 8.2-8.9 7 7 0 0 1 7.8 7.8A8.9 8.9 0 0 1 11 20z"/><path d="M12.5 4.5c.5 4.5-1 7.5-5 9.5"/></svg> இல்லற &amp; மரபு வழிகாட்டல் (Legacy Action):</strong> ${legacyAdvice}
      </div>
    `;
  }

  if (actionEl) {
    actionEl.innerHTML = `
      <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap; margin-top:14px;">
        <button type="button" onclick="window.print()" class="sheet-btn" style="background:linear-gradient(135deg,#059669,#0d9488); color:#ffffff; font-weight:700; padding:8px 18px; border-radius:10px; cursor:pointer;">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg> மதிப்பீட்டுச் சான்றிதழை அச்சிடுக
        </button>
        <a href="kalvi.html#grihasthaTracker" class="sheet-btn" style="background:linear-gradient(135deg,#d4af37,#996515); color:#000000; font-weight:700; padding:8px 18px; border-radius:10px; text-decoration:none;">
          <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> பஞ்ச மகா யக்ஞ சாதனா தொடங்குக <svg class="gkd-icon gkd-external-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
        </a>
      </div>
    `;
  }

  resultBox.style.display = 'block';
  resultBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function restorePatanjaliAssessment() {
  try {
    const raw = localStorage.getItem('gurukula_patanjali_answers');
    if (!raw) return;
    const answers = JSON.parse(raw);
    for (let k in answers) {
      const radios = document.getElementsByName(k);
      for (let r of radios) {
        if (parseInt(r.value, 10) === answers[k]) {
          r.checked = true;
        }
      }
    }
    const score = parseInt(localStorage.getItem('gurukula_patanjali_score'), 10);
    if (score && document.getElementById('patScoreResultBox')) {
      renderPatanjaliResult(score);
    }
  } catch (e) {}
}

/* ========================================================================== */
/* FEATURE 2: ASHRAM SOUNDSCAPE & DINACHARYA BELL (WEB AUDIO SYNTHESIS)       */
/* ========================================================================== */

let _audioCtx = null;
let _omOsc1 = null;
let _omOsc2 = null;
let _omGain = null;
let _isOmPlaying = false;

function getAudioContext() {
  if (!_audioCtx) {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (AudioContext) {
      _audioCtx = new AudioContext();
    }
  }
  if (_audioCtx && _audioCtx.state === 'suspended') {
    _audioCtx.resume();
  }
  return _audioCtx;
}

/**
 * Synthesizes an authentic bronze temple bell with inharmonic resonant partials.
 * @param {number} baseFreq Base frequency in Hz (Default: 432 Hz sacred A / 528 Hz)
 */
function playAshramTempleBell(baseFreq = 432) {
  const ctx = getAudioContext();
  if (!ctx) return;

  const now = ctx.currentTime;
  const masterGain = ctx.createGain();
  masterGain.connect(ctx.destination);

  // Inharmonic bell partial multipliers (approx. resonant ratios of traditional temple bells)
  const partials = [
    { ratio: 1.0, gain: 0.6, decay: 3.5 },
    { ratio: 2.02, gain: 0.4, decay: 2.8 },
    { ratio: 3.01, gain: 0.25, decay: 2.0 },
    { ratio: 4.24, gain: 0.18, decay: 1.5 },
    { ratio: 5.43, gain: 0.12, decay: 1.1 },
    { ratio: 6.81, gain: 0.08, decay: 0.8 }
  ];

  masterGain.gain.setValueAtTime(0.8, now);

  partials.forEach(p => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(baseFreq * p.ratio, now);

    // Strike attack and exponential decay
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(p.gain, now + 0.008);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + p.decay);

    osc.connect(gain);
    gain.connect(masterGain);

    osc.start(now);
    osc.stop(now + p.decay + 0.1);
  });
}

/**
 * Plays a distinct melodic chime for each of the 4 Ashram Yamas.
 * @param {number} yamaIndex 0: Usha (528Hz), 1: Vidya (432Hz), 2: Seva (384Hz), 3: Sandhya (288Hz)
 */
function playYamaChime(yamaIndex) {
  const freqs = [528, 432, 384, 288];
  const freq = freqs[yamaIndex] || 432;
  playAshramTempleBell(freq);

  // Show a gentle visual toast if possible
  const yamaNames = ['உஷா காலம் (பிரம்ம முகூர்த்தம்)', 'வித்யா யாமம் (சுவடிப் பாடம்)', 'சேவா யாமம் (கோ சேவை)', 'சந்தியா யாமம் (தீபாராதனை)'];
  console.log('ஆசிரம யாம நாதம் ஒலித்தது:', yamaNames[yamaIndex] || 'ஆசிரம மணி');
}

/**
 * Toggles ambient continuous Pranava Om (136.1 Hz) + Tambura harmonic drone.
 */
function toggleAshramOmDrone() {
  const ctx = getAudioContext();
  if (!ctx) return false;

  const btn = document.getElementById('ashramSoundToggleBtn');

  if (_isOmPlaying) {
    if (_omGain) {
      _omGain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 1.0);
      setTimeout(() => {
        if (_omOsc1) { _omOsc1.stop(); _omOsc1.disconnect(); }
        if (_omOsc2) { _omOsc2.stop(); _omOsc2.disconnect(); }
        _isOmPlaying = false;
        if (btn) {
          btn.classList.remove('active');
          btn.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c-.8 2-1.5 3.5-1.5 5a1.5 1.5 0 0 0 3 0c0-1.5-.7-3-1.5-5z" fill="currentColor"/><path d="M5 13c0 4 3 6 7 6s7-2 7-6H5z"/><path d="M10 19v2h4v-2"/></svg> <span>ஓம் நாதம் கேட்க</span>';
        }
      }, 1000);
    }
    return false;
  } else {
    const now = ctx.currentTime;
    _omGain = ctx.createGain();
    _omGain.gain.setValueAtTime(0.0001, now);
    _omGain.gain.linearRampToValueAtTime(0.25, now + 1.5);
    _omGain.connect(ctx.destination);

    // Fundamental Om tone (136.1 Hz - Earth frequency / Cosmic Aum)
    _omOsc1 = ctx.createOscillator();
    _omOsc1.type = 'sine';
    _omOsc1.frequency.setValueAtTime(136.1, now);

    // Fifth harmonic (204.15 Hz Pa / Panchama tanpura string)
    _omOsc2 = ctx.createOscillator();
    _omOsc2.type = 'sine';
    _omOsc2.frequency.setValueAtTime(204.15, now);

    _omOsc1.connect(_omGain);
    _omOsc2.connect(_omGain);

    _omOsc1.start(now);
    _omOsc2.start(now);
    _isOmPlaying = true;

    if (btn) {
      btn.classList.add('active');
      btn.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/></svg> <span>ஓம் நாதம் நிறுத்துக</span>';
    }
    return true;
  }
}

/* ========================================================================== */
/* FEATURE 4: PALM-LEAF MANUSCRIPT (ஓலைச்சுவடி வடிவம்) CONTROLLER             */
/* ========================================================================== */

function togglePalmLeafMode() {
  document.body.classList.toggle('palm-leaf-mode-active');
  const isEnabled = document.body.classList.contains('palm-leaf-mode-active');
  try {
    localStorage.setItem('gurukula_palm_leaf_mode', isEnabled ? 'true' : 'false');
  } catch (e) {}

  const btn = document.getElementById('palmLeafToggleBtn');
  if (btn) {
    btn.classList.toggle('active', isEnabled);
    btn.innerHTML = isEnabled ? (GKD_ICONS.scroll + ' <span>இயல்பு வடிவம் (Modern)</span>') : (GKD_ICONS.scroll + ' <span>ஓலைச்சுவடி வடிவம் (Palm-Leaf)</span>');
  }
}

function restorePalmLeafMode() {
  try {
    const isEnabled = localStorage.getItem('gurukula_palm_leaf_mode') === 'true';
    if (isEnabled) {
      document.body.classList.add('palm-leaf-mode-active');
      const btn = document.getElementById('palmLeafToggleBtn');
      if (btn) {
        btn.classList.add('active');
        btn.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H4a2 2 0 0 0-2 2v13a3 3 0 0 0 3 3h13a3 3 0 0 0 3-3V5a2 2 0 0 0-2-2h-7"/><path d="M19 18a3 3 0 0 0 0-6H6a2 2 0 0 0 0 4h12"/><line x1="8" y1="7" x2="14" y2="7"/><line x1="8" y1="11" x2="12" y2="11"/></svg> <span>இயல்பு வடிவம் (Modern)</span>';
      }
    }
  } catch (e) {}
}

/* ========================================================================== */
/* FEATURE 5: PWA & OFFLINE SERVICE WORKER REGISTRATION                       */
/* ========================================================================== */

if ('serviceWorker' in navigator && (window.location.protocol === 'https:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js').then((reg) => {
      console.log('ஆசிரம ஆஃப்லைன் சேவை இயங்குகிறது (PWA Service Worker registered):', reg.scope);
    }).catch((err) => {
      console.warn('PWA Service Worker registration skipped or failed:', err);
    });
  });
}

/* ========================================================================== */
/* FEATURE 6: GURU SPEECH SYNTHESIS ENGINE (குரு உரை கேட்போம்)                 */
/* ========================================================================== */

let _currentSpeechUtterance = null;

function speakLessonText(text, btnElement) {
  if (!('speechSynthesis' in window)) {
    alert('உங்கள் உலாவியில் குரல் வாசிப்பு வசதி (Speech Synthesis) ஆதரிக்கப்படவில்லை.');
    return;
  }

  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
    if (btnElement && btnElement.classList.contains('speaking')) {
      btnElement.classList.remove('speaking');
      btnElement.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg> குரு உரை கேட்க';
      return;
    }
  }

  const cleanText = text.replace(/<[^>]*>/g, '').trim();
  if (!cleanText) return;

  const utterance = new SpeechSynthesisUtterance(cleanText);
  utterance.rate = 0.88; // Calm, meditative pace
  utterance.pitch = 1.0;

  // Search for available Tamil voice
  const voices = window.speechSynthesis.getVoices();
  const tamilVoice = voices.find(v => v.lang.startsWith('ta')) || voices.find(v => v.lang.includes('IN'));
  if (tamilVoice) {
    utterance.voice = tamilVoice;
  }

  if (btnElement) {
    btnElement.classList.add('speaking');
    btnElement.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="currentColor"><rect x="5" y="5" width="14" height="14" rx="2"/></svg> நிறுத்துக';
  }

  utterance.onend = function() {
    if (btnElement) {
      btnElement.classList.remove('speaking');
      btnElement.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg> குரு உரை கேட்க';
    }
  };

  utterance.onerror = function() {
    if (btnElement) {
      btnElement.classList.remove('speaking');
      btnElement.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg> குரு உரை கேட்க';
    }
  };

  _currentSpeechUtterance = utterance;
  window.speechSynthesis.speak(utterance);
}

/* ========================================================================== */
/* FEATURE 7: UNIVERSAL TEMPLE BELL & AUDIO CHIME (432Hz HARMONICS)           */
/* ========================================================================== */

let _gkdAudioContext = null;

function getGurukulaAudioContext() {
  if (!_gkdAudioContext) {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (AudioContext) {
      _gkdAudioContext = new AudioContext();
    }
  }
  return _gkdAudioContext;
}

function playTempleBell() {
  try {
    const ctx = getGurukulaAudioContext();
    if (!ctx) return;
    if (ctx.state === 'suspended') {
      ctx.resume();
    }
    const now = ctx.currentTime;
    // Fundamental Bell strike + Harmonics (432Hz root, 864Hz octave, 1296Hz fifth, 1728Hz)
    const freqs = [432, 864, 1296, 1728];
    const gains = [0.4, 0.25, 0.15, 0.08];

    freqs.forEach((freq, i) => {
      const osc = ctx.createOscillator();
      const gainNode = ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, now);

      gainNode.gain.setValueAtTime(gains[i], now);
      gainNode.gain.exponentialRampToValueAtTime(0.0001, now + 3.2);

      osc.connect(gainNode);
      gainNode.connect(ctx.destination);

      osc.start(now);
      osc.stop(now + 3.3);
    });
  } catch (err) {
    console.warn('Audio bell synthesis skipped:', err);
  }
}

/* ========================================================================== */
/* FEATURE 8: UNIVERSAL TOAST NOTIFICATION SYSTEM                            */
/* ========================================================================== */

function showToast(message, duration) {
  duration = duration || 3500;
  let container = document.getElementById('gurukula-toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'gurukula-toast-container';
    container.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:100000;display:flex;flex-direction:column;gap:10px;pointer-events:none;';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'gurukula-toast';
  toast.style.cssText = 'background:rgba(15,23,42,0.96);border:1px solid var(--border-gold-hover,#f6e05e);color:#ffffff;padding:12px 20px;border-radius:12px;box-shadow:0 10px 25px rgba(0,0,0,0.5),0 0 15px rgba(246,224,94,0.2);font-size:0.92rem;font-weight:600;display:flex;align-items:center;gap:10px;transform:translateY(20px);opacity:0;transition:all 0.3s cubic-bezier(0.16,1,0.3,1);pointer-events:auto;max-width:420px;line-height:1.5;';
  toast.innerHTML = '<span>' + message + '</span>';
  container.appendChild(toast);

  // Animate in
  requestAnimationFrame(() => {
    toast.style.transform = 'translateY(0)';
    toast.style.opacity = '1';
  });

  // Animate out
  setTimeout(() => {
    toast.style.transform = 'translateY(20px)';
    toast.style.opacity = '0';
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }, duration);
}

/* ========================================================================== */
/* FEATURE 9: GURUKULA STUDENT LMS PROGRESS TRACKER & COMPLETION SYSTEM      */
/* ========================================================================== */

function isChapterCompleted(grade, chapter) {
  try {
    return localStorage.getItem('gkd_completed_' + grade + '_' + chapter) === 'true';
  } catch (e) {
    return false;
  }
}

function updateLMSButtonUI(grade, chapter, isCompleted) {
  const btn = document.getElementById('lms-btn-' + grade + '-' + chapter);
  const icon = document.getElementById('lms-icon-' + grade + '-' + chapter);
  const text = document.getElementById('lms-text-' + grade + '-' + chapter);
  const box = document.getElementById('lms-box-' + grade + '-' + chapter);

  if (btn) {
    if (isCompleted) {
      btn.classList.add('completed');
      btn.style.background = 'rgba(16, 185, 129, 0.22)';
      btn.style.borderColor = '#10b981';
      btn.style.color = '#10b981';
      if (icon) icon.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
      if (text) text.innerHTML = '<svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg> பாடம் நிறைவுற்றது (Completed)';
    } else {
      btn.classList.remove('completed');
      btn.style.background = 'rgba(56, 189, 248, 0.12)';
      btn.style.borderColor = 'rgba(56, 189, 248, 0.4)';
      btn.style.color = '#38bdf8';
      if (icon) icon.innerHTML = '<span class="gkd-status-circle"></span>';
      if (text) text.textContent = 'பாடம் முடிந்தது எனக் குறிக்கவும்';
    }
  }

  if (box) {
    if (isCompleted) {
      box.style.borderColor = 'rgba(16, 185, 129, 0.5)';
      box.style.background = 'rgba(16, 185, 129, 0.06)';
    } else {
      box.style.borderColor = '';
      box.style.background = '';
    }
  }
}

function toggleChapterCompletion(grade, chapter) {
  try {
    const key = 'gkd_completed_' + grade + '_' + chapter;
    const currentState = localStorage.getItem(key) === 'true';
    const newState = !currentState;

    if (newState) {
      localStorage.setItem(key, 'true');
      updateLMSButtonUI(grade, chapter, true);
      showToast('தரம் ' + grade + ' — பாடம் ' + chapter + ' வெற்றிகரமாக நிறைவுற்றது! (+50 வேத ஞான XP)');
      playTempleBell();
    } else {
      localStorage.removeItem(key);
      updateLMSButtonUI(grade, chapter, false);
      showToast('பாடப் பதிவு மீட்டமைக்கப்பட்டது.');
    }

    // If on school.html, update overall metrics dynamically
    if (typeof calculateOverallSchoolProgress === 'function') {
      calculateOverallSchoolProgress();
    }
  } catch (err) {
    console.error('Error toggling LMS chapter completion:', err);
  }
}

function restoreLMSProgress() {
  try {
    const buttons = document.querySelectorAll('[id^="lms-btn-"]');
    buttons.forEach(btn => {
      const parts = btn.id.split('-');
      if (parts.length >= 4) {
        const grade = parts[2];
        const chapter = parts[3];
        if (isChapterCompleted(grade, chapter)) {
          updateLMSButtonUI(grade, chapter, true);
        }
      }
    });

    if (typeof calculateOverallSchoolProgress === 'function') {
      calculateOverallSchoolProgress();
    }
  } catch (e) {
    console.warn('Could not restore LMS progress:', e);
  }
}

/* ========================================================================== */
/* FEATURE 10: PATANJALI 7-LEVEL MATRIX FILTER (SYLLABUS PORTAL)             */
/* ========================================================================== */

function filterPatLevel(level) {
  // Update pill active states
  const pills = document.querySelectorAll('.pat-pill-btn');
  pills.forEach(pill => {
    const oc = pill.getAttribute('onclick') || '';
    if (oc.includes("'" + level + "'")) {
      pill.classList.add('active');
    } else {
      pill.classList.remove('active');
    }
  });

  // Filter cards
  const cards = document.querySelectorAll('.pat-level-card');
  cards.forEach(card => {
    const cardLevel = card.getAttribute('data-pat-level');
    if (level === 'all' || cardLevel === level) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });

  if (level !== 'all') {
    const targetCard = document.querySelector('.pat-level-card[data-pat-level="' + level + '"]');
    if (targetCard) {
      targetCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }
}

/* ========================================================================== */
/* FEATURE 11: VIRTUES & ETHICAL TIERS FILTER (VIRTUES PORTAL)              */
/* ========================================================================== */

function filterVirtues(tier, btn) {
  // Sync tab pills
  document.querySelectorAll('.context-tab-pill').forEach(b => {
    const oc = b.getAttribute('onclick') || '';
    if (oc.includes("'" + tier + "'")) {
      b.classList.add('active');
    } else if (oc.includes('filterVirtues')) {
      b.classList.remove('active');
    }
  });

  // Sync tier-filter-btn
  document.querySelectorAll('.tier-filter-btn').forEach(b => {
    const oc = b.getAttribute('onclick') || '';
    if (oc.includes("'" + tier + "'")) {
      b.classList.add('active');
    } else {
      b.classList.remove('active');
    }
  });

  // Toggle display of .virtue-grade-block
  const blocks = document.querySelectorAll('.virtue-grade-block');
  blocks.forEach(b => {
    if (tier === 'all' || b.classList.contains(tier)) {
      b.style.display = 'block';
    } else {
      b.style.display = 'none';
    }
  });
}

// Alias for backwards compatibility
function filterTier(tier, btn) {
  filterVirtues(tier, btn);
}
