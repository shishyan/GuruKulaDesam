import os
import re

print("=== Adding Navigation Layout Options to Settings & Preferences ===")

js_paths = ['assets/js/main.js', 'docs/assets/js/main.js', 'site/assets/js/main.js']

for jp in js_paths:
    if not os.path.exists(jp):
        continue

    with open(jp, 'r', encoding='utf-8') as fp:
        js = fp.read()

    # 1. Update DEFAULT_USER_PREFS to include navLayout: 'sidebar'
    if "navLayout: 'sidebar'" not in js:
        js = js.replace(
            "fontScale: 1.0,",
            "fontScale: 1.0,\n  navLayout: 'sidebar', // 'sidebar' (default), 'topbar' (classic), 'hybrid' (both)"
        )

    # 2. Add changeNavLayout function if not present
    if "function changeNavLayout(" not in js:
        change_fn = """function changeNavLayout(layout) {
  userPrefs.navLayout = layout;
  saveUserPreferences();
  applyUserPreferences();
}
"""
        js = js.replace("function changeTheme(themeName)", change_fn + "\nfunction changeTheme(themeName)")

    # 3. Enhance applyUserPreferences to handle layoutMode
    old_apply_snippet = """  // Profile Badges & Avatars in UI"""
    new_apply_snippet = """  // Navigation Shell Layout Mode
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

  // Profile Badges & Avatars in UI"""

    if "const layout = userPrefs.navLayout || 'sidebar';" not in js:
        js = js.replace(old_apply_snippet, new_apply_snippet)

    # 4. Add Navigation Layout Options into Preferences Tab in mountAppShell() modal HTML
    target_modal_markup = """        <!-- PREFERENCES TAB -->
        <div class="user-tab-content" id="tabContentPreferences">"""

    layout_form_group = """        <!-- PREFERENCES TAB -->
        <div class="user-tab-content" id="tabContentPreferences">
          <div class="settings-form-group">
            <label class="settings-label">🧭 தள வழிசெலுத்தல் அமைப்பு (Navigation Shell Layout):</label>
            <div class="radio-pill-group">
              <label class="radio-pill">
                <input type="radio" name="layoutChoice" value="sidebar" onchange="changeNavLayout('sidebar')">
                <div>
                  <strong style="color: var(--gold-bright);">📌 இடது பக்கப்பட்டி முறைமை (Left Sidebar + Context Tabs) [இயல்பு / Default]</strong>
                  <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;">இடதுபுறம் அனைத்து தளங்களின் நேரடி அணுகல் • மேற்புறம் அப்பக்கத்திற்குரிய சூழல் உணர் தத்தல்கள்</div>
                </div>
              </label>
              <label class="radio-pill">
                <input type="radio" name="layoutChoice" value="topbar" onchange="changeNavLayout('topbar')">
                <div>
                  <strong style="color: var(--gold-soft);">🏛️ மரபு மேல் பட்டி முறைமை (Classic Top Navbar)</strong>
                  <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;">முந்தைய நேரடி மேல் மெனு மற்றும் கீழ்விரிவுப் பட்டியல்கள் (பக்கப்பட்டி மறைக்கப்படும்)</div>
                </div>
              </label>
              <label class="radio-pill">
                <input type="radio" name="layoutChoice" value="hybrid" onchange="changeNavLayout('hybrid')">
                <div>
                  <strong style="color: var(--gold-soft);">🔱 இருவழி கூட்டு முறைமை (Dual Hybrid Shell)</strong>
                  <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;">இடது பக்கப்பட்டி மற்றும் மேல் மெனு இரண்டும் ஒரே நேரத்தில் செயல்படும் முழுமை முறைமை</div>
                </div>
              </label>
            </div>
          </div>"""

    if "name=\"layoutChoice\"" not in js:
        js = js.replace(target_modal_markup, layout_form_group)

    with open(jp, 'w', encoding='utf-8') as fp:
        fp.write(js)
    print(f"Updated navigation layout settings in: {jp}")

print("=== Navigation Layout Options Successfully Added ===")
