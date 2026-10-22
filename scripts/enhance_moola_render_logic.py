import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('moola-nool.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Inspect how renderScripture builds the HTML
# We will inject the Dual-Mode toggle bar, Kid-friendly summary, and the archive viewer block.

old_header_end = "html += '</div>';\n\n      // Section Tabs"

new_header_elements = """html += '</div>';

      // DUAL MODE SELECTOR BAR (CHILDREN-FRIENDLY READABLE vs AUTHENTIC ARCHIVE SCAN)
      html += '<div class="view-mode-bar">';
      html += '  <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">';
      html += '    <div class="view-mode-tabs">';
      html += '      <button type="button" class="view-mode-btn' + (currentViewMode === 'readable' ? ' active' : '') + '" id="viewModeBtnReadable" onclick="setViewMode(\\'readable\\')">';
      html += '        <span>📖</span> <span>1. எளிய வாசிப்பு நெறி (Kids & Learners Mode)</span>';
      html += '      </button>';
      html += '      <button type="button" class="view-mode-btn' + (currentViewMode === 'archive' ? ' active' : '') + '" id="viewModeBtnArchive" onclick="setViewMode(\\'archive\\')">';
      html += '        <span>📜</span> <span>2. அசல் நூலக ஏட்டுச்சுவடி / ஆவணம் (Authentic Scan Mode)</span>';
      html += '      </button>';
      html += '    </div>';
      html += '    <span class="kid-friendly-badge">✨ சிறுவர் எளிய விளக்கம் & நீதிக் கதை</span>';
      html += '  </div>';
      if (sc.rawPdfUrl || sc.archivePdfUrl) {
        var rawUrl = sc.rawPdfUrl || sc.archivePdfUrl;
        html += '  <a href="' + rawUrl + '" target="_blank" rel="noopener noreferrer" class="meta-pill gold" style="text-decoration:none; display:inline-flex; align-items:center; gap:6px;">';
        html += '    <svg class="gkd-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px; height:14px;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> அசல் நூல் பதிவிறக்கு (Original PDF)';
        html += '  </a>';
      }
      html += '</div>';

      // ARCHIVE VIEWER BLOCK (MODE 2)
      html += '<div id="archiveContentBlock" style="display:' + (currentViewMode === 'archive' ? 'block' : 'none') + ';">';
      if (sc.rawPdfUrl || sc.archivePdfUrl) {
        var pdfSrc = sc.rawPdfUrl || sc.archivePdfUrl;
        html += '  <div class="archive-meta-banner">';
        html += '    <div>';
        html += '      <div style="font-size:0.95rem; font-weight:700; color:#ffd700;">🏛️ ஈழத்து மூல ஆவணக் காப்பகம் (Authentic Sri Lankan Archival Document)</div>';
        html += '      <div style="font-size:0.84rem; color:#94a3b8; margin-top:2px;">பதிப்பு: ' + escapeHtml(sc.commentaryTradition) + (sc.noolahamId ? ' | நூலக எண்: ' + sc.noolahamId : '') + '</div>';
        html += '    </div>';
        html += '    <div style="display:flex; gap:10px;">';
        html += '      <a href="' + pdfSrc + '" target="_blank" class="sec-tab-btn" style="text-decoration:none; font-size:0.82rem;">முழுத் திரையில் திறக்குக ↗</a>';
        html += '    </div>';
        html += '  </div>';
        html += '  <iframe class="archive-doc-viewer" src="' + pdfSrc + '" title="' + escapeHtml(sc.title) + ' Archival Scan" loading="lazy"></iframe>';
      } else {
        html += '  <div style="padding:40px; text-align:center; color:#94a3b8; background:rgba(15,23,42,0.6); border-radius:12px;">இந்நூலின் அசல் ஏட்டுச்சுவடி எண்ணிம நகல் விரைவில் இணைக்கப்படும். எளிய வாசிப்பு நெறியைப் பயன்படுத்தவும்.</div>';
      }
      html += '</div>';

      // READABLE CONTENT BLOCK WRAPPER START (MODE 1)
      html += '<div id="readableContentBlock" style="display:' + (currentViewMode === 'readable' ? 'block' : 'none') + ';">';
"""

if 'DUAL MODE SELECTOR BAR' not in html:
    html = html.replace(old_header_end, new_header_elements + "\n\n      // Section Tabs")
    # Close readableContentBlock at the end of section block loop
    old_end = "sc.sections.forEach(function(sec, sIdx) {"
    # We find where container.innerHTML is set
    set_html_marker = "container.innerHTML = html;"
    html = html.replace(set_html_marker, "html += '</div>'; // Close readableContentBlock\n      " + set_html_marker)

# Also let's enhance how verse notes with story are rendered
# If note contains '【குழந்தைகளுக்கான அறக்கதை】', format it nicely into a kid-story-box
old_note_block = """          if (v.notes) {
            html += '    <div class="verse-notes-block">';
            html += '      <div class="verse-notes-title">விளக்கக் குறிப்பு & பாஷ்ய சாரம்</div>';
            html += '      <div class="verse-notes-body">' + escapeHtml(v.notes) + '</div>';
            html += '    </div>';
          }"""

new_note_block = """          if (v.notes) {
            if (v.notes.indexOf('【குழந்தைகளுக்கான அறக்கதை】') !== -1) {
              var parts = v.notes.split('【ஈழத்து மூல ஆவணக் குறிப்பு】:');
              var kidStory = parts[0].replace('【குழந்தைகளுக்கான அறக்கதை】:', '').trim();
              var archNote = parts.length > 1 ? parts[1].trim() : '';

              html += '    <div class="kid-story-box">';
              html += '      <div class="kid-story-title"><span>🌟</span> <span>சிறுவர்களுக்கான அறக்கதை விளக்கம் (Moral Story for Kids)</span></div>';
              html += '      <div style="font-size:0.92rem; color:#fde68a; line-height:1.6;">' + escapeHtml(kidStory) + '</div>';
              html += '    </div>';

              if (archNote) {
                html += '    <div class="verse-notes-block" style="margin-top:10px;">';
                html += '      <div class="verse-notes-title">🏛️ ஈழத்து மூல ஆவணச் சான்று (Authentic Jaffna Archival Note)</div>';
                html += '      <div class="verse-notes-body" style="font-size:0.85rem; color:#94a3b8;">' + escapeHtml(archNote) + '</div>';
                html += '    </div>';
              }
            } else {
              html += '    <div class="verse-notes-block">';
              html += '      <div class="verse-notes-title">விளக்கக் குறிப்பு & பாஷ்ய சாரம்</div>';
              html += '      <div class="verse-notes-body">' + escapeHtml(v.notes) + '</div>';
              html += '    </div>';
            }
          }"""

html = html.replace(old_note_block, new_note_block)

with open('moola-nool.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully injected Dual Mode rendering and Kid-Story boxes into moola-nool.html!")
