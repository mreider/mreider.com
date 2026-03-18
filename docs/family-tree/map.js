// Satellite map view for family tree
(function() {
  var canvas = document.getElementById('map-canvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');

  // Layout constants
  var NODE_W = 140, NODE_H = 44, PAD_X = 24, PAD_Y = 60;
  var FONT = '12px -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif';
  var FONT_SMALL = '10px -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif';

  // Colors
  var COL_BG = '#fafaf8';
  var COL_NODE = '#fff';
  var COL_BORDER = '#d0d0d0';
  var COL_TEXT = '#1a1a1a';
  var COL_DATES = '#888';
  var COL_LINE = '#ccc';
  var COL_ACTIVE = '#2563eb';
  var COL_ACTIVE_TEXT = '#fff';
  var COL_HOVER = '#e8f0fe';
  var COL_MATT = '#2563eb';

  // State
  var nodes = [];     // {name, x, y, w, h, gen}
  var nodeMap = {};   // name -> node
  var offsetX = 0, offsetY = 0, scale = 1;
  var dragging = false, dragStartX, dragStartY, dragOffX, dragOffY;
  var hoveredNode = null;
  var highlightedName = null;
  var dpr = window.devicePixelRatio || 1;

  // --- Generation assignment ---
  function computeGen(name, seen) {
    if (seen[name]) return seen[name];
    seen[name] = -1; // cycle guard
    var p = byName[name];
    if (!p || !p.parents || !p.parents.length) { seen[name] = 0; return 0; }
    var maxParent = 0;
    for (var i = 0; i < p.parents.length; i++) {
      if (byName[p.parents[i]]) {
        var pg = computeGen(p.parents[i], seen);
        if (pg > maxParent) maxParent = pg;
      }
    }
    seen[name] = maxParent + 1;
    return seen[name];
  }

  // --- Layout ---
  function layoutNodes() {
    var gens = {};
    var genOf = {};
    nodes = [];
    nodeMap = {};

    // Compute generation for each person
    for (var i = 0; i < rawData.length; i++) {
      computeGen(rawData[i].name, genOf);
    }

    // Place spouses in same generation (use higher gen)
    for (var i = 0; i < rawData.length; i++) {
      var p = rawData[i];
      if (p.spouse && byName[p.spouse]) {
        var g1 = genOf[p.name] || 0;
        var g2 = genOf[p.spouse] || 0;
        var mg = Math.max(g1, g2);
        genOf[p.name] = mg;
        genOf[p.spouse] = mg;
      }
    }

    // Group by generation
    for (var i = 0; i < rawData.length; i++) {
      var g = genOf[rawData[i].name] || 0;
      if (!gens[g]) gens[g] = [];
      gens[g].push(rawData[i]);
    }

    // Sort generations, place couples together
    var genKeys = Object.keys(gens).map(Number).sort(function(a,b){return a-b;});

    for (var gi = 0; gi < genKeys.length; gi++) {
      var g = genKeys[gi];
      var people = gens[g];

      // Order: place couples adjacent, sort by birth year
      var placed = {};
      var ordered = [];
      // Sort by born year first
      people.sort(function(a,b) {
        return (a.born ? parseInt(a.born) : 9999) - (b.born ? parseInt(b.born) : 9999);
      });
      for (var j = 0; j < people.length; j++) {
        var p = people[j];
        if (placed[p.name]) continue;
        ordered.push(p);
        placed[p.name] = true;
        if (p.spouse && byName[p.spouse] && !placed[p.spouse] && (genOf[p.spouse] === g)) {
          ordered.push(byName[p.spouse]);
          placed[p.spouse] = true;
        }
      }

      var rowWidth = ordered.length * (NODE_W + PAD_X) - PAD_X;
      var startX = -rowWidth / 2;
      var y = gi * (NODE_H + PAD_Y);

      for (var j = 0; j < ordered.length; j++) {
        var x = startX + j * (NODE_W + PAD_X);
        var node = { name: ordered[j].name, x: x, y: y, w: NODE_W, h: NODE_H, gen: g };
        nodes.push(node);
        nodeMap[ordered[j].name] = node;
      }
    }
  }

  // --- Years helper ---
  function nodeYears(p) {
    var parts = [];
    if (p.born) { var b = String(p.born); parts.push(b.length > 4 ? b.split('-')[0] : b); }
    if (p.died) { var d = String(p.died); parts.push(d.length > 4 ? d.split('-')[0] : d); }
    else if (parts.length) parts.push('');
    return parts.length < 2 ? (parts[0] || '') : parts[0] + '\u2013' + parts[1];
  }

  // --- Drawing ---
  function draw() {
    canvas.width = canvas.clientWidth * dpr;
    canvas.height = canvas.clientHeight * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    ctx.fillStyle = COL_BG;
    ctx.fillRect(0, 0, canvas.clientWidth, canvas.clientHeight);

    ctx.save();
    ctx.translate(offsetX, offsetY);
    ctx.scale(scale, scale);

    // Draw lines first
    ctx.strokeStyle = COL_LINE;
    ctx.lineWidth = 1;
    for (var i = 0; i < rawData.length; i++) {
      var p = rawData[i];
      if (!p.parents) continue;
      var childNode = nodeMap[p.name];
      if (!childNode) continue;
      var childCX = childNode.x + childNode.w / 2;
      var childTop = childNode.y;
      for (var j = 0; j < p.parents.length; j++) {
        var parentNode = nodeMap[p.parents[j]];
        if (!parentNode) continue;
        var parentCX = parentNode.x + parentNode.w / 2;
        var parentBot = parentNode.y + parentNode.h;
        var midY = (parentBot + childTop) / 2;
        ctx.beginPath();
        ctx.moveTo(parentCX, parentBot);
        ctx.lineTo(parentCX, midY);
        ctx.lineTo(childCX, midY);
        ctx.lineTo(childCX, childTop);
        ctx.stroke();
      }
    }

    // Draw spouse connectors
    ctx.strokeStyle = '#ddd';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([3, 3]);
    var drawnSpouse = {};
    for (var i = 0; i < rawData.length; i++) {
      var p = rawData[i];
      if (!p.spouse || drawnSpouse[p.name] || drawnSpouse[p.spouse]) continue;
      var n1 = nodeMap[p.name], n2 = nodeMap[p.spouse];
      if (!n1 || !n2) continue;
      drawnSpouse[p.name] = true;
      drawnSpouse[p.spouse] = true;
      var x1 = n1.x + n1.w, x2 = n2.x;
      if (x1 > x2) { x1 = n2.x + n2.w; x2 = n1.x; }
      var cy = n1.y + n1.h / 2;
      ctx.beginPath();
      ctx.moveTo(x1, cy);
      ctx.lineTo(x2, cy);
      ctx.stroke();
    }
    ctx.setLineDash([]);

    // Draw nodes
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      var person = byName[n.name];
      var isHovered = hoveredNode === n;
      var isHighlighted = highlightedName === n.name;
      var isMatt = n.name === 'Matt Reider';

      // Background
      if (isHighlighted) {
        ctx.fillStyle = COL_ACTIVE;
      } else if (isHovered) {
        ctx.fillStyle = COL_HOVER;
      } else {
        ctx.fillStyle = COL_NODE;
      }

      // Rounded rect
      var r = 4;
      ctx.beginPath();
      ctx.moveTo(n.x + r, n.y);
      ctx.lineTo(n.x + n.w - r, n.y);
      ctx.quadraticCurveTo(n.x + n.w, n.y, n.x + n.w, n.y + r);
      ctx.lineTo(n.x + n.w, n.y + n.h - r);
      ctx.quadraticCurveTo(n.x + n.w, n.y + n.h, n.x + n.w - r, n.y + n.h);
      ctx.lineTo(n.x + r, n.y + n.h);
      ctx.quadraticCurveTo(n.x, n.y + n.h, n.x, n.y + n.h - r);
      ctx.lineTo(n.x, n.y + r);
      ctx.quadraticCurveTo(n.x, n.y, n.x + r, n.y);
      ctx.closePath();
      ctx.fill();

      // Border
      ctx.strokeStyle = isMatt ? COL_MATT : (isHighlighted ? COL_ACTIVE : COL_BORDER);
      ctx.lineWidth = isMatt ? 2 : 1;
      ctx.stroke();

      // Name text
      ctx.fillStyle = isHighlighted ? COL_ACTIVE_TEXT : COL_TEXT;
      ctx.font = FONT;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      var label = n.name;
      // Truncate if too long
      while (ctx.measureText(label).width > n.w - 12 && label.length > 3) {
        label = label.slice(0, -4) + '\u2026';
      }

      var years = person ? nodeYears(person) : '';
      if (years) {
        ctx.fillText(label, n.x + n.w/2, n.y + n.h/2 - 7);
        ctx.font = FONT_SMALL;
        ctx.fillStyle = isHighlighted ? 'rgba(255,255,255,0.8)' : COL_DATES;
        ctx.fillText(years, n.x + n.w/2, n.y + n.h/2 + 9);
      } else {
        ctx.fillText(label, n.x + n.w/2, n.y + n.h/2);
      }
    }

    ctx.restore();
  }

  // --- Hit testing ---
  function nodeAt(mx, my) {
    var wx = (mx - offsetX) / scale;
    var wy = (my - offsetY) / scale;
    for (var i = nodes.length - 1; i >= 0; i--) {
      var n = nodes[i];
      if (wx >= n.x && wx <= n.x + n.w && wy >= n.y && wy <= n.y + n.h) return n;
    }
    return null;
  }

  // --- Interaction ---
  canvas.addEventListener('mousedown', function(e) {
    dragging = true;
    dragStartX = e.clientX;
    dragStartY = e.clientY;
    dragOffX = offsetX;
    dragOffY = offsetY;
    canvas.style.cursor = 'grabbing';
  });

  window.addEventListener('mousemove', function(e) {
    if (dragging) {
      offsetX = dragOffX + (e.clientX - dragStartX);
      offsetY = dragOffY + (e.clientY - dragStartY);
      draw();
    } else {
      var rect = canvas.getBoundingClientRect();
      var mx = e.clientX - rect.left;
      var my = e.clientY - rect.top;
      var n = nodeAt(mx, my);
      if (n !== hoveredNode) {
        hoveredNode = n;
        canvas.style.cursor = n ? 'pointer' : 'grab';
        draw();
      }
    }
  });

  window.addEventListener('mouseup', function(e) {
    if (dragging) {
      var dx = Math.abs(e.clientX - dragStartX);
      var dy = Math.abs(e.clientY - dragStartY);
      dragging = false;
      canvas.style.cursor = hoveredNode ? 'pointer' : 'grab';
      // If barely moved, treat as click
      if (dx < 4 && dy < 4) {
        var rect = canvas.getBoundingClientRect();
        var n = nodeAt(e.clientX - rect.left, e.clientY - rect.top);
        if (n) {
          window.mapNavigateTo(n.name);
        }
      }
    }
  });

  canvas.addEventListener('wheel', function(e) {
    e.preventDefault();
    var rect = canvas.getBoundingClientRect();
    var mx = e.clientX - rect.left;
    var my = e.clientY - rect.top;
    var zoom = e.deltaY < 0 ? 1.1 : 0.9;
    var newScale = Math.min(3, Math.max(0.15, scale * zoom));
    // Zoom toward cursor
    offsetX = mx - (mx - offsetX) * (newScale / scale);
    offsetY = my - (my - offsetY) * (newScale / scale);
    scale = newScale;
    draw();
  }, { passive: false });

  // Touch support
  var lastTouchDist = 0;
  var lastTouchMid = null;
  canvas.addEventListener('touchstart', function(e) {
    if (e.touches.length === 1) {
      dragging = true;
      dragStartX = e.touches[0].clientX;
      dragStartY = e.touches[0].clientY;
      dragOffX = offsetX;
      dragOffY = offsetY;
    } else if (e.touches.length === 2) {
      dragging = false;
      var dx = e.touches[1].clientX - e.touches[0].clientX;
      var dy = e.touches[1].clientY - e.touches[0].clientY;
      lastTouchDist = Math.sqrt(dx*dx + dy*dy);
      lastTouchMid = { x: (e.touches[0].clientX + e.touches[1].clientX)/2, y: (e.touches[0].clientY + e.touches[1].clientY)/2 };
    }
  }, { passive: true });

  canvas.addEventListener('touchmove', function(e) {
    e.preventDefault();
    if (e.touches.length === 1 && dragging) {
      offsetX = dragOffX + (e.touches[0].clientX - dragStartX);
      offsetY = dragOffY + (e.touches[0].clientY - dragStartY);
      draw();
    } else if (e.touches.length === 2) {
      var dx = e.touches[1].clientX - e.touches[0].clientX;
      var dy = e.touches[1].clientY - e.touches[0].clientY;
      var dist = Math.sqrt(dx*dx + dy*dy);
      var mid = { x: (e.touches[0].clientX + e.touches[1].clientX)/2, y: (e.touches[0].clientY + e.touches[1].clientY)/2 };
      if (lastTouchDist > 0) {
        var zoom = dist / lastTouchDist;
        var newScale = Math.min(3, Math.max(0.15, scale * zoom));
        var rect = canvas.getBoundingClientRect();
        var mx = mid.x - rect.left;
        var my = mid.y - rect.top;
        offsetX = mx - (mx - offsetX) * (newScale / scale);
        offsetY = my - (my - offsetY) * (newScale / scale);
        scale = newScale;
      }
      // Pan with two fingers
      if (lastTouchMid) {
        offsetX += mid.x - lastTouchMid.x;
        offsetY += mid.y - lastTouchMid.y;
      }
      lastTouchDist = dist;
      lastTouchMid = mid;
      draw();
    }
  }, { passive: false });

  canvas.addEventListener('touchend', function(e) {
    if (e.touches.length < 2) { lastTouchDist = 0; lastTouchMid = null; }
    if (e.touches.length === 0) {
      if (dragging) {
        dragging = false;
        // Tap detection
        var touch = e.changedTouches[0];
        var dx = Math.abs(touch.clientX - dragStartX);
        var dy = Math.abs(touch.clientY - dragStartY);
        if (dx < 10 && dy < 10) {
          var rect = canvas.getBoundingClientRect();
          var n = nodeAt(touch.clientX - rect.left, touch.clientY - rect.top);
          if (n) window.mapNavigateTo(n.name);
        }
      }
    }
  }, { passive: true });

  // --- Public API ---
  window.mapInit = function() {
    layoutNodes();
    centerOnPerson('Matt Reider');
  };

  window.mapCenterOn = function(name) {
    centerOnPerson(name);
  };

  window.mapResize = function() {
    draw();
  };

  function centerOnPerson(name) {
    var n = nodeMap[name];
    if (!n) { // fallback: fit all
      fitAll();
      return;
    }
    highlightedName = name;
    // Center the node in the canvas
    var cw = canvas.clientWidth, ch = canvas.clientHeight;
    scale = 1;
    offsetX = cw/2 - (n.x + n.w/2) * scale;
    offsetY = ch/2 - (n.y + n.h/2) * scale;
    draw();
  }

  function fitAll() {
    if (!nodes.length) return;
    var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      if (n.x < minX) minX = n.x;
      if (n.y < minY) minY = n.y;
      if (n.x + n.w > maxX) maxX = n.x + n.w;
      if (n.y + n.h > maxY) maxY = n.y + n.h;
    }
    var tw = maxX - minX, th = maxY - minY;
    var cw = canvas.clientWidth, ch = canvas.clientHeight;
    var pad = 40;
    scale = Math.min((cw - pad*2) / tw, (ch - pad*2) / th, 1);
    offsetX = (cw - tw * scale) / 2 - minX * scale;
    offsetY = (ch - th * scale) / 2 - minY * scale;
    draw();
  }

  canvas.style.cursor = 'grab';
})();
