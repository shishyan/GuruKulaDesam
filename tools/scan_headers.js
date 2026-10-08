const fs = require('fs');

const files = fs.readdirSync('.').filter(f => f.endsWith('.html'));
files.sort();

console.log('Total HTML files:', files.length);
files.forEach(f => {
  const c = fs.readFileSync(f, 'utf8');
  const hasTabs = c.includes('id="contextTabsNav"') || c.includes('class="context-tabs-nav"');
  const hasSiteHeader = c.includes('class="site-header"');
  const hasContextTopBar = c.includes('class="context-top-bar"');
  const hasBackBtn = c.includes('breadcrumb-back-btn');
  if (hasTabs || hasSiteHeader || !hasBackBtn) {
    console.log(`${f.padEnd(25)} | tabs: ${String(hasTabs).padEnd(5)} | siteHeader: ${String(hasSiteHeader).padEnd(5)} | topBar: ${String(hasContextTopBar).padEnd(5)} | backBtn: ${String(hasBackBtn).padEnd(5)}`);
  }
});
