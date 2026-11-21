// SOLECRAFT INTERACTIVE SHOE CUSTOMISATION STUDIO ENGINE

(function () {
  'use strict';

  // Base Silhouette Pricing
  const SILHOUETTE_PRICES = {
    retro_low: 160.0,
    high_top: 195.0,
    aeroknit_runner: 180.0,
    urban_slipon: 165.0
  };

  // Material Premiums
  const MATERIAL_PRICES = {
    'Italian Leather': 20.0,
    'Nubuck Suede': 15.0,
    'AeroKnit Mesh': 10.0,
    'Vintage Canvas': 0.0,
    'Metallic Platinum': 30.0
  };

  // Current State
  let state = {
    title: 'Custom SoleCraft Bespoke',
    shoe_type: 'retro_low',
    active_part: 'base', // base, upper, sole, laces, tongue, heel, swoosh
    base_color: '#FFFFFF',
    upper_color: '#111111',
    sole_color: '#FFFFFF',
    lace_color: '#FF6B35',
    tongue_color: '#111111',
    heel_color: '#FF6B35',
    swoosh_color: '#FF6B35',
    upper_material: 'Italian Leather',
    pattern: 'none',
    custom_text: '',
    custom_text_color: '#FFFFFF',
    view_angle: 'lateral',
    size: 'US 9',
    quantity: 1
  };

  // Undo / Redo History Stacks
  const history = {
    past: [],
    future: []
  };

  function pushStateToHistory() {
    // Keep max 25 history frames
    if (history.past.length > 25) history.past.shift();
    history.past.push(JSON.parse(JSON.stringify(state)));
    history.future = [];
    updateUndoRedoUI();
  }

  function updateUndoRedoUI() {
    const undoBtn = document.getElementById('btn-undo');
    const redoBtn = document.getElementById('btn-redo');
    if (undoBtn) undoBtn.disabled = history.past.length <= 1;
    if (redoBtn) redoBtn.disabled = history.future.length === 0;
  }

  // Calculate live dynamic price
  function calculateTotal() {
    let total = SILHOUETTE_PRICES[state.shoe_type] || 160.0;
    total += MATERIAL_PRICES[state.upper_material] || 0.0;
    if (state.pattern !== 'none') total += 12.0;
    if (state.custom_text && state.custom_text.trim().length > 0) total += 10.0;
    return total;
  }

  function updatePriceDisplay() {
    const total = calculateTotal();
    const priceValEl = document.getElementById('studio-price-val');
    if (priceValEl) {
      priceValEl.innerText = total.toFixed(2);
    }
    const basePriceEl = document.getElementById('price-breakdown-base');
    if (basePriceEl) {
      basePriceEl.innerText = `$${(SILHOUETTE_PRICES[state.shoe_type] || 160.0).toFixed(2)}`;
    }
    const matPriceEl = document.getElementById('price-breakdown-mat');
    if (matPriceEl) {
      matPriceEl.innerText = `+$${(MATERIAL_PRICES[state.upper_material] || 0.0).toFixed(2)}`;
    }
    const patternPriceEl = document.getElementById('price-breakdown-pat');
    if (patternPriceEl) {
      patternPriceEl.innerText = state.pattern !== 'none' ? '+$12.00' : '$0.00';
    }
    const monoPriceEl = document.getElementById('price-breakdown-mono');
    if (monoPriceEl) {
      monoPriceEl.innerText = (state.custom_text && state.custom_text.trim().length > 0) ? '+$10.00' : '$0.00';
    }
  }

  // SVG Geometry Templates for Each Shoe Type
  function getSilhouettePaths(type, angle) {
    if (type === 'high_top') {
      return {
        sole: "M 80 290 L 510 290 C 515 315, 490 330, 440 330 L 100 330 C 80 330, 75 310, 80 290 Z",
        upper: "M 90 280 L 110 150 C 120 120, 160 110, 190 120 L 250 140 C 270 170, 310 210, 360 230 L 440 240 C 470 250, 490 270, 500 290 L 90 290 Z",
        quarter: "M 90 280 L 110 150 C 120 120, 160 110, 190 120 L 220 180 L 180 280 Z",
        collar: "M 110 150 C 130 110, 190 100, 240 120 L 230 170 C 180 150, 130 160, 110 150 Z",
        swoosh: "M 160 210 Q 280 180, 380 255 Q 310 250, 210 260 Z",
        heel: "M 85 200 L 105 200 L 100 280 L 85 280 Z",
        tongue: "M 180 120 L 245 135 L 235 175 L 180 145 Z",
        laces: [
          {x1: 230, y1: 150, x2: 248, y2: 158},
          {x1: 250, y1: 175, x2: 268, y2: 183},
          {x1: 275, y1: 200, x2: 293, y2: 208},
          {x1: 305, y1: 220, x2: 323, y2: 228},
          {x1: 335, y1: 240, x2: 353, y2: 248}
        ],
        textPos: { x: 135, y: 245 }
      };
    } else if (type === 'aeroknit_runner') {
      return {
        sole: "M 70 270 C 90 270, 140 270, 200 275 C 320 285, 430 290, 520 265 C 525 295, 480 335, 430 335 L 120 335 C 80 335, 60 305, 70 270 Z",
        upper: "M 100 270 C 130 200, 190 190, 250 190 L 340 205 C 410 220, 460 240, 505 270 L 100 270 Z",
        quarter: "M 100 270 C 115 220, 160 195, 210 200 L 220 270 Z",
        collar: "M 170 195 C 190 170, 240 170, 260 190 Z",
        swoosh: "M 180 230 Q 300 205, 410 250 Q 320 245, 220 255 Z",
        heel: "M 85 220 L 100 220 L 98 270 L 85 270 Z",
        tongue: "M 200 175 L 250 180 L 245 205 L 195 200 Z",
        laces: [
          {x1: 240, y1: 200, x2: 258, y2: 208},
          {x1: 270, y1: 215, x2: 288, y2: 223},
          {x1: 300, y1: 230, x2: 318, y2: 238},
          {x1: 330, y1: 245, x2: 348, y2: 253}
        ],
        textPos: { x: 145, y: 250 }
      };
    } else if (type === 'urban_slipon') {
      return {
        sole: "M 90 275 L 510 275 C 510 305, 475 325, 430 325 L 110 325 C 90 325, 85 305, 90 275 Z",
        upper: "M 100 275 C 120 200, 180 185, 250 195 C 330 205, 420 230, 500 275 L 100 275 Z",
        quarter: "M 100 275 C 110 220, 150 190, 190 195 L 205 275 Z",
        collar: "M 180 195 C 210 180, 260 180, 280 200 Z",
        swoosh: "M 200 235 Q 320 225, 430 265",
        heel: "M 90 220 L 105 220 L 103 275 L 90 275 Z",
        tongue: "M 210 180 L 260 185 L 255 205 L 205 200 Z",
        laces: [],
        textPos: { x: 140, y: 245 }
      };
    } else {
      // retro_low default
      return {
        sole: "M 80 275 L 515 275 C 518 305, 480 330, 440 330 L 100 330 C 80 330, 75 305, 80 275 Z",
        upper: "M 95 275 C 110 190, 175 170, 240 180 L 330 195 C 400 215, 460 240, 505 275 L 95 275 Z",
        quarter: "M 95 275 C 90 220, 130 180, 180 180 L 195 275 Z",
        collar: "M 140 180 C 170 155, 225 155, 250 180 Z",
        swoosh: "M 170 225 Q 300 190, 420 250 Q 330 245, 220 255 Z",
        heel: "M 85 210 L 98 210 L 95 270 L 85 270 Z",
        tongue: "M 170 160 L 230 165 L 225 195 L 165 190 Z",
        laces: [
          {x1: 230, y1: 185, x2: 248, y2: 193},
          {x1: 260, y1: 200, x2: 278, y2: 208},
          {x1: 290, y1: 215, x2: 308, y2: 223},
          {x1: 320, y1: 230, x2: 338, y2: 238},
          {x1: 350, y1: 245, x2: 368, y2: 253}
        ],
        textPos: { x: 135, y: 245 }
      };
    }
  }

  // Render SVG Layers
  function renderShoe() {
    const geo = getSilhouettePaths(state.shoe_type, state.view_angle);

    // 1. Sole Path & Fill
    const soleEl = document.getElementById('svg-sole');
    if (soleEl) {
      soleEl.setAttribute('d', geo.sole);
      soleEl.setAttribute('fill', state.sole_color);
    }

    // 2. Base Upper
    const upperEl = document.getElementById('svg-upper');
    if (upperEl) {
      upperEl.setAttribute('d', geo.upper);
      upperEl.setAttribute('fill', state.base_color);
    }

    // 3. Quarter / Overlay
    const quarterEl = document.getElementById('svg-quarter');
    if (quarterEl) {
      quarterEl.setAttribute('d', geo.quarter);
      quarterEl.setAttribute('fill', state.upper_color);
    }

    // 4. Tongue
    const tongueEl = document.getElementById('svg-tongue');
    if (tongueEl) {
      tongueEl.setAttribute('d', geo.tongue);
      tongueEl.setAttribute('fill', state.tongue_color);
    }

    // 5. Collar
    const collarEl = document.getElementById('svg-collar');
    if (collarEl) {
      collarEl.setAttribute('d', geo.collar);
    }

    // 6. Heel Tab
    const heelEl = document.getElementById('svg-heel');
    if (heelEl) {
      heelEl.setAttribute('d', geo.heel);
      heelEl.setAttribute('fill', state.heel_color);
    }

    // 7. Signature Swoosh / Wave
    const swooshEl = document.getElementById('svg-swoosh');
    if (swooshEl) {
      swooshEl.setAttribute('d', geo.swoosh);
      swooshEl.setAttribute('fill', state.swoosh_color);
    }

    // 8. Laces
    const lacesGroup = document.getElementById('svg-laces-group');
    if (lacesGroup) {
      lacesGroup.innerHTML = '';
      geo.laces.forEach(l => {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', l.x1);
        line.setAttribute('y1', l.y1);
        line.setAttribute('x2', l.x2);
        line.setAttribute('y2', l.y2);
        line.setAttribute('stroke', state.lace_color);
        line.setAttribute('stroke-width', '4.5');
        line.setAttribute('stroke-linecap', 'round');
        line.setAttribute('filter', 'url(#dropShadow)');
        lacesGroup.appendChild(line);
      });
    }

    // 9. Pattern Layer
    const patternLayer = document.getElementById('svg-pattern-layer');
    if (patternLayer) {
      patternLayer.innerHTML = '';
      if (state.pattern === 'racing_stripe') {
        const stripe = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        stripe.setAttribute('d', 'M 210 200 L 290 280 L 315 280 L 235 200 Z');
        stripe.setAttribute('fill', state.lace_color);
        stripe.setAttribute('opacity', '0.85');
        patternLayer.appendChild(stripe);
      } else if (state.pattern === 'camo') {
        const p1 = document.createElementNS('http://www.w3.org/2000/svg', 'ellipse');
        p1.setAttribute('cx', '360');
        p1.setAttribute('cy', '240');
        p1.setAttribute('rx', '35');
        p1.setAttribute('ry', '18');
        p1.setAttribute('fill', state.heel_color);
        p1.setAttribute('opacity', '0.45');
        p1.setAttribute('transform', 'rotate(-25 360 240)');
        patternLayer.appendChild(p1);

        const p2 = document.createElementNS('http://www.w3.org/2000/svg', 'ellipse');
        p2.setAttribute('cx', '430');
        p2.setAttribute('cy', '255');
        p2.setAttribute('rx', '25');
        p2.setAttribute('ry', '14');
        p2.setAttribute('fill', state.swoosh_color);
        p2.setAttribute('opacity', '0.5');
        patternLayer.appendChild(p2);
      } else if (state.pattern === 'geometric') {
        for (let i = 0; i < 4; i++) {
          const poly = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
          const ox = 260 + i * 35;
          const oy = 210 + i * 14;
          poly.setAttribute('points', `${ox},${oy} ${ox + 16},${oy + 6} ${ox + 12},${oy + 20} ${ox - 4},${oy + 14}`);
          poly.setAttribute('fill', state.heel_color);
          poly.setAttribute('opacity', '0.6');
          patternLayer.appendChild(poly);
        }
      } else if (state.pattern === 'gradient') {
        const glow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        glow.setAttribute('d', geo.quarter);
        glow.setAttribute('fill', 'url(#accentGlowGrad)');
        glow.setAttribute('opacity', '0.6');
        patternLayer.appendChild(glow);
      }
    }

    // 10. Monogram Debossed Text
    const monogramTextEl = document.getElementById('svg-monogram-text');
    if (monogramTextEl) {
      if (state.custom_text && state.custom_text.trim().length > 0) {
        monogramTextEl.textContent = state.custom_text.toUpperCase().trim();
        monogramTextEl.setAttribute('x', geo.textPos.x);
        monogramTextEl.setAttribute('y', geo.textPos.y);
        monogramTextEl.setAttribute('fill', state.custom_text_color);
        monogramTextEl.style.display = 'block';
      } else {
        monogramTextEl.textContent = '';
        monogramTextEl.style.display = 'none';
      }
    }

    // Mirror for medial angle
    const canvasEl = document.querySelector('.svg-canvas-container');
    if (canvasEl) {
      if (state.view_angle === 'medial') {
        canvasEl.style.transform = 'scaleX(-1)';
      } else {
        canvasEl.style.transform = 'scaleX(1)';
      }
    }

    updatePriceDisplay();
  }

  // Initialize Customizer
  window.initSoleCraftStudio = function (initialSpecs) {
    if (initialSpecs) {
      try {
        const loaded = typeof initialSpecs === 'string' ? JSON.parse(initialSpecs) : initialSpecs;
        Object.assign(state, loaded);
      } catch (e) {
        console.error('Failed to parse initial specs:', e);
      }
    }

    pushStateToHistory();
    renderShoe();
    bindEvents();
  };

  function bindEvents() {
    // Tab switching in dock
    document.querySelectorAll('.studio-tab-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        document.querySelectorAll('.studio-tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.studio-tab-pane').forEach(p => p.classList.add('d-none'));

        this.classList.add('active');
        const targetTab = this.getAttribute('data-tab');
        const pane = document.getElementById(`tab-${targetTab}`);
        if (pane) pane.classList.remove('d-none');
      });
    });

    // Silhouette Selection
    document.querySelectorAll('.silhouette-card').forEach(card => {
      card.addEventListener('click', function () {
        document.querySelectorAll('.silhouette-card').forEach(c => c.classList.remove('active'));
        this.classList.add('active');

        const newType = this.getAttribute('data-type');
        if (newType !== state.shoe_type) {
          state.shoe_type = newType;
          pushStateToHistory();
          renderShoe();
        }
      });
    });

    // Angle Pills
    document.querySelectorAll('.btn-angle-pill').forEach(btn => {
      btn.addEventListener('click', function () {
        document.querySelectorAll('.btn-angle-pill').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        state.view_angle = this.getAttribute('data-angle');
        renderShoe();
      });
    });

    // Active Part Choice (Base, Upper, Sole, Laces, Tongue, Heel, Swoosh)
    document.querySelectorAll('.btn-part-choice').forEach(btn => {
      btn.addEventListener('click', function () {
        document.querySelectorAll('.btn-part-choice').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        state.active_part = this.getAttribute('data-part');
        highlightActiveSwatch();
      });
    });

    // Color Swatches
    document.querySelectorAll('.swatch-circle').forEach(swatch => {
      swatch.addEventListener('click', function () {
        const color = this.getAttribute('data-color');
        const part = state.active_part;

        if (part === 'base') state.base_color = color;
        else if (part === 'upper') state.upper_color = color;
        else if (part === 'sole') state.sole_color = color;
        else if (part === 'laces') state.lace_color = color;
        else if (part === 'tongue') state.tongue_color = color;
        else if (part === 'heel') state.heel_color = color;
        else if (part === 'swoosh') state.swoosh_color = color;

        highlightActiveSwatch();
        pushStateToHistory();
        renderShoe();
      });
    });

    // Material Selection
    document.querySelectorAll('.material-card').forEach(card => {
      card.addEventListener('click', function () {
        document.querySelectorAll('.material-card').forEach(c => c.classList.remove('active'));
        this.classList.add('active');
        state.upper_material = this.getAttribute('data-material');
        pushStateToHistory();
        renderShoe();
      });
    });

    // Pattern Selection
    document.querySelectorAll('.pattern-choice-card').forEach(card => {
      card.addEventListener('click', function () {
        document.querySelectorAll('.pattern-choice-card').forEach(c => c.classList.remove('active'));
        this.classList.add('active');
        state.pattern = this.getAttribute('data-pattern');
        pushStateToHistory();
        renderShoe();
      });
    });

    // Monogram Text Input
    const textInput = document.getElementById('monogram-input');
    if (textInput) {
      textInput.addEventListener('input', function () {
        state.custom_text = this.value.trim().slice(0, 10);
        renderShoe();
      });
      textInput.addEventListener('change', function () {
        pushStateToHistory();
      });
    }

    // Monogram Color Swatches
    document.querySelectorAll('.mono-color-swatch').forEach(swatch => {
      swatch.addEventListener('click', function () {
        state.custom_text_color = this.getAttribute('data-color');
        pushStateToHistory();
        renderShoe();
      });
    });

    // Undo Button
    const undoBtn = document.getElementById('btn-undo');
    if (undoBtn) {
      undoBtn.addEventListener('click', function () {
        if (history.past.length > 1) {
          const current = history.past.pop();
          history.future.push(current);
          state = JSON.parse(JSON.stringify(history.past[history.past.length - 1]));
          updateUndoRedoUI();
          syncControlsWithState();
          renderShoe();
        }
      });
    }

    // Redo Button
    const redoBtn = document.getElementById('btn-redo');
    if (redoBtn) {
      redoBtn.addEventListener('click', function () {
        if (history.future.length > 0) {
          const next = history.future.pop();
          history.past.push(next);
          state = JSON.parse(JSON.stringify(next));
          updateUndoRedoUI();
          syncControlsWithState();
          renderShoe();
        }
      });
    }

    // Reset Button
    const resetBtn = document.getElementById('btn-reset');
    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        if (confirm('Reset customizer back to factory baseline?')) {
          state.base_color = '#FFFFFF';
          state.upper_color = '#111111';
          state.sole_color = '#FFFFFF';
          state.lace_color = '#FF6B35';
          state.tongue_color = '#111111';
          state.heel_color = '#FF6B35';
          state.swoosh_color = '#FF6B35';
          state.pattern = 'none';
          state.custom_text = '';
          state.upper_material = 'Italian Leather';
          if (textInput) textInput.value = '';
          pushStateToHistory();
          syncControlsWithState();
          renderShoe();
        }
      });
    }

    // Save Design to Profile Vault
    const saveBtn = document.getElementById('btn-save-design');
    if (saveBtn) {
      saveBtn.addEventListener('click', function () {
        const payload = Object.assign({}, state, {
          calculated_price: calculateTotal(),
          preview_image: getSvgDataUrl()
        });

        saveBtn.disabled = true;
        saveBtn.innerHTML = 'Saving...';

        fetch('/customizer/api/save', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
          saveBtn.disabled = false;
          saveBtn.innerHTML = '<i class="bi bi-bookmark me-1"></i> Save to Vault';
          if (data.success) {
            window.showToast(data.message, 'success');
          }
        })
        .catch(err => {
          saveBtn.disabled = false;
          saveBtn.innerHTML = '<i class="bi bi-bookmark me-1"></i> Save to Vault';
          console.error(err);
        });
      });
    }

    // Add Customized Shoe to Cart
    const addCartBtn = document.getElementById('btn-add-custom-cart');
    if (addCartBtn) {
      addCartBtn.addEventListener('click', function () {
        const sizeSelect = document.getElementById('custom-size-select');
        const size = sizeSelect ? sizeSelect.value : 'US 9';

        const payload = Object.assign({}, state, {
          size: size,
          quantity: 1,
          calculated_price: calculateTotal(),
          preview_image: getSvgDataUrl()
        });

        addCartBtn.disabled = true;
        addCartBtn.innerHTML = 'Crafting...';

        fetch('/customizer/api/add-to-cart', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
          addCartBtn.disabled = false;
          addCartBtn.innerHTML = '<i class="bi bi-bag-plus me-1"></i> Add Bespoke to Bag';
          if (data.success) {
            window.showToast(data.message, 'success');
            if (window.updateCartBadges) window.updateCartBadges(data.cart_count);
            setTimeout(() => {
              window.location.href = data.cart_url;
            }, 800);
          }
        })
        .catch(err => {
          addCartBtn.disabled = false;
          addCartBtn.innerHTML = '<i class="bi bi-bag-plus me-1"></i> Add Bespoke to Bag';
          console.error(err);
        });
      });
    }
  }

  function highlightActiveSwatch() {
    const part = state.active_part;
    let currentColor = '#FFFFFF';
    if (part === 'base') currentColor = state.base_color;
    else if (part === 'upper') currentColor = state.upper_color;
    else if (part === 'sole') currentColor = state.sole_color;
    else if (part === 'laces') currentColor = state.lace_color;
    else if (part === 'tongue') currentColor = state.tongue_color;
    else if (part === 'heel') currentColor = state.heel_color;
    else if (part === 'swoosh') currentColor = state.swoosh_color;

    document.querySelectorAll('.swatch-circle').forEach(sw => {
      if (sw.getAttribute('data-color').toLowerCase() === currentColor.toLowerCase()) {
        sw.classList.add('active');
      } else {
        sw.classList.remove('active');
      }
    });
  }

  function syncControlsWithState() {
    // Sync silhouette card
    document.querySelectorAll('.silhouette-card').forEach(c => {
      if (c.getAttribute('data-type') === state.shoe_type) c.classList.add('active');
      else c.classList.remove('active');
    });

    // Sync material card
    document.querySelectorAll('.material-card').forEach(c => {
      if (c.getAttribute('data-material') === state.upper_material) c.classList.add('active');
      else c.classList.remove('active');
    });

    // Sync pattern card
    document.querySelectorAll('.pattern-choice-card').forEach(c => {
      if (c.getAttribute('data-pattern') === state.pattern) c.classList.add('active');
      else c.classList.remove('active');
    });

    // Sync text input
    const input = document.getElementById('monogram-input');
    if (input) input.value = state.custom_text || '';

    highlightActiveSwatch();
  }

  function getSvgDataUrl() {
    const svgEl = document.querySelector('.svg-canvas-container svg');
    if (!svgEl) return null;
    const serializer = new XMLSerializer();
    const svgString = serializer.serializeToString(svgEl);
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgString);
  }

})();
