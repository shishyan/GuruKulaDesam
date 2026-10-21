/* D3 Interactive Multi-Node Cosmic Hierarchy Tree Engine */
(function() {
  'use strict';

  let currentLang = localStorage.getItem('gkd_lang') || 'ta';
  let rootData = null;
  let svg, g, treeLayout, zoomBehavior;
  let i = 0;
  let duration = 500;
  let width = 1200;
  let height = 750;
  let activeFilter = 'all';

  // Palette by branch/type
  const typeColors = {
    root: '#ec4899',       // Pink / Supreme
    creator: '#a855f7',    // Royal Violet
    prajapati: '#38bdf8',  // Sky Blue
    rishi: '#06b6d4',      // Cyan
    manu: '#f59e0b',       // Amber Gold
    solar: '#ea580c',      // Solar Orange
    lunar: '#3b82f6',      // Lunar Indigo-Blue
    avatar: '#10b981',     // Emerald Divine
    tamil: '#e11d48',      // Ruby Crimson
    king: '#facc15'        // Imperial Yellow
  };

  const typeLabels = {
    root: { ta: 'பரம்பொருள்', en: 'Supreme Source' },
    creator: { ta: 'படைப்பு', en: 'Creator' },
    prajapati: { ta: 'பிரஜாபதி', en: 'Prajapati' },
    rishi: { ta: 'ரிஷி / முனிவர்', en: 'Rishi / Seer' },
    manu: { ta: 'மனு', en: 'Manu' },
    solar: { ta: 'சூரிய குலம்', en: 'Solar Clan' },
    lunar: { ta: 'சந்திர குலம்', en: 'Lunar Clan' },
    avatar: { ta: 'அவதாரம்', en: 'Avatara' },
    tamil: { ta: 'தமிழ் மரபு', en: 'Tamil Dynasty' },
    king: { ta: 'மன்னர்', en: 'Monarch' }
  };

  // Helper to initialize Tree
  window.initCosmicHierarchyTree = function(data) {
    rootData = data;
    const container = document.getElementById('cosmicTreeContainer');
    if (!container) return;

    container.innerHTML = '';
    width = container.clientWidth || 1200;
    height = Math.max(680, window.innerHeight - 250);

    svg = d3.select('#cosmicTreeContainer')
      .append('svg')
      .attr('width', '100%')
      .attr('height', height)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('class', 'cosmic-d3-svg');

    // Filter definitions (Glow effects)
    const defs = svg.append('defs');
    const filter = defs.append('filter')
      .attr('id', 'nodeGlow')
      .attr('x', '-50%').attr('y', '-50%')
      .attr('width', '200%').attr('height', '200%');
    filter.append('feGaussianBlur')
      .attr('stdDeviation', '4')
      .attr('result', 'coloredBlur');
    const feMerge = filter.append('feMerge');
    feMerge.append('feMergeNode').attr('in', 'coloredBlur');
    feMerge.append('feMergeNode').attr('in', 'SourceGraphic');

    g = svg.append('g').attr('class', 'tree-viewport');

    zoomBehavior = d3.zoom()
      .scaleExtent([0.15, 3.5])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });

    svg.call(zoomBehavior);

    // Initial transform: Center horizontally at top
    svg.call(zoomBehavior.transform, d3.zoomIdentity.translate(width / 2, 80).scale(0.85));

    treeLayout = d3.tree().nodeSize([190, 130]);

    // Build hierarchy
    const root = d3.hierarchy(rootData, d => d.children);
    root.x0 = 0;
    root.y0 = 0;

    // By default, collapse deep branches beyond depth 2 for clean initial view
    function collapseDeep(d) {
      if (d.children && d.depth >= 2) {
        d._children = d.children;
        d._children.forEach(collapseDeep);
        d.children = null;
      } else if (d.children) {
        d.children.forEach(collapseDeep);
      }
    }
    collapseDeep(root);

    window.cosmicTreeRoot = root;
    updateTree(root);
  };

  function updateTree(source) {
    const root = window.cosmicTreeRoot;
    const treeData = treeLayout(root);

    const nodes = treeData.descendants();
    const links = treeData.links();

    // Normalize vertical depth
    nodes.forEach(d => {
      d.y = d.depth * 135;
    });

    // ********** LINKS SECTION **********
    const link = g.selectAll('path.cosmic-tree-link')
      .data(links, d => d.target.data.id || d.target.id);

    const linkEnter = link.enter().insert('path', 'g')
      .attr('class', 'cosmic-tree-link')
      .attr('d', d => {
        const o = { x: source.x0 || 0, y: source.y0 || 0 };
        return diagonal(o, o);
      })
      .attr('stroke', d => typeColors[d.target.data.type] || '#a855f7')
      .attr('stroke-width', 2)
      .attr('stroke-opacity', 0.45)
      .attr('fill', 'none');

    const linkUpdate = linkEnter.merge(link);
    linkUpdate.transition().duration(duration)
      .attr('d', d => diagonal(d.source, d.target))
      .attr('stroke', d => typeColors[d.target.data.type] || '#a855f7')
      .attr('stroke-opacity', d => (activeFilter === 'all' || d.target.data.type === activeFilter) ? 0.6 : 0.15)
      .attr('stroke-width', d => (activeFilter === 'all' || d.target.data.type === activeFilter) ? 2.5 : 1);

    link.exit().transition().duration(duration)
      .attr('d', d => {
        const o = { x: source.x, y: source.y };
        return diagonal(o, o);
      })
      .remove();

    // ********** NODES SECTION **********
    const node = g.selectAll('g.cosmic-tree-node')
      .data(nodes, d => d.data.id || (d.id = ++i));

    const nodeEnter = node.enter().append('g')
      .attr('class', d => `cosmic-tree-node type-${d.data.type}`)
      .attr('transform', d => `translate(${source.x0 || 0},${source.y0 || 0})`)
      .style('cursor', 'pointer')
      .on('click', (event, d) => {
        // If has children or _children, toggle
        if (d.children) {
          d._children = d.children;
          d.children = null;
        } else if (d._children) {
          d.children = d._children;
          d._children = null;
        }
        updateTree(d);
        showNodeDetails(d.data);
      });

    // Outer Glow / Halo for key figures
    nodeEnter.append('circle')
      .attr('class', 'node-halo')
      .attr('r', d => ['avatar', 'root', 'creator', 'manu'].includes(d.data.type) ? 32 : 24)
      .attr('fill', d => typeColors[d.data.type] || '#a855f7')
      .attr('fill-opacity', 0.12)
      .attr('stroke', d => typeColors[d.data.type] || '#a855f7')
      .attr('stroke-width', 1.5)
      .attr('stroke-dasharray', d => d._children ? '3 3' : 'none');

    // Main Circle
    nodeEnter.append('circle')
      .attr('class', 'node-circle')
      .attr('r', d => ['avatar', 'root', 'creator', 'manu'].includes(d.data.type) ? 22 : 17)
      .attr('fill', d => typeColors[d.data.type] || '#a855f7')
      .attr('filter', 'url(#nodeGlow)');

    // Expansion Badge Indicator (+ / -)
    nodeEnter.append('text')
      .attr('class', 'node-expand-indicator')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('font-size', '13px')
      .attr('font-weight', 'bold')
      .attr('fill', '#ffffff')
      .text(d => d._children ? '+' : (d.children ? '−' : ''));

    // Node Label: Tamil Name (Top/Main)
    nodeEnter.append('text')
      .attr('class', 'node-name-ta')
      .attr('dy', 38)
      .attr('text-anchor', 'middle')
      .attr('font-size', '13.5px')
      .attr('font-weight', '700')
      .attr('fill', '#f8fafc')
      .text(d => currentLang === 'ta' ? d.data.name_ta : d.data.name_en);

    // Node Label: Role / Epithet
    nodeEnter.append('text')
      .attr('class', 'node-role-label')
      .attr('dy', 54)
      .attr('text-anchor', 'middle')
      .attr('font-size', '10.5px')
      .attr('font-weight', '500')
      .attr('fill', d => typeColors[d.data.type] || '#38bdf8')
      .text(d => currentLang === 'ta' ? d.data.role_ta : d.data.role_en);

    // Secondary Language Subtitle (English or Tamil)
    nodeEnter.append('text')
      .attr('class', 'node-name-en')
      .attr('dy', 68)
      .attr('text-anchor', 'middle')
      .attr('font-size', '9.5px')
      .attr('font-style', 'italic')
      .attr('fill', '#94a3b8')
      .text(d => currentLang === 'ta' ? d.data.name_en : d.data.name_ta);

    // Node Update
    const nodeUpdate = nodeEnter.merge(node);

    nodeUpdate.transition().duration(duration)
      .attr('transform', d => `translate(${d.x},${d.y})`)
      .style('opacity', d => {
        if (activeFilter === 'all') return 1;
        return d.data.type === activeFilter ? 1 : 0.25;
      });

    nodeUpdate.select('.node-expand-indicator')
      .text(d => d._children ? '+' : (d.children ? '−' : ''));

    nodeUpdate.select('.node-halo')
      .attr('stroke-dasharray', d => d._children ? '3 3' : 'none')
      .attr('stroke-width', d => d._children ? 2.5 : 1.5);

    nodeUpdate.select('.node-name-ta')
      .text(d => currentLang === 'ta' ? d.data.name_ta : d.data.name_en);

    nodeUpdate.select('.node-role-label')
      .text(d => currentLang === 'ta' ? d.data.role_ta : d.data.role_en);

    nodeUpdate.select('.node-name-en')
      .text(d => currentLang === 'ta' ? d.data.name_en : d.data.name_ta);

    // Node Exit
    const nodeExit = node.exit().transition().duration(duration)
      .attr('transform', d => `translate(${source.x},${source.y})`)
      .remove();

    nodeExit.select('circle').attr('r', 1e-6);
    nodeExit.select('text').style('fill-opacity', 1e-6);

    // Store old positions for transition
    nodes.forEach(d => {
      d.x0 = d.x;
      d.y0 = d.y;
    });
  }

  function diagonal(s, d) {
    return `M ${s.x} ${s.y}
            C ${s.x} ${(s.y + d.y) / 2},
              ${d.x} ${(s.y + d.y) / 2},
              ${d.x} ${d.y}`;
  }

  // Details Modal / Drawer Drawer
  function showNodeDetails(data) {
    const modal = document.getElementById('ancestorModal');
    if (!modal) return;

    const badge = document.getElementById('modalBadge');
    const title = document.getElementById('modalTitle');
    const subtitle = document.getElementById('modalSubtitle');
    const dynasty = document.getElementById('modalDynasty');
    const epoch = document.getElementById('modalEpoch');
    const scriptural = document.getElementById('modalScriptural');
    const deeds = document.getElementById('modalDeeds');
    const connections = document.getElementById('modalConnections');

    const typeMeta = typeLabels[data.type] || { ta: data.type, en: data.type };
    if (badge) {
      badge.textContent = currentLang === 'ta' ? typeMeta.ta : typeMeta.en;
      badge.style.background = typeColors[data.type] || '#a855f7';
      badge.style.color = '#ffffff';
    }

    if (title) title.textContent = currentLang === 'ta' ? data.name_ta : data.name_en;
    if (subtitle) subtitle.textContent = currentLang === 'ta' ? (data.name_en + ' — ' + data.role_ta) : (data.name_ta + ' — ' + data.role_en);
    if (dynasty) dynasty.textContent = currentLang === 'ta' ? (typeMeta.ta + ' மரபு') : (typeMeta.en + ' Heritage');
    if (epoch) epoch.textContent = data.epoch || (currentLang === 'ta' ? 'அநாதி தொன்மை' : 'Ancient Era');
    if (scriptural) scriptural.textContent = data.purana || (currentLang === 'ta' ? '12 மகாபுராணங்கள் & இதிகாசங்கள்' : '12 Mahapuranas & Itihasas');
    if (deeds) deeds.textContent = currentLang === 'ta' ? data.desc_ta : data.desc_en;

    if (connections) {
      let subCount = (data.children || []).length;
      connections.textContent = currentLang === 'ta'
        ? `நேரடி வழித்தோன்றல்கள்: ${subCount} கிளைகள் பதிவு செய்யப்பட்டுள்ளன.`
        : `Direct descendants: ${subCount} recorded branch nodes.`;
    }

    modal.classList.add('active');
  }

  // Interactive Controls: Expand All, Collapse All, Reset Zoom, Search
  window.expandAllNodes = function() {
    function expand(d) {
      if (d._children) {
        d.children = d._children;
        d._children = null;
      }
      if (d.children) d.children.forEach(expand);
    }
    if (window.cosmicTreeRoot) {
      expand(window.cosmicTreeRoot);
      updateTree(window.cosmicTreeRoot);
    }
  };

  window.collapseAllNodes = function() {
    function collapse(d) {
      if (d.children && d.depth >= 1) {
        d._children = d.children;
        d._children.forEach(collapse);
        d.children = null;
      } else if (d.children) {
        d.children.forEach(collapse);
      }
    }
    if (window.cosmicTreeRoot) {
      collapse(window.cosmicTreeRoot);
      updateTree(window.cosmicTreeRoot);
    }
  };

  window.resetTreeZoom = function() {
    if (svg && zoomBehavior) {
      svg.transition().duration(750).call(
        zoomBehavior.transform,
        d3.zoomIdentity.translate(width / 2, 80).scale(0.85)
      );
    }
  };

  window.filterTreeByType = function(type) {
    activeFilter = type;
    document.querySelectorAll('.tree-filter-btn').forEach(b => {
      b.classList.toggle('active', b.dataset.type === type);
    });
    if (window.cosmicTreeRoot) {
      updateTree(window.cosmicTreeRoot);
    }
  };

  window.searchCosmicTree = function(query) {
    if (!query) {
      activeFilter = 'all';
      updateTree(window.cosmicTreeRoot);
      return;
    }
    const q = query.trim().toLowerCase();
    let matchNode = null;

    // Uncollapse everything on search path
    function findAndExpand(d) {
      let match = (d.data.name_ta && d.data.name_ta.toLowerCase().includes(q)) ||
                  (d.data.name_en && d.data.name_en.toLowerCase().includes(q)) ||
                  (d.data.role_ta && d.data.role_ta.toLowerCase().includes(q)) ||
                  (d.data.desc_ta && d.data.desc_ta.toLowerCase().includes(q));

      if (match && !matchNode) {
        matchNode = d;
      }

      // Check children in both children and _children
      let childList = (d.children || []).concat(d._children || []);
      let childMatched = false;
      childList.forEach(c => {
        if (findAndExpand(c)) childMatched = true;
      });

      if (childMatched || match) {
        if (d._children) {
          d.children = d._children;
          d._children = null;
        }
        return true;
      }
      return false;
    }

    if (window.cosmicTreeRoot) {
      findAndExpand(window.cosmicTreeRoot);
      updateTree(window.cosmicTreeRoot);

      if (matchNode && svg && zoomBehavior) {
        // Zoom and center on matched node
        svg.transition().duration(1000).call(
          zoomBehavior.transform,
          d3.zoomIdentity.translate(width / 2 - matchNode.x * 1.2, height / 2 - matchNode.y * 1.2).scale(1.2)
        );
        showNodeDetails(matchNode.data);
      }
    }
  };

  // Language change listener
  window.setTreeLanguage = function(lang) {
    currentLang = lang;
    if (window.cosmicTreeRoot) {
      updateTree(window.cosmicTreeRoot);
    }
  };

})();
